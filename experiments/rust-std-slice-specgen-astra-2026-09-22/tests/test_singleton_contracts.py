import copy
import csv
import io
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

from scripts import check_native, export_completeness


ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = {
    "from_ref": (203, 205, "&T", "&[T]", 166, 169, "&[T; 1]"),
    "from_mut": (211, 213, "&mut T", "&mut [T]", 174, 177, "&mut [T; 1]"),
}


def compact(text):
    return re.sub(r"\s+", "", text)


def clauses(name, module="contracts"):
    if name == "from_ref":
        return f"ensures {module}::singleton_post(*s, result@),"
    return (
        f"ensures {module}::singleton_post(*old(s), result@),"
        f"{module}::singleton_post(*final(s), final(result)@),"
    )


class SingletonBindings(unittest.TestCase):
    def test_source_signatures_expressions_and_delegates_are_unchanged(self):
        slice_lines = check_native.SINGLETON_SLICE_SOURCE.read_text().splitlines()
        array_lines = check_native.SINGLETON_ARRAY_SOURCE.read_text().splitlines()
        bridge = (ROOT / "proofs/correctness/array/singleton.rs").read_text()
        for name, (start, end, parameter, result, array_start, array_end, array_result) in FUNCTIONS.items():
            proof = (ROOT / f"proofs/correctness/slice/{name}.rs").read_text()
            for text, lines, first, last, return_type in (
                (proof, slice_lines, start, end, result),
                (bridge, array_lines, array_start, array_end, array_result),
            ):
                with self.subTest(api=name, return_type=return_type):
                    self.assertEqual(
                        lines[first - 1],
                        f"pub const fn {name}<T>(s: {parameter}) -> {return_type} {{",
                    )
                    signature = f"pub const fn {name}<T>(s: {parameter}) -> (result: {return_type})"
                    self.assertIn(compact(signature), compact(text))
                    definition = re.search(
                        rf"pub const fn {name}<T>.*?^\{{\n(.*?)^\}}",
                        text, re.MULTILINE | re.DOTALL,
                    )
                    self.assertIsNotNone(definition)
                    self.assertEqual(
                        compact(definition[1]),
                        compact("\n".join(lines[first:last - 1])),
                    )
            self.assertIn('#[path = "../array/singleton.rs"]\nmod array;', proof)

    def test_array_source_bridge_has_no_assumed_contract(self):
        for relative in (
            "proofs/correctness/array/singleton.rs",
            "proofs/correctness/slice/from_ref.rs",
            "proofs/correctness/slice/from_mut.rs",
        ):
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text()
                self.assertNotRegex(
                    text, r"\b(?:assume_specification|external_body|admit|assume|axiom|requires)\b"
                )
                self.assertNotRegex(text, r"\b(?:Copy|Default|Eq|where)\b|'static|\?Sized")
                self.assertNotIn("core::array::", text)

    def test_source_and_direct_analysis_bindings_keep_both_state_relations(self):
        bindings = (ROOT / "specs/slice/raw.rs").read_text()
        bridge = (ROOT / "proofs/correctness/array/singleton.rs").read_text()
        for name, (_, _, parameter, result, _, _, _) in FUNCTIONS.items():
            with self.subTest(api=name):
                direct = (
                    "proofs/completeness/slice/history/from_mut_direct.rs"
                    if name == "from_mut" else f"proofs/completeness/slice/inputs/{name}.rs"
                )
                for relative in (
                    f"proofs/correctness/slice/{name}.rs",
                    direct,
                ):
                    text = (ROOT / relative).read_text()
                    self.assertIn(compact(clauses(name)), compact(text))
                    self.assertNotIn("requires", text)
                self.assertIn(compact(clauses(name)), compact(bridge))
                declaration = (
                    f"pub assume_specification<T>[ core::slice::{name} ]"
                    f"(s: {parameter}) -> (result: {result})"
                )
                self.assertIn(
                    compact(declaration + clauses(name, "post") + ";"),
                    compact(bindings),
                )
                analysis = (ROOT / direct).read_text()
                self.assertIn(
                    compact(declaration + clauses(name) + ";"), compact(analysis)
                )
                self.assertEqual(analysis.count("pub assume_specification"), 1)
                self.assertNotRegex(analysis, r"\b(?:Copy|Default|Eq|where)\b|'static|\?Sized")
        self.assertEqual(bindings.count("pub assume_specification"), 2)
        self.assertNotIn("requires", bindings)

    def test_complete_sequence_predicate_has_no_duplicate_length_clause(self):
        predicate = (ROOT / "specs/slice/raw_post.rs").read_text()
        self.assertIn(
            compact(
                "pub open spec fn singleton_post<T>(value: T, elements: Seq<T>) -> bool "
                "{ elements =~= seq![value] }"
            ),
            compact(predicate),
        )
        self.assertEqual(predicate.count("pub open spec fn"), 1)
        self.assertNotRegex(predicate, r"\b(?:len|requires|assume|axiom|uninterp)\b")

    def test_aggregate_includes_the_exact_public_bindings(self):
        aggregate = (ROOT / "specs/mod.rs").read_text()
        self.assertIn('#[path = "slice/raw.rs"]\npub mod slice_raw;', aggregate)
        self.assertNotIn("correctness", aggregate)
        self.assertNotIn("completeness", aggregate)

    def test_authoritative_inventory_signatures_and_documentation(self):
        with (ROOT / "inventory/apis.tsv").open() as stream:
            inventory = {
                row["canonical_id"]: row
                for row in csv.DictReader(stream, delimiter="\t")
            }
        source = check_native.SINGLETON_SLICE_SOURCE.read_text().splitlines()
        for name, (start, end, parameter, result, _, _, _) in FUNCTIONS.items():
            with self.subTest(api=name):
                row = inventory[f"core::slice::{name}"]
                self.assertEqual(
                    row["signature"], f"pub const fn {name}<T>(s: {parameter}) -> {result}"
                )
                self.assertEqual(row["source_span"], f"slice/raw.rs:{start}-{end}")
                self.assertEqual(row["effective_stability"], "stable")
                self.assertEqual(row["stable_since"], "1.28.0")
                doc_line = 198 if name == "from_ref" else 207
                self.assertEqual(row["doc_spans"], f'["slice/raw.rs:{doc_line}-{doc_line}"]')
                self.assertEqual(
                    source[doc_line - 1],
                    "/// Converts a reference to T into a slice of length 1 (without copying).",
                )


class SingletonExports(unittest.TestCase):
    def assert_native_export_matches(self, api, before, after):
        _, result, native = export_completeness.checked_singleton_run(api, "analyze")
        _, _, replay = export_completeness.checked_singleton_run(api, "replay")
        original = Path(native["harness"]).read_text()
        self.assertEqual(original, Path(replay["harness"]).read_text())
        exported = (ROOT / f"proofs/completeness/slice/{api}.rs").read_text()
        self.assertEqual(original.count(before), 1)
        self.assertEqual(exported.split("\n", 3)[3], original.replace(before, after, 1))
        self.assertEqual(result["proofs"][0]["verified_goals"], 1)
        return result, native

    def test_shared_native_proof_and_reexecution_export_match(self):
        self.assert_native_export_matches(
            "from_ref",
            '#[path = "../../../../specs/slice/raw_post.rs"]',
            '#[path = "../../../specs/slice/raw_post.rs"]',
        )

    def test_mutable_native_proof_and_reexecution_export_match(self):
        result, native = self.assert_native_export_matches(
            "from_mut", '#[path = "../from_mut_state.rs"]', '#[path = "from_mut_state.rs"]',
        )
        self.assertEqual(result["target"]["name"], "from_mut_observation")
        self.assertEqual(result["target"]["kind"], "function")
        self.assertEqual(result["diagnostics"], [])
        comparison = native["det_spec"]
        self.assertIn(
            "(((r1)@.0 =~= (r2)@.0) && ((r1)@.1 == (r2)@.1))",
            comparison["equal_fn_def"],
        )
        self.assertEqual(comparison["equal_policy"]["ignore_fields"], [])
        self.assertEqual(
            result["coverage"]["ignored_dimensions"], ["return.representation_beyond_view"]
        )

    def test_historical_direct_mutable_failure_is_not_the_current_proof(self):
        historical = (ROOT / "proofs/completeness/slice/history/from_mut_direct.rs").read_bytes()
        for phase in ("analyze", "replay"):
            with self.subTest(phase=phase):
                report = json.loads(
                    (ROOT / f"logs/singletons/completeness/from_mut/{phase}.json").read_text()
                )
                result = report["results"][0]
                self.assertIsNone(result["baseline"])
                self.assertEqual(result["proofs"], [])
                self.assertEqual(result["verdict"], "not_evaluated")
                self.assertEqual(
                    historical,
                    (Path(report["run_dir"]) / "workspace" / result["target"]["file"]).read_bytes(),
                )
                _, current, _ = export_completeness.checked_singleton_run("from_mut", phase)
                self.assertEqual(current["target"]["name"], "from_mut_observation")
                self.assertEqual(current["verdict"], "deterministic")

    def test_coverage_separates_zero_source_functions_from_completeness_goals(self):
        with (ROOT / "inventory/coverage.tsv").open() as stream:
            coverage = {
                row["canonical_id"]: row
                for row in csv.DictReader(stream, delimiter="\t")
            }
        self.assertEqual(len(coverage), 331)
        for name in FUNCTIONS:
            with self.subTest(api=name):
                row = coverage[f"core::slice::{name}"]
                self.assertEqual(row["correctness_target_functions"], "0")
                self.assertIn("0 dependency functions verified", row["correctness_result"])
                self.assertEqual(row["independent_review"], "pending")
                self.assertEqual(row["mission_scope"], "slice_singletons")
                self.assertIn("issues/V-METADATA.md", row["issues"])
                self.assertIn("array/singleton.rs", row["correctness_proof"])
                self.assertIn("vstd/array.rs:11-21,90-95,115-121,175-183", row["view"])
        shared = coverage["core::slice::from_ref"]
        mutable = coverage["core::slice::from_mut"]
        self.assertEqual(shared["completeness_result"], "deterministic")
        self.assertEqual(shared["completeness_checked_goals"], "1")
        self.assertTrue((ROOT / shared["native_query"]).is_file())
        self.assertTrue(mutable["completeness_result"].startswith("deterministic;"))
        self.assertIn("full initial sequence + full returned T", mutable["completeness_result"])
        self.assertIn(
            "same initial T and arbitrary lawful final caller sequence",
            mutable["completeness_result"],
        )
        self.assertEqual(mutable["completeness_checked_goals"], "1")
        self.assertEqual(mutable["completeness_proof"], "proofs/completeness/slice/from_mut.rs")
        self.assertTrue((ROOT / mutable["native_query"]).is_file())
        self.assertIn("proofs/completeness/slice/from_mut_state.rs", mutable["view"])
        self.assertEqual(
            mutable["checker_report"],
            ";".join(
                f"logs/singleton-writeback/completeness/from_mut-ghost-inputs/{phase}.json"
                for phase in ("analyze", "replay")
            ),
        )
        self.assertIn("issues/S-MUT-RETURN.md", mutable["issues"])

    def test_export_rejects_narrowed_comparisons_and_zero_goals(self):
        for api, logs in export_completeness.SINGLETON_CHECKER_LOGS.items():
            report = json.loads((ROOT / logs / "analyze.json").read_text())
            for corruption in (
                "premise", "ignored", "ignored-dimension", "zero-goals",
                "baseline", "comparison", "generic-bound",
            ):
                with self.subTest(api=api, corruption=corruption):
                    changed = copy.deepcopy(report)
                    result = changed["results"][0]
                    proof = result["proofs"][0]
                    comparison = proof["native"]["det_spec"]
                    if corruption == "premise":
                        comparison["det_check_template"] += "\nrequires false,"
                    elif corruption == "ignored":
                        comparison["equal_policy"]["ignore_fields"] = ["element"]
                    elif corruption == "ignored-dimension":
                        result["coverage"]["ignored_dimensions"].append("writeback")
                    elif corruption == "zero-goals":
                        proof["verified_goals"] = 0
                    elif corruption == "baseline":
                        result["baseline"]["constraints"] = ["false"]
                    elif corruption == "comparison":
                        comparison["equal_fn_def"] = comparison["equal_fn_def"].replace(
                            "(r1 =~= r2)" if api == "from_ref" else "((r1)@.1 == (r2)@.1)",
                            "true",
                        )
                    else:
                        comparison["generics_decl"] = "<T: Copy>"
                    with patch.object(export_completeness.json, "loads", return_value=changed):
                        with self.assertRaises(ValueError):
                            export_completeness.checked_singleton_run(api, "analyze")

    def test_mutable_export_rejects_stale_dependencies_in_either_snapshot_before_writing(self):
        read_bytes = Path.read_bytes
        for phase in ("analyze", "replay"):
            report = json.loads(
                (ROOT / export_completeness.SINGLETON_CHECKER_LOGS["from_mut"]
                 / f"{phase}.json").read_text()
            )
            for dependency in (
                "proofs/completeness/slice/inputs/from_mut.rs",
                "proofs/completeness/slice/from_mut_state.rs",
                "specs/slice/raw.rs",
                "specs/slice/raw_post.rs",
                "proofs/completeness/slice/singletons.toml",
            ):
                snapshot = Path(report["run_dir"]) / "workspace" / dependency

                def changed_bytes(path):
                    data = read_bytes(path)
                    return data + b"\n" if path == snapshot else data

                with self.subTest(phase=phase, dependency=dependency), patch.object(
                    Path, "read_bytes", changed_bytes
                ), patch.object(Path, "write_text") as write:
                    with self.assertRaisesRegex(
                        ValueError, f"checked snapshot: {re.escape(dependency)}"
                    ):
                        export_completeness.singleton_evidence(["from_mut"])
                    write.assert_not_called()

    def test_mutable_export_rejects_enabled_original_search_guards(self):
        read_text = Path.read_text
        report = json.loads(
            (ROOT / export_completeness.SINGLETON_CHECKER_LOGS["from_mut"] / "analyze.json").read_text()
        )
        query = Path(report["results"][0]["baseline"]["artifact"])

        def enabled_guard(path, *args, **kwargs):
            text = read_text(path, *args, **kwargs)
            return text.replace("(not g_neq_tuple!)", "g_neq_tuple!") if path == query else text

        with patch.object(Path, "read_text", enabled_guard):
            with self.assertRaisesRegex(ValueError, "did not disable every search guard"):
                export_completeness.checked_singleton_run("from_mut", "analyze")

    def test_invalid_programmatic_selections_do_not_write(self):
        for apis in ([], [""], ["default_mut"], ["from_mut", "from_mut"]):
            with self.subTest(apis=apis), patch.object(Path, "write_text") as write:
                with self.assertRaisesRegex(ValueError, "Select distinct singleton APIs"):
                    export_completeness.singleton_evidence(apis)
                write.assert_not_called()

    def test_selectors_preserve_the_existing_dispatch(self):
        cases = (
            ([], "readonly_evidence", ()),
            (["--defaults"], "default_evidence", (("default_shared", "default_mut"),)),
            (["--defaults", "default_mut"], "default_evidence", (["default_mut"],)),
            (["--singletons"], "singleton_evidence", (("from_ref", "from_mut"),)),
            (["--singletons", "from_ref"], "singleton_evidence", (["from_ref"],)),
            (["--singletons", "from_mut"], "singleton_evidence", (["from_mut"],)),
        )
        for args, selected, arguments in cases:
            with self.subTest(args=args), patch.object(sys, "argv", ["export_completeness.py", *args]):
                with patch.object(
                    export_completeness, "readonly_evidence", side_effect=RuntimeError("selected")
                ) as readonly, patch.object(
                    export_completeness, "default_evidence", side_effect=RuntimeError("selected")
                ) as defaults, patch.object(
                    export_completeness, "singleton_evidence", side_effect=RuntimeError("selected")
                ) as singletons:
                    with self.assertRaisesRegex(RuntimeError, "^selected$"):
                        export_completeness.main()
                    for name, function in (
                        ("readonly_evidence", readonly),
                        ("default_evidence", defaults),
                        ("singleton_evidence", singletons),
                    ):
                        if name == selected:
                            function.assert_called_once_with(*arguments)
                        else:
                            function.assert_not_called()

    def test_invalid_and_mixed_selectors_are_rejected(self):
        for args in (
            ["--singletons", "default_mut"],
            ["--singletons", "--defaults"],
            ["--singletons", ""],
            ["--singletons", "from_mut", "from_mut"],
            ["--singletons", "from_ref", "from_mut", "from_ref"],
        ):
            with self.subTest(args=args), patch.object(
                sys, "argv", ["export_completeness.py", *args]
            ), patch.object(sys, "stderr", io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    export_completeness.main()
                self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
