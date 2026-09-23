import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class AsciiCaseNativeRunner(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(
            dir=check_native.ROOT, prefix=".ascii-case-runner-test-"
        )
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.ascii_case_negative_cases()
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

    def compiler(self, output_root, project, override=None, preserved=()):
        output = output_root.resolve() / "target/ascii-case/native"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, project)
            self.assertTrue(text)
            self.assertTrue(capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["RUSTUP_HOME"], "/home/chentianyu/.rustup")
            self.assertEqual(env["TMPDIR"], str(output))
            self.assertEqual(
                env["SLICE_ASCII_CASE_SOURCE"], str(output / "source_ascii_case.rs")
            )
            self.assertTrue((output / "source_ascii_case.rs").is_file())
            for name in self.cases:
                rejected = output / f"rejected-{name}.rlib"
                if rejected not in preserved:
                    self.assertFalse(rejected.exists())
            active_probes = [
                output / f"rejection-{name}.rs" for name in self.cases
                if (output / f"rejection-{name}.rs").exists()
                and output / f"rejection-{name}.rs" not in preserved
            ]
            returncode, stdout, stderr = 0, "", ""
            binary = output / "ascii_case_behavior"
            if command == ["rustc", "+1.96.0", "-vV"]:
                name = "rustc-version"
                stdout = "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/ascii_case_behavior.rs", "-o", str(binary),
            ]:
                name = "compile"
                binary.write_text("mock binary\n")
            elif command == [str(binary), "--test-threads=1"]:
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
                    "--crate-name=ascii_case_rejection", "--error-format=json",
                ])
                self.assertEqual(len(command), 9)
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                self.assertIn(name, self.cases)
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, output)
                self.assertEqual(active_probes, [probe])
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\n'
                    'mod source { include!(env!("SLICE_ASCII_CASE_SOURCE")); }\n'
                    + body + "\n",
                )
                rejected = output / f"rejected-{name}.rlib"
                self.assertEqual(command[7:], ["-o", str(rejected)])
                rejected.write_text("mock partial compiler output\n")
                returncode, stderr = 1, self.diagnostic(expected)
            if name in ("rustc-version", "compile", "behavior"):
                self.assertEqual(active_probes, [])
            seen.append(name)
            result = check_native.subprocess.CompletedProcess(
                command, returncode, stdout, stderr
            )
            return override(name, result) if override else result

        return run, seen

    def invoke(self, run, output_root=None, project=None, redirected=True):
        output_root = output_root or self.output_root
        project = project or self.project
        args = ["--group", "ascii-case"]
        if redirected:
            args += ["--output-root", str(output_root)]
        with patch.object(check_native, "ROOT", project), patch.object(
            check_native, "SOURCE", self.root / "must-not-read-default-source.rs"
        ), patch.object(
            check_native, "check_singletons",
            side_effect=AssertionError("unexpected singleton dispatch"),
        ), patch.dict(
            check_native.os.environ,
            {"RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/must-not-use-this-rustup"},
        ), patch.object(
            check_native.subprocess, "run", side_effect=run
        ), patch("builtins.print"):
            check_native.main(args)

    def test_selected_group_dispatch_output_paths_and_preservation(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected):
                base = self.root / str(redirected)
                project = base / "project"
                output_root = base / "results" if redirected else project
                output = output_root / "target/ascii-case/native"
                logs = output_root / "logs/ascii-case/native"
                preserved = {
                    output / "unrelated-output": "preserve output",
                    output / "rejection-previous.rs": "preserve old probe",
                    output / "rejected-previous.rlib": "preserve old binary",
                    logs / "previous.log": "preserve log",
                    output_root / "target/defaults/native/old": "preserve Defaults",
                    output_root / "logs/defaults/native/results.json": "old Defaults results",
                    output_root / "target/singleton/native/old": "preserve singletons",
                    output_root / "logs/singleton/native/results.json": "old singleton results",
                }
                for path, text in preserved.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
                run, seen = self.compiler(output_root, project)
                self.invoke(run, output_root, project, redirected)
                self.assertEqual(
                    seen, ["rustc-version", "compile", "behavior"] + list(self.cases)
                )
                self.assertEqual(
                    set(output.iterdir()), {path for path in preserved if path.parent == output}
                )
                for path, text in preserved.items():
                    self.assertEqual(path.read_text(), text)
                if redirected:
                    self.assertFalse(project.exists())
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 19)
                self.assertEqual(
                    [item["returncode"] for item in commands], [0] * 3 + [1] * 16
                )
                for command in commands:
                    self.assertIsNone(command["RUSTC_BOOTSTRAP"])
                    self.assertEqual(command["RUSTUP_HOME"], "/home/chentianyu/.rustup")
                    self.assertEqual(command["cwd"], str(project))
                    self.assertTrue(Path(command["log"]).is_relative_to(logs))
                    self.assertTrue(Path(command["log"]).is_file())
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["group"], "ascii-case")
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["positive_tests"], 17)
                self.assertEqual(len(results["negative_cases"]), 16)
                for case in results["negative_cases"]:
                    self.assertTrue(case["passed"])
                    self.assertEqual(case["returncode"], 1)
                    expected = self.cases[case["name"]][1]
                    self.assertEqual(case["diagnostic"]["code"], expected["code"])
                    self.assertEqual(Path(case["log"]).read_text(), self.diagnostic(expected))
                self.assertEqual(
                    len(json.loads((logs / "source-spans.json").read_text())), 6
                )

    def test_relative_output_root_is_resolved(self):
        relative = self.output_root.relative_to(check_native.ROOT)
        run, seen = self.compiler(self.output_root, self.project)
        self.invoke(run, relative)
        self.assertEqual(len(seen), 19)
        logs = self.output_root / "logs/ascii-case/native"
        commands = json.loads((logs / "commands.json").read_text())
        self.assertTrue(all(Path(item["log"]).is_absolute() for item in commands))
        self.assertFalse(self.project.exists())

    def test_redirected_outputs_allow_read_only_inputs(self):
        tests = self.project / "tests"
        tests.mkdir(parents=True)
        source = self.project / "ascii.rs"
        source.write_text(check_native.ASCII_CASE_SOURCE.read_text())
        behavior = tests / "ascii_case_behavior.rs"
        behavior.write_text((check_native.ROOT / "tests/ascii_case_behavior.rs").read_text())
        original_source = source.read_text()
        original_behavior = behavior.read_text()
        source.chmod(0o444)
        behavior.chmod(0o444)
        tests.chmod(0o555)
        self.project.chmod(0o555)
        self.addCleanup(tests.chmod, 0o755)
        self.addCleanup(self.project.chmod, 0o755)
        run, seen = self.compiler(self.output_root, self.project)
        with patch.object(check_native, "ASCII_CASE_SOURCE", source):
            self.invoke(run)
        self.assertEqual(len(seen), 19)
        self.assertEqual(source.read_text(), original_source)
        self.assertEqual(behavior.read_text(), original_behavior)
        self.assertEqual(set(self.project.iterdir()), {source, tests})
        self.assertEqual(list(tests.iterdir()), [behavior])

    def test_source_copies_preserve_canonical_spans(self):
        text, spans = check_native.ascii_case_source()
        self.assertEqual(
            [(span["name"], span["kind"], span["start"], span["end"]) for span in spans],
            [
                ("make_ascii_uppercase", "documentation", 161, 169),
                ("make_ascii_uppercase", "attributes", 170, 172),
                ("make_ascii_uppercase", "function", 173, 181),
                ("make_ascii_lowercase", "documentation", 183, 191),
                ("make_ascii_lowercase", "attributes", 192, 194),
                ("make_ascii_lowercase", "function", 195, 203),
            ],
        )
        lines = check_native.ASCII_CASE_SOURCE.read_text().splitlines()
        for span in spans:
            self.assertEqual(span["module"], "slice")
            self.assertEqual(Path(span["path"]), check_native.ASCII_CASE_SOURCE)
            original = "\n".join(lines[span["start"] - 1 : span["end"]])
            self.assertEqual(span["text"], original)
            if span["kind"] == "documentation":
                self.assertIn(original, text)
            elif span["kind"] == "function":
                lifted = original.replace("&mut self", "slice: &mut [u8]", 1)
                lifted = re.sub(r"\bself\b", "slice", lifted)
                self.assertIn(lifted, text)
                self.assertIn(
                    "        while i < slice.len() {\n"
                    "            let byte = &mut slice[i];\n"
                    f"            byte.{span['name']}();\n"
                    "            i += 1;\n",
                    text,
                )
            else:
                self.assertIn('since = "1.23.0"', original)
                self.assertIn('since = "1.84.0"', original)
        self.assertNotIn("#[stable(", text)
        self.assertNotIn("#[rustc_const_stable(", text)
        self.assertNotIn("#![feature(", text)
        self.assertNotIn("-> ()", text)

    def test_source_span_drift_fails_before_compiler(self):
        original = check_native.ASCII_CASE_SOURCE.read_text().splitlines(keepends=True)
        for line_number, before, after in (
            (161, "equivalent", "different"),
            (169, "to_ascii_uppercase", "to_ascii_lowercase"),
            (170, "1.23.0", "1.24.0"),
            (171, "1.84.0", "1.85.0"),
            (173, "pub const fn", "pub fn"),
            (174, "FIXME", "CHANGED"),
            (176, "i < self.len()", "i <= self.len()"),
            (178, "make_ascii_uppercase", "make_ascii_lowercase"),
            (179, "i += 1", "i += 2"),
            (183, "lower", "upper"),
            (192, "1.23.0", "1.24.0"),
            (193, "1.84.0", "1.85.0"),
            (195, "&mut self", "&self"),
            (197, "let mut i = 0", "let mut i = 1"),
            (199, "&mut self[i]", "&mut self[0]"),
            (200, "make_ascii_lowercase", "make_ascii_uppercase"),
            (201, "i += 1", "i += 2"),
        ):
            with self.subTest(line=line_number):
                lines = original.copy()
                self.assertIn(before, lines[line_number - 1])
                lines[line_number - 1] = lines[line_number - 1].replace(before, after)
                changed = self.root / f"changed-{line_number}.rs"
                changed.write_text("".join(lines))
                output_root = self.root / f"drift-{line_number}"
                run = Mock()
                with patch.object(check_native, "ASCII_CASE_SOURCE", changed):
                    with self.assertRaisesRegex(ValueError, f"Source span changed: .*{changed.name}"):
                        self.invoke(run, output_root)
                run.assert_not_called()
                logs = output_root / "logs/ascii-case/native"
                self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
                self.assertEqual(list((output_root / "target/ascii-case/native").iterdir()), [])

    def test_negative_cases_cover_each_public_and_source_api(self):
        self.assertEqual(
            set(self.cases),
            {
                f"{label}-{direction}-{rejection}"
                for label in ("source", "public")
                for direction in ("uppercase", "lowercase")
                for rejection in ("shared-receiver", "wrong-element", "wrong-result", "extra-argument")
            },
        )
        for name, (text, expected) in self.cases.items():
            label, direction, rejection = name.split("-", 2)
            binding = "source" if label == "source" else "<[u8]>"
            self.assertIn(f"{binding}::make_ascii_{direction}(", text)
            self.assertNotIn("API", text)
            self.assertEqual(
                expected["code"], "E0061" if rejection == "extra-argument" else "E0308"
            )
            self.assertIn({
                "shared-receiver": "let input: &[u8]",
                "wrong-element": "[97u16]",
                "wrong-result": "let _: usize",
                "extra-argument": "(&mut input, 1u8)",
            }[rejection], text)

    def test_rejection_requires_exact_exit_code_and_meaningful_diagnostics(self):
        log = self.root / "diagnostic.log"
        for code in ("E0308", "E0061"):
            expected = {"code": code}
            valid = self.diagnostic(expected)
            accepted = check_native.subprocess.CompletedProcess([], 1, "", valid)
            self.assertEqual(
                check_native.check_singleton_rejection(accepted, expected, log)["code"], code
            )
            for returncode, stderr in (
                (0, valid), (2, valid), (101, valid), (-11, valid),
                (1, ""), (1, "compiler unavailable"), (1, "[]"), (1, "null"),
                (1, self.diagnostic({"code": "E0425"})),
                (1, valid + valid),
                (1, valid + json.dumps({"level": "error", "message": "linking failed"})),
                (1, json.dumps({
                    "level": "error", "code": None, "spans": [],
                    "message": "aborting due to 1 previous error",
                })),
            ):
                with self.subTest(code=code, returncode=returncode, stderr=stderr):
                    result = check_native.subprocess.CompletedProcess([], returncode, "", stderr)
                    with self.assertRaisesRegex(AssertionError, "see .*diagnostic.log"):
                        check_native.check_singleton_rejection(result, expected, log)

    def test_wrong_rejection_stops_and_cleans_each_probe(self):
        first = next(iter(self.cases))

        def wrong_diagnostic(name, result):
            if name == first:
                result.stderr = self.diagnostic({"code": "E0061"})
            return result

        run, seen = self.compiler(self.output_root, self.project, wrong_diagnostic)
        with self.assertRaisesRegex(AssertionError, f"exactly one .*E0308.*{first}.log"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version", "compile", "behavior", first])
        self.assertEqual(list((self.output_root / "target/ascii-case/native").iterdir()), [])
        logs = self.output_root / "logs/ascii-case/native"
        self.assertIn("E0061", (logs / f"{first}.log").read_text())
        results = json.loads((logs / "results.json").read_text())
        self.assertEqual(results["status"], "failed")
        self.assertFalse(results["negative_cases"][0]["passed"])

    def test_successful_compilation_is_not_a_rejection(self):
        first = next(iter(self.cases))

        def accepts(name, result):
            if name == first:
                result.returncode, result.stderr = 0, ""
            return result

        run, seen = self.compiler(self.output_root, self.project, accepts)
        with self.assertRaisesRegex(AssertionError, "Expected rustc exit 1"):
            self.invoke(run)
        self.assertEqual(seen[-1], first)
        logs = self.output_root / "logs/ascii-case/native"
        results = json.loads((logs / "results.json").read_text())
        self.assertEqual(results["status"], "failed")
        self.assertEqual(results["negative_cases"][0]["returncode"], 0)
        self.assertFalse(results["negative_cases"][0]["passed"])
        self.assertEqual(list((self.output_root / "target/ascii-case/native").iterdir()), [])

    def test_missing_compiler_records_failure_and_removes_copies(self):
        def unavailable(*args, **kwargs):
            raise OSError("compiler unavailable")

        with self.assertRaisesRegex(OSError, "compiler unavailable"):
            self.invoke(unavailable)
        logs = self.output_root / "logs/ascii-case/native"
        commands = json.loads((logs / "commands.json").read_text())
        self.assertEqual(len(commands), 1)
        self.assertIsNone(commands[0]["returncode"])
        self.assertIn("compiler unavailable", commands[0]["error"])
        self.assertIn("compiler unavailable", (logs / "rustc-version.log").read_text())
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
        self.assertEqual(list((self.output_root / "target/ascii-case/native").iterdir()), [])

    def test_command_failures_do_not_run_later_stages(self):
        stages = ("rustc-version", "compile", "behavior")
        for index, stage in enumerate(stages):
            with self.subTest(stage=stage):
                output_root = self.root / stage

                def fail(name, result):
                    if name == stage:
                        result.returncode = 101
                        result.stdout = "retained stdout\n"
                        result.stderr = "compiler or executable failed\n"
                    return result

                run, seen = self.compiler(output_root, self.project, fail)
                with self.assertRaisesRegex(AssertionError, f"{stage}: expected exit 0, got 101"):
                    self.invoke(run, output_root)
                self.assertEqual(seen, list(stages[:index + 1]))
                self.assertEqual(list((output_root / "target/ascii-case/native").iterdir()), [])
                logs = output_root / "logs/ascii-case/native"
                self.assertEqual(
                    (logs / f"{stage}.log").read_text(),
                    "retained stdout\ncompiler or executable failed\n",
                )
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(commands[-1]["returncode"], 101)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertEqual(results["negative_cases"], [])

    def test_linking_failures_cannot_pass_compilation_or_rejection(self):
        first = next(iter(self.cases))
        for stage in ("compile", first):
            with self.subTest(stage=stage):
                output_root = self.root / f"link-{stage}"

                def linking_failure(name, result):
                    if name == stage:
                        result.returncode = 1
                        result.stderr = self.diagnostic({
                            "code": None, "message": "linking with `cc` failed: exit status: 1",
                        })
                    return result

                run, seen = self.compiler(output_root, self.project, linking_failure)
                with self.assertRaisesRegex(AssertionError, f"see .*{stage}.log"):
                    self.invoke(run, output_root)
                self.assertEqual(
                    seen,
                    ["rustc-version", "compile"] if stage == "compile"
                    else ["rustc-version", "compile", "behavior", first],
                )
                logs = output_root / "logs/ascii-case/native"
                self.assertIn("linking with `cc` failed", (logs / f"{stage}.log").read_text())
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertEqual(list((output_root / "target/ascii-case/native").iterdir()), [])

    def test_behavior_requires_all_nonempty_unfiltered_tests(self):
        for index, stdout in enumerate((
            "",
            "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 16 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out;",
            "test result: FAILED. 16 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out;",
        )):
            with self.subTest(stdout=stdout):
                output_root = self.root / f"behavior-{index}"

                def incomplete(name, result):
                    if name == "behavior":
                        result.stdout = stdout
                    return result

                run, seen = self.compiler(output_root, self.project, incomplete)
                with self.assertRaisesRegex(AssertionError, "Expected all 17 executed ASCII-case tests"):
                    self.invoke(run, output_root)
                self.assertEqual(seen, ["rustc-version", "compile", "behavior"])
                self.assertEqual(list((output_root / "target/ascii-case/native").iterdir()), [])
                logs = output_root / "logs/ascii-case/native"
                self.assertEqual((logs / "behavior.log").read_text(), stdout)
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_wrong_rust_version_stops_before_compile(self):
        def wrong_version(name, result):
            if name == "rustc-version":
                result.stdout = "rustc 1.97.0\nrelease: 1.97.0\n"
            return result

        run, seen = self.compiler(self.output_root, self.project, wrong_version)
        with self.assertRaisesRegex(AssertionError, "Expected Rust 1.96.0"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version"])
        logs = self.output_root / "logs/ascii-case/native"
        self.assertIn("release: 1.97.0", (logs / "rustc-version.log").read_text())
        self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
        self.assertEqual(list((self.output_root / "target/ascii-case/native").iterdir()), [])

    def test_os_errors_clean_current_probes_and_partial_binaries(self):
        first = next(iter(self.cases))
        for stage in ("behavior", first):
            with self.subTest(stage=stage):
                output_root = self.root / f"os-error-{stage}"

                def unavailable(name, result):
                    if name == stage:
                        raise OSError("cannot execute command")
                    return result

                run, seen = self.compiler(output_root, self.project, unavailable)
                with self.assertRaisesRegex(OSError, "cannot execute command"):
                    self.invoke(run, output_root)
                self.assertEqual(seen[-1], stage)
                self.assertEqual(list((output_root / "target/ascii-case/native").iterdir()), [])
                logs = output_root / "logs/ascii-case/native"
                commands = json.loads((logs / "commands.json").read_text())
                self.assertIsNone(commands[-1]["returncode"])
                self.assertIn("cannot execute command", commands[-1]["error"])
                self.assertIn("cannot execute command", (logs / f"{stage}.log").read_text())
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_existing_artifact_collisions_are_preserved(self):
        first = next(iter(self.cases))
        for filename in (
            "source_ascii_case.rs", "ascii_case_behavior",
            f"rejection-{first}.rs", f"rejected-{first}.rlib",
        ):
            with self.subTest(filename=filename):
                output_root = self.root / filename
                output = output_root / "target/ascii-case/native"
                output.mkdir(parents=True)
                existing = output / filename
                existing.write_text("preserve existing artifact\n")
                run, seen = self.compiler(output_root, self.project, preserved=(existing,))
                with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite existing native artifact"):
                    self.invoke(run, output_root)
                self.assertEqual(existing.read_text(), "preserve existing artifact\n")
                self.assertEqual(list(output.iterdir()), [existing])
                if filename in ("source_ascii_case.rs", "ascii_case_behavior"):
                    self.assertEqual(seen, [])
                else:
                    self.assertEqual(seen, ["rustc-version", "compile", "behavior"])
                logs = output_root / "logs/ascii-case/native"
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_cli_help_preserves_existing_group_choices(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout, patch.object(
            check_native, "check_ascii_case"
        ) as ascii_case, patch.object(
            check_native, "check_singletons"
        ) as singleton, patch.object(check_native.subprocess, "run") as run:
            with self.assertRaises(SystemExit) as exit_status:
                check_native.main(["--help"])
        self.assertEqual(exit_status.exception.code, 0)
        self.assertIn("{defaults,singleton,ascii-case}", stdout.getvalue())
        self.assertIn("observers/Defaults checks (default)", stdout.getvalue())
        ascii_case.assert_not_called()
        singleton.assert_not_called()
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
