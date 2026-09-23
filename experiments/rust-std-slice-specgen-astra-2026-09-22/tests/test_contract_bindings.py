import csv
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_native
from scripts.check_native import DEFAULTS, FUNCTIONS, ROOT, SOURCE
from scripts.export_completeness import checked_default_run


def compact(text):
    return re.sub(r"\s+", "", text)


class NativeCheckOutputPaths(unittest.TestCase):
    def test_default_and_redirected_outputs_preserve_source_root(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected), tempfile.TemporaryDirectory(
                dir=ROOT, prefix=".native-output-path-test-"
            ) as tmp:
                project = Path(tmp) / "project"
                output_root = Path(tmp) / "scratch" if redirected else project
                arguments = ["--output-root", str(output_root)] if redirected else []
                with patch.object(check_native, "ROOT", project), patch.object(
                    check_native.subprocess, "run",
                    side_effect=OSError("compiler unavailable"),
                ) as run:
                    with self.assertRaisesRegex(OSError, "compiler unavailable"):
                        check_native.main(arguments)
                output = output_root / "target/defaults/native"
                logs = output_root / "logs/defaults/native"
                self.assertTrue(output.is_dir())
                self.assertEqual(list(output.iterdir()), [])
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(commands[0]["command"], ["rustc", "+1.96.0", "-vV"])
                self.assertEqual(run.call_args.kwargs["cwd"], project)
                environment = run.call_args.kwargs["env"]
                self.assertEqual(
                    environment["SLICE_NATIVE_SOURCE"], str(output / "source_observers.rs")
                )
                self.assertEqual(
                    environment["SLICE_DEFAULT_SOURCE"], str(output / "source_defaults.rs")
                )
                if redirected:
                    self.assertFalse(project.exists())


class ContractBindings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_lines = SOURCE.read_text().splitlines()

    def source_parts(self, name):
        start, end = FUNCTIONS[name]
        lines = self.source_lines[start - 1 : end]
        signature = lines[0].strip()
        result = signature.split(" -> ", 1)[1].removesuffix(" {")
        body = "\n".join(line[4:] for line in lines[1:-1])
        body = re.sub(r"\bself\b", "slice", body)
        return result, body

    def test_exact_source_bodies(self):
        allowed_diff = {
            "first": (
                "    if let [first, ..] = slice { Some(first) } else { None }",
                "    if slice.len() == 0 { None } else { Some(&slice[0]) }",
            ),
            "last": (
                "    if let [.., last] = slice { Some(last) } else { None }",
                "    if slice.len() == 0 { None } else { Some(&slice[slice.len() - 1]) }",
            ),
            "split_first": (
                "    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }",
                "    if slice.len() == 0 {\n"
                "        None\n"
                "    } else {\n"
                "        Some((&slice[0], slice.split_at(1).1))\n"
                "    }",
            ),
            "split_last": (
                "    if let [init @ .., last] = slice { Some((last, init)) } else { None }",
                "    if slice.len() == 0 {\n"
                "        None\n"
                "    } else {\n"
                "        let i = slice.len() - 1;\n"
                "        Some((&slice[i], slice.split_at(i).0))\n"
                "    }",
            ),
        }
        for name in FUNCTIONS:
            with self.subTest(api=name):
                result, expected = self.source_parts(name)
                proof = (ROOT / f"proofs/correctness/slice/{name}.rs").read_text()
                signature = f"pub const fn {name}<T>(slice: &[T]) -> (result: {result})"
                self.assertIn(signature + "\n", proof)
                if name in allowed_diff:
                    original, adopted = allowed_diff[name]
                    self.assertEqual(expected, original)
                    group = "splits" if name in ("split_first", "split_last") else "endpoints"
                    before = (
                        ROOT / f"logs/{group}/adoption-before/proofs/correctness/slice/{name}.rs"
                    ).read_text()
                    self.assertEqual(before.count(original), 1)
                    self.assertEqual(proof, before.replace(original, adopted, 1))
                    expected = adopted
                match = re.search(r"^\{\n(.*?)^\}", proof, re.MULTILINE | re.DOTALL)
                self.assertIsNotNone(match)
                self.assertEqual(match[1], expected + "\n")
                self.assertNotRegex(
                    proof, r"\b(?:assume_specification|external_body|admit|assume|loop)\b"
                )
                self.assertNotIn("requires", proof)

    def test_exact_analysis_binding(self):
        for name in FUNCTIONS:
            with self.subTest(api=name):
                result, expected = self.source_parts(name)
                adapter = (ROOT / f"proofs/completeness/slice/inputs/{name}.rs").read_text()
                signature = f"pub const fn {name}<T>(slice: &[T]) -> {result}"
                body = "\n".join("    " + line for line in expected.splitlines())
                if name == "len":
                    self.assertEqual(body, "        ptr::metadata(slice)")
                    body = "        core::ptr::metadata(slice)"
                declaration = (
                    f"pub assume_specification<T>[source::{name}::<T>]"
                    f"(slice: &[T]) -> (result: {result})\n"
                    f"    ensures\n        contracts::{name}_post(slice, result),\n;"
                )
                self.assertEqual(
                    adapter,
                    ("#![feature(ptr_metadata)]\n" if name == "len" else "")
                    + 'use vstd::prelude::*;\n'
                    '#[path = "../../../../specs/slice/mod.rs"]\nmod contracts;\n\n'
                    "mod source {\n"
                    + f"    {signature} {{\n{body}\n    }}\n"
                    "}\n\nverus! {\n"
                    "// Analysis declaration only; the implementation proof is kept separately.\n"
                    + declaration + "\n}\n",
                )

    def test_same_predicate_in_both_tracks(self):
        for name in FUNCTIONS:
            with self.subTest(api=name):
                clause = f"ensures contracts::{name}_post(slice, result),"
                for relative in (
                    f"proofs/correctness/slice/{name}.rs",
                    f"proofs/completeness/slice/inputs/{name}.rs",
                ):
                    self.assertIn(compact(clause), compact((ROOT / relative).read_text()))

    def test_original_observers_stay_pure(self):
        root = (ROOT / "specs/mod.rs").read_text()
        predicates = (ROOT / "specs/slice/mod.rs").read_text()
        self.assertIn("pub mod slice;", root)
        self.assertIn('#[path = "slice/default.rs"]\npub mod slice_default;', root)
        self.assertNotIn("completeness", root)
        self.assertNotRegex(predicates, r"\b(?:assume_specification|external_body|admit|assume)\b")
        self.assertEqual(predicates.count("pub open spec fn "), 6)


class DefaultBindings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_lines = SOURCE.read_text().splitlines()
        with (ROOT / "inventory/apis.tsv").open() as stream:
            cls.inventory = {
                row["canonical_id"]: row
                for row in csv.DictReader(stream, delimiter="\t")
            }

    def test_exact_default_source_bodies_and_lifetimes(self):
        for name, (start, end, result) in DEFAULTS.items():
            with self.subTest(api=name):
                original = self.source_lines[start - 1 : end]
                self.assertEqual(original[0].strip(), "fn default() -> Self {")
                proof = (ROOT / f"proofs/correctness/slice/{name}.rs").read_text()
                signature = f"pub fn {name}<'a, T>() -> (result: {result})"
                self.assertIn(compact(signature), compact(proof))
                body = re.search(r"^\{\n(.*?)^\}", proof, re.MULTILINE | re.DOTALL)
                self.assertIsNotNone(body)
                self.assertEqual(compact(body[1]), compact("\n".join(original[1:-1])))
                self.assertNotRegex(
                    proof, r"\b(?:assume_specification|external_body|admit|assume|loop|requires)\b"
                )
                self.assertNotIn("core::default", proof)
                self.assertIn('#[path = "../../../specs/slice/default_post.rs"]', proof)

    def test_real_trait_bindings_have_no_arguments_or_extra_bounds(self):
        bindings = (ROOT / "specs/slice/default.rs").read_text()
        self.assertEqual(bindings.count("pub assume_specification"), 2)
        self.assertIn('#[path = "default_post.rs"]', bindings)
        for _, _, result in DEFAULTS.values():
            declaration = (
                f"pub assume_specification<'a, T>"
                f"[<{result} as core::default::Default>::default]() -> (result: {result}) "
                "ensures post::default_post(result),;"
            )
            self.assertIn(compact(declaration), compact(bindings))
        self.assertNotIn("requires", bindings)
        self.assertNotRegex(bindings, r"\b(?:Copy|Default\s*\+|where)\b|'static")

    def test_source_inventory_and_non_const_stability(self):
        for name, (start, end, result) in DEFAULTS.items():
            receiver = result.replace("'a ", "")
            row = self.inventory[f"<{receiver} as core::default::Default>::default"]
            self.assertEqual(row["signature"], "fn default() -> Self")
            self.assertEqual(row["receiver"], "(associated; no self)")
            self.assertEqual(row["self_type"], receiver)
            self.assertEqual(row["source_span"], f"slice/mod.rs:{start}-{end}")
            self.assertEqual(json.loads(row["doc_spans"]), [f"slice/mod.rs:{start-1}-{start-1}"])
            self.assertEqual(row["effective_stability"], "stable")
            self.assertEqual(row["stable_since"], "1.0.0" if name == "default_shared" else "1.5.0")
            self.assertTrue(row["const_stability"].startswith("unstable:"))
            self.assertIn("const_default", row["const_stability"])
            self.assertEqual(row["existing_vstd_coverage"], "generic-trait-only")
            expected_doc = (
                "/// Creates an empty slice." if name == "default_shared"
                else "/// Creates a mutable empty slice."
            )
            self.assertEqual(self.source_lines[start - 2].strip(), expected_doc)

    def test_same_full_sequence_predicate_in_both_tracks(self):
        predicate = (ROOT / "specs/slice/default_post.rs").read_text()
        self.assertIn("result@ =~= Seq::<T>::empty()", predicate)
        self.assertNotIn("requires", predicate)
        for name in DEFAULTS:
            for relative in (
                f"proofs/correctness/slice/{name}.rs",
                f"proofs/completeness/slice/inputs/{name}.rs",
            ):
                text = (ROOT / relative).read_text()
                self.assertIn(
                    "ensurescontracts::default_post(result),", compact(text)
                )

    def test_direct_analysis_uses_the_exact_trait_declarations(self):
        for name, (_, _, result) in DEFAULTS.items():
            filename = name if name == "default_shared" else "default_mut_direct"
            text = (ROOT / f"proofs/completeness/slice/inputs/{filename}.rs").read_text()
            declaration = (
                f"pub assume_specification<'a, T>"
                f"[<{result} as core::default::Default>::default]() -> (result: {result}) "
                "ensures contracts::default_post(result),;"
            )
            self.assertIn(compact(declaration), compact(text))
            self.assertNotIn("requires", text)

    def test_mutable_analysis_reborrow_does_not_assume_the_target(self):
        adapter = (ROOT / "proofs/completeness/slice/inputs/default_mut.rs").read_text()
        self.assertIn('#[path = "../../../correctness/slice/default_mut.rs"]', adapter)
        self.assertNotRegex(adapter, r"\b(?:assume_specification|external_body|admit|assume|requires)\b")
        self.assertIn("result@ == old(value)@", adapter)
        self.assertIn("(left =~= right) <==> (left@ =~= right@)", adapter)
        self.assertIn("observe(source::default_mut())", adapter)

    def assert_native_checker_reexecution_and_exported_input_match(self, name):
        _, _, native = checked_default_run(name, "analyze")
        _, _, replay = checked_default_run(name, "replay")
        original = (ROOT / native["harness"]).read_text()
        self.assertEqual(original, (ROOT / replay["harness"]).read_text())
        expected = original.replace(
            '#[path = "../../../../specs/slice/default_post.rs"]',
            '#[path = "../../../specs/slice/default_post.rs"]',
            1,
        )
        if name == "default_mut":
            expected = expected.replace(
                '#[path = "../../../correctness/slice/default_mut.rs"]',
                '#[path = "../../correctness/slice/default_mut.rs"]',
                1,
            )
        exported = (ROOT / f"proofs/completeness/slice/{name}.rs").read_text()
        self.assertEqual(exported.split("\n", 3)[3], expected)

    def test_shared_native_checker_reexecution_and_exported_input_match(self):
        self.assert_native_checker_reexecution_and_exported_input_match("default_shared")

    def test_mutable_native_checker_reexecution_and_exported_input_match(self):
        self.assert_native_checker_reexecution_and_exported_input_match("default_mut")

    def test_coverage_keeps_the_six_original_results(self):
        with (ROOT / "inventory/coverage.tsv").open() as stream:
            rows = list(csv.DictReader(stream, delimiter="\t"))
        coverage = {row["canonical_id"]: row for row in rows}
        self.assertEqual(len(coverage), len(rows))
        self.assertEqual(coverage.keys(), self.inventory.keys())
        for name in FUNCTIONS:
            row = coverage[f"<[T]>::{name}"]
            self.assertEqual(row["mission_scope"], "current_six")
            self.assertEqual(row["completeness_result"], "deterministic")
            self.assertEqual(row["completeness_checked_goals"], "1")
            self.assertEqual(
                row["correctness_target_functions"],
                "0" if name == "len" else "1",
            )
            if name in ("first", "last"):
                self.assertEqual(
                    row["correctness_log"], f"logs/endpoints/correctness/{name}/verus.stdout",
                )
                self.assertIn("reviewed pattern-to-length/index conversion", row["correctness_result"])
            elif name in ("split_first", "split_last"):
                self.assertEqual(
                    row["correctness_log"], f"logs/splits/correctness/{name}/verus.stdout",
                )
                self.assertIn("reviewed pattern-to-length/index/split_at conversion", row["correctness_result"])
                self.assertIn("not metadata or split_at implementation verification", row["correctness_result"])
            self.assertTrue(row["checker_report"].startswith("logs/foundation/"))
        for _, _, result in DEFAULTS.values():
            receiver = result.replace("'a ", "")
            row = coverage[f"<{receiver} as core::default::Default>::default"]
            self.assertEqual(row["mission_scope"], "slice_defaults")
            self.assertEqual(row["correctness_target_functions"], "1")
            self.assertEqual(row["completeness_checked_goals"], "1")
            self.assertEqual(row["completeness_result"], "deterministic")


class MutableSingletonObservationBindings(unittest.TestCase):
    def test_observation_has_only_the_derived_caller_domain_and_both_outputs(self):
        adapter = (ROOT / "proofs/completeness/slice/inputs/from_mut.rs").read_text()
        self.assertIn('#[path = "../from_mut_state.rs"]\nmod state;', adapter)
        self.assertIn(
            compact(
                "pub fn from_mut_observation<T>("
                "input_initial: Ghost<T>, caller_final: Ghost<Seq<T>>,"
                ") -> (result: Ghost<(Seq<T>, T)>)"
            ),
            compact(adapter),
        )
        contract = re.search(r"\brequires(.*?)\bensures(.*?)^\{", adapter, re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(contract)
        self.assertEqual(compact(contract[1]), "caller_final@.len()==1,")
        self.assertEqual(
            compact(contract[2]),
            compact(
                "state::post::singleton_post(input_initial@, result@.0),"
                "result@.1 == caller_final@[0],"
            ),
        )
        self.assertNotRegex(
            adapter, r"\b(?:assume_specification|external_body|admit|assume|Copy|Eq|where)\b|'static"
        )
        self.assertIn("state::all_caller_writes(input_initial@, caller_final@);", adapter)
        self.assertIn("state::observation_correspondence(", adapter)
        self.assertIn("Ghost((seq![input_initial@], caller_final@[0]))", adapter)

    def test_state_relation_uses_the_unchanged_initial_and_final_predicate(self):
        state = (ROOT / "proofs/completeness/slice/from_mut_state.rs").read_text()
        self.assertIn('#[path = "../../../specs/slice/raw_post.rs"]\npub mod post;', state)
        self.assertIn(
            compact(
                "pub open spec fn from_mut_post<T>("
                "input_initial: T, caller_final: Seq<T>, observations: (Seq<T>, T),"
                ") -> bool {"
                "&&& post::singleton_post(input_initial, observations.0)"
                "&&& post::singleton_post(observations.1, caller_final)"
                "}"
            ),
            compact(state),
        )
        self.assertIn(
            compact(
                "from_mut_post(*old(s), final(result)@, (old(result)@, *final(s)))"
                "<==> (post::singleton_post(*old(s), old(result)@)"
                "&& post::singleton_post(*final(s), final(result)@))"
            ),
            compact(state),
        )
        self.assertNotRegex(
            state, r"\b(?:assume_specification|external_body|admit|assume|axiom|Copy|Eq|where)\b|'static"
        )

    def test_caller_domain_and_index_restatement_do_not_freeze_writes(self):
        state = (ROOT / "proofs/completeness/slice/from_mut_state.rs").read_text()
        self.assertEqual(
            re.findall(r"pub proof fn (\w+)<T>", state),
            [
                "candidate_correspondence", "caller_domain", "observation_correspondence",
                "all_caller_writes", "full_value_comparison",
            ],
        )
        self.assertIn("vstd::slice::mut_ref_slice_len_eq(result);", state)
        self.assertIn("final(*result)@.len() == 1,", state)
        for name in ("observation_correspondence", "all_caller_writes"):
            contract = re.search(
                rf"pub proof fn {name}<T>.*?\brequires(.*?)\bensures(.*?)^\{{",
                state, re.MULTILINE | re.DOTALL,
            )
            self.assertIsNotNone(contract)
            self.assertEqual(compact(contract[1]), "caller_final.len()==1,")
        self.assertIn(
            compact(
                "from_mut_post(input_initial, caller_final, observations) <==> ("
                "post::singleton_post(input_initial, observations.0)"
                "&& observations.1 == caller_final[0])"
            ),
            compact(state),
        )
        self.assertIn(
            compact(
                "from_mut_post(input_initial, caller_final, (seq![input_initial], caller_final[0]))"
            ),
            compact(state),
        )
        self.assertIn(
            compact(
                "(left =~= right && left_returned == right_returned)"
                "<==> (left@ =~= right@ && left_returned == right_returned)"
            ),
            compact(state),
        )


if __name__ == "__main__":
    unittest.main()
