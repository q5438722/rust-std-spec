import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class MutableEndpointNativeRunner(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get(
            "TMPDIR", check_native.ROOT / "logs/mutable-endpoints/scratch",
        ))
        scratch.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(
            dir=scratch, prefix="mutable-endpoints-runner-test-",
        )
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.proofs = self.project / "proofs/correctness/slice"
        (self.proofs / "proposals").mkdir(parents=True)
        self.contract = self.project / "specs/slice/mutable_endpoints.rs"
        self.contract.parent.mkdir(parents=True)
        self.contract.write_bytes(
            (check_native.ROOT / "specs/slice/mutable_endpoints.rs").read_bytes(),
        )
        self.behavior = (
            check_native.ROOT / "tests/mutable_endpoint_behavior.rs"
        ).read_text()
        (self.project / "tests").mkdir()
        (self.project / "tests/mutable_endpoint_behavior.rs").write_text(self.behavior)
        for api in ("first_mut", "last_mut"):
            for relative in (Path(f"{api}.rs"), Path(f"proposals/{api}.rs")):
                (self.proofs / relative).write_bytes(
                    (check_native.MUTABLE_ENDPOINT_PROOFS / relative).read_bytes(),
                )
        self.inputs = {
            path: path.read_bytes() for path in self.project.rglob("*") if path.is_file()
        }
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.mutable_endpoint_negative_cases()
        }
        self.generic_mir = "\n".join(
            f"fn {module}::{api}(_1: &mut [T]) -> Option<&mut T> {{}}"
            for module in ("original", "adopted") for api in ("first_mut", "last_mut")
        )

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

    @staticmethod
    def paths(root):
        root = root.resolve()
        return (
            root / "target/mutable-endpoints/native",
            root / "logs/mutable-endpoints/native",
        )

    def invoke(self, run, root=None, redirected=True):
        args = ["--group", "mutable-endpoints"]
        if redirected:
            args += ["--output-root", str(root or self.output_root)]
        with patch.object(check_native, "ROOT", self.project), patch.object(
            check_native, "MUTABLE_ENDPOINT_PROOFS", self.proofs,
        ), patch.object(
            check_native, "check_pattern_comparison", side_effect=AssertionError("existing dispatch"),
        ), patch.object(
            check_native, "check_singletons", side_effect=AssertionError("singleton dispatch"),
        ), patch.object(
            check_native, "check_ascii_case", side_effect=AssertionError("ASCII dispatch"),
        ), patch.dict(
            check_native.os.environ, {"RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/wrong"},
        ), patch.object(
            check_native.subprocess, "run", side_effect=run,
        ), patch("builtins.print"):
            check_native.main(args)

    def compiler(self, root=None, override=None):
        output, logs = self.paths(root or self.output_root)
        binary = output / "mutable_endpoint_behavior"
        derived = logs / "source_mutable_endpoints.rs"
        metadata = logs / "mutable_endpoints.rmeta"
        mir = logs / "mutable_endpoints.mir"
        harness = logs / "mutable_endpoint_behavior.rs"
        behavior_mir = logs / "mutable_endpoint_behavior.mir"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, self.project)
            self.assertTrue(text and capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["RUSTUP_HOME"], "/home/chentianyu/.rustup")
            for variable in ("TMPDIR", "TMP", "TEMP"):
                self.assertEqual(env[variable], str(output))
            self.assertEqual(env["SLICE_MUTABLE_ENDPOINTS_SOURCE"], str(derived))
            self.assertTrue(derived.is_file())
            self.assertEqual(harness.read_text(), self.behavior)
            self.assertEqual(list(output.glob("rejected-*.rmeta")), [])
            returncode, stdout, stderr = 0, "", ""
            if command == ["rustc", "+1.96.0", "-vV"]:
                name, stdout = "rustc-version", "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=mutable_endpoints", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ]:
                name = "compile-metadata-mir"
                metadata.write_bytes(b"mock native metadata\n")
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
                    "running 17 tests\n"
                    "test result: ok. 17 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=mutable_endpoint_rejection", "--error-format=json",
                ])
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, logs)
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\n'
                    'include!(env!("SLICE_MUTABLE_ENDPOINTS_SOURCE"));\n' + body + "\n",
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

    def test_exact_authority_adopted_current_and_pure_bindings_are_retained(self):
        with patch.object(check_native, "MUTABLE_ENDPOINT_PROOFS", self.proofs):
            text, spans, mappings = check_native.mutable_endpoint_source()
        self.assertIn("ADOPTED current source-proof input", text)
        self.assertIn("pub mod adopted", text)
        self.assertNotIn("proposal", text)
        for span in spans:
            source = Path(span["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(span["text"], "".join(source[span["start"] - 1:span["end"]]))
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "documentation"],
            [("first_mut", 159, 173), ("last_mut", 285, 299)],
        )
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "function"],
            [("first_mut", 178, 180), ("last_mut", 304, 306)],
        )
        self.assertEqual(
            [s["role"] for s in spans if s["kind"] == "proof"],
            ["current", "current"],
        )
        self.assertEqual(
            [s["text"] for s in spans if s["kind"] == "pure-postconditions"],
            [self.contract.read_text()],
        )
        for mapping, api in zip(mappings, ("first_mut", "last_mut")):
            self.assertEqual(mapping["api"], f"<[T]>::{api}")
            self.assertEqual(mapping["native_adopted"], f"adopted::{api}")
            self.assertNotIn("proposal", mapping)
            self.assertNotEqual(mapping["current"]["body"], mapping["original_body"])
            self.assertIn(mapping["original_body"], text.split("pub mod adopted {")[0])
            self.assertIn(mapping["current"]["body"], text.split("pub mod adopted {")[1])
            authority = next(
                span for span in spans if span["kind"] == "function" and span["name"] == api
            )
            self.assertEqual(
                mapping["original_body"],
                authority["text"].splitlines()[1][4:].replace("self", "slice"),
            )
            proof = mapping["current"]
            self.assertEqual(Path(proof["path"]), self.proofs / f"{api}.rs")
            lines = Path(proof["path"]).read_text().splitlines()
            self.assertEqual(
                "\n".join(lines[proof["body_start"] - 1:proof["body_end"]]), proof["body"],
            )
            self.assertEqual(Path(proof["contract"]), self.contract)
            self.assertEqual(
                proof["signature"],
                f"pub const fn {api}<T>(slice: &mut [T]) -> (result: Option<&mut T>)",
            )
            self.assertIn("old(slice)@", proof["ensures"])
            self.assertIn("Some(*final(value))", proof["ensures"])
            self.assertIn("Some(*value) }, final(slice)@", proof["ensures"])
            self.assertNotIn(f".{api}(", proof["body"])
            self.assertIn(proof["signature"].replace(
                "-> (result: Option<&mut T>)", "-> Option<&mut T>",
            ), text)
        for erased in ("#[stable(", "#[rustc_const_stable(", "ensures", "vstd", "final("):
            self.assertNotIn(erased, text)
        self.assert_inputs_unchanged()

    def test_selected_group_retains_evidence_and_preserves_old_outputs(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected):
                root = self.output_root if redirected else self.project
                output, logs = self.paths(root)
                preserved = {
                    output / "previous-output": "previous executable\n",
                    logs / "previous.log": "previous evidence\n",
                }
                for group in (
                    "defaults", "singleton", "ascii-case", "endpoints", "splits",
                    "mutable-endpoints-proposal",
                ):
                    preserved[root / f"target/{group}/native/previous"] = "old group output\n"
                    preserved[root / f"logs/{group}/native/results.json"] = "old group evidence\n"
                for path, content in preserved.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                run, seen = self.compiler(root)
                self.invoke(run, root, redirected)
                self.assertEqual(seen, [
                    "rustc-version", "compile-metadata-mir", "compile", "behavior", *self.cases,
                ])
                self.assertEqual(list(output.iterdir()), [output / "previous-output"])
                for path, content in preserved.items():
                    self.assertEqual(path.read_text(), content)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["group"], "mutable-endpoints")
                self.assertIn("ADOPTED current first_mut/last_mut", results["source_status"])
                self.assertEqual(results["positive_tests"], 17)
                self.assertEqual(len(results["negative_cases"]), 96)
                for case in results["negative_cases"]:
                    self.assertTrue(case["passed"])
                    self.assertEqual(case["returncode"], 1)
                    self.assertEqual(Path(case["input"]).read_text(), case["source"])
                    self.assertIn(self.cases[case["name"]][0], case["source"])
                    self.assertEqual(
                        Path(case["log"]).read_text(), self.diagnostic(case["expected"]),
                    )
                for kind in ("metadata", "mir"):
                    self.assertTrue(Path(results[kind]["path"]).is_file())
                    self.assertEqual(len(results[kind]["generic_functions"]), 4)
                self.assertTrue(Path(results["mir"]["behavior_path"]).is_file())
                self.assertTrue(all(Path(p).is_file() for p in results["mir"]["source_inputs"]))
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 100)
                self.assertEqual([c["returncode"] for c in commands], [0] * 4 + [1] * 96)
                for command in commands:
                    self.assertIsNone(command["RUSTC_BOOTSTRAP"])
                    self.assertEqual(command["RUSTUP_HOME"], "/home/chentianyu/.rustup")
                    self.assertEqual(command["cwd"], str(self.project))
                    self.assertEqual(
                        Path(command["log"]).read_text(), command["stdout"] + command["stderr"],
                    )
                    self.assertTrue(Path(command["log"]).is_relative_to(root))
                dependencies = json.loads((logs / "dependencies.json").read_text())
                self.assertEqual(dependencies["current_proof_inputs"], [
                    str(self.proofs / f"{api}.rs") for api in ("first_mut", "last_mut")
                ])
                self.assertNotIn("isolated_proof_inputs", dependencies)
                self.assertEqual(dependencies["unchanged_contracts"], [str(self.contract)])
                self.assertIn("not an equivalence proof", dependencies["mir_use"])
                self.assert_inputs_unchanged()

    def test_relative_output_root_changes_neither_cwd_nor_source_roots(self):
        before_cwd = Path.cwd()
        run, seen = self.compiler()
        self.invoke(run, os.path.relpath(self.output_root))
        self.assertEqual(len(seen), 100)
        self.assertEqual(Path.cwd(), before_cwd)
        self.assertEqual(self.inputs, {
            path: path.read_bytes() for path in self.project.rglob("*") if path.is_file()
        })
        self.assertFalse((self.project / "target").exists())
        self.assertFalse((self.project / "logs").exists())

    def test_authority_docs_attributes_signatures_and_bodies_cannot_drift(self):
        original = check_native.SOURCE.read_text().splitlines(keepends=True)
        changes = (
            (101, "impl<T>", "impl<T: Copy>"),
            (117, "ptr::metadata(self)", "0"),
            (159, "first element", "last element"),
            (167, "*first = 5", "*first = 6"),
            (174, "1.0.0", "1.1.0"),
            (175, "1.83.0", "1.84.0"),
            (178, "pub const fn", "pub fn"),
            (178, "&mut self", "&self"),
            (179, "[first, ..]", "[_, first, ..]"),
            (285, "last item", "first item"),
            (293, "*last = 10", "*last = 11"),
            (304, "Option<&mut T>", "Option<&T>"),
            (305, "Some(last)", "None"),
        )
        for index, (line, old, new) in enumerate(changes):
            with self.subTest(line=line, variant=index):
                changed = original.copy()
                self.assertIn(old, changed[line - 1])
                changed[line - 1] = changed[line - 1].replace(old, new, 1)
                source = self.root / f"authority-{index}.rs"
                source.write_text("".join(changed))
                root = self.root / f"authority-drift-{index}"
                run = Mock()
                with patch.object(check_native, "SOURCE", source):
                    with self.assertRaisesRegex(ValueError, "Source span changed"):
                        self.invoke(run, root)
                run.assert_not_called()
                _, logs = self.paths(root)
                self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
        self.assert_inputs_unchanged()

    def test_current_mutation_lifetime_const_and_mapping_drift_are_rejected(self):
        for api, endpoint, pattern in (
            ("first_mut", "first", "[first, ..]"), ("last_mut", "last", "[.., last]"),
        ):
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
                ("Option<&mut T>", "Option<&T>"),
                ("Option<&mut T>", "Option<T>"),
                ("Option<&mut T>", "Option<&'static mut T>"),
                ("    ensures", "    requires slice.len() > 0,\n    ensures"),
                (f"contracts::{api}_post", "contracts::other_post"),
                ("old(slice)@", "slice@"),
                ("Some(*final(value))", "Some(*value)"),
                ("Some(*value) }, final(slice)@", "Some(*final(value)) }, final(slice)@"),
                ("final(slice)@", "old(slice)@"),
                ("specs/slice/mutable_endpoints.rs", "specs/slice/mod.rs"),
                ("use vstd::prelude::*;", "use vstd::slice::*;"),
                ("verus! {", "fn hidden() {}\nverus! {"),
                ("pub const fn", "#[verifier::external_body]\npub const fn"),
                ("pub const fn", "#[verifier::external]\npub const fn"),
                (body, "    None"),
                (body, f"    slice.{api}()"),
                (body, f"    <[T]>::{api}(slice)"),
                (body, "    proof { assume(false); }\n" + body),
                (body, "    admit();\n" + body),
                (body, body + "\n    // Additional executable input drift."),
                (body, f"    if let {pattern} = slice {{ Some({endpoint}) }} else {{ None }}"),
                ("slice.len() == 0", "slice.is_empty()"),
                (
                    ("Some(&mut slice[0])", "Some(&mut slice[1])")
                    if api == "first_mut"
                    else ("let i = slice.len() - 1;", "let i = slice.len() - 2;")
                ),
            ]
            for index, (old, new) in enumerate(changes):
                with self.subTest(api=api, variant=index):
                    self.assertIn(old, original)
                    path.write_text(original.replace(old, new, 1))
                    run = Mock()
                    root = self.root / f"current-{api}-drift-{index}"
                    try:
                        with self.assertRaisesRegex(ValueError, "Mutable endpoint current source drift"):
                            self.invoke(run, root)
                        run.assert_not_called()
                        _, logs = self.paths(root)
                        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                        self.assertEqual(
                            json.loads((logs / "results.json").read_text())["status"], "failed",
                        )
                    finally:
                        path.write_text(original)
        self.assert_inputs_unchanged()

    def test_missing_or_modified_isolated_proposals_cannot_affect_the_native_route(self):
        with patch.object(check_native, "MUTABLE_ENDPOINT_PROOFS", self.proofs):
            text, spans, mappings = check_native.mutable_endpoint_source()
        paths = [self.proofs / f"proposals/{api}.rs" for api in ("first_mut", "last_mut")]
        for variant in ("missing", "modified"):
            with self.subTest(variant=variant):
                for path in paths:
                    if variant == "missing":
                        path.unlink()
                    else:
                        path.write_text("not an adopted native input\n")
                root = self.root / f"isolated-{variant}"
                run, seen = self.compiler(root)
                try:
                    self.invoke(run, root)
                    self.assertEqual(len(seen), 100)
                    _, logs = self.paths(root)
                    self.assertEqual((logs / "source_mutable_endpoints.rs").read_text(), text)
                    self.assertEqual(json.loads((logs / "source-spans.json").read_text()), spans)
                    self.assertEqual(json.loads((logs / "source-mappings.json").read_text()), mappings)
                    self.assertEqual(
                        json.loads((logs / "results.json").read_text())["status"], "passed",
                    )
                finally:
                    for path in paths:
                        path.write_bytes(self.inputs[path])
        self.assert_inputs_unchanged()

    def test_pure_postconditions_cannot_be_weakened_or_rebound(self):
        original = self.contract.read_text()
        changes = (
            ("pub open spec fn", "pub fn"),
            ("<T>(", "<T: Copy>("),
            ("caller_final: Option<T>", "caller_final: T"),
            ("observations: (Option<T>, Seq<T>)", "observations: (Seq<T>, Option<T>)"),
            ("input_initial.len() == 0 && observations.1 =~= seq![]", "true"),
            ("observations.1 =~= seq![]", "observations.1 == seq![]"),
            ("value == input_initial[0]", "value == written"),
            ("input_initial.update(0, written)", "input_initial"),
            ("input_initial.update(input_initial.len() - 1, written)", "input_initial"),
            ("_ => false", "_ => true"),
            ("verus! {", "verus! {\n#[verifier::external_body]"),
            ("match (observations.0, caller_final) {", "assume(false);\n    match (observations.0, caller_final) {"),
        )
        for index, (old, new) in enumerate(changes):
            with self.subTest(variant=index):
                self.assertIn(old, original)
                self.contract.write_text(original.replace(old, new, 1))
                run = Mock()
                try:
                    with self.assertRaisesRegex(ValueError, "Mutable endpoint pure contract drift"):
                        self.invoke(run, self.root / f"contract-drift-{index}")
                    run.assert_not_called()
                finally:
                    self.contract.write_text(original)
        self.assert_inputs_unchanged()

    def test_missing_inputs_fail_without_compiler_execution(self):
        for index, path in enumerate(self.inputs):
            if path.is_relative_to(self.proofs / "proposals"):
                continue
            with self.subTest(path=path):
                original = path.read_bytes()
                path.unlink()
                run = Mock()
                root = self.root / f"missing-{index}"
                try:
                    with self.assertRaises(FileNotFoundError):
                        self.invoke(run, root)
                    run.assert_not_called()
                    _, logs = self.paths(root)
                    self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                    self.assertEqual(
                        json.loads((logs / "results.json").read_text())["status"], "failed",
                    )
                finally:
                    path.write_bytes(original)

    def test_negative_cases_cover_every_implementation_and_live_borrow_conflicts(self):
        expected = {
            "wrong-receiver": "E0308", "missing-receiver": "E0061",
            "extra-argument": "E0061", "shared-receiver": "E0308",
            "immutable-binding": "E0596", "wrong-element": "E0308",
            "owned-result": "E0308", "slice-result": "E0308", "missing-option": "E0308",
            "shared-function-result": "E0308", "shared-function-argument": "E0308",
            "local-escape": "E0515", "short-lifetime": "E0597", "static-escape": None,
            "conflicting-shared-access": "E0502", "conflicting-mutable-access": "E0499",
        }
        self.assertEqual(set(self.cases), {
            f"{module}-{api}-{case}" for module in ("original", "adopted", "public")
            for api in ("first_mut", "last_mut") for case in expected
        })
        for name, (text, diagnostic) in self.cases.items():
            module, api, case = name.split("-", 2)
            binding = f"<[u8]>::{api}" if module == "public" else f"{module}::{api}::<u8>"
            self.assertIn(binding, text)
            self.assertNotIn("API", text)
            self.assertEqual(diagnostic["code"], expected[case])
            if case == "static-escape":
                self.assertEqual(diagnostic["message"], "lifetime may not live long enough")
            if case.startswith("conflicting-"):
                self.assertLess(text.index("core::hint::black_box"), text.index("*result = 2"))

    def test_missing_or_duplicate_negative_targets_never_pass(self):
        cases = list(check_native.mutable_endpoint_negative_cases())
        for index, incomplete in enumerate(([], cases[:1], [cases[0]] * 96)):
            with self.subTest(variant=index):
                root = self.root / f"incomplete-negatives-{index}"
                run = Mock()
                with patch.object(check_native, "mutable_endpoint_negative_cases", return_value=incomplete):
                    with self.assertRaisesRegex(AssertionError, "Expected 96 distinct"):
                        self.invoke(run, root)
                run.assert_not_called()
                _, logs = self.paths(root)
                self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_cleanup_on_each_failure_preserves_inputs_evidence_and_earlier_outputs(self):
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
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(commands[-1]["returncode"], 101)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertTrue((logs / "source_mutable_endpoints.rs").is_file())
                self.assertTrue((logs / "mutable_endpoint_behavior.rs").is_file())
                if stage == first:
                    self.assertFalse(results["negative_cases"][0]["passed"])
                    self.assertTrue(Path(results["negative_cases"][0]["input"]).is_file())
                self.assert_inputs_unchanged()

    def test_execution_errors_are_logged_and_current_outputs_are_cleaned(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile-metadata-mir", "compile", "behavior", first):
            with self.subTest(stage=stage):
                root = self.root / f"execution-error-{stage}"

                def fail(name, result):
                    if name == stage:
                        raise OSError("cannot execute command")
                    return result

                run, seen = self.compiler(root, fail)
                with self.assertRaisesRegex(OSError, "cannot execute command"):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], stage)
                output, logs = self.paths(root)
                self.assertEqual(list(output.iterdir()), [])
                commands = json.loads((logs / "commands.json").read_text())
                self.assertIsNone(commands[-1]["returncode"])
                self.assertIn("cannot execute command", commands[-1]["error"])
                self.assertIn("cannot execute command", (logs / f"{stage}.log").read_text())
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_wrong_rust_version_stops_before_compilation(self):
        def wrong(name, result):
            if name == "rustc-version":
                result.stdout = "rustc 1.97.0\nrelease: 1.97.0\n"
            return result

        run, seen = self.compiler(override=wrong)
        with self.assertRaisesRegex(AssertionError, "Expected Rust 1.96.0"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version"])

    def test_missing_empty_or_nongeneric_metadata_and_mir_never_pass(self):
        variants = ("metadata-missing", "metadata-empty", "mir-missing", "mir-empty", "mir-incomplete", "mir-shared", "mir-monomorphic")
        for variant in variants:
            with self.subTest(variant=variant):
                root = self.root / variant
                _, logs = self.paths(root)

                def incomplete(name, result):
                    if name == "compile-metadata-mir":
                        metadata, mir = logs / "mutable_endpoints.rmeta", logs / "mutable_endpoints.mir"
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
                        else:
                            mir.write_text(self.generic_mir.replace("T", "u8"))
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaises((FileNotFoundError, AssertionError)):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir"])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_linked_executable_and_behavior_mir_are_required_before_execution(self):
        for variant in ("binary-missing", "mir-missing", "mir-empty"):
            with self.subTest(variant=variant):
                root = self.root / variant
                output, logs = self.paths(root)

                def incomplete(name, result):
                    if name == "compile":
                        if variant == "binary-missing":
                            (output / "mutable_endpoint_behavior").unlink()
                        elif variant == "mir-missing":
                            (logs / "mutable_endpoint_behavior.mir").unlink()
                        else:
                            (logs / "mutable_endpoint_behavior.mir").write_text("")
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaisesRegex(AssertionError, "Expected (linked|retained)"):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile"])
                self.assertEqual(list(output.iterdir()), [])

    def test_zero_partial_ignored_filtered_or_unexecuted_tests_never_pass(self):
        valid = (
            "running 17 tests\n"
            "test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;\n"
        )
        for index, summary in enumerate((
            "",
            valid.replace("17", "0"),
            valid.replace("17", "16"),
            valid.replace("17 passed; 0 failed; 0 ignored", "16 passed; 0 failed; 1 ignored"),
            valid.replace("17 passed", "16 passed").replace("0 filtered out", "1 filtered out"),
            valid.replace("ok. 17 passed; 0 failed", "FAILED. 16 passed; 1 failed"),
            valid.removeprefix("running 17 tests\n"),
            valid + valid,
        )):
            with self.subTest(summary=summary):
                root = self.root / f"incomplete-runtime-{index}"

                def incomplete(name, result):
                    if name == "behavior":
                        result.stdout = summary
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaisesRegex(
                    AssertionError, "Expected all 17 executed mutable endpoint tests",
                ):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile", "behavior"])
                output, logs = self.paths(root)
                self.assertEqual(list(output.iterdir()), [])
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertEqual(results["positive_tests"], 0)
                self.assertEqual(results["negative_cases"], [])

    def test_only_the_specific_single_expected_diagnostic_is_accepted(self):
        log = self.root / "diagnostic.log"
        for expected in ({"code": "E0502"}, {
            "code": None, "message": "lifetime may not live long enough",
        }):
            valid = self.diagnostic(expected)
            accepted = check_native.subprocess.CompletedProcess([], 1, "", valid)
            self.assertEqual(
                check_native.check_singleton_rejection(accepted, expected, log)["code"],
                expected["code"],
            )
            for code, stderr in (
                (0, valid), (2, valid), (101, valid), (-11, valid),
                (1, ""), (1, "compiler unavailable"), (1, "[]"), (1, valid + valid),
                (1, self.diagnostic({"code": "E0425"})),
                (1, self.diagnostic({"code": None, "message": "linking failed"})),
            ):
                with self.subTest(expected=expected, code=code, stderr=stderr):
                    failed = check_native.subprocess.CompletedProcess([], code, "", stderr)
                    with self.assertRaises(AssertionError):
                        check_native.check_singleton_rejection(failed, expected, log)

    def test_a_successful_or_irrelevant_negative_compilation_fails_the_group(self):
        first = next(iter(self.cases))
        for index, (code, stderr) in enumerate((
            (0, ""),
            (1, self.diagnostic({"code": "E0061"})),
            (1, self.diagnostic({"code": None, "message": "linking failed"})),
        )):
            with self.subTest(code=code, stderr=stderr):
                root = self.root / f"bad-diagnostic-{index}"

                def wrong(name, result):
                    if name == first:
                        result.returncode, result.stderr = code, stderr
                    return result

                run, seen = self.compiler(root, wrong)
                with self.assertRaisesRegex(AssertionError, "Expected rustc exit 1"):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], first)
                output, logs = self.paths(root)
                self.assertEqual(list(output.iterdir()), [])
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertFalse(results["negative_cases"][0]["passed"])
                self.assertEqual((logs / f"{first}.log").read_text(), stderr)

    def test_existing_named_outputs_are_not_overwritten_or_deleted(self):
        first = next(iter(self.cases))
        paths = [
            "target/mutable-endpoints/native/mutable_endpoint_behavior",
            f"target/mutable-endpoints/native/rejected-{first}.rmeta",
            *(f"logs/mutable-endpoints/native/{name}" for name in (
                "source_mutable_endpoints.rs", "mutable_endpoint_behavior.rs",
                "mutable_endpoints.rmeta", "mutable_endpoints.mir",
                "mutable_endpoint_behavior.mir",
                "source-spans.json", "source-mappings.json", "dependencies.json",
                "commands.json", "results.json", "rustc-version.log",
                "compile-metadata-mir.log", "compile.log", "behavior.log",
                f"{first}.log", f"rejection-{first}.rs",
            )),
        ]
        for index, relative in enumerate(paths):
            with self.subTest(relative=relative):
                root = self.root / f"previous-{index}"
                existing = root / relative
                existing.parent.mkdir(parents=True)
                existing.write_text("preserve previous evidence\n")
                run = Mock()
                with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite existing native"):
                    self.invoke(run, root)
                run.assert_not_called()
                self.assertEqual(existing.read_text(), "preserve previous evidence\n")
                self.assertEqual([p for p in root.rglob("*") if p.is_file()], [existing])

    def test_dangling_named_output_symlinks_are_not_overwritten(self):
        _, logs = self.paths(self.output_root)
        logs.mkdir(parents=True)
        existing = logs / "results.json"
        existing.symlink_to(self.output_root / "missing-target")
        run = Mock()
        with self.assertRaises(FileExistsError):
            self.invoke(run)
        run.assert_not_called()
        self.assertTrue(existing.is_symlink())
        self.assertFalse(existing.exists())

    def test_output_parent_symlinks_cannot_escape_the_requested_root(self):
        for name in ("target", "logs"):
            with self.subTest(name=name):
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

    def test_help_describes_adoption_and_the_new_group_dispatches(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--help"])
        self.assertEqual(result.exception.code, 0)
        help_text = " ".join(stdout.getvalue().split())
        self.assertIn("--group mutable-endpoints", help_text)
        self.assertIn("ADOPTED current proof bodies", help_text)
        self.assertIn("proposals are retained but are not native inputs", help_text)
        self.assertNotIn("mutable-endpoints-proposal", help_text)
        self.assertIn("{defaults,singleton,ascii-case}", help_text)
        with patch.object(check_native, "check_mutable_endpoints") as selected:
            check_native.main([
                "--group", "mutable-endpoints", "--output-root", str(self.output_root),
            ])
        selected.assert_called_once_with(self.output_root.resolve())

    def test_obsolete_proposal_route_is_rejected_without_execution(self):
        with patch("sys.stderr", new_callable=io.StringIO) as stderr, patch.object(
            check_native, "check_mutable_endpoints",
        ) as selected, patch.object(check_native.subprocess, "run") as run:
            with self.assertRaises(SystemExit) as result:
                check_native.main([
                    "--group", "mutable-endpoints-proposal",
                    "--output-root", str(self.output_root),
                ])
        self.assertEqual(result.exception.code, 2)
        self.assertIn("invalid choice: 'mutable-endpoints-proposal'", stderr.getvalue())
        selected.assert_not_called()
        run.assert_not_called()
        self.assertFalse(self.output_root.exists())


if __name__ == "__main__":
    unittest.main()
