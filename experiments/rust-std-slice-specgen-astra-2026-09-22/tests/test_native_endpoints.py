import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from scripts import check_native


class EndpointNativeRunner(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(
            dir=check_native.ROOT, prefix=".endpoints-runner-test-"
        )
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.project = self.root / "project"
        self.output_root = self.root / "results"
        self.proofs = self.project / "proofs/correctness/slice"
        self.proofs.mkdir(parents=True)
        (self.project / "tests").mkdir()
        self.behavior = (check_native.ROOT / "tests/endpoint_proposal_behavior.rs").read_text()
        (self.project / "tests/endpoint_proposal_behavior.rs").write_text(self.behavior)
        for name in ("first", "last"):
            current = (check_native.ENDPOINT_PROOFS / f"{name}.rs").read_text()
            (self.proofs / f"{name}.rs").write_text(current)
        self.cases = {
            name: (text, expected)
            for name, text, expected in check_native.endpoint_negative_cases()
        }

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

    def compiler(self, output_root, override=None):
        output = output_root.resolve() / "target/endpoints/native"
        logs = output_root.resolve() / "logs/endpoints/native"
        seen = []

        def run(command, *, cwd, env, text, capture_output):
            self.assertEqual(cwd, self.project)
            self.assertTrue(text)
            self.assertTrue(capture_output)
            self.assertNotIn("RUSTC_BOOTSTRAP", env)
            self.assertEqual(env["RUSTUP_HOME"], "/home/chentianyu/.rustup")
            self.assertEqual(env["TMPDIR"], str(output))
            self.assertEqual(
                env["SLICE_ENDPOINTS_SOURCE"],
                str(logs / "source_endpoints.rs"),
            )
            self.assertTrue((logs / "source_endpoints.rs").is_file())
            self.assertEqual((logs / "endpoint_behavior.rs").read_text(), self.behavior)
            self.assertEqual(list(output.glob("rejected-*.rlib")), [])
            binary = output / "endpoint_behavior"
            returncode, stdout, stderr = 0, "", ""
            if command == ["rustc", "+1.96.0", "-vV"]:
                name = "rustc-version"
                stdout = "rustc 1.96.0\nrelease: 1.96.0\n"
            elif command == [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                str(logs / "endpoint_behavior.rs"),
                "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=link,mir={logs / 'endpoint_behavior.mir'}",
                "-o", str(binary),
            ]:
                name = "compile"
                binary.write_text("mock binary\n")
                (logs / "endpoint_behavior.mir").write_text("\n".join(
                    f"fn {module}::{api}(_1: &[T]) -> Option<&T> {{}}"
                    for module in ("original", "adopted") for api in ("first", "last")
                ))
            elif command == [str(binary), "--test-threads=1"]:
                name = "behavior"
                self.assertTrue(binary.is_file())
                stdout = (
                    "running 14 tests\n"
                    "test result: ok. 14 passed; 0 failed; 0 ignored; "
                    "0 measured; 0 filtered out; finished in 0.00s\n"
                )
            else:
                self.assertEqual(command[:6], [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--crate-name=endpoint_rejection", "--error-format=json",
                ])
                self.assertEqual(len(command), 9)
                probe = Path(command[6])
                name = probe.stem.removeprefix("rejection-")
                body, expected = self.cases[name]
                self.assertEqual(probe.parent, output)
                self.assertEqual(list(output.glob("rejection-*.rs")), [probe])
                self.assertEqual(
                    probe.read_text(),
                    '#![allow(dead_code)]\n'
                    'include!(env!("SLICE_ENDPOINTS_SOURCE"));\n' + body + "\n",
                )
                rejected = output / f"rejected-{name}.rlib"
                self.assertEqual(command[7:], ["-o", str(rejected)])
                rejected.write_text("mock partial compiler output\n")
                returncode, stderr = 1, self.diagnostic(expected)
            if name in ("rustc-version", "compile", "behavior"):
                self.assertEqual(list(output.glob("rejection-*.rs")), [])
            seen.append(name)
            result = check_native.subprocess.CompletedProcess(command, returncode, stdout, stderr)
            return override(name, result) if override else result

        return run, seen

    def invoke(self, run, output_root=None, redirected=True):
        args = ["--group", "endpoints"]
        if redirected:
            args += ["--output-root", str(output_root or self.output_root)]
        with patch.object(check_native, "ROOT", self.project), patch.object(
            check_native, "ENDPOINT_PROOFS", self.proofs
        ), patch.object(
            check_native, "check_singletons", side_effect=AssertionError("singleton dispatch")
        ), patch.object(
            check_native, "check_ascii_case", side_effect=AssertionError("ASCII dispatch")
        ), patch.dict(
            check_native.os.environ, {"RUSTC_BOOTSTRAP": "1", "RUSTUP_HOME": "/wrong"}
        ), patch.object(
            check_native.subprocess, "run", side_effect=run
        ), patch("builtins.print"):
            check_native.main(args)

    def test_source_copies_retain_exact_authority_and_adopted_current_mapping(self):
        with patch.object(check_native, "ENDPOINT_PROOFS", self.proofs):
            text, spans, mappings = check_native.endpoint_source()
        self.assertIn("ADOPTED current source-proof input", text)
        self.assertNotIn("proposal", text)
        for span in spans:
            source = Path(span["path"]).read_text().splitlines(keepends=True)
            self.assertEqual(span["text"], "".join(source[span["start"] - 1:span["end"]]))
        self.assertEqual(
            [(s["name"], s["start"], s["end"]) for s in spans if s["kind"] == "function"],
            [("first", 155, 157), ("last", 281, 283)],
        )
        self.assertEqual(
            [s["role"] for s in spans if s["kind"] == "proof"], ["current", "current"]
        )
        for mapping, name, pattern, expression in zip(
            mappings, ("first", "last"), ("[first, ..]", "[.., last]"),
            ("Some(&slice[0])", "Some(&slice[slice.len() - 1])"),
        ):
            self.assertEqual(mapping["api"], f"<[T]>::{name}")
            self.assertEqual(
                mapping["original_body"],
                f"    if let {pattern} = slice {{ Some({name}) }} else {{ None }}",
            )
            self.assertEqual(
                mapping["current"]["body"],
                f"    if slice.len() == 0 {{ None }} else {{ {expression} }}",
            )
            self.assertNotEqual(mapping["original_body"], mapping["current"]["body"])
            self.assertNotIn("proposal", mapping)
            self.assertEqual(mapping["native_adopted"], f"adopted::{name}")
            self.assertEqual(Path(mapping["current"]["path"]), self.proofs / f"{name}.rs")
            proof = Path(mapping["current"]["path"]).read_text()
            self.assertEqual(
                proof.splitlines()[mapping["current"]["body_start"] - 1],
                mapping["current"]["body"],
            )
            self.assertIn(mapping["original_body"], text.split("pub mod adopted {")[0])
            self.assertIn(mapping["current"]["body"], text.split("pub mod adopted {")[1])
            self.assertEqual(
                Path(mapping["current"]["contract"]), self.project / "specs/slice/mod.rs"
            )
            self.assertIn(mapping["current"]["signature"].replace(
                "-> (result: Option<&T>)", "-> Option<&T>"
            ), text)
        self.assertNotIn("#[stable(", text)
        self.assertNotIn("#[rustc_const_stable(", text)
        self.assertNotIn("ensures", text)
        self.assertNotIn("vstd", text)

    def test_selected_group_paths_evidence_and_previous_outputs_are_preserved(self):
        for redirected in (False, True):
            with self.subTest(redirected=redirected):
                root = self.output_root if redirected else self.project
                output = root / "target/endpoints/native"
                logs = root / "logs/endpoints/native"
                preserved = {
                    output / "previous-output": "old output",
                    logs / "previous.log": "old log",
                }
                for group in ("defaults", "singleton", "ascii-case", "endpoints-proposal"):
                    preserved[root / f"target/{group}/native/previous"] = "old group output"
                    preserved[root / f"logs/{group}/native/results.json"] = "old group evidence"
                for path, content in preserved.items():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                run, seen = self.compiler(root)
                self.invoke(run, root, redirected)
                self.assertEqual(seen, ["rustc-version", "compile", "behavior"] + list(self.cases))
                self.assertEqual(list(output.iterdir()), [output / "previous-output"])
                for path, content in preserved.items():
                    self.assertEqual(path.read_text(), content)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "passed")
                self.assertEqual(results["group"], "endpoints")
                self.assertIn("ADOPTED current first/last", results["source_status"])
                self.assertEqual(results["positive_tests"], 14)
                self.assertEqual(len(results["negative_cases"]), 60)
                for case in results["negative_cases"]:
                    self.assertTrue(case["passed"])
                    self.assertEqual(case["returncode"], 1)
                    self.assertIn(self.cases[case["name"]][0], case["source"])
                    self.assertEqual(
                        Path(case["log"]).read_text(), self.diagnostic(case["expected"])
                    )
                self.assertTrue(Path(results["mir"]["path"]).is_file())
                self.assertEqual(len(results["mir"]["generic_functions"]), 4)
                self.assertTrue(all(Path(path).is_file() for path in results["mir"]["source_inputs"]))
                commands = json.loads((logs / "commands.json").read_text())
                self.assertEqual(len(commands), 63)
                self.assertEqual([c["returncode"] for c in commands], [0] * 3 + [1] * 60)
                for command in commands:
                    self.assertIsNone(command["RUSTC_BOOTSTRAP"])
                    self.assertEqual(command["RUSTUP_HOME"], "/home/chentianyu/.rustup")
                    self.assertEqual(command["cwd"], str(self.project))
                    self.assertTrue(Path(command["log"]).is_file())
                self.assertEqual(len(json.loads((logs / "source-mappings.json").read_text())), 2)
                dependencies = json.loads((logs / "dependencies.json").read_text())
                self.assertEqual(dependencies["proof_inputs"], [
                    str(self.proofs / f"{name}.rs") for name in ("first", "last")
                ])
                self.assertEqual(
                    dependencies["unchanged_contracts"], [str(self.project / "specs/slice/mod.rs")]
                )
                self.assertIn("not an equivalence proof", dependencies["mir_use"])

    def test_relative_output_root_does_not_write_to_project_inputs(self):
        before = {
            path: path.read_text() for path in self.project.rglob("*") if path.is_file()
        }
        run, seen = self.compiler(self.output_root)
        self.invoke(run, self.output_root.relative_to(check_native.ROOT))
        self.assertEqual(len(seen), 63)
        self.assertEqual(
            before, {path: path.read_text() for path in self.project.rglob("*") if path.is_file()}
        )
        self.assertFalse((self.project / "target").exists())
        self.assertFalse((self.project / "logs").exists())

    def test_authority_drift_fails_before_compilation(self):
        original = check_native.SOURCE.read_text().splitlines(keepends=True)
        for line, before, after in (
            (101, "impl<T>", "impl<T: Copy>"),
            (140, "first element", "different element"),
            (151, "1.0.0", "1.1.0"),
            (152, "1.56.0", "1.57.0"),
            (155, "pub const fn", "pub fn"),
            (156, "[first, ..]", "[_, first, ..]"),
            (266, "last element", "different element"),
            (281, "&self", "&mut self"),
            (282, "Some(last)", "None"),
        ):
            with self.subTest(line=line):
                changed = original.copy()
                self.assertIn(before, changed[line - 1])
                changed[line - 1] = changed[line - 1].replace(before, after)
                path = self.root / f"changed-source-{line}.rs"
                path.write_text("".join(changed))
                run = Mock()
                root = self.root / f"source-drift-{line}"
                with patch.object(check_native, "SOURCE", path):
                    with self.assertRaisesRegex(ValueError, "Source span changed"):
                        self.invoke(run, root)
                run.assert_not_called()
                logs = root / "logs/endpoints/native"
                self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_current_drift_cannot_be_silently_substituted(self):
        for name, pattern in (("first", "[first, ..]"), ("last", "[.., last]")):
            path = self.proofs / f"{name}.rs"
            original = path.read_text()
            body = next(line for line in original.splitlines() if line.startswith("    if "))
            for index, (before, after) in enumerate((
                (body, "    None"),
                (body, f"    if let {pattern} = slice {{ Some({name}) }} else {{ None }}"),
                ("slice.len() == 0", "slice.is_empty()"),
                ("slice.len() == 0", "0 == slice.len()"),
                ("pub const fn", "pub fn"),
                ("<T>(slice", "<T: Copy>(slice"),
                ("<T>(slice", "<T: Eq>(slice"),
                ("<T>(slice", "<T: 'static>(slice"),
                ("slice: &[T]", "slice: &'static [T]"),
                ("Option<&T>", "Option<&mut T>"),
                ("Option<&T>", "Option<T>"),
                (f"{name}_post(slice, result)", "is_empty_post(slice, true)"),
                ("    ensures", "    requires slice.len() > 0,\n    ensures"),
                ("specs/slice/mod.rs", "specs/slice/other.rs"),
                ("use vstd::prelude::*;", "use vstd::slice::*;"),
                (body, body + "\n    // Unsanctioned body drift."),
                ("verus! {", "fn hidden() {}\nverus! {"),
            )):
                with self.subTest(name=name, variant=index):
                    self.assertIn(before, original)
                    path.write_text(original.replace(before, after, 1))
                    run = Mock()
                    root = self.root / f"current-{name}-drift-{index}"
                    try:
                        with self.assertRaisesRegex(ValueError, "Endpoint current source drift"):
                            self.invoke(run, root)
                        run.assert_not_called()
                        logs = root / "logs/endpoints/native"
                        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
                        self.assertEqual(
                            json.loads((logs / "results.json").read_text())["status"], "failed"
                        )
                    finally:
                        path.write_text(original)

    def test_missing_current_proof_is_an_explicit_failure(self):
        (self.proofs / "last.rs").unlink()
        run = Mock()
        with self.assertRaisesRegex(FileNotFoundError, "slice/last.rs"):
            self.invoke(run)
        run.assert_not_called()
        logs = self.output_root / "logs/endpoints/native"
        self.assertEqual(json.loads((logs / "commands.json").read_text()), [])
        self.assertIn("slice/last.rs", json.loads((logs / "results.json").read_text())["error"])

    def test_historical_proposals_are_not_native_inputs(self):
        proposals = self.proofs / "proposals"
        self.assertFalse(proposals.exists())
        proposals.mkdir()
        for name in ("first", "last"):
            (proposals / f"{name}.rs").write_text("not a valid current proof\n")
        run, seen = self.compiler(self.output_root)
        self.invoke(run)
        self.assertEqual(len(seen), 63)
        logs = self.output_root / "logs/endpoints/native"
        for filename in ("source-spans.json", "source-mappings.json", "dependencies.json"):
            self.assertNotIn(str(proposals), (logs / filename).read_text())
        for name in ("first", "last"):
            self.assertEqual((proposals / f"{name}.rs").read_text(), "not a valid current proof\n")

    def test_negative_cases_cover_both_apis_in_all_three_implementations(self):
        expected = {
            "wrong-receiver": "E0308", "missing-receiver": "E0061",
            "extra-argument": "E0061", "wrong-element": "E0308",
            "mutable-result": "E0308", "owned-result": "E0308",
            "write-through-result": "E0594", "local-escape": "E0515",
            "short-lifetime": "E0597", "static-escape": None,
        }
        self.assertEqual(set(self.cases), {
            f"{implementation}-{api}-{case}"
            for implementation in ("original", "adopted", "public")
            for api in ("first", "last") for case in expected
        })
        for name, (text, diagnostic) in self.cases.items():
            implementation, api, case = name.split("-", 2)
            self.assertIn(
                f"<[u8]>::{api}(" if implementation == "public"
                else f"{implementation}::{api}::<u8>(", text,
            )
            self.assertNotIn("API", text)
            self.assertEqual(diagnostic["code"], expected[case])
            if case == "static-escape":
                self.assertEqual(diagnostic["message"], "lifetime may not live long enough")

    def test_exact_diagnostics_not_just_any_failure_are_required(self):
        log = self.root / "diagnostic.log"
        for expected in ({"code": "E0308"}, {
            "code": None, "message": "lifetime may not live long enough",
        }):
            valid = self.diagnostic(expected)
            accepted = check_native.subprocess.CompletedProcess([], 1, "", valid)
            checked = check_native.check_singleton_rejection(accepted, expected, log)
            self.assertEqual(checked["code"], expected["code"])
            for code, stderr in (
                (0, valid), (2, valid), (101, valid), (-11, valid),
                (1, ""), (1, "compiler unavailable"), (1, "[]"),
                (1, self.diagnostic({"code": "E0425"})),
                (1, self.diagnostic({"code": None, "message": "linking failed"})),
                (1, valid + valid),
            ):
                with self.subTest(expected=expected, returncode=code, stderr=stderr):
                    failed = check_native.subprocess.CompletedProcess([], code, "", stderr)
                    with self.assertRaises(AssertionError):
                        check_native.check_singleton_rejection(failed, expected, log)

    def test_failure_logs_are_retained_and_only_current_outputs_are_cleaned(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "compile", "behavior", first):
            with self.subTest(stage=stage):
                root = self.root / stage

                def fail(name, result):
                    if name == stage:
                        result.returncode = 101
                        result.stdout = "retained stdout\n"
                        result.stderr = "retained failure\n"
                    return result

                run, seen = self.compiler(root, fail)
                with self.assertRaises(AssertionError):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], stage)
                self.assertEqual(list((root / "target/endpoints/native").iterdir()), [])
                logs = root / "logs/endpoints/native"
                self.assertEqual(
                    (logs / f"{stage}.log").read_text(), "retained stdout\nretained failure\n"
                )
                self.assertEqual(json.loads((logs / "commands.json").read_text())[-1]["returncode"], 101)
                results = json.loads((logs / "results.json").read_text())
                self.assertEqual(results["status"], "failed")
                self.assertTrue((logs / "source_endpoints.rs").is_file())
                self.assertTrue((logs / "endpoint_behavior.rs").is_file())
                if stage == first:
                    self.assertFalse(results["negative_cases"][0]["passed"])

    def test_missing_compiler_and_execution_errors_are_logged(self):
        first = next(iter(self.cases))
        for stage in ("rustc-version", "behavior", first):
            with self.subTest(stage=stage):
                root = self.root / f"missing-{stage}"

                def missing(name, result):
                    if name == stage:
                        raise OSError("cannot execute command")
                    return result

                run, seen = self.compiler(root, missing)
                with self.assertRaisesRegex(OSError, "cannot execute command"):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], stage)
                logs = root / "logs/endpoints/native"
                commands = json.loads((logs / "commands.json").read_text())
                self.assertIsNone(commands[-1]["returncode"])
                self.assertIn("cannot execute command", commands[-1]["error"])
                self.assertIn("cannot execute command", (logs / f"{stage}.log").read_text())
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")
                self.assertEqual(list((root / "target/endpoints/native").iterdir()), [])

    def test_wrong_version_stops_before_compilation(self):
        def wrong(name, result):
            if name == "rustc-version":
                result.stdout = "rustc 1.97.0\nrelease: 1.97.0\n"
            return result

        run, seen = self.compiler(self.output_root, wrong)
        with self.assertRaisesRegex(AssertionError, "Expected Rust 1.96.0"):
            self.invoke(run)
        self.assertEqual(seen, ["rustc-version"])

    def test_zero_partial_filtered_ignored_or_failed_tests_cannot_pass(self):
        for index, summary in enumerate((
            "",
            "test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 13 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out;",
            "test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out;",
            "test result: FAILED. 13 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out;",
        )):
            with self.subTest(summary=summary):
                root = self.root / f"behavior-{index}"

                def incomplete(name, result):
                    if name == "behavior":
                        result.stdout = summary
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaisesRegex(AssertionError, "Expected all 14 executed adopted endpoint tests"):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile", "behavior"])
                logs = root / "logs/endpoints/native"
                self.assertEqual((logs / "behavior.log").read_text(), summary)
                self.assertEqual(json.loads((logs / "results.json").read_text())["status"], "failed")

    def test_successful_or_irrelevant_rejection_does_not_pass(self):
        first = next(iter(self.cases))
        for index, (code, stderr) in enumerate((
            (0, ""),
            (1, self.diagnostic({"code": "E0061"})),
            (1, self.diagnostic({"code": None, "message": "linking failed"})),
        )):
            with self.subTest(returncode=code, stderr=stderr):
                root = self.root / f"rejection-{index}"

                def wrong(name, result):
                    if name == first:
                        result.returncode, result.stderr = code, stderr
                    return result

                run, seen = self.compiler(root, wrong)
                with self.assertRaisesRegex(AssertionError, "Expected rustc exit 1"):
                    self.invoke(run, root)
                self.assertEqual(seen[-1], first)
                logs = root / "logs/endpoints/native"
                results = json.loads((logs / "results.json").read_text())
                self.assertFalse(results["negative_cases"][0]["passed"])
                self.assertEqual((logs / f"{first}.log").read_text(), stderr)
                self.assertEqual(list((root / "target/endpoints/native").iterdir()), [])

    def test_missing_or_incomplete_generic_mir_is_not_accepted(self):
        for absent in (False, True):
            with self.subTest(absent=absent):
                root = self.root / f"mir-{absent}"
                mir = root / "logs/endpoints/native/endpoint_behavior.mir"

                def incomplete(name, result):
                    if name == "compile":
                        if absent:
                            mir.unlink()
                        else:
                            mir.write_text("fn original::first(_1: &[u8]) -> Option<&u8> {}\n")
                    return result

                run, seen = self.compiler(root, incomplete)
                with self.assertRaises(FileNotFoundError if absent else AssertionError):
                    self.invoke(run, root)
                self.assertEqual(seen, ["rustc-version", "compile"])
                results = json.loads((mir.parent / "results.json").read_text())
                self.assertEqual(results["status"], "failed")

    def test_preexisting_artifacts_and_evidence_are_never_overwritten_or_deleted(self):
        first = next(iter(self.cases))
        for index, relative in enumerate((
            "target/endpoints/native/endpoint_behavior",
            f"target/endpoints/native/rejection-{first}.rs",
            f"target/endpoints/native/rejected-{first}.rlib",
            "logs/endpoints/native/source_endpoints.rs",
            "logs/endpoints/native/endpoint_behavior.rs",
            "logs/endpoints/native/endpoint_behavior.mir",
            "logs/endpoints/native/commands.json",
            "logs/endpoints/native/results.json",
            "logs/endpoints/native/compile.log",
            f"logs/endpoints/native/{first}.log",
        )):
            with self.subTest(relative=relative):
                root = self.root / f"preserved-{index}"
                existing = root / relative
                existing.parent.mkdir(parents=True)
                existing.write_text("preserve previous evidence\n")
                run = Mock()
                with self.assertRaisesRegex(FileExistsError, "Refusing to overwrite existing native"):
                    self.invoke(run, root)
                run.assert_not_called()
                self.assertEqual(existing.read_text(), "preserve previous evidence\n")
                self.assertEqual([p for p in root.rglob("*") if p.is_file()], [existing])

    def test_cli_help_keeps_existing_groups_and_marks_current_adoption(self):
        with patch("sys.stdout", new_callable=io.StringIO) as stdout, patch.object(
            check_native.subprocess, "run"
        ) as run:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--help"])
        self.assertEqual(result.exception.code, 0)
        self.assertIn("{defaults,singleton,ascii-case}", stdout.getvalue())
        self.assertIn("endpoints", stdout.getvalue())
        self.assertIn("ADOPTED current", stdout.getvalue())
        self.assertNotIn("endpoints-proposal", stdout.getvalue())
        run.assert_not_called()

    def test_old_proposal_group_is_not_an_executable_path(self):
        with patch("sys.stderr", new_callable=io.StringIO) as stderr, patch.object(
            check_native.subprocess, "run"
        ) as run:
            with self.assertRaises(SystemExit) as result:
                check_native.main(["--group", "endpoints-proposal"])
        self.assertEqual(result.exception.code, 2)
        self.assertIn("invalid choice", stderr.getvalue())
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
