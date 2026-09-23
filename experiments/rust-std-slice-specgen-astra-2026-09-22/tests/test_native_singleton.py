import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_native


class SingletonNativeRunner(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(
            dir=check_native.ROOT, prefix=".singleton-runner-test-"
        )
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.singleton_negative_cases()
        }

    @staticmethod
    def diagnostic(expected):
        code = expected["code"]
        return json.dumps({
            "$message_type": "diagnostic",
            "level": "error",
            "code": None if code is None else {"code": code},
            "message": expected.get("message", "mock compile rejection"),
            "spans": [{"file_name": "probe.rs"}],
        }) + "\n" + json.dumps({
            "$message_type": "diagnostic",
            "level": "error",
            "code": None,
            "message": "aborting due to 1 previous error",
            "spans": [],
        }) + "\n"

    def compiler(self, output_root, project, override=None):
        output = output_root / "target/singleton/native"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, project)
            self.assertTrue(text)
            self.assertTrue(capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["TMPDIR"], str(output))
            self.assertEqual(
                env["SLICE_SINGLETON_SOURCE"], str(output / "source_singletons.rs")
            )
            self.assertTrue((output / "source_singletons.rs").is_file())
            self.assertEqual(list(output.glob("rejected-*.rlib")), [])
            returncode, stdout, stderr = 0, "", ""
            binary = output / "singleton_behavior"
            if command == ["rustc", "+1.96.0", "-vV"]:
                name = "rustc-version"
                stdout = "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/singleton_behavior.rs", "-o", str(binary),
            ]:
                name = "compile"
                binary.write_text("mock binary\n")
            elif command == [str(binary), "--test-threads=1"]:
                name = "behavior"
                self.assertTrue(binary.is_file())
                stdout = (
                    "running 16 tests\n"
                    "test result: ok. 16 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=singleton_rejection", "--error-format=json",
                ])
                self.assertEqual(len(command), 9)
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                self.assertIn(name, self.cases)
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, output)
                self.assertEqual(list(output.glob("rejection-*.rs")), [probe])
                self.assertIn(body, probe.read_text())
                rejected = output / f"rejected-{name}.rlib"
                self.assertEqual(command[7:], ["-o", str(rejected)])
                rejected.write_text("mock partial compiler output\n")
                returncode, stderr = 1, self.diagnostic(expected)
            if name in ("rustc-version", "compile", "behavior"):
                self.assertEqual(list(output.glob("rejection-*.rs")), [])
            seen.append(name)
            result = check_native.subprocess.CompletedProcess(
                command, returncode, stdout, stderr
            )
            return override(name, result) if override else result

        return run, seen

    def invoke(self, run, output_root=None, project=None, redirected=True):
        output_root = output_root or self.output_root
        project = project or self.project
        args = ["--group", "singleton"]
        if redirected:
            args += ["--output-root", str(output_root)]
        with patch.object(check_native, "ROOT", project), patch.object(
            check_native, "SOURCE", self.root / "must-not-read-default-source.rs"
        ), patch.dict(check_native.os.environ, {"RUSTC_BOOTSTRAP": "1"}), patch.object(
            check_native.subprocess, "run", side_effect=run
        ), patch("builtins.print"):
            check_native.main(args)

    def test_selected_group_dispatch_and_output_paths(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected):
                base = self.root / str(redirected)
                project = base / "project"
                output_root = base / "results" if redirected else project
                output = output_root / "target/singleton/native"
                logs = output_root / "logs/singleton/native"
                output.mkdir(parents=True)
                logs.mkdir(parents=True)
                sentinel = output / "unrelated-output"
                sentinel.write_text("preserve output")
                (logs / "previous.log").write_text("preserve log")
                run, seen = self.compiler(output_root, project)
                self.invoke(run, output_root, project, redirected)
                self.assertEqual(seen, ["rustc-version", "compile", "behavior"] + list(self.cases))
                self.assertEqual(list(output.iterdir()), [sentinel])
                self.assertEqual(sentinel.read_text(), "preserve output")
                self.assertEqual((logs / "previous.log").read_text(), "preserve log")
                self.assertFalse((output_root / "target/defaults").exists())
                self.assertFalse((output_root / "logs/defaults").exists())
                if redirected:
                    self.assertFalse(project.exists())
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 69)
                self.assertEqual([item["returncode"] for item in commands], [0] * 3 + [1] * 66)
                self.assertTrue(all(item["RUSTC_BOOTSTRAP"] is None for item in commands))
                self.assertTrue(all(Path(item["log"]).is_file() for item in commands))
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["positive_tests"], 16)
                self.assertEqual(len(results["negative_cases"]), 66)
                self.assertTrue(all(item["passed"] for item in results["negative_cases"]))
                self.assertTrue(all(item["returncode"] == 1 for item in results["negative_cases"]))
                spans = json.loads((logs / "source-spans.json").read_text())
                self.assertEqual(len(spans), 4)

    def test_source_copies_preserve_canonical_spans(self):
        text, spans = check_native.singleton_source()
        self.assertEqual(
            [(item["module"], item["start"], item["end"]) for item in spans],
            [("array", 166, 169), ("array", 174, 177), ("slice", 203, 205), ("slice", 211, 213)],
        )
        for span in spans:
            path = Path(span["path"])
            expected_path = (
                check_native.SINGLETON_ARRAY_SOURCE
                if span["module"] == "array" else check_native.SINGLETON_SLICE_SOURCE
            )
            self.assertEqual(path, expected_path)
            original = "\n".join(path.read_text().splitlines()[span["start"] - 1 : span["end"]])
            self.assertEqual(span["text"], original)
            self.assertIn(original, text)
        self.assertTrue(text.startswith("mod array {\n"))
        self.assertIn("pub const fn from_ref<T>(s: &T) -> &[T] {\n    array::from_ref(s)\n}", text)
        self.assertIn(
            "pub const fn from_mut<T>(s: &mut T) -> &mut [T] {\n    array::from_mut(s)\n}", text
        )
        self.assertIn("unsafe { &*(s as *const T).cast::<[T; 1]>() }", text)
        self.assertIn("unsafe { &mut *(s as *mut T).cast::<[T; 1]>() }", text)

    def test_missing_compiler_records_failure_and_removes_copies(self):
        def unavailable(*args, **kwargs):
            raise OSError("compiler unavailable")

        with self.assertRaisesRegex(OSError, "compiler unavailable"):
            self.invoke(unavailable)
        output = self.output_root / "target/singleton/native"
        logs = self.output_root / "logs/singleton/native"
        self.assertEqual(list(output.iterdir()), [])
        commands = json.loads((logs / "commands.json").read_text())
        self.assertEqual(len(commands), 1)
        self.assertIsNone(commands[0]["returncode"])
        self.assertIn("compiler unavailable", commands[0]["error"])
        self.assertIn("compiler unavailable", (logs / "rustc-version.log").read_text())
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_source_span_drift_fails_before_compiler(self):
        changed = self.root / "changed-array.rs"
        changed.write_text("\n" * 165 + "pub fn changed() {}\n")
        with patch.object(check_native, "SINGLETON_ARRAY_SOURCE", changed), patch.object(
            check_native.subprocess, "run"
        ) as run:
            with self.assertRaisesRegex(ValueError, "Source span changed: .*changed-array.rs"):
                self.invoke(run)
            run.assert_not_called()
        logs = self.output_root / "logs/singleton/native"
        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
        self.assertEqual(list((self.output_root / "target/singleton/native").iterdir()), [])

    def test_rejection_requires_exact_exit_code_and_diagnostics(self):
        expected = {"code": "E0061"}
        valid = self.diagnostic(expected)
        log = self.root / "diagnostic.log"
        result = check_native.subprocess.CompletedProcess([], 1, "", valid)
        self.assertEqual(check_native.check_singleton_rejection(result, expected, log)["code"], "E0061")
        variants = [
            (0, valid), (2, valid), (101, valid), (-11, valid),
            (1, ""), (1, "compiler unavailable"), (1, "[]"),
            (1, self.diagnostic({"code": "E0308"})),
            (1, valid + valid),
            (1, valid + json.dumps({"level": "error", "message": "unexpected error"})),
        ]
        for returncode, stderr in variants:
            with self.subTest(returncode=returncode, stderr=stderr):
                result = check_native.subprocess.CompletedProcess([], returncode, "", stderr)
                with self.assertRaisesRegex(AssertionError, "see .*diagnostic.log"):
                    check_native.check_singleton_rejection(result, expected, log)

    def test_unnumbered_lifetime_diagnostics_are_not_ignored(self):
        expected = {"code": None, "message": "lifetime may not live long enough"}
        valid = self.diagnostic(expected)
        log = self.root / "lifetime.log"
        result = check_native.subprocess.CompletedProcess([], 1, "", valid)
        self.assertEqual(check_native.check_singleton_rejection(result, expected, log), expected)
        for stderr in (
            self.diagnostic({"code": None, "message": "unrelated compiler error"}),
            self.diagnostic({"code": "E0515", "message": expected["message"]}),
            valid + valid,
            json.dumps({"level": "error", "message": "aborting due to 1 previous error"}),
        ):
            with self.subTest(stderr=stderr):
                result = check_native.subprocess.CompletedProcess([], 1, "", stderr)
                with self.assertRaisesRegex(AssertionError, "see .*lifetime.log"):
                    check_native.check_singleton_rejection(result, expected, log)

    def test_wrong_rejection_stops_and_cleans_each_probe(self):
        first_case = next(iter(self.cases))

        def wrong_diagnostic(name, result):
            if name == first_case:
                result.stderr = self.diagnostic({"code": "E0308"})
            return result

        run, seen = self.compiler(self.output_root, self.project, wrong_diagnostic)
        with self.assertRaisesRegex(AssertionError, "exactly one .*E0061.*source-shared-missing-argument.log"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version", "compile", "behavior", first_case])
        self.assertEqual(list((self.output_root / "target/singleton/native").iterdir()), [])
        logs = self.output_root / "logs/singleton/native"
        commands = json.loads((logs / "commands.json").read_text())
        self.assertEqual([item["returncode"] for item in commands], [0, 0, 0, 1])
        self.assertIn("E0308", (logs / f"{first_case}.log").read_text())
        results = json.loads((logs / "results.json").read_text())
        self.assertEqual(results["status"], "failed")
        self.assertFalse(results["negative_cases"][0]["passed"])

    def test_command_failures_do_not_run_later_stages(self):
        stages = ("rustc-version", "compile", "behavior")
        for index, stage in enumerate(stages):
            with self.subTest(stage=stage):
                output_root = self.root / stage

                def fail(name, result):
                    if name == stage:
                        result.returncode = 101
                        result.stderr = "compiler or executable failed"
                    return result

                run, seen = self.compiler(output_root, self.project, fail)
                with self.assertRaisesRegex(AssertionError, f"{stage}: expected exit 0, got 101"):
                    self.invoke(run, output_root)
                self.assertEqual(seen, list(stages[:index + 1]))
                self.assertEqual(list((output_root / "target/singleton/native").iterdir()), [])
                logs = output_root / "logs/singleton/native"
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(commands[-1]["returncode"], 101)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertEqual(results["negative_cases"], [])

    def test_behavior_requires_nonempty_unfiltered_execution(self):
        for index, stdout in enumerate((
            "",
            "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 15 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out;",
        )):
            with self.subTest(stdout=stdout):
                output_root = self.root / f"behavior-{index}"

                def empty_execution(name, result):
                    if name == "behavior":
                        result.stdout = stdout
                    return result

                run, seen = self.compiler(output_root, self.project, empty_execution)
                with self.assertRaisesRegex(AssertionError, "Expected executed, nonempty singleton tests"):
                    self.invoke(run, output_root)
                self.assertEqual(seen, ["rustc-version", "compile", "behavior"])
                self.assertEqual(list((output_root / "target/singleton/native").iterdir()), [])
                logs = output_root / "logs/singleton/native"
                self.assertEqual((logs / "behavior.log").read_text(), stdout)
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_explicit_defaults_preserves_legacy_dispatch(self):
        with patch.object(check_native, "ROOT", self.project), patch.object(
            check_native, "check_singletons"
        ) as singleton, patch.object(
            check_native.subprocess, "run", side_effect=OSError("compiler unavailable")
        ) as run:
            with self.assertRaisesRegex(OSError, "compiler unavailable"):
                check_native.main(["--group", "defaults", "--output-root", str(self.output_root)])
            singleton.assert_not_called()
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0], ["rustc", "+1.96.0", "-vV"])
        self.assertTrue((self.output_root / "logs/defaults/native/commands.json").is_file())
        self.assertEqual(list((self.output_root / "target/defaults/native").iterdir()), [])
        self.assertFalse((self.output_root / "target/singleton").exists())


if __name__ == "__main__":
    unittest.main()
