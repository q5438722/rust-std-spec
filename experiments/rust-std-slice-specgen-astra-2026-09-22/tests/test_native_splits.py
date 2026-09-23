import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class SplitNativeRunner(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="slice-splits-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.proofs = self.project / "proofs/correctness/slice"
        self.proofs.mkdir(parents=True)
        (self.project / "tests").mkdir()
        self.behavior = (check_native.ROOT / "tests/split_behavior.rs").read_text()
        (self.project / "tests/split_behavior.rs").write_text(self.behavior)
        for name in ("split_first", "split_last"):
            relative = Path(f"{name}.rs")
            (self.proofs / relative).write_bytes((check_native.SPLIT_PROOFS / relative).read_bytes())
        self.cases = {
            name: (text, expected) for name, text, expected in check_native.split_negative_cases()
        }

    def invoke(self, run, root=None):
        with patch.object(check_native, "ROOT", self.project), patch.object(
            check_native, "SPLIT_PROOFS", self.proofs
        ), patch.object(
            check_native, "check_endpoints", side_effect=AssertionError("endpoint dispatch")
        ), patch.object(
            check_native, "check_singletons", side_effect=AssertionError("singleton dispatch")
        ), patch.object(
            check_native, "check_ascii_case", side_effect=AssertionError("ASCII dispatch")
        ), patch.dict(
            check_native.os.environ, {"RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/wrong"}
        ), patch.object(check_native.subprocess, "run", side_effect=run), patch("builtins.print"):
            check_native.main([
                "--group", "splits", "--output-root", str(root or self.output_root),
            ])

    def compiler(self, root=None, override=None):
        root = (root or self.output_root).resolve()
        output = root / "target/splits/native"
        logs = root / "logs/splits/native"
        binary = output / "split_behavior"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, self.project)
            self.assertTrue(text and capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["RUSTUP_HOME"], "/home/chentianyu/.rustup")
            self.assertEqual(env["TMPDIR"], str(output))
            self.assertEqual(env["SLICE_SPLITS_SOURCE"], str(logs / "source_splits.rs"))
            self.assertEqual((logs / "split_behavior.rs").read_text(), self.behavior)
            returncode, stdout, stderr = 0, "", ""
            if command == ["rustc", "+1.96.0", "-vV"]:
                name, stdout = "rustc-version", "rustc 1.96.0\nrelease: 1.96.0\n"
            elif "--test" in command:
                name = "compile"
                self.assertEqual(command, [
                    "rustc", "+1.96.0", "--edition=2021", "--test",
                    str(logs / "split_behavior.rs"),
                    "-C", "overflow-checks=yes", "-C", "opt-level=0",
                    f"--emit=link,mir={logs / 'split_behavior.mir'}", "-o", str(binary),
                ])
                binary.write_text("mock executable\n")
                (logs / "split_behavior.mir").write_text("\n".join(
                    f"fn {module}::{name}(_1: &[T]) -> Option<(&T, &[T])> {{}}"
                    for module in ("original", "adopted")
                    for name in ("split_first", "split_last")
                ))
            elif command == [str(binary), "--test-threads=1"]:
                name = "behavior"
                stdout = (
                    "test result: ok. 15 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=split_rejection", "--error-format=json",
                ])
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                body, expected = self.cases[name]
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\ninclude!(env!("SLICE_SPLITS_SOURCE"));\n' + body + "\n",
                )
                self.assertEqual(list(output.glob("rejection-*.rs")), [probe])
                self.assertEqual(command[7:], ["-o", str(output / f"rejected-{name}.rlib")])
                Path(command[8]).write_text("mock partial output\n")
                code = expected["code"]
                stderr = json.dumps({
                    "level": "error", "code": None if code is None else {"code": code},
                    "message": expected.get("message", "mock rejection"),
                    "spans": [{"file_name": str(probe)}],
                }) + "\n"
                returncode = 1
            seen.append(name)
            result = check_native.subprocess.CompletedProcess(command, returncode, stdout, stderr)
            return override(name, result) if override else result

        return run, seen

    def test_source_mapping_keeps_authority_patterns_and_exact_adopted_diff(self):
        with patch.object(check_native, "SPLIT_PROOFS", self.proofs):
            text, spans, mappings = check_native.split_source()
        self.assertIn("ADOPTED current source-proof input", text)
        self.assertNotIn("proposal", text)
        self.assertNotIn("ensures", text)
        self.assertNotIn("vstd", text)
        for span in spans:
            source = Path(span["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(span["text"], "".join(source[span["start"] - 1:span["end"]]))
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "function"],
            [("split_first", 198, 200), ("split_last", 240, 242)],
        )
        self.assertEqual(
            [s["kind"] for s in spans if s["role"] == "native-dependency"],
            ["slice-len", "split-at", "split-at-unchecked", "split-at-checked"],
        )
        for mapping in mappings:
            self.assertNotEqual(mapping["original_body"], mapping["current"]["body"])
            self.assertNotIn("proposal", mapping)
            proof = Path(mapping["current"]["path"]).read_text().splitlines()
            self.assertEqual(
                "\n".join(proof[mapping["current"]["body_start"] - 1:mapping["current"]["body_end"]]),
                mapping["current"]["body"],
            )
            self.assertEqual(
                Path(mapping["current"]["contract"]), self.project / "specs/slice/mod.rs",
            )
            self.assertIn(mapping["original_body"], text.split("pub mod adopted {")[0])
            self.assertIn(mapping["current"]["body"], text.split("pub mod adopted {")[1])

    def test_all_paths_outputs_and_inputs_are_preserved(self):
        before = {path: path.read_bytes() for path in self.project.rglob("*") if path.is_file()}
        run, seen = self.compiler()
        self.invoke(run, os.path.relpath(self.output_root))
        self.assertEqual(seen, ["rustc-version", "compile", "behavior", *self.cases])
        logs = self.output_root / "logs/splits/native"
        results = json.loads((logs / "results.json").read_text())
        self.assertEqual(results["status"], "passed")
        self.assertEqual(results["group"], "splits")
        self.assertIn("ADOPTED current", results["source_status"])
        self.assertEqual(results["positive_tests"], 15)
        self.assertEqual(len(results["negative_cases"]), 120)
        self.assertTrue(all(case["passed"] for case in results["negative_cases"]))
        commands = json.loads((logs / "commands.json").read_text())
        self.assertEqual([c["returncode"] for c in commands], [0] * 3 + [1] * 120)
        self.assertEqual(list((self.output_root / "target/splits/native").iterdir()), [])
        self.assertEqual(
            before, {path: path.read_bytes() for path in self.project.rglob("*") if path.is_file()},
        )
        dependencies = json.loads((logs / "dependencies.json").read_text())
        self.assertEqual(dependencies["proof_inputs"], [
            str(self.proofs / f"{name}.rs") for name in ("split_first", "split_last")
        ])

    def test_both_components_are_checked_in_all_bindings(self):
        self.assertEqual(len(self.cases), 120)
        for module in ("original", "adopted", "public"):
            for api in ("split_first", "split_last"):
                selected = [key for key in self.cases if key.startswith(f"{module}-{api}-")]
                self.assertEqual(len(selected), 20)
                for component in ("element", "remainder"):
                    for action in ("mutable", "owned", "write", "local", "short", "static"):
                        self.assertIn(f"{module}-{api}-{action}-{component}", selected)
                self.assertIn(f"{module}-{api}-reversed-result", selected)
                self.assertIn(f"{module}-{api}-missing-option", selected)
                for key in selected:
                    self.assertNotIn("API", self.cases[key][0])

    def test_current_drift_is_rejected_before_compiling(self):
        for api in ("split_first", "split_last"):
            path = self.proofs / f"{api}.rs"
            original = path.read_text()
            changes = [
                ("pub const fn", "pub fn"), ("<T>(slice", "<T: Copy>(slice"),
                ("<T>(slice", "<T: Eq>(slice"), ("<T>(slice", "<T: 'static>(slice"),
                ("slice: &[T]", "slice: &'static [T]"),
                ("Option<(&T, &[T])>", "Option<(&[T], &T)>"),
                ("Option<(&T, &[T])>", "Option<(&T, &mut [T])>"),
                ("    ensures", "    requires slice.len() > 0,\n    ensures"),
                (f"{api}_post(slice, result)", "is_empty_post(slice, true)"),
                ("specs/slice/mod.rs", "specs/slice/other.rs"),
                ("slice.len() == 0", "slice.is_empty()"),
                ("slice.split_at(1).1", "slice.split_at(1).0") if api == "split_first"
                else ("slice.split_at(i).0", "slice.split_at(i).1"),
            ]
            for index, (old, new) in enumerate(changes):
                with self.subTest(api=api, variant=index):
                    self.assertIn(old, original)
                    path.write_text(original.replace(old, new, 1))
                    run = Mock()
                    try:
                        with self.assertRaisesRegex(ValueError, "Split current source drift"):
                            self.invoke(run, self.root / f"current-{api}-{index}")
                        run.assert_not_called()
                    finally:
                        path.write_text(original)

    def test_authority_docs_signatures_and_bodies_cannot_drift(self):
        original = check_native.SOURCE.read_text().splitlines(keepends=True)
        for line, old, new in (
            (101, "impl<T>", "impl<T: Copy>"), (182, "all the rest", "some of the rest"),
            (198, "pub const fn", "pub fn"), (199, "tail @ ..", "tail, .."),
            (224, "last", "first"), (240, "&self", "&mut self"),
            (241, "Some((last, init))", "Some((init, last))"),
        ):
            with self.subTest(line=line):
                changed = original.copy()
                self.assertIn(old, changed[line - 1])
                changed[line - 1] = changed[line - 1].replace(old, new)
                source = self.root / f"source-{line}.rs"
                source.write_text("".join(changed))
                run = Mock()
                with patch.object(check_native, "SOURCE", source):
                    with self.assertRaisesRegex(ValueError, "Source span changed"):
                        self.invoke(run, self.root / f"authority-{line}")
                run.assert_not_called()

    def test_failed_link_zero_tests_and_wrong_rejections_never_pass(self):
        first = next(iter(self.cases))
        for stage in ("compile", "behavior", first):
            with self.subTest(stage=stage):
                root = self.root / f"failed-{stage}"

                def fail(name, result):
                    if name == stage:
                        if name == "behavior":
                            result.stdout = (
                                "test result: ok. 0 passed; 0 failed; 0 ignored; "
                                "0 measured; 0 filtered out;"
                            )
                        else:
                            result.returncode, result.stderr = 1, "linking failed"
                    return result

                run, seen = self.compiler(root, fail)
                with self.assertRaises(AssertionError):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], stage)
                logs = root / "logs/splits/native"
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
                self.assertTrue((logs / f"{stage}.log").is_file())
                self.assertEqual(list((root / "target/splits/native").iterdir()), [])

    def test_existing_results_are_not_overwritten(self):
        existing = self.output_root / "logs/splits/native/results.json"
        existing.parent.mkdir(parents=True)
        existing.write_text("earlier result\n")
        run = Mock()
        with self.assertRaises(FileExistsError):
            self.invoke(run)
        run.assert_not_called()
        self.assertEqual(existing.read_text(), "earlier result\n")

    def test_help_marks_adopted_scope_without_restoring_old_proposal_routes(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--help"])
        self.assertEqual(result.exception.code, 0)
        self.assertIn("splits", stdout.getvalue())
        self.assertIn("ADOPTED", stdout.getvalue())
        self.assertNotIn("splits-proposal", stdout.getvalue())
        self.assertNotIn("endpoints-proposal", stdout.getvalue())

    def test_historical_proposals_are_not_current_native_inputs(self):
        proposals = self.proofs / "proposals"
        proposals.mkdir()
        for api in ("split_first", "split_last"):
            (proposals / f"{api}.rs").write_text("not a current proof\n")
        run, seen = self.compiler()
        self.invoke(run)
        self.assertEqual(len(seen), 123)
        logs = self.output_root / "logs/splits/native"
        for name in ("source-spans.json", "source-mappings.json", "dependencies.json"):
            self.assertNotIn(str(proposals), (logs / name).read_text())

    def test_old_proposal_group_is_not_an_execution_path(self):
        with patch("sys.stderr", new_callable=io.StringIO), patch.object(
            check_native.subprocess, "run",
        ) as run:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--group", "splits-proposal"])
        self.assertEqual(result.exception.code, 2)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
