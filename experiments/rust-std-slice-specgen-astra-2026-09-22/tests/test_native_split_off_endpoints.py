from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class SplitOffEndpointNativeRunner(unittest.TestCase):
    group = "split-off-endpoints"

    def setUp(self):
        scratch = Path(os.environ.get(
            "TMPDIR", check_native.ROOT / f"target/{self.group}/python-tests",
        ))
        scratch.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(prefix="case-", dir=scratch)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.proofs = self.project / "proofs/correctness/slice"
        self.authority = self.root / "authority/library/core/src/slice/mod.rs"
        self.contract = self.project / "specs/slice/split_off_post.rs"
        self.public_contract = self.contract.with_name("split_off.rs")
        copies = [
            (check_native.SOURCE, self.authority),
            (check_native.ROOT / "specs/slice/split_off_post.rs", self.contract),
            (check_native.ROOT / "specs/slice/split_off.rs", self.public_contract),
            (
                check_native.ROOT / "tests/split_off_endpoint_behavior.rs",
                self.project / "tests/split_off_endpoint_behavior.rs",
            ),
        ]
        for relative in ("split_off_first.rs", "split_off_last.rs", "split_last.rs"):
            copies.append((check_native.SPLIT_OFF_ENDPOINT_PROOFS / relative, self.proofs / relative))
        for source, destination in copies:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        self.inputs = {destination: destination.read_bytes() for _, destination in copies}
        self.proposal = self.proofs / "proposals/split_off_last.rs"
        self.proposal.parent.mkdir(parents=True)
        self.proposal.write_text("Retained historical proposal; not a native input.\n")
        self.historical_inputs = {self.proposal: self.proposal.read_bytes()}
        self.behavior = (self.project / "tests/split_off_endpoint_behavior.rs").read_text()
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.split_off_endpoint_negative_cases()
        }
        self.generic_mir = "\n".join(
            f"fn {module}::{api}(_1: &mut &[T]) -> Option<&T> {{}}"
            for module, apis in (
                ("original", ("split_off_first", "split_off_last")),
                ("adopted", ("split_off_first", "split_off_last")),
            )
            for api in apis
        ) + "\nfn split_last(_1: &[T]) -> Option<(&T, &[T])> {}\n"

    def paths(self, root):
        root = root.resolve()
        return root / f"target/{self.group}/native", root / f"logs/{self.group}/native"

    def source_patches(self):
        stack = ExitStack()
        for name, value in (
            ("ROOT", self.project), ("SOURCE", self.authority),
            ("SPLIT_OFF_ENDPOINT_PROOFS", self.proofs),
        ):
            stack.enter_context(patch.object(check_native, name, value))
        return stack

    def invoke(self, run, root=None, redirected=True):
        args = ["--group", self.group]
        if redirected:
            args += ["--output-root", str(root or self.output_root)]
        with self.source_patches() as stack:
            for name in (
                "check_pattern_comparison", "check_endpoints", "check_mutable_endpoints",
                "check_mutable_splits", "check_singletons", "check_ascii_case",
            ):
                stack.enter_context(patch.object(
                    check_native, name, side_effect=AssertionError(f"old group executed: {name}"),
                ))
            stack.enter_context(patch.dict(check_native.os.environ, {
                "RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/wrong", "PATH": "original-path",
                "TMPDIR": "wrong", "TMP": "wrong", "TEMP": "wrong",
            }))
            stack.enter_context(patch.object(check_native.subprocess, "run", side_effect=run))
            printed = stack.enter_context(patch("builtins.print"))
            check_native.main(args)
            return printed

    @staticmethod
    def diagnostic(expected):
        code = expected["code"]
        return json.dumps({
            "$message_type": "diagnostic", "level": "error",
            "code": None if code is None else {"code": code},
            "message": expected.get("message", "mock compiler rejection"),
            "spans": [{"file_name": "probe.rs"}],
        }) + "\n" + json.dumps({
            "$message_type": "diagnostic", "level": "error", "code": None,
            "message": "aborting due to 1 previous error", "spans": [],
        }) + "\n"

    def compiler(self, root=None, override=None):
        output, logs = self.paths(root or self.output_root)
        derived = logs / "source_split_off_endpoints.rs"
        harness = logs / "split_off_endpoint_behavior.rs"
        metadata = logs / "split_off_endpoints.rmeta"
        mir = logs / "split_off_endpoints.mir"
        behavior_mir = logs / "split_off_endpoint_behavior.mir"
        binary = output / "split_off_endpoint_behavior"
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
            self.assertEqual(env["SLICE_SPLIT_OFF_ENDPOINTS_SOURCE"], str(derived))
            self.assertTrue(derived.is_file())
            self.assertEqual(harness.read_text(), self.behavior)
            self.assertEqual(list(output.glob("rejected-*.rmeta")), [])
            returncode, stdout, stderr = 0, "", ""
            if command == ["rustc", "+1.96.0", "-vV"]:
                name, stdout = "rustc-version", "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=split_off_endpoints", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ]:
                name = "compile-metadata-mir"
                metadata.write_bytes(b"mock metadata\n")
                mir.write_text(self.generic_mir)
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "--error-format=json", "-C", "overflow-checks=yes", "-C", "opt-level=0",
                "-C", f"linker={self.project / 'toolchain/review-native/bin/cc'}",
                f"--emit=link,mir={behavior_mir}", "-o", str(binary),
            ]:
                name = "compile"
                binary.write_text("mock linked executable\n")
                behavior_mir.write_text(self.generic_mir)
            elif command == [str(binary), "--test-threads=1", "--color=never"]:
                name = "behavior"
                self.assertTrue(binary.is_file())
                stdout = (
                    "running 20 tests\n"
                    "test result: ok. 20 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=split_off_endpoint_rejection", "--error-format=json",
                ])
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, logs)
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\n'
                    'include!(env!("SLICE_SPLIT_OFF_ENDPOINTS_SOURCE"));\n' + body + "\n",
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
        for path, before in (self.inputs | self.historical_inputs).items():
            self.assertEqual(path.read_bytes(), before)

    def assert_failed_without_compiling(self, root, run):
        run.assert_not_called()
        _, logs = self.paths(root)
        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def assert_drift_rejected(self, path, changes, label, error):
        original = path.read_text()
        for index, (old, new) in enumerate(changes):
            with self.subTest(source=label, variant=index):
                self.assertIn(old, original)
                path.write_text(original.replace(old, new, 1))
                root = self.root / f"{label}-{index}"
                run = Mock()
                try:
                    with self.assertRaisesRegex(ValueError, error):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    path.write_text(original)

    def test_extraction_uses_exact_adopted_formals_and_only_the_approved_last_call_and_import(self):
        with self.source_patches():
            text, spans, mappings = check_native.split_off_endpoint_source()
        self.assertIn("ADOPTED current split-off endpoints", text)
        self.assertIn(
            "issues/V-ASCII-CALL-BINDING.md#independent-split-off-permission-before-adoption",
            text,
        )
        self.assertIn("pub mod original", text)
        self.assertIn("pub mod adopted", text)
        self.assertNotIn("pub mod current", text)
        self.assertNotIn("proposal", text)
        for span in spans:
            self.assertNotIn("proposals", Path(span["path"]).parts)
            lines = Path(span["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(span["text"], "".join(lines[span["start"] - 1:span["end"]]))
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "documentation"],
            [("split_off_first", 4993, 5006), ("split_off_last", 5043, 5056)],
        )
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "function"],
            [("split_off_first", 5010, 5015), ("split_off_last", 5060, 5065)],
        )
        self.assertEqual(
            [s["kind"] for s in spans if s["role"] == "contract"],
            ["pure-postconditions", "public-declarations"],
        )
        self.assertEqual([s["role"] for s in spans if s["kind"] == "proof"],
                         ["current", "current", "dependency"])
        original_module, adopted_module = text.split("pub mod adopted {", 1)
        for mapping, endpoint in zip(mappings, ("first", "last")):
            api = f"split_off_{endpoint}"
            self.assertEqual(mapping["api"], f"<[T]>::{api}")
            self.assertEqual(mapping["native_adopted"], f"adopted::{api}")
            self.assertNotIn("native_current", mapping)
            self.assertNotIn("native_proposal", mapping)
            self.assertNotIn("proposal", mapping)
            expected_body = mapping["original_body"]
            if endpoint == "last":
                expected_body = expected_body.replace(
                    "slice.split_last()", "split_dependency::split_last(*slice)", 1,
                )
            self.assertEqual(mapping["current"]["body"], expected_body)
            self.assertIn(mapping["original_body"], original_module)
            self.assertIn(mapping["current"]["body"], adopted_module)
            authority = next(s for s in spans if s["kind"] == "function" and s["name"] == api)
            self.assertEqual(
                mapping["original_body"],
                "\n".join(line[4:] for line in authority["text"].splitlines()[1:-1]).replace("self", "slice"),
            )
            proof = mapping["current"]
            self.assertEqual(
                "\n".join(Path(proof["path"]).read_text().splitlines()[proof["body_start"] - 1:proof["body_end"]]),
                proof["body"],
            )
            self.assertEqual(
                proof["signature"],
                f"pub const fn {api}<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)",
            )
            self.assertEqual(Path(proof["contract"]), self.contract)
            for binding in ("(*old(slice))@", "Some(value) => Some(*value)", "(*final(slice))@"):
                self.assertIn(binding, proof["ensures"])
            self.assertNotIn("caller_final", proof["ensures"])
            self.assertNotIn("final(value)", proof["ensures"])
            self.assertEqual(mapping["runtime_stable_since"], "1.87.0")
            self.assertIn("UNSTABLE: const_split_off_first_last", mapping["public_const"])
            self.assertIn(f"pub const fn {api}<'a, T>(slice: &mut &'a [T]) -> Option<&'a T>", text)
        first, last = [mapping["current"] for mapping in mappings]
        self.assertNotIn("dependency", first)
        self.assertNotIn("dependency_import", first)
        self.assertNotIn("split_dependency", Path(first["path"]).read_text())
        self.assertIn(
            '#[path = "split_last.rs"]\nmod split_dependency;\n', Path(last["path"]).read_text(),
        )
        dependency = last["dependency"]
        self.assertEqual(Path(dependency["path"]), self.proofs / "split_last.rs")
        self.assertEqual(last["dependency_import"], "split_last.rs")
        self.assertEqual(
            Path(dependency["path"]), Path(last["path"]).parent / last["dependency_import"],
        )
        self.assertIn(dependency["body"], (self.proofs / "split_last.rs").read_text())
        self.assertIn(dependency["body"], adopted_module)
        self.assertIn("let i = slice.len() - 1;", dependency["body"])
        self.assertIn("Some((&slice[i], slice.split_at(i).0))", dependency["body"])
        for erased in ("vstd", "ensures", "assume_specification", "proof {", "#[stable(", "#[rustc_const"):
            self.assertNotIn(erased, text)
        self.assertEqual(text.count("#[inline]"), 2)
        self.assert_inputs_unchanged()

    def test_success_retains_evidence_and_all_previous_groups_and_only_cleans_named_transients(self):
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
                    "mutable-endpoints", "mutable-splits", "split-off-endpoints-proposal",
                ):
                    preserved[root / f"target/{group}/native/previous"] = "old output\n"
                    preserved[root / f"logs/{group}/native/results.json"] = "old evidence\n"
                for name in ("commands.json", "source-spans.json", "source-mappings.json", "behavior.log"):
                    preserved[root / f"logs/split-off-endpoints-proposal/native/{name}"] = "historical proposal evidence\n"
                for path, content in preserved.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                run, seen = self.compiler(root)
                printed = self.invoke(run, root, redirected)
                self.assertEqual(
                    printed.call_args.args,
                    ("Adopted split-off endpoints: 20 runtime tests and "
                     "110 exact compiler rejections passed; not a Verus result.",),
                )
                self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile", "behavior", *self.cases])
                self.assertEqual(list(output.iterdir()), [output / "previous-output"])
                for path, content in preserved.items():
                    self.assertEqual(path.read_text(), content)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["group"], self.group)
                self.assertIn("ADOPTED current formal sources", results["source_status"])
                self.assertIn("first remains unchanged", results["source_status"])
                self.assertNotIn("proposal", results["source_status"])
                self.assertIn("Not run", results["formal_verification"])
                self.assertIn("not a source equivalence", results["limits"])
                self.assertIn("cannot be established from address equality", results["limits"])
                self.assertEqual(results["positive_tests"], 20)
                self.assertEqual(len(results["negative_cases"]), 110)
                for case in results["negative_cases"]:
                    self.assertTrue(case["passed"])
                    self.assertEqual(case["returncode"], 1)
                    self.assertEqual(Path(case["input"]).read_text(), case["source"])
                    self.assertEqual(Path(case["log"]).read_text(), self.diagnostic(case["expected"]))
                for kind in ("metadata", "mir"):
                    self.assertTrue(Path(results[kind]["path"]).is_file())
                    self.assertEqual(results[kind]["generic_functions"], [
                        "original::split_off_first", "original::split_off_last",
                        "adopted::split_off_first", "adopted::split_off_last", "split_last",
                    ])
                self.assertTrue(Path(results["mir"]["behavior_path"]).is_file())
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 114)
                self.assertEqual([c["returncode"] for c in commands], [0] * 4 + [1] * 110)
                for command in commands:
                    self.assertIsNone(command["RUSTC_BOOTSTRAP"])
                    self.assertEqual(command["RUSTUP_HOME"], "/home/chentianyu/.rustup")
                    self.assertEqual(command["cwd"], str(self.project))
                    self.assertEqual(Path(command["log"]).read_text(), command["stdout"] + command["stderr"])
                    self.assertTrue(Path(command["log"]).is_relative_to(root))
                dependencies = json.loads((logs / "dependencies.json").read_text())
                self.assertEqual(dependencies["current_proof_inputs"], [
                    str(self.proofs / f"{api}.rs") for api in ("split_off_first", "split_off_last")
                ])
                self.assertEqual(dependencies["current_dependency_input"], str(self.proofs / "split_last.rs"))
                self.assertEqual(
                    dependencies["authorization"],
                    "issues/V-ASCII-CALL-BINDING.md#independent-split-off-permission-before-adoption",
                )
                self.assertNotIn("isolated_proof_inputs", dependencies)
                self.assertNotIn("proposal", json.dumps(dependencies))
                self.assertEqual(dependencies["unchanged_contracts"], [str(self.contract), str(self.public_contract)])
                self.assertIn("never the public", dependencies["contract_use"])
                self.assertIn("not an equivalence proof", dependencies["mir_use"])
                self.assertEqual(dependencies["linker"], str(self.project / "toolchain/review-native/bin/cc"))
                self.assert_inputs_unchanged()

    def test_relative_output_root_preserves_cwd_and_sources(self):
        before = Path.cwd()
        run, seen = self.compiler()
        self.invoke(run, os.path.relpath(self.output_root))
        self.assertEqual(Path.cwd(), before)
        self.assertEqual(len(seen), 114)
        self.assertFalse((self.project / "target").exists())
        self.assertFalse((self.project / "logs").exists())
        self.assert_inputs_unchanged()

    def test_authority_documentation_attributes_signature_and_control_flow_cannot_drift(self):
        original = self.authority.read_text().splitlines(keepends=True)
        for index, (line, old, new) in enumerate((
            (101, "impl<T>", "impl<T: Copy>"),
            (4993, "first element", "last element"), (4996, "`None`", "`Some`"),
            (5001, "'a', 'b', 'c'", "'c', 'b', 'a'"),
            (5007, "#[inline]", "#[inline(always)]"), (5008, "1.87.0", "1.86.0"),
            (5009, "rustc_const_unstable", "rustc_const_stable"),
            (5009, "const_split_off_first_last", "other_const_feature"),
            (5010, "pub const fn", "pub fn"), (5010, "&mut &'a Self", "&'a mut &'a Self"),
            (5011, "Use `?`", "Use a different expression"),
            (5012, "split_first()", "split_last()"),
            (5012, "return None", "None"), (5013, "*self = rem", "*self = &[]"),
            (5014, "Some(first)", "None"),
            (5043, "last element", "first element"),
            (5059, "138539", "0"), (5060, "Option<&'a T>", "Option<&'a mut T>"),
            (5062, "split_last()", "split_first()"), (5063, "*self = rem", "let _ = rem"),
        )):
            with self.subTest(line=line):
                changed = original.copy()
                self.assertIn(old, changed[line - 1])
                changed[line - 1] = changed[line - 1].replace(old, new, 1)
                self.authority.write_text("".join(changed))
                run = Mock()
                root = self.root / f"authority-{index}"
                try:
                    with self.assertRaisesRegex(ValueError, "Source span changed"):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    self.authority.write_text("".join(original))

    def test_current_sources_require_exact_lifetimes_ensures_imports_and_assignment_order(self):
        for endpoint in ("first", "last"):
            api = f"split_off_{endpoint}"
            path = self.proofs / f"{api}.rs"
            call = (
                "slice.split_first()" if endpoint == "first"
                else "split_dependency::split_last(*slice)"
            )
            changes = [
                ("pub const fn", "pub fn"), ("<'a, T>", "<'a, T: Copy>"),
                ("<'a, T>", "<'a, T: Eq>"), ("<'a, T>", "<'a, T: Default>"),
                ("<'a, T>", "<'a, T: 'static>"),
                ("slice: &mut &'a [T]", "slice: &'a mut &'a [T]"),
                ("slice: &mut &'a [T]", "slice: &mut &'static [T]"),
                ("Option<&'a T>", "Option<&'a mut T>"), ("Option<&'a T>", "Option<T>"),
                ("Option<&'a T>", "Option<&'static T>"),
                ("    ensures", "    requires slice.len() > 0,\n    ensures"),
                ("(*old(slice))@", "(*slice)@"), ("(*final(slice))@", "(*old(slice))@"),
                ("Some(*value)", "Some(*final(value))"),
                (f"contracts::{api}_post", "contracts::split_first_post"),
                ("specs/slice/split_off_post.rs", "specs/slice/split_off.rs"),
                ("../../../specs", "../../../../specs"),
                ("use vstd::prelude::*;", "use vstd::slice::*;"),
                ("// Rust 1.96", "// Rust 1.95"),
                ("Use `?` when available in const", "Use a different expression"),
                ("verus! {", "fn hidden() {}\nverus! {"),
                ("pub const fn", "#[verifier::external_body]\npub const fn"),
                ("pub const fn", "#[verifier::external]\npub const fn"),
                ("    let Some", "    proof { assume(false); }\n    let Some"),
                ("    let Some", "    proof { assert(true); }\n    let Some"),
                ("    let Some", "    admit();\n    let Some"),
                (call, f"<[T]>::split_{endpoint}(*slice)"),
                (call, f"split_dependency::split_{endpoint}(slice)"),
                ("else { return None }", "else { return Some(&slice[0]) }"),
                ("    *slice = rem;", "    *slice = &[];"),
                (
                    f"    *slice = rem;\n    Some({endpoint})",
                    f"    let result = Some({endpoint});\n    *slice = rem;\n    result",
                ),
                (
                    f"    let Some(({endpoint}, rem)) = {call} else {{ return None }};\n    *slice = rem;",
                    f"    *slice = &[];\n    let Some(({endpoint}, rem)) = {call} else {{ return None }};",
                ),
                (f"    Some({endpoint})", "    None"),
            ]
            if endpoint == "first":
                changes.extend((
                    (call, "split_dependency::split_first(*slice)"),
                    (
                        "mod contracts;\n",
                        'mod contracts;\n#[path = "split_first.rs"]\nmod split_dependency;\n',
                    ),
                ))
            else:
                changes.extend((
                    (call, "slice.split_last()"),
                    (call, "split_dependency::split_first(*slice)"),
                    ('#[path = "split_last.rs"]', '#[path = "../slice/split_last.rs"]'),
                    ('#[path = "split_last.rs"]', '#[path = "split_first.rs"]'),
                    ('#[path = "split_last.rs"]\nmod split_dependency;\n', ""),
                    ("mod split_dependency;", "use super::split_dependency;"),
                ))
            self.assert_drift_rejected(path, changes, api, "Split-off endpoint current source drift")
        self.assert_inputs_unchanged()

    def test_historical_last_proposal_is_never_read_or_used_even_if_changed_or_removed(self):
        with self.source_patches():
            expected = check_native.split_off_endpoint_source()
        read_text = Path.read_text

        def read_native(path, *args, **kwargs):
            self.assertNotEqual(path, self.proposal, "historical proposal was read as a native input")
            return read_text(path, *args, **kwargs)

        try:
            for content in ("invalid changed historical proposal\n", None):
                if content is None:
                    self.proposal.unlink()
                else:
                    self.proposal.write_text(content)
                with self.source_patches(), patch.object(Path, "read_text", read_native):
                    self.assertEqual(check_native.split_off_endpoint_source(), expected)
            run, _ = self.compiler()
            with patch.object(Path, "read_text", read_native):
                self.invoke(run)
        finally:
            self.proposal.write_bytes(self.historical_inputs[self.proposal])
        self.assert_inputs_unchanged()

    def test_actual_local_shared_split_last_dependency_is_checked_not_guessed(self):
        self.assert_drift_rejected(self.proofs / "split_last.rs", (
            ("pub const fn", "pub fn"), ("<T>", "<T: Copy>"),
            ("slice: &[T]", "slice: &'static [T]"),
            ("Option<(&T, &[T])>", "Option<(&[T], &T)>"),
            ("specs/slice/mod.rs", "specs/slice/split_off.rs"),
            ("contracts::split_last_post(slice, result)", "contracts::split_first_post(slice, result)"),
            ("    ensures", "    requires slice.len() > 0,\n    ensures"),
            ("slice.len() == 0", "slice.is_empty()"), ("slice.len() - 1", "slice.len() - 2"),
            ("&slice[i]", "&slice[0]"), ("slice.split_at(i).0", "slice.split_at(i).1"),
            ("Some((&slice[i], slice.split_at(i).0))", "slice.split_last()"),
            ("        None", "        slice.split_last()"),
            ("pub const fn", "#[verifier::external_body]\npub const fn"),
            ("    if slice.len()", "    proof { assume(false); }\n    if slice.len()"),
        ), "dependency", "Split-off endpoint dependency source drift")
        self.assert_inputs_unchanged()

    def test_pure_candidate_requires_complete_initial_and_return_state_relations(self):
        self.assert_drift_rejected(self.contract, (
            ("pub open spec fn", "pub fn"), ("<T>(", "<T: Copy>("),
            ("observations: (Option<T>, Seq<T>)", "observations: (Option<&T>, Seq<T>)"),
            ("    observations:", "    caller_final: Seq<T>,\n    observations:"),
            ("input_initial.len() == 0 && observations.1 =~= input_initial", "true"),
            ("observations.1 =~= input_initial,", "observations.1 =~= seq![],"),
            ("input_initial.len() > 0", "input_initial.len() > 1"),
            ("value == input_initial[0]", "value == input_initial[input_initial.len() - 1]"),
            ("value == input_initial[input_initial.len() - 1]", "value == input_initial[0]"),
            ("observations.1 =~= input_initial.subrange(1, input_initial.len() as int)", "true"),
            ("observations.1 =~= input_initial.subrange(0, input_initial.len() - 1)", "true"),
            ("subrange(1, input_initial.len() as int)", "subrange(0, input_initial.len() - 1)"),
            ("subrange(0, input_initial.len() - 1)", "subrange(1, input_initial.len() as int)"),
            ("verus! {", "verus! {\npub assume_specification<T>[ <[T]>::split_off_first ]();"),
        ), "pure-candidate", "Split-off endpoint pure-postconditions drift")
        self.assert_inputs_unchanged()

    def test_separate_public_declarations_are_read_only_gates_never_compiled_assumptions(self):
        self.assert_drift_rejected(self.public_contract, (
            ('#[path = "split_off_post.rs"]', '#[path = "mod.rs"]'),
            ("<'a, T>", "<'a, T: Copy>"),
            ("slice: &mut &'a [T]", "slice: &'a mut &'a [T]"),
            ("Option<&'a T>", "Option<&'a mut T>"),
            ("(*old(slice))@", "(*slice)@"), ("(*final(slice))@", "(*old(slice))@"),
            ("Some(*value)", "Some(*final(value))"),
            ("post::split_off_last_post", "post::split_off_first_post"),
            ("<[T]>::split_off_last", "<[T]>::split_off_first"),
            ("    no_unwind\n", ""),
            ("const use requires const_split_off_first_last.", "stable const."),
        ), "public-declarations", "Split-off endpoint public-declarations drift")

    def test_a_first_proposal_is_not_an_input_or_a_substitute_for_current_first(self):
        with self.source_patches():
            expected = check_native.split_off_endpoint_source()
        path = self.proofs / "proposals/split_off_first.rs"
        path.write_text("not an input; no first-call rebinding was requested\n")
        with self.source_patches():
            self.assertEqual(check_native.split_off_endpoint_source(), expected)
        path.unlink()
        with self.source_patches():
            self.assertEqual(check_native.split_off_endpoint_source(), expected)
        self.assert_inputs_unchanged()

    def test_missing_actual_inputs_fail_before_any_compiler_command(self):
        for index, (path, original) in enumerate(self.inputs.items()):
            with self.subTest(path=path):
                path.unlink()
                root = self.root / f"missing-{index}"
                run = Mock()
                try:
                    with self.assertRaises(FileNotFoundError):
                        self.invoke(run, root)
                    self.assert_failed_without_compiling(root, run)
                finally:
                    path.write_bytes(original)

    def test_exact_negative_matrix_distinguishes_owner_lifetimes_and_public_const_stability(self):
        base = {
            "wrong-receiver": "E0308", "missing-receiver": "E0061", "extra-argument": "E0061",
            "shared-slot": "E0308", "direct-mutable-slice": "E0308", "immutable-slot": "E0596",
            "wrong-element": "E0308", "wrong-result-element": "E0308", "mutable-result": "E0308",
            "owned-result": "E0308", "slice-result": "E0308", "missing-option": "E0308",
            "write-through-result": "E0594", "local-escape": "E0515", "short-lifetime": "E0597",
            "static-escape": None, "shared-function-argument": "E0308", "mutable-function-result": "E0308",
        }
        expected_names = set()
        for module, apis in (
            ("original", ("split_off_first", "split_off_last")),
            ("adopted", ("split_off_first", "split_off_last")),
            ("public", ("split_off_first", "split_off_last")),
        ):
            for api in apis:
                binding = f"<[u8]>::{api}" if module == "public" else f"{module}::{api}::<u8>"
                for case, code in base.items():
                    name = f"{module}-{api}-{case}"
                    expected_names.add(name)
                    source, expected = self.cases[name]
                    self.assertIn(binding, source)
                    self.assertNotIn("API", source)
                    self.assertNotIn("unsafe", source)
                    self.assertNotIn("#![feature", source)
                    self.assertEqual(expected["code"], code)
                    if case == "static-escape":
                        self.assertEqual(expected["message"], "lifetime may not live long enough")
                    if case in ("local-escape", "short-lifetime"):
                        self.assertIn("let input = [1u8, 2]", source)
                        self.assertIn("let mut slice = &input[..]", source)
                if module == "public":
                    name = f"public-{api}-const-without-feature"
                    expected_names.add(name)
                    source, expected = self.cases[name]
                    self.assertIn("const BAD: Option<&u8>", source)
                    self.assertIn(f"{binding}(&mut slice)", source)
                    self.assertNotIn("#![feature", source)
                    self.assertIsNone(expected["code"])
                    self.assertEqual(
                        expected["message"],
                        f"`core::slice::<impl [T]>::{api}` is not yet stable as a const fn",
                    )
        self.assertEqual(set(self.cases), expected_names)
        self.assertEqual(len(self.cases), 110)

    def test_behavior_has_the_positive_independent_outer_lifetime_probe_and_required_cases(self):
        self.assertEqual(self.behavior.count("#[test]"), 20)
        self.assertIn("type SplitOff<T> = for<'a, 'b> fn(&'b mut &'a [T]) -> Option<&'a T>;", self.behavior)
        self.assertIn("fn first_bindings<T>() -> [SplitOff<T>; 3]", self.behavior)
        self.assertIn("fn last_bindings<T>() -> [SplitOff<T>; 3]", self.behavior)
        self.assertIn("fn bindings<T>() -> [(SplitOff<T>, bool); 6]", self.behavior)
        for name in (
            "positive_lifetime_probe_result_outlives_the_outer_slot_and_borrow",
            "first_result_survives_arbitrary_slot_reassignment",
            "last_result_survives_arbitrary_slot_reassignment",
            "repeated_first_calls_keep_all_earlier_results_live",
            "repeated_last_calls_keep_all_earlier_results_live",
            "alternating_calls_preserve_every_return_and_whole_remainder",
            "exhausted_repeated_calls_preserve_the_empty_slot_origin",
            "zero_sized_elements_use_variants_and_lengths_not_addresses",
            "maximum_length_legal_zero_sized_slice", "legal_empty_uninhabited_elements",
            "unconstrained_non_copy_elements_keep_all_values_and_frame",
            "non_static_elements_borrow_local_owners",
        ):
            self.assertIn(f"fn {name}()", self.behavior)
        self.assertIn(
            "        {\n            let mut slot = input;\n"
            "            result = split(&mut slot);\n        }\n        result",
            self.behavior,
        )
        for forbidden in ("proposal::", "current::", "#[ignore]", "#![feature", "unsafe {", "const RESULTS"):
            self.assertNotIn(forbidden, self.behavior)

    def test_missing_or_duplicate_negative_targets_are_explicit_failures(self):
        cases = list(check_native.split_off_endpoint_negative_cases())
        for index, incomplete in enumerate(([], cases[:1], [cases[0]] * 110)):
            root = self.root / f"incomplete-targets-{index}"
            run = Mock()
            with patch.object(check_native, "split_off_endpoint_negative_cases", return_value=incomplete):
                with self.assertRaisesRegex(AssertionError, "Expected 110 distinct"):
                    self.invoke(run, root)
            self.assert_failed_without_compiling(root, run)

    def test_command_failures_retain_diagnostics_and_previous_outputs_without_installing(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile-metadata-mir", "compile", "behavior", first):
            root = self.root / f"failure-{stage}"
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
            self.assert_inputs_unchanged()

    def test_missing_executables_are_explicit_retained_errors(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile-metadata-mir", "compile", "behavior", first):
            root = self.root / f"missing-executable-{stage}"

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

    def test_metadata_and_all_generic_adopted_original_dependency_signatures_are_required(self):
        variants = [
            "metadata-missing", "metadata-empty", "mir-missing", "mir-empty",
            "mir-shared-slot", "mir-mutable-return", "mir-monomorphic",
            *(f"missing-function-{index}" for index in range(5)),
        ]
        for variant in variants:
            root = self.root / variant
            _, logs = self.paths(root)

            def incomplete(name, result):
                if name == "compile-metadata-mir":
                    metadata, mir = logs / "split_off_endpoints.rmeta", logs / "split_off_endpoints.mir"
                    if variant == "metadata-missing":
                        metadata.unlink()
                    elif variant == "metadata-empty":
                        metadata.write_bytes(b"")
                    elif variant == "mir-missing":
                        mir.unlink()
                    elif variant == "mir-empty":
                        mir.write_text("")
                    elif variant == "mir-shared-slot":
                        mir.write_text(self.generic_mir.replace("&mut &[T]", "&&[T]"))
                    elif variant == "mir-mutable-return":
                        mir.write_text(self.generic_mir.replace("Option<&T>", "Option<&mut T>"))
                    elif variant == "mir-monomorphic":
                        mir.write_text(self.generic_mir.replace("T", "u8"))
                    else:
                        lines = self.generic_mir.splitlines()
                        del lines[int(variant.removeprefix("missing-function-"))]
                        mir.write_text("\n".join(lines))
                return result

            run, seen = self.compiler(root, incomplete)
            with self.assertRaises((FileNotFoundError, AssertionError)):
                self.invoke(run, root)
            self.assertEqual(seen, ["rustc-version", "compile-metadata-mir"])
            self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_missing_link_output_or_behavior_mir_never_counts_as_native_success(self):
        for variant in ("binary-missing", "binary-empty", "mir-missing", "mir-empty"):
            root = self.root / variant
            output, logs = self.paths(root)

            def incomplete(name, result):
                if name == "compile":
                    if variant == "binary-missing":
                        (output / "split_off_endpoint_behavior").unlink()
                    elif variant == "binary-empty":
                        (output / "split_off_endpoint_behavior").write_bytes(b"")
                    elif variant == "mir-missing":
                        (logs / "split_off_endpoint_behavior.mir").unlink()
                    else:
                        (logs / "split_off_endpoint_behavior.mir").write_text("")
                return result

            run, seen = self.compiler(root, incomplete)
            with self.assertRaisesRegex(AssertionError, "Expected (linked|retained)"):
                self.invoke(run, root)
            self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile"])
            self.assertEqual(list(output.iterdir()), [])
            self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_zero_partial_ignored_filtered_unexecuted_or_duplicate_runtime_summaries_fail(self):
        valid = (
            "running 20 tests\n"
            "test result: ok. 20 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;\n"
        )
        for index, summary in enumerate((
            "", valid.replace("20", "0"), valid.replace("20", "19"),
            valid.replace("20 passed; 0 failed; 0 ignored", "19 passed; 0 failed; 1 ignored"),
            valid.replace("20 passed", "19 passed").replace("0 filtered out", "1 filtered out"),
            valid.replace("ok. 20 passed; 0 failed", "FAILED. 19 passed; 1 failed"),
            valid.removeprefix("running 20 tests\n"), valid + valid,
        )):
            root = self.root / f"incomplete-runtime-{index}"

            def incomplete(name, result):
                if name == "behavior":
                    result.stdout = summary
                return result

            run, seen = self.compiler(root, incomplete)
            with self.assertRaisesRegex(AssertionError, "Expected all 20 executed split-off endpoint tests"):
                self.invoke(run, root)
            self.assertEqual(seen, ["rustc-version", "compile-metadata-mir", "compile", "behavior"])
            output, logs = self.paths(root)
            self.assertEqual(list(output.iterdir()), [])
            results = json.loads((logs / "results.json").read_text())
            self.assertEqual(results["positive_tests"], 0)
            self.assertEqual(results["negative_cases"], [])
            self.assertEqual(results["status"], "failed")

    def test_success_crashes_unrelated_or_multiple_negative_errors_never_pass(self):
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

    def test_public_const_rejection_requires_the_const_stability_error_not_just_any_failure(self):
        stage = "public-split_off_first-const-without-feature"

        def wrong(name, result):
            if name == stage:
                result.stderr = self.diagnostic({"code": None, "message": "unrelated const error"})
            return result

        run, seen = self.compiler(override=wrong)
        with self.assertRaises(AssertionError):
            self.invoke(run)
        self.assertEqual(seen[-1], stage)
        _, logs = self.paths(self.output_root)
        case = json.loads((logs / "results.json").read_text())["negative_cases"][-1]
        self.assertEqual(case["name"], stage)
        self.assertFalse(case["passed"])

    def test_named_evidence_and_artifact_collisions_are_rejected_before_execution(self):
        first, last = next(iter(self.cases)), next(reversed(self.cases))
        paths = [
            f"target/{self.group}/native/split_off_endpoint_behavior",
            *(f"target/{self.group}/native/rejected-{name}.rmeta" for name in (first, last)),
            *(f"logs/{self.group}/native/{name}" for name in (
                "source_split_off_endpoints.rs", "split_off_endpoint_behavior.rs",
                "split_off_endpoints.rmeta", "split_off_endpoints.mir", "split_off_endpoint_behavior.mir",
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

    def test_new_group_dispatch_does_not_change_any_existing_selectors(self):
        selectors = (
            (self.group, "check_split_off_endpoints", {}),
            ("mutable-splits", "check_mutable_splits", {}),
            ("mutable-endpoints", "check_mutable_endpoints", {}),
            ("splits", "check_pattern_comparison", {"splits": True}),
            ("endpoints", "check_endpoints", {}),
            ("ascii-case", "check_ascii_case", {}),
            ("singleton", "check_singletons", {}),
        )
        for group, selected, kwargs in selectors:
            with self.subTest(group=group), ExitStack() as stack:
                mocks = {
                    name: stack.enter_context(patch.object(check_native, name))
                    for _, name, _ in selectors
                }
                check_native.main(["--group", group, "--output-root", str(self.output_root)])
                mocks[selected].assert_called_once_with(self.output_root.resolve(), **kwargs)
                for name, mock in mocks.items():
                    if name != selected:
                        mock.assert_not_called()
        for index, selector in enumerate(([], ["--group", "defaults"])):
            source = Mock()
            source.read_text.side_effect = RuntimeError("original defaults source path reached")
            with ExitStack() as stack:
                mocks = [
                    stack.enter_context(patch.object(check_native, name)) for _, name, _ in selectors
                ]
                stack.enter_context(patch.object(check_native, "SOURCE", source))
                with self.assertRaisesRegex(RuntimeError, "original defaults source path reached"):
                    check_native.main(selector + ["--output-root", str(self.root / f"default-{index}")])
                source.read_text.assert_called_once_with()
                for mock in mocks:
                    mock.assert_not_called()

    def test_help_marks_the_adopted_scope_and_rejects_the_historical_proposal_route(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--help"])
        self.assertEqual(result.exception.code, 0)
        help_text = " ".join(stdout.getvalue().split())
        self.assertIn("--group split-off-endpoints compares", help_text)
        self.assertIn("ADOPTED current shared split-off proof bodies", help_text)
        self.assertIn("Only the last call/import changed; first is unchanged", help_text)
        self.assertIn("from the adopted last proof's actual dependency", help_text)
        self.assertNotIn("split-off-endpoints-proposal", help_text)
        self.assertNotIn("UNAPPROVED", help_text)
        self.assertIn("public const calls are not", help_text)
        self.assertIn("ADOPTED current proof bodies", help_text)
        self.assertIn("{defaults,singleton,ascii-case}", help_text)
        for group in (
            "split-off-endpoints-proposal", "split-off-first-proposal", "endpoints-proposal",
            "splits-proposal", "mutable-endpoints-proposal", "mutable-splits-proposal",
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
