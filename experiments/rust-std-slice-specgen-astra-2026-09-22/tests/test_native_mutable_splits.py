from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class MutableSplitNativeRunner(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get(
            "TMPDIR", check_native.ROOT / "target/mutable-splits/python-tests",
        ))
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="case-", dir=scratch)
        self.root = Path(temporary.name)
        self.addCleanup(temporary.cleanup)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.proofs = self.project / "proofs/correctness/slice"
        self.contract = self.project / "specs/slice/mutable_splits_post.rs"
        self.authority = self.root / "authority/library/core/src/slice/mod.rs"
        self.vstd = self.root / "vstd"
        copies = [
            (check_native.SOURCE, self.authority),
            (check_native.SOURCE.with_name("raw.rs"), self.authority.with_name("raw.rs")),
            (
                check_native.SOURCE.parent.parent / "ptr/docs/add.md",
                self.authority.parent.parent / "ptr/docs/add.md",
            ),
            (check_native.MUTABLE_SPLIT_VSTD / "slice.rs", self.vstd / "slice.rs"),
            (
                check_native.MUTABLE_SPLIT_VSTD / "std_specs/slice.rs",
                self.vstd / "std_specs/slice.rs",
            ),
            (check_native.ROOT / "specs/slice/mutable_splits_post.rs", self.contract),
            (
                check_native.ROOT / "tests/mutable_split_behavior.rs",
                self.project / "tests/mutable_split_behavior.rs",
            ),
        ]
        for api in ("split_first_mut", "split_last_mut"):
            relative = Path(f"{api}.rs")
            copies.append((check_native.MUTABLE_SPLIT_PROOFS / relative, self.proofs / relative))
        for source, destination in copies:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        self.inputs = {destination: destination.read_bytes() for _, destination in copies}
        self.behavior = (self.project / "tests/mutable_split_behavior.rs").read_text()
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.mutable_split_negative_cases()
        }
        self.generic_mir = "\n".join(
            f"fn {module}::{api}(_1: &mut [T]) -> Option<(&mut T, &mut [T])> {{}}"
            for module in ("original", "adopted") for api in ("split_first_mut", "split_last_mut")
        )

    @staticmethod
    def paths(root):
        root = root.resolve()
        return root / "target/mutable-splits/native", root / "logs/mutable-splits/native"

    def source_patches(self):
        stack = ExitStack()
        for name, value in (
            ("ROOT", self.project), ("SOURCE", self.authority),
            ("MUTABLE_SPLIT_PROOFS", self.proofs), ("MUTABLE_SPLIT_VSTD", self.vstd),
        ):
            stack.enter_context(patch.object(check_native, name, value))
        return stack

    def invoke(self, run, root=None, redirected=True):
        args = ["--group", "mutable-splits"]
        if redirected:
            args += ["--output-root", str(root or self.output_root)]
        with self.source_patches() as stack:
            for name in (
                "check_pattern_comparison", "check_endpoints", "check_mutable_endpoints",
                "check_singletons", "check_ascii_case",
            ):
                stack.enter_context(patch.object(
                    check_native, name, side_effect=AssertionError(f"old group executed: {name}"),
                ))
            stack.enter_context(patch.dict(check_native.os.environ, {
                "RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/wrong",
                "TMPDIR": "wrong", "TMP": "wrong", "TEMP": "wrong", "PATH": "original-path",
            }))
            stack.enter_context(patch.object(check_native.subprocess, "run", side_effect=run))
            stack.enter_context(patch("builtins.print"))
            check_native.main(args)

    @staticmethod
    def diagnostic(expected):
        code = expected["code"]
        return json.dumps({
            "$message_type": "diagnostic", "level": "error",
            "code": None if code is None else {"code": code},
            "message": expected.get("message", "mock compile rejection"),
            "spans": [{"file_name": "probe.rs"}],
        }) + "\n" + json.dumps({
            "$message_type": "diagnostic", "level": "error", "code": None,
            "message": "aborting due to 1 previous error", "spans": [],
        }) + "\n"

    def compiler(self, root=None, override=None):
        output, logs = self.paths(root or self.output_root)
        derived = logs / "source_mutable_splits.rs"
        harness = logs / "mutable_split_behavior.rs"
        metadata = logs / "mutable_splits.rmeta"
        mir = logs / "mutable_splits.mir"
        behavior_mir = logs / "mutable_split_behavior.mir"
        binary = output / "mutable_split_behavior"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, self.project)
            self.assertTrue(text and capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["RUSTUP_HOME"], "/home/chentianyu/.rustup")
            self.assertEqual(
                env["PATH"], str(self.project / "toolchain/review-native/bin") + os.pathsep + "original-path",
            )
            for variable in ("TMPDIR", "TMP", "TEMP"):
                self.assertEqual(env[variable], str(output))
            self.assertEqual(env["SLICE_MUTABLE_SPLITS_SOURCE"], str(derived))
            self.assertTrue(derived.is_file())
            self.assertEqual(harness.read_text(), self.behavior)
            self.assertEqual(list(output.glob("rejected-*.rmeta")), [])
            returncode, stdout, stderr = 0, "", ""
            if command == ["rustc", "+1.96.0", "-vV"]:
                name, stdout = "rustc-version", "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=mutable_splits", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ]:
                name = "compile-metadata-mir"
                metadata.write_bytes(b"mock metadata\n")
                mir.write_text(self.generic_mir)
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "--error-format=json", "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=link,mir={behavior_mir}", "-o", str(binary),
            ]:
                name = "compile"
                binary.write_text("mock linked executable\n")
                behavior_mir.write_text(self.generic_mir)
            elif command == [str(binary), "--test-threads=1", "--color=never"]:
                name = "behavior"
                self.assertTrue(binary.is_file())
                stdout = (
                    "running 19 tests\n"
                    "test result: ok. 19 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=mutable_split_rejection", "--error-format=json",
                ])
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, logs)
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\n'
                    'include!(env!("SLICE_MUTABLE_SPLITS_SOURCE"));\n' + body + "\n",
                )
                rejected = output / f"rejected-{name}.rmeta"
                self.assertEqual(command[7:], [
                    "-C", "overflow-checks=yes", "-C", "opt-level=0",
                    f"--emit=metadata={rejected}",
                ])
                rejected.write_text("mock partial compiler output\n")
                returncode, stderr = 1, self.diagnostic(expected)
            seen.append(name)
            result = check_native.subprocess.CompletedProcess(command, returncode, stdout, stderr)
            return override(name, result) if override else result

        return run, seen

    def assert_inputs_unchanged(self):
        for path, before in self.inputs.items():
            self.assertEqual(path.read_bytes(), before)

    def assert_failed_without_compiling(self, root, run):
        run.assert_not_called()
        _, logs = self.paths(root)
        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_exact_authority_and_current_pure_mapping_and_dependencies(self):
        with self.source_patches():
            text, spans, mappings = check_native.mutable_split_source()
        self.assertIn("ADOPTED", text)
        self.assertIn("permission: issues/V-SLICE-PATTERN.md", text)
        self.assertIn("pub mod adopted", text)
        self.assertNotIn("pub mod proposal", text)
        self.assertNotIn("proof {", text)
        self.assertNotIn("mut_ref_slice_len_eq", text)
        for span in spans:
            source = Path(span["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(span["text"], "".join(source[span["start"] - 1:span["end"]]))
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "documentation"],
            [("split_first_mut", 202, 215), ("split_last_mut", 244, 257)],
        )
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "function"],
            [("split_first_mut", 220, 222), ("split_last_mut", 262, 264)],
        )
        self.assertEqual(
            [(s["kind"], s["start"], s["end"]) for s in spans if s["role"] == "native-dependency"],
            [
                ("slice-len", 102, 118), ("split-at-mut", 1959, 1991),
                ("split-at-mut-unchecked", 2056, 2112), ("split-at-mut-checked", 2163, 2204),
                ("as-mut-ptr", 730, 759), ("from-raw-parts-mut", 143, 196), ("pointer-add", 1, 24),
            ],
        )
        self.assertEqual(
            [s["kind"] for s in spans if s["role"] == "vstd-contract"],
            [
                "slice-view", "slice-len", "slice-index-trait", "mutable-borrow-length",
                "mutable-usize-index", "split-at-mut", "existing-split-first-mut",
            ],
        )
        self.assertEqual(
            [s["text"] for s in spans if s["kind"] == "pure-postconditions"],
            [self.contract.read_text()],
        )
        for mapping, api in zip(mappings, ("split_first_mut", "split_last_mut")):
            self.assertEqual(mapping["api"], f"<[T]>::{api}")
            self.assertEqual(mapping["native_adopted"], f"adopted::{api}")
            self.assertNotIn("proposal", mapping)
            self.assertNotIn("native_proposal", mapping)
            self.assertNotIn("original-proof", mapping)
            self.assertNotEqual(mapping["current"]["body"], mapping["original_body"])
            authority = next(
                s for s in spans if s["kind"] == "function" and s["name"] == api
            )
            self.assertEqual(
                mapping["original_body"],
                authority["text"].splitlines()[1][4:].replace("self", "slice"),
            )
            self.assertIn(mapping["original_body"], text.split("pub mod adopted {")[0])
            self.assertIn(mapping["current"]["native_body"], text.split("pub mod adopted {")[1])
            proof = mapping["current"]["erased_proof"]
            self.assertEqual(mapping["current"]["body"].count(proof), 1)
            self.assertEqual(
                mapping["current"]["native_body"],
                mapping["current"]["body"].replace(proof, "", 1),
            )
            proof = mapping["current"]
            path = self.proofs / f"{api}.rs"
            self.assertEqual(Path(proof["path"]), path)
            self.assertEqual(
                "\n".join(path.read_text().splitlines()[proof["body_start"] - 1:proof["body_end"]]),
                proof["body"],
            )
            self.assertEqual(Path(proof["contract"]), self.contract)
            self.assertEqual(
                proof["signature"],
                f"pub const fn {api}<T>(slice: &mut [T]) -> (result: Option<(&mut T, &mut [T])>)",
            )
            for relation in (
                f"contracts::{api}_post", "old(slice)@",
                "Some((*final(value), final(remainder)@))",
                "Some((*value, remainder@))", "final(slice)@",
            ):
                self.assertIn(relation, proof["ensures"])
            self.assertNotIn(f".{api}(", proof["body"])
            self.assertNotIn("assume_specification", path.read_text())
            self.assertNotIn("specs/slice/mutable_splits.rs", path.read_text())
        for erased in ("#[stable(", "#[rustc_const_stable(", "ensures", "vstd", "final("):
            self.assertNotIn(erased, text)
        self.assert_inputs_unchanged()

    def test_success_retains_evidence_redirects_only_new_group_and_cleans_transients(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected):
                root = self.output_root if redirected else self.project
                output, logs = self.paths(root)
                preserved = {
                    output / "previous-output": "previous executable\n",
                    logs / "previous.log": "previous evidence\n",
                }
                for group in ("defaults", "singleton", "ascii-case", "endpoints", "splits", "mutable-endpoints"):
                    preserved[root / f"target/{group}/native/previous"] = "old output\n"
                    preserved[root / f"logs/{group}/native/results.json"] = "old evidence\n"
                for path, content in preserved.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                run, seen = self.compiler(root)
                self.invoke(run, root, redirected)
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile", "behavior", *self.cases])
                self.assertEqual(list(output.iterdir()), [output / "previous-output"])
                for path, content in preserved.items():
                    self.assertEqual(path.read_text(), content)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["group"], "mutable-splits")
                self.assertIn("ADOPTED current", results["source_status"])
                self.assertIn("not a source equivalence", results["limits"])
                self.assertIn("cannot be established from address equality", results["limits"])
                self.assertEqual(results["positive_tests"], 19)
                self.assertEqual(len(results["negative_cases"]), 216)
                for case in results["negative_cases"]:
                    self.assertTrue(case["passed"])
                    self.assertEqual(case["returncode"], 1)
                    self.assertEqual(Path(case["input"]).read_text(), case["source"])
                    self.assertEqual(Path(case["log"]).read_text(), self.diagnostic(case["expected"]))
                for kind in ("metadata", "mir"):
                    self.assertTrue(Path(results[kind]["path"]).is_file())
                    self.assertEqual(len(results[kind]["generic_functions"]), 4)
                self.assertTrue(Path(results["mir"]["behavior_path"]).is_file())
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 220)
                self.assertEqual([c["returncode"] for c in commands], [0] * 4 + [1] * 216)
                for command in commands:
                    self.assertIsNone(command["RUSTC_BOOTSTRAP"])
                    self.assertEqual(command["RUSTUP_HOME"], "/home/chentianyu/.rustup")
                    self.assertEqual(command["cwd"], str(self.project))
                    self.assertEqual(Path(command["log"]).read_text(), command["stdout"] + command["stderr"])
                    self.assertTrue(Path(command["log"]).is_relative_to(root))
                dependencies = json.loads((logs / "dependencies.json").read_text())
                self.assertEqual(dependencies["current_proof_inputs"], [
                    str(self.proofs / f"{api}.rs") for api in ("split_first_mut", "split_last_mut")
                ])
                self.assertNotIn("isolated_proof_inputs", dependencies)
                self.assertEqual(dependencies["unchanged_contracts"], [str(self.contract)])
                self.assertIn("not an equivalence proof", dependencies["mir_use"])
                self.assertIn("never the public", dependencies["contract_use"])
                self.assertEqual(dependencies["linker"], str(self.project / "toolchain/review-native/bin/cc"))
                self.assert_inputs_unchanged()

    def test_relative_output_root_preserves_cwd_and_source_roots(self):
        before = Path.cwd()
        run, seen = self.compiler()
        self.invoke(run, os.path.relpath(self.output_root))
        self.assertEqual(Path.cwd(), before)
        self.assertEqual(len(seen), 220)
        self.assertFalse((self.project / "target").exists())
        self.assertFalse((self.project / "logs").exists())
        self.assert_inputs_unchanged()

    def test_authority_docs_attributes_unconstrained_signatures_and_patterns_cannot_drift(self):
        original = self.authority.read_text().splitlines(keepends=True)
        for index, (line, old, new) in enumerate((
            (101, "impl<T>", "impl<T: Copy>"), (117, "ptr::metadata(self)", "0"),
            (202, "first and all the rest", "first and some of the rest"),
            (210, "*first = 3", "*first = 6"), (211, "elements[0] = 4", "elements[0] = 7"),
            (216, "1.5.0", "1.6.0"), (217, "1.83.0", "1.84.0"),
            (220, "pub const fn", "pub fn"), (220, "&mut self", "&self"),
            (221, "Some((first, tail))", "Some((tail, first))"),
            (244, "last and all the rest", "first and all the rest"),
            (256, "&[4, 5, 3]", "&[3, 4, 5]"),
            (262, "Option<(&mut T, &mut [T])>", "Option<(&T, &[T])>"),
            (263, "[init @ .., last]", "[init, .., last]"),
        )):
            with self.subTest(line=line):
                changed = original.copy()
                self.assertIn(old, changed[line - 1])
                changed[line - 1] = changed[line - 1].replace(old, new, 1)
                self.authority.write_text("".join(changed))
                run = Mock()
                root = self.root / f"authority-drift-{index}"
                try:
                    with self.assertRaisesRegex(ValueError, "Source span changed"):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    self.authority.write_text("".join(original))

    def test_current_sources_require_exact_const_generic_lifetimes_pure_bindings_and_bodies(self):
        for api in ("split_first_mut", "split_last_mut"):
            path = self.proofs / f"{api}.rs"
            original = path.read_text()
            body = original.split("\n{\n", 1)[1].removesuffix("\n}\n}\n")
            changes = [
                ("pub const fn", "pub fn"),
                ("<T>(slice", "<T: Copy>(slice"),
                ("<T>(slice", "<T: Eq>(slice"),
                ("<T>(slice", "<T: Default>(slice"),
                ("<T>(slice", "<T: 'static>(slice"),
                ("slice: &mut [T]", "slice: &[T]"),
                ("slice: &mut [T]", "slice: &'static mut [T]"),
                ("Option<(&mut T, &mut [T])>", "Option<(&mut [T], &mut T)>"),
                ("Option<(&mut T, &mut [T])>", "Option<(&T, &mut [T])>"),
                ("Option<(&mut T, &mut [T])>", "Option<(&mut T, &[T])>"),
                ("Option<(&mut T, &mut [T])>", "Option<(T, Seq<T>)>"),
                ("Option<(&mut T, &mut [T])>", "Option<(&'static mut T, &'static mut [T])>"),
                ("    ensures", "    requires slice.len() > 0,\n    ensures"),
                (f"contracts::{api}_post", "contracts::split_first_post"),
                ("old(slice)@", "slice@"),
                ("Some((*final(value), final(remainder)@))", "Some((*value, final(remainder)@))"),
                ("Some((*final(value), final(remainder)@))", "Some((*final(value), remainder@))"),
                ("Some((*final(value), final(remainder)@))", "Some((*final(value), seq![]))"),
                ("Some((*value, remainder@))", "Some((*value, seq![]))"),
                ("Some((*value, remainder@))", "Some((*final(value), remainder@))"),
                ("final(slice)@", "old(slice)@"),
                ("specs/slice/mutable_splits_post.rs", "specs/slice/mutable_splits.rs"),
                ("specs/slice/mutable_splits_post.rs", "specs/slice/mod.rs"),
                ("use vstd::prelude::*;", "use vstd::slice::*;"),
                ("verus! {", "fn hidden() {}\nverus! {"),
                ("pub const fn", "#[verifier::external_body]\npub const fn"),
                ("pub const fn", "#[verifier::external]\npub const fn"),
                (body, "    None"),
                (body, f"    slice.{api}()"),
                (body, f"    <[T]>::{api}(slice)"),
                (body, "    proof { assert(true); }\n" + body),
                (body, "    proof { assume(false); }\n" + body),
                (body, "    admit();\n" + body),
                (body, body + "\n    // Unapproved body text."),
                ("vstd::slice::mut_ref_slice_len_eq", "vstd::slice::axiom_spec_len"),
                ("slice.len() == 0", "slice.is_empty()"),
            ]
            if api == "split_first_mut":
                changes += [
                    ("slice.split_at_mut(1)", "slice.split_at_mut(0)"),
                    ("mut_ref_slice_len_eq(&tail)", "mut_ref_slice_len_eq(&head)"),
                    (
                        "        proof {\n"
                        "            vstd::slice::mut_ref_slice_len_eq(&tail);\n"
                        "        }\n", "",
                    ),
                    ("Some((&mut head[0], tail))", "Some((&mut tail[0], head))"),
                    (body, "    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }"),
                ]
            else:
                changes += [
                    ("slice.len() - 1", "slice.len() - 2"),
                    ("slice.split_at_mut(i)", "slice.split_at_mut(1)"),
                    ("mut_ref_slice_len_eq(&init)", "mut_ref_slice_len_eq(&last)"),
                    (
                        "        proof {\n"
                        "            vstd::slice::mut_ref_slice_len_eq(&init);\n"
                        "        }\n", "",
                    ),
                    ("Some((&mut last[0], init))", "Some((&mut init[0], last))"),
                    (body, "    if let [init @ .., last] = slice { Some((last, init)) } else { None }"),
                ]
            for index, (old, new) in enumerate(changes):
                with self.subTest(api=api, variant=index):
                    self.assertIn(old, original)
                    path.write_text(original.replace(old, new, 1))
                    run = Mock()
                    root = self.root / f"current-{api}-drift-{index}"
                    try:
                        with self.assertRaisesRegex(ValueError, "Mutable split current source drift"):
                            self.invoke(run, root)
                        self.assert_failed_without_compiling(root, run)
                    finally:
                        path.write_text(original)
        self.assert_inputs_unchanged()

    def test_historical_proposals_are_not_native_inputs(self):
        with self.source_patches():
            expected = check_native.mutable_split_source()
        for api in ("split_first_mut", "split_last_mut"):
            path = self.proofs / f"proposals/{api}.rs"
            path.parent.mkdir(exist_ok=True)
            path.write_text("not an adopted source input\n")
            with self.source_patches():
                self.assertEqual(check_native.mutable_split_source(), expected)
            path.unlink()
            with self.source_patches():
                self.assertEqual(check_native.mutable_split_source(), expected)
        self.assert_inputs_unchanged()

    def test_pure_candidate_cannot_omit_initial_or_final_full_relations_or_length_domain(self):
        original = self.contract.read_text()
        changes = (
            ("pub open spec fn", "pub fn"), ("<T>(", "<T: Copy>("),
            ("caller_final: Option<(T, Seq<T>)>", "caller_final: Option<T>"),
            ("observations: (Option<(T, Seq<T>)>, Seq<T>)", "observations: (Seq<T>, Option<T>)"),
            ("input_initial.len() == 0 && observations.1 =~= seq![]", "true"),
            ("observations.1 =~= seq![]", "observations.1 == seq![]"),
            ("input_initial.len() > 0", "input_initial.len() > 1"),
            ("value == input_initial[0]", "value == written"),
            ("value == input_initial[input_initial.len() - 1]", "value == written"),
            ("remainder == input_initial.subrange(1, input_initial.len() as int)", "remainder == seq![]"),
            ("remainder == input_initial.subrange(0, input_initial.len() - 1)", "remainder == seq![]"),
            ("written_remainder.len() == remainder.len()", "remainder.len() == remainder.len()"),
            ("observations.1 =~= seq![written] + written_remainder", "true"),
            ("observations.1 =~= written_remainder + seq![written]", "true"),
            ("seq![written] + written_remainder", "written_remainder + seq![written]"),
            ("written_remainder + seq![written]", "seq![written] + written_remainder"),
            ("_ => false", "_ => true"),
            ("verus! {", "verus! {\n#[verifier::external_body]"),
            ("verus! {", "verus! {\npub assume_specification<T>[ <[T]>::split_first_mut ]();"),
            ("match (observations.0, caller_final) {", "match (caller_final, caller_final) {"),
        )
        for index, (old, new) in enumerate(changes):
            with self.subTest(variant=index):
                self.assertIn(old, original)
                self.contract.write_text(original.replace(old, new, 1))
                run = Mock()
                root = self.root / f"candidate-drift-{index}"
                try:
                    with self.assertRaisesRegex(ValueError, "Mutable split pure contract drift"):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    self.contract.write_text(original)
        self.assert_inputs_unchanged()

    def test_missing_extraction_or_behavior_inputs_never_invoke_the_compiler(self):
        for index, (path, original) in enumerate(self.inputs.items()):
            with self.subTest(path=path):
                path.unlink()
                run = Mock()
                root = self.root / f"missing-{index}"
                try:
                    with self.assertRaises(FileNotFoundError):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    path.write_bytes(original)

    def test_all_three_bindings_check_both_lifetimes_conflicts_and_overlapping_aliases(self):
        base = {
            "wrong-receiver": "E0308", "missing-receiver": "E0061",
            "extra-argument": "E0061", "shared-receiver": "E0308",
            "immutable-binding": "E0596", "wrong-element": "E0308",
            "wrong-result-element": "E0308", "wrong-result-remainder": "E0308",
            "reversed-result": "E0308", "owned-element": "E0308", "owned-remainder": "E0308",
            "missing-option": "E0308", "shared-function-argument": "E0308",
            "shared-function-element": "E0308", "shared-function-remainder": "E0308",
            "shared-function-results": "E0308",
        }
        for component in ("element", "remainder"):
            for action, code in (
                ("local", "E0515"), ("short", "E0597"), ("static", None),
                ("conflicting-shared", "E0502"), ("conflicting-mutable", "E0499"),
                ("duplicate-mutable", "E0499"), ("shared-then-mutable", "E0502"),
                ("duplicate-moved", "E0382"),
            ):
                base[f"{action}-{component}"] = code
            for order in ("element-first", "slice-first"):
                base[f"overlap-{component}-{order}"] = "E0499"
        self.assertEqual(set(self.cases), {
            f"{module}-{api}-{case}" for module in ("original", "adopted", "public")
            for api in ("split_first_mut", "split_last_mut") for case in base
        })
        self.assertEqual(len(self.cases), 216)
        for name, (text, expected) in self.cases.items():
            module, api, case = name.split("-", 2)
            binding = f"<[u8]>::{api}" if module == "public" else f"{module}::{api}::<u8>"
            self.assertIn(binding, text)
            self.assertNotIn("API", text)
            self.assertNotIn("unsafe", text)
            self.assertEqual(expected["code"], base[case])
            if case.startswith("static-"):
                self.assertEqual(expected["message"], "lifetime may not live long enough")
            if case.startswith("conflicting-"):
                written = "*view = 3" if case.endswith("element") else "view[0] = 3"
                self.assertLess(text.index("core::hint::black_box"), text.index(written))

    def test_missing_or_duplicate_negative_targets_never_pass(self):
        cases = list(check_native.mutable_split_negative_cases())
        for index, incomplete in enumerate(([], cases[:1], [cases[0]] * 216)):
            root = self.root / f"incomplete-targets-{index}"
            run = Mock()
            with patch.object(check_native, "mutable_split_negative_cases", return_value=incomplete):
                with self.assertRaisesRegex(AssertionError, "Expected 216 distinct"):
                    self.invoke(run, root)
            self.assert_failed_without_compiling(root, run)

    def test_failures_at_each_command_preserve_inputs_logs_and_previous_outputs(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile-metadata-mir", "compile", "behavior", first):
            with self.subTest(stage=stage):
                root = self.root / f"failed-{stage}"
                output, logs = self.paths(root)
                output.mkdir(parents=True)
                previous = output / "previous"
                previous.write_text("previous output\n")

                def fail(name, result):
                    if name == stage:
                        result.returncode, result.stdout, result.stderr = 101, "stdout\n", "failure\n"
                    return result

                run, seen = self.compiler(root, fail)
                with self.assertRaises(AssertionError):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], stage)
                self.assertEqual(list(output.iterdir()), [previous])
                self.assertEqual(previous.read_text(), "previous output\n")
                self.assertEqual((logs / f"{stage}.log").read_text(), "stdout\nfailure\n")
                self.assertEqual(json.loads((logs / "commands.json").read_text())[-1]["returncode"], 101)
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
                self.assertTrue((logs / "source_mutable_splits.rs").is_file())
                self.assert_inputs_unchanged()

    def test_missing_executables_and_os_errors_are_retained_without_installing_dependencies(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile-metadata-mir", "compile", "behavior", first):
            root = self.root / f"execution-error-{stage}"

            def fail(name, result):
                if name == stage:
                    raise FileNotFoundError("missing requested executable")
                return result

            run, seen = self.compiler(root, fail)
            with self.assertRaisesRegex(FileNotFoundError, "missing requested executable"):
                self.invoke(run, root)
            self.assertEqual(seen[-1], stage)
            output, logs = self.paths(root)
            self.assertEqual(list(output.iterdir()), [])
            command = json.loads((logs / "commands.json").read_text())[-1]
            self.assertIsNone(command["returncode"])
            self.assertIn("missing requested executable", command["error"])
            self.assertIn("missing requested executable", (logs / f"{stage}.log").read_text())
            self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_wrong_rust_version_fails_before_compilation(self):
        def wrong(name, result):
            if name == "rustc-version":
                result.stdout = "rustc 1.97.0\nrelease: 1.97.0\n"
            return result

        run, seen = self.compiler(override=wrong)
        with self.assertRaisesRegex(AssertionError, "Expected Rust 1.96.0"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version"])

    def test_nonempty_metadata_and_all_four_correct_generic_mir_signatures_are_required(self):
        for variant in (
            "metadata-missing", "metadata-empty", "mir-missing", "mir-empty",
            "mir-incomplete", "mir-shared", "mir-monomorphic", "mir-reversed",
        ):
            with self.subTest(variant=variant):
                root = self.root / variant
                _, logs = self.paths(root)

                def incomplete(name, result):
                    if name == "compile-metadata-mir":
                        metadata, mir = logs / "mutable_splits.rmeta", logs / "mutable_splits.mir"
                        if variant == "metadata-missing":
                            metadata.unlink()
                        elif variant == "metadata-empty":
                            metadata.write_bytes(b"")
                        elif variant == "mir-missing":
                            mir.unlink()
                        elif variant == "mir-empty":
                            mir.write_text("")
                        elif variant == "mir-incomplete":
                            mir.write_text(self.generic_mir.splitlines()[0])
                        elif variant == "mir-shared":
                            mir.write_text(self.generic_mir.replace("&mut", "&"))
                        elif variant == "mir-reversed":
                            mir.write_text(self.generic_mir.replace(
                                "Option<(&mut T, &mut [T])>", "Option<(&mut [T], &mut T)>",
                            ))
                        else:
                            mir.write_text(self.generic_mir.replace("T", "u8"))
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaises((FileNotFoundError, AssertionError)):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir"])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_runtime_requires_real_link_output_and_retained_behavior_mir(self):
        for variant in ("binary-missing", "mir-missing", "mir-empty"):
            root = self.root / variant
            output, logs = self.paths(root)

            def incomplete(name, result):
                if name == "compile":
                    if variant == "binary-missing":
                        (output / "mutable_split_behavior").unlink()
                    elif variant == "mir-missing":
                        (logs / "mutable_split_behavior.mir").unlink()
                    else:
                        (logs / "mutable_split_behavior.mir").write_text("")
                return result

            run, seen = self.compiler(root, incomplete)
            with self.assertRaisesRegex(AssertionError, "Expected (linked|retained)"):
                self.invoke(run, root)
            self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile"])
            self.assertEqual(list(output.iterdir()), [])

    def test_zero_partial_ignored_filtered_unexecuted_or_duplicate_test_summaries_fail(self):
        valid = (
            "running 19 tests\n"
            "test result: ok. 19 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;\n"
        )
        for index, summary in enumerate((
            "", valid.replace("19", "0"), valid.replace("19", "18"),
            valid.replace("19 passed; 0 failed; 0 ignored", "18 passed; 0 failed; 1 ignored"),
            valid.replace("19 passed", "18 passed").replace("0 filtered out", "1 filtered out"),
            valid.replace("ok. 19 passed; 0 failed", "FAILED. 18 passed; 1 failed"),
            valid.removeprefix("running 19 tests\n"), valid + valid,
        )):
            root = self.root / f"incomplete-runtime-{index}"

            def incomplete(name, result):
                if name == "behavior":
                    result.stdout = summary
                return result

            run, seen = self.compiler(root, incomplete)
            with self.assertRaisesRegex(AssertionError, "Expected all 19 executed mutable split tests"):
                self.invoke(run, root)
            self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile", "behavior"])
            output, logs = self.paths(root)
            self.assertEqual(list(output.iterdir()), [])
            results = json.loads((logs / "results.json").read_text())
            self.assertEqual(results["positive_tests"], 0)
            self.assertEqual(results["negative_cases"], [])
            self.assertEqual(results["status"], "failed")

    def test_success_crash_unrelated_or_multiple_negative_diagnostics_never_pass(self):
        first = next(iter(self.cases))
        valid = self.diagnostic(self.cases[first][1])
        for index, (code, stderr) in enumerate((
            (0, ""), (2, valid), (101, valid), (-11, valid),
            (1, ""), (1, "not JSON"), (1, "[]"), (1, valid + valid),
            (1, self.diagnostic({"code": "E0061"})),
            (1, self.diagnostic({"code": None, "message": "linking failed"})),
        )):
            root = self.root / f"bad-diagnostic-{index}"

            def wrong(name, result):
                if name == first:
                    result.returncode, result.stderr = code, stderr
                return result

            run, seen = self.compiler(root, wrong)
            with self.assertRaises(AssertionError):
                self.invoke(run, root)
            self.assertEqual(seen[-1], first)
            output, logs = self.paths(root)
            self.assertEqual(list(output.iterdir()), [])
            results = json.loads((logs / "results.json").read_text())
            self.assertEqual(results["status"], "failed")
            self.assertFalse(results["negative_cases"][0]["passed"])
            self.assertEqual((logs / f"{first}.log").read_text(), stderr)

    def test_each_named_evidence_or_artifact_collision_is_rejected_before_execution(self):
        first, last = next(iter(self.cases)), next(reversed(self.cases))
        paths = [
            "target/mutable-splits/native/mutable_split_behavior",
            *(f"target/mutable-splits/native/rejected-{name}.rmeta" for name in (first, last)),
            *(f"logs/mutable-splits/native/{name}" for name in (
                "source_mutable_splits.rs", "mutable_split_behavior.rs",
                "mutable_splits.rmeta", "mutable_splits.mir",
                "mutable_split_behavior.mir",
                "source-spans.json", "source-mappings.json", "dependencies.json",
                "commands.json", "results.json", "rustc-version.log",
                "compile-metadata-mir.log", "compile.log", "behavior.log",
                f"{first}.log", f"rejection-{first}.rs", f"{last}.log", f"rejection-{last}.rs",
            )),
        ]
        for index, relative in enumerate(paths):
            with self.subTest(relative=relative):
                root = self.root / f"collision-{index}"
                existing = root / relative
                existing.parent.mkdir(parents=True)
                existing.write_text("retain earlier result\n")
                run = Mock()
                with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite existing native"):
                    self.invoke(run, root)
                run.assert_not_called()
                self.assertEqual(existing.read_text(), "retain earlier result\n")
                self.assertEqual([p for p in root.rglob("*") if p.is_file()], [existing])

    def test_dangling_named_output_symlinks_are_not_overwritten(self):
        _, logs = self.paths(self.output_root)
        logs.mkdir(parents=True)
        existing = logs / "results.json"
        existing.symlink_to(self.root / "missing")
        run = Mock()
        with self.assertRaises(FileExistsError):
            self.invoke(run)
        run.assert_not_called()
        self.assertTrue(existing.is_symlink())
        self.assertFalse(existing.exists())

    def test_output_parent_symlinks_cannot_escape_the_requested_root(self):
        for name in ("target", "logs"):
            root = self.root / f"escaping-{name}"
            outside = self.root / f"outside-{name}"
            root.mkdir()
            outside.mkdir()
            (root / name).symlink_to(outside, target_is_directory=True)
            run = Mock()
            with self.assertRaisesRegex(ValueError, "Native output escapes"):
                self.invoke(run, root)
            run.assert_not_called()
            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(list(root.iterdir()), [root / name])

    def test_new_group_dispatch_does_not_change_existing_selectors(self):
        for group, selected, kwargs in (
            ("mutable-splits", "check_mutable_splits", {}),
            ("mutable-endpoints", "check_mutable_endpoints", {}),
            ("splits", "check_pattern_comparison", {"splits": True}),
            ("endpoints", "check_endpoints", {}),
            ("ascii-case", "check_ascii_case", {}),
            ("singleton", "check_singletons", {}),
        ):
            with self.subTest(group=group), ExitStack() as stack:
                mocks = {
                    name: stack.enter_context(patch.object(check_native, name))
                    for name in (
                        "check_mutable_splits", "check_mutable_endpoints",
                        "check_pattern_comparison", "check_endpoints", "check_ascii_case",
                        "check_singletons",
                    )
                }
                check_native.main(["--group", group, "--output-root", str(self.output_root)])
                mocks[selected].assert_called_once_with(self.output_root.resolve(), **kwargs)
                for name, mock in mocks.items():
                    if name != selected:
                        mock.assert_not_called()

    def test_help_preserves_adopted_scope_and_does_not_restore_old_proposal_routes(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--help"])
        self.assertEqual(result.exception.code, 0)
        help_text = " ".join(stdout.getvalue().split())
        self.assertIn("--group mutable-splits compares", help_text)
        self.assertIn("proposals are retained but are not native inputs", help_text)
        self.assertIn("ADOPTED current proof bodies", help_text)
        self.assertIn("{defaults,singleton,ascii-case}", help_text)
        for group in (
            "endpoints-proposal", "splits-proposal", "mutable-endpoints-proposal",
            "mutable-splits-proposal",
        ):
            with patch("sys.stderr", new_callable=io.StringIO), patch.object(
                check_native.subprocess, "run",
            ) as run:
                with self.assertRaises(SystemExit) as result:
                    check_native.main(["--group", group])
                self.assertEqual(result.exception.code, 2)
                run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
