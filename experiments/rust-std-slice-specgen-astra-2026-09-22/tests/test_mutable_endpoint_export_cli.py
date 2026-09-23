from contextlib import contextmanager
import csv
import io
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts import export_completeness as export
import test_endpoint_export_cli as endpoint_tests


ROOT = Path(__file__).resolve().parents[1]
APIS = export.MUTABLE_ENDPOINTS
CHECKER_LOGS = Path(export.MUTABLE_CHECKER_LOGS)
SOURCE_LOGS = Path("logs/mutable-endpoints/correctness")
STATE_LOGS = Path("logs/mutable-endpoints-proposal/value-state/state")
BEFORE = Path("logs/mutable-endpoints/adoption-before")


class MutableEndpointExportCLI(unittest.TestCase):
    @staticmethod
    def copy_project(project):
        def copy(path, relocate=False):
            source = ROOT / path
            target = project / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            if relocate:
                target.write_text(source.read_text().replace(str(ROOT), str(project)))
            else:
                shutil.copyfile(source, target)

        for path in (
            "scripts/export_completeness.py", "inventory/apis.tsv", *export.MUTABLE_DEPENDENCIES,
            BEFORE / export.MUTABLE_POST, BEFORE / export.MUTABLE_STATE,
            *[path for path in (ROOT / "proofs/completeness/slice").glob("*.rs")
              if path.stem not in APIS],
            *[f"logs/foundation/correctness/{api}/verus.log"
              for api in ("len", "first", "last", "split_first", "split_last")],
        ):
            copy(path)
        shutil.copyfile(
            ROOT / BEFORE / "inventory/coverage.tsv", project / "inventory/coverage.tsv",
        )
        for name in ("command.json", "verus.log", "libstate.rlib", "queries/root.smt2",
                     "queries/root.smt_transcript"):
            copy(STATE_LOGS / name)
        for api in APIS:
            source = f"proofs/correctness/slice/{api}.rs"
            analysis = f"proofs/completeness/slice/inputs/{api}.rs"
            for path in (
                source, analysis, BEFORE / source,
                f"proofs/correctness/slice/proposals/{api}.rs",
                f"proofs/completeness/slice/history/{api}_direct.rs",
                f"logs/mutable-endpoints-proposal/correctness/original/{api}/verus.log",
            ):
                copy(path)
            logs = SOURCE_LOGS / api
            for name in (
                "verus-command.txt", "verus-execution.json", "verus.exit-code.txt",
                "verus.stdout", "verus.stderr",
            ):
                copy(logs / name, relocate=True)
            for path in (
                logs / f"libslice_{api}.rlib",
                logs / "inputs" / source, logs / "inputs" / export.MUTABLE_POST,
                logs / "queries/root.smt2", logs / "queries/root.smt_transcript",
                logs / "queries/contracts.smt2",
            ):
                copy(path)
            for phase in ("analyze", "replay"):
                logs = CHECKER_LOGS / api
                report = json.loads((ROOT / logs / f"{phase}.json").read_text())
                run = Path(report["run_dir"])
                for path in (analysis, *export.MUTABLE_DEPENDENCIES):
                    copy(run / "workspace" / path)
                for name in ("manifest.json", "effective-config.json"):
                    copy(run / name, relocate=True)
                result = report["results"][0]
                native = result["proofs"][0]["native"]
                for path in (
                    result["baseline"]["artifact"], native["harness"], native["source"],
                    *[Path(native["worktree"]) / dependency for dependency in export.MUTABLE_DEPENDENCIES],
                ):
                    copy(path)
                for name in (f"{phase}.json", f"{phase}-command.json", f"{phase}.stderr"):
                    copy(logs / name, relocate=True)

    @contextmanager
    def project(self, case):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/mutable-endpoints/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix=f"{case}-") as directory:
            project = Path(directory) / "project"
            self.copy_project(project)
            yield project

    def invoke(self, project, case, arguments, selected=(), expected_code=0):
        def contents():
            return {
                str(path.relative_to(project)): path.read_bytes()
                for path in project.rglob("*") if path.is_file()
            }

        before = contents()
        command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
        result = subprocess.run(
            command, cwd=project, capture_output=True, text=True, timeout=30,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
        after = contents()
        changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
        log_root = os.environ.get("MUTABLE_ENDPOINT_EXPORT_TEST_LOG_DIR")
        if log_root:
            log = ROOT / log_root / "cli" / case
            log.mkdir(parents=True, exist_ok=False)
            (log / "command.txt").write_text(
                f"cd {shlex.quote(str(project))} && {shlex.join(command)}\n"
            )
            (log / "stdout.log").write_text(result.stdout)
            (log / "stderr.log").write_text(result.stderr)
            (log / "result.json").write_text(json.dumps({
                "returncode": result.returncode, "expected_returncode": expected_code,
                "selected": selected, "changed_files": changed,
                "preexisting_files": len(before),
            }, indent=2) + "\n")
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        if expected_code:
            self.assertEqual(before, after)
            return
        allowed = {"inventory/coverage.tsv", *[
            f"proofs/completeness/slice/{api}.rs" for api in selected
        ]}
        self.assertLessEqual(set(changed), allowed)
        self.assertEqual(before.keys() - allowed, after.keys() - allowed)
        for path in before.keys() - allowed:
            self.assertEqual(before[path], after[path], path)
        fields, rows, records = endpoint_tests.EndpointExportCLI.table(before["inventory/coverage.tsv"])
        new_fields, new_rows, new_records = endpoint_tests.EndpointExportCLI.table(after["inventory/coverage.tsv"])
        self.assertEqual(fields, new_fields)
        self.assertEqual(list(rows), list(new_rows))
        self.assertEqual(len(rows), 331)
        self.assertEqual(records["header"], new_records["header"])
        for identity in rows:
            if identity not in {f"<[T]>::{api}" for api in selected}:
                self.assertEqual(records[identity], new_records[identity], identity)
            else:
                for field in fields[:4]:
                    self.assertEqual(rows[identity][field], new_rows[identity][field])
        for api in selected:
            row = new_rows[f"<[T]>::{api}"]
            self.assertEqual(row["specification"], f"{export.MUTABLE_POST}::{api}_post")
            self.assertEqual(row["correctness_proof"], f"proofs/correctness/slice/{api}.rs")
            self.assertEqual(row["correctness_target_functions"], "1")
            self.assertIn("--compile --no-cheating", row["correctness_command"])
            self.assertIn("1 target + 0 imported proof functions", row["correctness_result"])
            self.assertIn("index-update contracts and Seq view", row["correctness_result"])
            self.assertIn("final implementation review pending", row["correctness_result"])
            self.assertEqual(row["completeness_checked_goals"], "1")
            self.assertIn("entire final Seq<T>", row["completeness_result"])
            self.assertIn("all 13 search guards off", row["completeness_result"])
            self.assertIn("unchanged analysis/reexecution retained", row["completeness_result"])
            self.assertEqual(row["issues"], "issues/V-SLICE-PATTERN.md;issues/S-MUT-RETURN.md")
            self.assertEqual(row["independent_review"], "pending")
            text = after[row["completeness_proof"]].decode()
            _, report = self.report(project, api=api)
            original = Path(report["results"][0]["proofs"][0]["native"]["harness"]).read_text()
            self.assertEqual(
                "\n".join(text.splitlines()[3:]) + "\n",
                original.replace('#[path = "../mutable_endpoints_state.rs"]',
                                 '#[path = "mutable_endpoints_state.rs"]', 1),
            )
        self.assertIn(f"Exported {len(selected)} checked mutable endpoint proofs", result.stdout)

    def check_case(self, case, change=None, arguments=None, selected=(), expected_code=1):
        with self.project(case) as project:
            if change is not None:
                change(project)
            self.invoke(
                project, case, ["--mutable-endpoints"] if arguments is None else arguments,
                selected, expected_code,
            )

    @staticmethod
    def report(project, phase="analyze", api="last_mut"):
        path = project / CHECKER_LOGS / api / f"{phase}.json"
        return path, json.loads(path.read_text())

    @classmethod
    def alter_report(cls, project, keys, value, phase="analyze"):
        cls.set_json(project / CHECKER_LOGS / "last_mut" / f"{phase}.json", keys, value)

    @staticmethod
    def set_json(path, keys, value):
        data = json.loads(path.read_text())
        target = data
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        path.write_text(json.dumps(data, indent=2) + "\n")

    @classmethod
    def location(cls, project, kind, phase="analyze"):
        _, data = cls.report(project, phase)
        result = data["results"][0]
        if kind == "query":
            return Path(result["baseline"]["artifact"])
        if kind in ("harness", "source", "worktree"):
            return Path(result["proofs"][0]["native"][kind])
        return Path(data["run_dir"]) / kind

    @classmethod
    def alter_command(cls, project, edit, phase="verus"):
        if phase == "verus":
            logs = project / SOURCE_LOGS / "last_mut"
            path = logs / "verus-execution.json"
        else:
            logs = project / CHECKER_LOGS / "last_mut"
            path = logs / f"{phase}-command.json"
        receipt = json.loads(path.read_text())
        edit(receipt["command"])
        path.write_text(json.dumps(receipt) + "\n")
        if phase == "verus":
            (logs / "verus-command.txt").write_text(
                "RUSTUP_HOME=/home/chentianyu/.rustup " + shlex.join(receipt["command"]) + "\n"
            )

    def test_selection_and_mutually_exclusive_flags(self):
        flag = "--mutable-endpoints"
        for case, arguments, selected, code in (
            ("first", [flag, "first_mut"], ("first_mut",), 0),
            ("last", [flag, "last_mut"], ("last_mut",), 0),
            ("both", [flag], APIS, 0),
            ("reverse", [flag, "last_mut", "first_mut"], APIS[::-1], 0),
            ("wrong", [flag, "first"], (), 2),
            ("empty", [flag, ""], (), 2),
            ("duplicate", [flag, "first_mut", "first_mut"], (), 2),
            *[(other, [flag, "--" + other], (), 2)
              for other in ("defaults", "singletons", "ascii-case", "endpoints", "splits")],
        ):
            with self.subTest(case=case):
                self.check_case(case, arguments=arguments, selected=selected, expected_code=code)

    def test_partial_exports_are_selective_and_repeated_exports_are_identical(self):
        with self.project("partial") as project:
            self.invoke(project, "partial-first", ["--mutable-endpoints", "first_mut"], ("first_mut",))
            self.assertFalse((project / "proofs/completeness/slice/last_mut.rs").exists())
            self.invoke(project, "partial-last", ["--mutable-endpoints", "last_mut"], ("last_mut",))
            coverage = (project / "inventory/coverage.tsv").read_bytes()
            self.invoke(project, "partial-repeat", ["--mutable-endpoints"], APIS)
            self.assertEqual(coverage, (project / "inventory/coverage.tsv").read_bytes())

    def test_unselected_checker_logs_are_not_required(self):
        def remove(project):
            shutil.rmtree(project / SOURCE_LOGS / "last_mut")
            shutil.rmtree(project / CHECKER_LOGS / "last_mut")
        self.check_case(
            "without-unselected-logs", remove, ["--mutable-endpoints", "first_mut"], ("first_mut",), 0,
        )

    def test_source_failures_never_partially_export_the_other_api(self):
        for case, path, value in (
            ("source-exit", "verus.exit-code.txt", "1\n"),
            ("source-error", "verus.stdout", "verification results:: 0 verified, 1 errors\n"),
            ("source-zero", "verus.stdout", "verification results:: 0 verified, 0 errors\n"),
            ("source-imported", "verus.stdout", "verification results:: 7 verified, 0 errors\n"),
            ("source-partial", "verus.stdout", "verification results:: 1 verified, 0 errors (partial verification)\n"),
            ("source-stderr", "verus.stderr", "error\n"),
            ("source-library", "libslice_last_mut.rlib", ""),
            ("source-query", "queries/root.smt2", ""),
            ("source-transcript", "queries/root.smt_transcript", "(check-sat)\nunknown\n"),
            ("source-extra-proof", "queries/contracts.smt2", ";; Function-Def imported\n"),
        ):
            self.check_case(
                case, lambda project, p=path, v=value: (project / SOURCE_LOGS / "last_mut" / p).write_text(v),
            )
        for name in ("verus-execution.json", "libslice_last_mut.rlib"):
            self.check_case(
                "missing-" + name, lambda project, name=name: (project / SOURCE_LOGS / "last_mut" / name).unlink(),
            )

    def test_source_command_cannot_skip_compile_or_change_the_target(self):
        for case, edit in (
            ("no-compile", lambda command: command.remove("--compile")),
            ("no-no-cheating", lambda command: command.remove("--no-cheating")),
            ("wrong-source", lambda command: command.__setitem__(1, "specs/mod.rs")),
            ("wrong-crate", lambda command: command.__setitem__(5, "slice_first_mut")),
            ("source-partial-option", lambda command: command.extend(["--verify-root"])),
        ):
            self.check_case(case, lambda project, edit=edit: self.alter_command(project, edit))
        for field, value in (("returncode", 1), ("cwd", "/wrong"), ("RUSTUP_HOME", "/wrong")):
            self.check_case(
                "source-receipt-" + field,
                lambda project, f=field, v=value: self.set_json(
                    project / SOURCE_LOGS / "last_mut/verus-execution.json", [f], v,
                ),
            )

    def test_stale_inputs_and_every_state_dependency_are_rejected(self):
        for location in ("current", "compiled"):
            for source in ("proofs/correctness/slice/last_mut.rs", export.MUTABLE_POST):
                def stale(project, source=source, location=location):
                    base = project if location == "current" else project / SOURCE_LOGS / "last_mut/inputs"
                    path = base / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(f"source-stale-{location}-{Path(source).name}", stale)
        for location in ("current", "analyze", "replay", "native-analyze", "native-replay"):
            for source in ("proofs/completeness/slice/inputs/last_mut.rs", *export.MUTABLE_DEPENDENCIES):
                if location.startswith("native-") and source.endswith("inputs/last_mut.rs"):
                    continue
                def stale(project, source=source, location=location):
                    if location == "current":
                        base = project
                    elif location.startswith("native-"):
                        base = self.location(project, "worktree", location.removeprefix("native-"))
                    else:
                        base = self.location(project, "workspace", location)
                    path = base / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(f"checker-stale-{location}-{Path(source).name}", stale)

    def test_state_correspondence_must_be_compiled_and_current(self):
        for case, name, text in (
            ("state-zero", "verus.log", "verification results:: 0 verified, 0 errors\n"),
            ("state-no-library", "libstate.rlib", ""),
            ("state-no-query", "queries/root.smt2", ""),
            ("state-unknown", "queries/root.smt_transcript", "unknown\n"),
        ):
            self.check_case(case, lambda project, n=name, t=text: (project / STATE_LOGS / n).write_text(t))
        def no_no_cheating(project):
            path = project / STATE_LOGS / "command.json"
            command = json.loads(path.read_text())["command"]
            command.remove("--no-cheating")
            self.set_json(path, ["command"], command)
        self.check_case("state-no-no-cheating", no_no_cheating)
        for source in (export.MUTABLE_POST, export.MUTABLE_STATE):
            def stale(project, source=source):
                path = project / BEFORE / source
                path.write_bytes(path.read_bytes() + b"\n")
            self.check_case("state-before-" + Path(source).name, stale)

    def test_checker_failure_zero_targets_and_unknown_are_not_success(self):
        prefix = ["results", 0]
        native = prefix + ["proofs", 0, "native"]
        for phase in ("analyze", "replay"):
            for case, keys, value in (
                ("exit", ["exit_code"], 1),
                ("run-failed", ["status"], "failed"),
                ("diagnostic", ["diagnostics"], [{"message": "unexpected"}]),
                ("no-targets", ["results"], []),
                ("target-failed", prefix + ["status"], "failed"),
                ("target-nondeterministic", prefix + ["verdict"], "nondeterministic"),
                ("target-diagnostic", prefix + ["diagnostics"], [{"message": "unexpected"}]),
                ("baseline-unknown", prefix + ["baseline", "status"], "unknown"),
                ("baseline-constrained", prefix + ["baseline", "constraints"], ["nonempty"]),
                ("zero-goals", prefix + ["proofs", 0, "verified_goals"], 0),
                ("not-baseline", native + ["baseline"], False),
                ("wrong-target", prefix + ["target", "name"], "first_mut_observation"),
                ("wrong-line", prefix + ["target", "line"], 13),
                ("ignored-writeback", prefix + ["coverage", "ignored_dimensions"], ["return.1"]),
                ("native-failed", native + ["invocations", 0, "process", "returncode"], 1),
                ("native-zero", native + ["invocations", 0, "verified_goals"], 0),
                ("native-timeout", native + ["invocations", 0, "process", "timed_out"], True),
                ("native-wrong-target", native + ["invocations", 0, "function"], "state::caller_domain"),
            ):
                self.check_case(
                    phase + "-" + case,
                    lambda project, k=keys, v=value, p=phase: self.alter_report(project, k, v, p),
                )
            def duplicate(project, phase=phase):
                _, report = self.report(project, phase)
                self.alter_report(project, ["results"], report["results"] * 2, phase)
            self.check_case(phase + "-duplicate-target", duplicate)

    def test_comparison_cannot_drop_the_variant_element_or_final_sequence(self):
        for phase in ("analyze", "replay"):
            for case, before, after in (
                ("variant", "(((r1)@.0 is Some) == ((r2)@.0 is Some))", "true"),
                ("element", "((r1)@.0->Some_0 == (r2)@.0->Some_0)", "true"),
                ("writeback", "((r1)@.1 =~= (r2)@.1)", "true"),
                ("length-only", "((r1)@.1 =~= (r2)@.1)", "((r1)@.1.len() == (r2)@.1.len())"),
            ):
                def change(project, phase=phase, before=before, after=after):
                    _, report = self.report(project, phase)
                    text = report["results"][0]["proofs"][0]["native"]["det_spec"]["equal_fn_def"]
                    self.assertIn(before, text)
                    self.alter_report(
                        project, ["results", 0, "proofs", 0, "native", "det_spec", "equal_fn_def"],
                        text.replace(before, after, 1), phase,
                    )
                self.check_case(f"{phase}-missing-{case}", change)
            self.check_case(
                f"{phase}-output-as-input",
                lambda project, p=phase: self.alter_report(
                    project, ["results", 0, "proofs", 0, "native", "det_spec", "det_check_template"],
                    "requires r1@.1 == r2@.1", p,
                ),
            )
            def altered_harness(project, phase=phase):
                for kind in ("harness", "source"):
                    path = self.location(project, kind, phase)
                    text = path.read_text()
                    self.assertIn("caller_final@, r2@", text)
                    path.write_text(text.replace("caller_final@, r2@", "caller_final@, r1@", 1))
            self.check_case(f"{phase}-actual-harness", altered_harness)

    def test_each_of_thirteen_search_guards_must_be_disabled(self):
        for phase in ("analyze", "replay"):
            _, report = self.report(ROOT, phase)
            query = Path(report["results"][0]["baseline"]["artifact"]).read_text()
            guards = re.findall(r"^\(declare-fun (g_\S+)! \(\) Bool\)$", query, re.MULTILINE)
            self.assertEqual(len(guards), 13)
            for guard in guards:
                def constrain(project, phase=phase, guard=guard):
                    path = self.location(project, "query", phase)
                    text = path.read_text()
                    self.assertIn(f"(not {guard}!)", text)
                    path.write_text(text.replace(f"(not {guard}!)", f"{guard}!", 1))
                self.check_case(f"{phase}-{guard}", constrain)
            def extra_query(project, phase=phase):
                path = self.location(project, "query", phase)
                path.write_text(path.read_text() + "(assert false)\n")
            self.check_case(f"{phase}-altered-query", extra_query)

    def test_run_configuration_and_reexecution_are_checked(self):
        for phase in ("analyze", "replay"):
            for name, keys, value in (
                ("selector", ["selectors"], []),
                ("assistance", ["assistance"], {"mode": "live"}),
                ("verus", ["toolchain", "executable"], "/wrong/verus"),
                ("partial-verification", ["toolchain", "extra_args"], ["--verify-root"]),
            ):
                self.check_case(
                    f"{phase}-config-{name}",
                    lambda project, p=phase, k=keys, v=value: self.set_json(
                        self.location(project, "effective-config.json", p), ["payload", *k], v,
                    ),
                )
            self.check_case(
                f"{phase}-command-exit", lambda project, p=phase: self.set_json(
                    project / CHECKER_LOGS / "last_mut" / f"{p}-command.json", ["returncode"], 1,
                ),
            )
        for case, edit in (
            ("without-reexecute", lambda command: command.remove("--reexecute")),
            ("wrong-run", lambda command: command.__setitem__(3, "/wrong/run")),
            ("config-override", lambda command: command.extend(["--config", "specdet.toml"])),
        ):
            self.check_case(
                "replay-" + case, lambda project, e=edit: self.alter_command(project, e, "replay"),
            )
        self.check_case(
            "wrong-analyze-selector",
            lambda project: self.alter_command(
                project, lambda command: command.__setitem__(command.index("--target") + 1, "*"), "analyze",
            ),
        )
        self.check_case(
            "wrong-replay-parent",
            lambda project: self.set_json(
                self.location(project, "manifest.json", "replay"), ["payload", "parent_run"], "/wrong/run",
            ),
        )

    def test_missing_duplicate_or_invalid_records_preserve_all_outputs(self):
        self.check_case("no-coverage", lambda project: (project / "inventory/coverage.tsv").unlink())
        for filename in ("apis.tsv", "coverage.tsv"):
            def duplicate(project, filename=filename):
                path = project / "inventory" / filename
                rows = path.read_bytes().splitlines(keepends=True)
                path.write_bytes(b"".join(rows + [rows[1]]))
            self.check_case("duplicate-" + filename, duplicate)
        def missing(project):
            for filename in ("apis.tsv", "coverage.tsv"):
                path = project / "inventory" / filename
                path.write_bytes(b"".join(
                    line for line in path.read_bytes().splitlines(keepends=True)
                    if not line.startswith(b"<[T]>::last_mut\t")
                ))
        self.check_case("missing-selected-identity", missing)
        def reviewed(project):
            path = project / "inventory/coverage.tsv"
            stream = io.StringIO(path.read_text())
            reader = csv.DictReader(stream, delimiter="\t")
            rows = list(reader)
            for row in rows:
                if row["canonical_id"] == "<[T]>::last_mut":
                    row["independent_review"] = "approved"
            with path.open("w") as out:
                writer = csv.DictWriter(out, fieldnames=reader.fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(rows)
        self.check_case("unexpected-independent-result", reviewed)

    def test_different_existing_proof_is_not_overwritten(self):
        self.check_case(
            "different-existing-proof",
            lambda project: (project / "proofs/completeness/slice/last_mut.rs").write_text("// other work\n"),
        )

    def test_raw_unselected_records_and_metadata_cells_are_preserved(self):
        with self.project("raw-tsv") as project:
            path = project / "inventory/coverage.tsv"
            raw = path.read_bytes().replace(b"\tpending\t", b'\t"pending"\t').replace(b"\n", b"\r\n")
            path.write_bytes(raw)
            self.invoke(project, "raw-tsv", ["--mutable-endpoints"], APIS)
            self.assertEqual(raw.count(b"\r\n"), path.read_bytes().count(b"\r\n"))


if __name__ == "__main__":
    unittest.main()
