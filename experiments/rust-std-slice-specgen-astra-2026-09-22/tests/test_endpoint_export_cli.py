from contextlib import contextmanager
import csv
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts import export_completeness


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FIELDS = {
    "correctness_proof", "correctness_command", "correctness_log",
    "correctness_result", "correctness_target_functions",
}
GUARDS = (
    "g_slice_leneq", "g_slice_lenrng", "g_r1_is_Some", "g_r1_is_None",
    "g_r2_is_Some", "g_r2_is_None", "g_neq_tuple",
)


class EndpointExportCLI(unittest.TestCase):
    GROUP = "endpoints"
    APIS = ("first", "last")
    INVALID_API = "split_first"
    LOG_ENV = "ENDPOINT_EXPORT_TEST_LOG_DIR"
    GUARDS = GUARDS

    def copy_project(self, project, foundation=False):
        def copy(path, relocate=False):
            source = ROOT / path
            destination = project / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if relocate:
                destination.write_text(source.read_text().replace(str(ROOT), str(project)))
            else:
                shutil.copyfile(source, destination)

        for path in (
            "scripts/export_completeness.py", "inventory/apis.tsv", "inventory/coverage.tsv",
            "specs/slice/mod.rs", "specdet.toml",
            *((ROOT / "proofs/completeness/slice").glob("*.rs")),
        ):
            copy(path)
        apis = export_completeness.PATTERNS if foundation else self.APIS
        for api in apis:
            group = "splits" if api in export_completeness.SPLITS else "endpoints"
            source = f"proofs/correctness/slice/{api}.rs"
            analysis = f"proofs/completeness/slice/inputs/{api}.rs"
            copy(source)
            copy(analysis)
            correctness = Path(f"logs/{group}/correctness/{api}")
            for name in (
                "verus-command.txt", "verus-execution.json", "verus.exit-code.txt",
                "verus.stdout", "verus.stderr",
            ):
                copy(correctness / name, relocate=True)
            copy(correctness / f"libslice_{api}.rlib")
            for path in (source, "specs/slice/mod.rs"):
                copy(correctness / "inputs" / path)
            for module in ("root", "contracts"):
                for extension in ("smt2", "smt_transcript"):
                    copy(correctness / "queries" / f"{module}.{extension}")
            logs = Path(f"logs/{group}/completeness/{api}")
            for phase in ("analyze", "replay"):
                report = json.loads((ROOT / logs / f"{phase}.json").read_text())
                run = Path(report["run_dir"])
                for path in (analysis, "specs/slice/mod.rs", "specdet.toml"):
                    copy(run / "workspace" / path)
                for name in ("manifest.json", "effective-config.json", "snapshot.json"):
                    copy(run / name, relocate=True)
                result = report["results"][0]
                native = result["proofs"][0]["native"]
                for path in (
                    result["baseline"]["artifact"], native["harness"], native["source"],
                    Path(native["worktree"]) / "specs/slice/mod.rs",
                    Path(native["worktree"]) / "specdet.toml",
                ):
                    copy(path)
                for name in (
                    f"{phase}.json", f"{phase}.stdout", f"{phase}.stderr",
                    f"{phase}.exit-code.txt", f"{phase}-command.txt", f"{phase}-execution.json",
                ):
                    copy(logs / name, relocate=True)
        if foundation:
            for api in ("len", "is_empty"):
                path = f"logs/foundation/completeness/{api}.json"
                report = json.loads((ROOT / path).read_text())
                copy(path, relocate=True)
                run = Path(report["run_dir"])
                source = f"proofs/completeness/slice/inputs/{api}.rs"
                copy(source)
                for path in (source, "specs/slice/mod.rs", "specdet.toml"):
                    copy(run / "workspace" / path)
                result = report["results"][0]
                copy(result["baseline"]["artifact"])
                copy(result["proofs"][0]["native"]["harness"])
                copy(f"logs/foundation/correctness/{api}/verus.log")

    @contextmanager
    def project(self, case, foundation=False):
        scratch = Path(os.environ.get("TMPDIR", ROOT / f"target/{self.GROUP}/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix=f"{case}-") as directory:
            project = Path(directory) / "project"
            self.copy_project(project, foundation)
            yield project

    @staticmethod
    def table(data):
        if data is None:
            return [], {}, {}
        stream = io.StringIO(data.decode(), newline="")
        reader = csv.DictReader(stream, delimiter="\t")
        fields = reader.fieldnames
        position = stream.tell()
        records = {"header": data.decode()[:position]}
        rows = {}
        for row in reader:
            end = stream.tell()
            records[row["canonical_id"]] = data.decode()[position:end]
            position = end
            rows[row["canonical_id"]] = row
        return fields, rows, records

    def invoke(self, project, case, arguments, selected=(), expected_code=0, default=False):
        coverage = project / "inventory/coverage.tsv"
        before = coverage.read_bytes() if coverage.exists() else None
        proof_root = project / "proofs/completeness/slice"
        proofs_before = {path.name: path.read_bytes() for path in proof_root.glob("*.rs")}
        command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
        result = subprocess.run(
            command, cwd=project, capture_output=True, text=True, timeout=30,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(project.parent)),
        )
        after = coverage.read_bytes() if coverage.exists() else None
        proofs_after = {path.name: path.read_bytes() for path in proof_root.glob("*.rs")}
        fields_before, rows_before, records_before = self.table(before)
        fields_after, rows_after, records_after = self.table(after)
        changed = {
            identity: sorted(
                key for key in rows_before[identity]
                if rows_before[identity][key] != rows_after[identity].get(key)
            )
            for identity in rows_before.keys() & rows_after.keys()
            if rows_before[identity] != rows_after[identity]
        }
        log_root = os.environ.get(self.LOG_ENV)
        if log_root:
            log = ROOT / log_root / "cli" / case
            log.mkdir(parents=True)
            (log / "command.txt").write_text(
                f"cd {shlex.quote(str(project))} && "
                f"PYTHONDONTWRITEBYTECODE=1 TMPDIR={shlex.quote(str(project.parent))} "
                f"{shlex.join(command)}\n"
            )
            (log / "stdout.log").write_text(result.stdout)
            (log / "stderr.log").write_text(result.stderr)
            (log / "exit-code.txt").write_text(f"{result.returncode}\n")
            (log / "isolation.json").write_text(json.dumps({
                "selected": selected, "default_export": default,
                "expected_exit_code": expected_code, "actual_exit_code": result.returncode,
                "changed_source_cells": changed,
                "coverage_byte_identical": before == after,
                "completeness_files": len(proofs_before),
                "changed_completeness_files": sorted(
                    name for name in proofs_before.keys() | proofs_after.keys()
                    if proofs_before.get(name) != proofs_after.get(name)
                ),
            }, indent=2) + "\n")
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        self.assertEqual(
            set(proofs_before),
            {path.name for path in (ROOT / "proofs/completeness/slice").glob("*.rs")},
        )
        self.assertEqual(proofs_before, proofs_after)
        if expected_code:
            self.assertEqual(before, after)
            return
        self.assertEqual(fields_before, fields_after)
        self.assertEqual(list(rows_before), list(rows_after))
        self.assertEqual(len(rows_before), 331)
        self.assertEqual(records_before["header"], records_after["header"])
        selected_ids = {f"<[T]>::{api}" for api in selected}
        for identity, row in rows_before.items():
            if identity not in selected_ids:
                self.assertEqual(row, rows_after[identity])
                self.assertEqual(records_before[identity], records_after[identity])
            else:
                for field in fields_before:
                    if field not in SOURCE_FIELDS:
                        self.assertEqual(row[field], rows_after[identity][field])
                self.assertLessEqual(set(changed.get(identity, [])), SOURCE_FIELDS)
        for api in selected:
            group = "splits" if api in export_completeness.SPLITS else "endpoints"
            row = rows_after[f"<[T]>::{api}"]
            self.assertEqual(row["correctness_proof"], f"proofs/correctness/slice/{api}.rs")
            self.assertEqual(row["correctness_target_functions"], "1")
            self.assertEqual(row["correctness_log"], f"logs/{group}/correctness/{api}/verus.stdout")
            self.assertIn("--compile --no-cheating", row["correctness_command"])
            self.assertIn("1 target + 2 imported consistency lemmas", row["correctness_result"])
            if api in export_completeness.SPLITS:
                self.assertIn("reviewed pattern-to-length/index/split_at conversion", row["correctness_result"])
                self.assertIn("trusts upstream slice length/index/split_at contracts", row["correctness_result"])
                self.assertIn("not metadata or split_at implementation verification", row["correctness_result"])
            else:
                self.assertIn("reviewed pattern-to-length/index conversion", row["correctness_result"])
                self.assertIn("trusts upstream slice length/index contracts", row["correctness_result"])
                self.assertIn("not metadata implementation verification", row["correctness_result"])
            self.assertIn("final implementation review pending", row["correctness_result"])
            self.assertEqual(row["independent_review"], "pending")
            self.assertIn("issues/V-SLICE-PATTERN.md", row["issues"])
        self.assertIn(
            "Exported 2 native completeness harnesses" if default
            else f"Updated {len(selected)} checked {self.GROUP[:-1]} source results",
            result.stdout,
        )

    def check_case(self, case, change=None, arguments=None, selected=(), expected_code=1):
        with self.project(case) as project:
            if change:
                change(project)
            self.invoke(
                project, case, [f"--{self.GROUP}", self.APIS[1]] if arguments is None else arguments,
                selected, expected_code,
            )

    @classmethod
    def report(cls, project, phase="analyze"):
        path = project / f"logs/{cls.GROUP}/completeness/{cls.APIS[1]}/{phase}.json"
        return path, json.loads(path.read_text())

    @classmethod
    def alter_report(cls, project, keys, value, phase="analyze"):
        path, report = cls.report(project, phase)
        item = report
        for key in keys[:-1]:
            item = item[key]
        item[keys[-1]] = value
        text = json.dumps(report, indent=2) + "\n"
        path.write_text(text)
        path.with_suffix(".stdout").write_text(text)

    @classmethod
    def artifact(cls, project, kind, phase="analyze"):
        _, report = cls.report(project, phase)
        result = report["results"][0]
        if kind == "query":
            return Path(result["baseline"]["artifact"])
        if kind == "harness":
            return Path(result["proofs"][0]["native"]["harness"])
        return Path(report["run_dir"]) / kind

    @staticmethod
    def set_json(path, keys, value):
        content = json.loads(path.read_text())
        item = content
        for key in keys[:-1]:
            item = item[key]
        item[keys[-1]] = value
        path.write_text(json.dumps(content, indent=2) + "\n")

    @classmethod
    def alter_command(cls, project, edit, phase="verus"):
        kind = "correctness" if phase == "verus" else "completeness"
        logs = project / f"logs/{cls.GROUP}/{kind}/{cls.APIS[1]}"
        path = logs / f"{phase}-execution.json"
        receipt = json.loads(path.read_text())
        edit(receipt["command"])
        path.write_text(json.dumps(receipt) + "\n")
        (logs / f"{phase}-command.txt").write_text(
            "RUSTUP_HOME=/home/chentianyu/.rustup " + shlex.join(receipt["command"]) + "\n"
        )

    def test_selected_both_invalid_and_mutually_exclusive_cli(self):
        flag = f"--{self.GROUP}"
        first, last = self.APIS
        for case, arguments, selected, code in (
            ("first", [flag, first], (first,), 0),
            ("last", [flag, last], (last,), 0),
            ("both", [flag], (first, last), 0),
            ("explicit-both", [flag, last, first], (last, first), 0),
            ("wrong-name", [flag, self.INVALID_API], (), 2),
            ("empty-name", [flag, ""], (), 2),
            ("duplicate", [flag, first, first], (), 2),
            ("duplicate-both", [flag, first, last, first], (), 2),
            ("mixed-defaults", [flag, "--defaults"], (), 2),
            ("mixed-singletons", [flag, "--singletons"], (), 2),
            ("mixed-ascii", [flag, "--ascii-case"], (), 2),
            ("mixed-patterns", ["--endpoints", "--splits"], (), 2),
        ):
            with self.subTest(case=case):
                self.check_case(case, arguments=arguments, selected=selected, expected_code=code)

    def test_selection_does_not_require_unselected_logs(self):
        def remove_last(project):
            for group in ("correctness", "completeness"):
                shutil.rmtree(project / f"logs/{self.GROUP}/{group}/{self.APIS[1]}")
        self.check_case(
            "first-only-evidence", remove_last, [f"--{self.GROUP}", self.APIS[0]], (self.APIS[0],), 0,
        )

    def test_default_export_uses_current_source_evidence_without_old_pattern_reports(self):
        with self.project("default", foundation=True) as project:
            other = "splits" if self.GROUP == "endpoints" else "endpoints"
            prepared = subprocess.run(
                [sys.executable, "-B", "scripts/export_completeness.py", f"--{other}"],
                cwd=project, capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
            self.invoke(project, "before-default", [f"--{self.GROUP}"], self.APIS)
            before = (project / "inventory/coverage.tsv").read_bytes()
            self.invoke(project, "default", [], export_completeness.PATTERNS, default=True)
            self.assertEqual(before, (project / "inventory/coverage.tsv").read_bytes())
            self.invoke(project, "repeat-patterns", [f"--{self.GROUP}"], self.APIS)
            (project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}/verus.exit-code.txt").write_text("1\n")
            self.invoke(project, "default-no-fallback", [], expected_code=1, default=True)

    def test_source_failures_are_atomic_even_after_another_selected_success(self):
        for case, path, value in (
            ("nonzero-exit", "verus.exit-code.txt", "1\n"),
            ("failed-proof", "verus.stdout", "verification results:: 2 verified, 1 errors\n"),
            ("zero-proof", "verus.stdout", "verification results:: 0 verified, 0 errors\n"),
            ("imported-only", "verus.stdout", "verification results:: 2 verified, 0 errors\n"),
            ("partial-proof", "verus.stdout",
             "verification results:: 3 verified, 0 errors (partial verification with `--verify-*`)\n"),
            ("skipped-proof", "verus.stdout", "verification results:: 3 verified, 0 errors\nskipped last\n"),
            ("proof-stderr", "verus.stderr", "error: compilation failed\n"),
            ("empty-compiled-proof", f"libslice_{self.APIS[1]}.rlib", ""),
            ("zero-target-query", "queries/root.smt2", ""),
            ("failed-target-query", "queries/root.smt_transcript", "(check-sat)\nsat\n"),
        ):
            with self.subTest(case=case):
                self.check_case(
                    case, lambda project, p=path, v=value:
                    (project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}" / p).write_text(v),
                    arguments=[f"--{self.GROUP}"],
                )
        for path in (f"libslice_{self.APIS[1]}.rlib", "verus-execution.json"):
            self.check_case(
                "missing-" + path, lambda project, p=path:
                (project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}" / p).unlink(),
            )
        for field, value in (("returncode", 1), ("cwd", "/wrong"), ("RUSTUP_HOME", "/wrong")):
            self.check_case(
                "source-receipt-" + field, lambda project, f=field, v=value: self.set_json(
                    project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}/verus-execution.json", [f], v,
                ),
            )
        self.check_case(
            "arbitrary-command-text", lambda project:
            (project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}/verus-command.txt").write_text("echo success\n"),
        )

    def test_source_commands_cannot_skip_compile_or_verify_a_different_target(self):
        for case, edit in (
            ("no-compile", lambda command: command.remove("--compile")),
            ("no-no-cheating", lambda command: command.remove("--no-cheating")),
            ("wrong-source", lambda command: command.__setitem__(1, "specs/slice/mod.rs")),
            ("wrong-verus", lambda command: command.__setitem__(0, "/wrong/verus")),
            ("wrong-crate", lambda command: command.__setitem__(5, f"slice_{self.APIS[0]}")),
            ("only-lemmas", lambda command: command.extend(["--verify-module", "contracts"])),
        ):
            with self.subTest(case=case):
                self.check_case(case, lambda project, edit=edit: self.alter_command(project, edit))
        def wrong_query(project):
            api = self.APIS[1]
            path = project / f"logs/{self.GROUP}/correctness/{api}/queries/root.smt2"
            path.write_text(path.read_text().replace(
                f";; Function-Def slice_{api}::{api}",
                f";; Function-Def slice_{api}::contracts::empty_results",
            ))
        self.check_case("wrong-target-query", wrong_query)

    def test_stale_source_proof_candidate_and_config_snapshots_do_not_export(self):
        sources = (f"proofs/correctness/slice/{self.APIS[1]}.rs", "specs/slice/mod.rs")
        for snapshot in (False, True):
            for source in sources:
                case = f"source-stale-{snapshot}-" + source.replace("/", "-")
                def stale(project, source=source, snapshot=snapshot):
                    base = project / f"logs/{self.GROUP}/correctness/{self.APIS[1]}/inputs" if snapshot else project
                    path = base / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(case, stale)
        for phase in ("current", "analyze", "replay"):
            for source in (
                f"proofs/completeness/slice/inputs/{self.APIS[1]}.rs", "specs/slice/mod.rs", "specdet.toml",
            ):
                case = f"checker-stale-{phase}-" + source.replace("/", "-")
                def stale(project, phase=phase, source=source):
                    base = project if phase == "current" else self.artifact(project, "workspace", phase)
                    path = base / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(case, stale)

    def test_checker_failure_zero_goals_diagnostics_and_extra_targets_do_not_export(self):
        prefix = ["results", 0]
        native = prefix + ["proofs", 0, "native"]
        for case, keys, value in (
            ("checker-exit", ["exit_code"], 1),
            ("checker-incomplete", ["status"], "failed"),
            ("checker-diagnostic", ["diagnostics"], [{"message": "unexpected"}]),
            ("target-diagnostic", prefix + ["diagnostics"], []),
            ("target-failed", prefix + ["status"], "failed"),
            ("target-nondeterministic", prefix + ["verdict"], "nondeterministic"),
            ("baseline-sat", prefix + ["baseline", "status"], "sat"),
            ("baseline-constrained", prefix + ["baseline", "constraints"], ["slice.len() > 0"]),
            ("zero-baseline-goals", prefix + ["proofs", 0, "verified_goals"], 0),
            ("not-native-baseline", native + ["baseline"], False),
            ("native-failed", native + ["invocations", 0, "process", "returncode"], 1),
            ("native-zero-goals", native + ["invocations", 0, "verified_goals"], 0),
            ("native-wrong-target", native + ["invocations", 0, "function"], "contracts::scalar_domain"),
            ("native-timeout", native + ["invocations", 0, "process", "timed_out"], True),
            ("wrong-target", prefix + ["target", "name"], self.APIS[0]),
            ("wrong-target-line", prefix + ["target", "line"], 7),
            ("ignored-value", prefix + ["coverage", "ignored_dimensions"], ["return.Some"]),
        ):
            with self.subTest(case=case):
                self.check_case(
                    case, lambda project, k=keys, v=value: self.alter_report(project, k, v),
                )
        for phase in ("analyze", "replay"):
            self.check_case(
                f"{phase}-nonzero-exit", lambda project, p=phase:
                (project / f"logs/{self.GROUP}/completeness/{self.APIS[1]}/{p}.exit-code.txt").write_text("1\n"),
            )
            def duplicate(project, phase=phase):
                _, report = self.report(project, phase)
                self.alter_report(project, ["results"], report["results"] * 2, phase)
            self.check_case(f"{phase}-extra-target", duplicate)

    def test_actual_comparison_premises_harness_and_all_search_guards_are_checked(self):
        native = ["results", 0, "proofs", 0, "native"]
        for phase in ("analyze", "replay"):
            for case, key, value in (
                ("variant-only", "equal_fn_def", "(r1 is Some) == (r2 is Some)"),
                ("value-only", "equal_fn_def", "r1->Some_0 == r2->Some_0"),
                ("premise", "det_check_template", "requires false"),
            ):
                self.check_case(
                    f"{phase}-{case}", lambda project, p=phase, k=key, v=value:
                    self.alter_report(project, native + ["det_spec", k], v, p),
                )
            for guard in self.GUARDS:
                def constrain(project, phase=phase, guard=guard):
                    query = self.artifact(project, "query", phase)
                    query.write_text(query.read_text().replace(f"(not {guard}!)", f"{guard}!"))
                self.check_case(f"{phase}-{guard}", constrain)
            def extra_constraint(project, phase=phase):
                query = self.artifact(project, "query", phase)
                query.write_text(query.read_text() + "(assert false)\n")
            self.check_case(f"{phase}-extra-constraint", extra_constraint)
            def altered_harness(project, phase=phase):
                harness = self.artifact(project, "harness", phase)
                harness.write_text(harness.read_text().replace(
                    f"contracts::{self.APIS[1]}_post(slice, r2)",
                    f"contracts::{self.APIS[1]}_post(&[], r2)",
                ))
            self.check_case(f"{phase}-actual-harness", altered_harness)

    def test_effective_selectors_assistance_native_dependencies_and_replay_link_are_checked(self):
        for phase in ("analyze", "replay"):
            for case, keys, value in (
                ("selectors", ["selectors"], []),
                ("assistance", ["assistance"], {"mode": "model"}),
                ("toolchain", ["toolchain", "executable"], "/wrong/verus"),
            ):
                self.check_case(
                    f"{phase}-config-{case}", lambda project, p=phase, k=keys, v=value:
                    self.set_json(self.artifact(project, "effective-config.json", p), ["payload", *k], v),
                )
            def native_dependency(project, phase=phase):
                _, report = self.report(project, phase)
                path = Path(report["results"][0]["proofs"][0]["native"]["worktree"]) / "specs/slice/mod.rs"
                path.write_bytes(path.read_bytes() + b"\n")
            self.check_case(f"{phase}-native-dependency", native_dependency)
        self.check_case(
            "replay-parent", lambda project: self.set_json(
                self.artifact(project, "manifest.json", "replay"), ["payload", "parent_run"], "/wrong/run",
            ),
        )
        for case, edit in (
            ("replay-without-reexecute", lambda command: command.remove("--reexecute")),
            ("replay-wrong-run", lambda command: command.__setitem__(3, "/wrong/run")),
            ("replay-config-override", lambda command: command.extend(["--config", "specdet.toml"])),
        ):
            self.check_case(case, lambda project, edit=edit: self.alter_command(project, edit, "replay"))
        self.check_case(
            "analyze-wrong-selector",
            lambda project: self.alter_command(
                project, lambda command: command.__setitem__(7, "proofs/completeness/slice/inputs/*.rs"),
                "analyze",
            ),
        )

    def test_missing_duplicate_or_unreviewed_identities_leave_every_output_untouched(self):
        self.check_case(
            "missing-coverage", lambda project: (project / "inventory/coverage.tsv").unlink(),
        )
        for filename in ("apis.tsv", "coverage.tsv"):
            def duplicate(project, filename=filename):
                path = project / "inventory" / filename
                lines = path.read_bytes().splitlines(keepends=True)
                path.write_bytes(b"".join(lines + [lines[1]]))
            self.check_case("duplicate-" + filename, duplicate)
        def missing(project):
            for filename in ("apis.tsv", "coverage.tsv"):
                path = project / "inventory" / filename
                path.write_bytes(b"".join(
                    line for line in path.read_bytes().splitlines(keepends=True)
                    if not line.startswith(f"<[T]>::{self.APIS[1]}\t".encode())
                ))
        self.check_case("missing-endpoint-identity", missing)
        for case, before, after in (
            ("missing-issue", "issues/V-SLICE-PATTERN.md", ""),
            ("review-not-pending", "\tpending\t", "\tapproved\t"),
        ):
            def change(project, before=before, after=after):
                path = project / "inventory/coverage.tsv"
                path.write_text("".join(
                    line.replace(before, after) if line.startswith(f"<[T]>::{self.APIS[1]}\t") else line
                    for line in path.read_text().splitlines(keepends=True)
                ))
            self.check_case(case, change)

    def test_noncanonical_tsv_quoting_and_line_endings_are_preserved(self):
        with self.project("raw-tsv") as project:
            path = project / "inventory/coverage.tsv"
            raw = path.read_bytes()
            raw = raw.replace(b"\tpending\t", b'\t"pending"\t')
            raw = raw.replace(b"\tdeterministic\t", b'\t"deterministic"\t')
            raw = raw.replace(b"\n", b"\r\n")
            path.write_bytes(raw)
            self.invoke(project, "raw-tsv", [f"--{self.GROUP}"], self.APIS)
            after = path.read_bytes()
            self.assertEqual(raw.count(b"\r\n"), after.count(b"\r\n"))
            self.assertEqual(raw.count(b'\t"pending"\t'), after.count(b'\t"pending"\t'))
            self.assertEqual(raw.count(b'\t"deterministic"\t'), after.count(b'\t"deterministic"\t'))

    def test_external_scratch_keeps_temporary_projects_outside_reviewed_inputs(self):
        with tempfile.TemporaryDirectory(prefix=f"{self.GROUP}-review-scratch-") as directory:
            with mock.patch.dict(os.environ, {"TMPDIR": directory}):
                with self.project("external-scratch") as project:
                    self.assertTrue(project.is_relative_to(Path(directory)))
                    self.invoke(project, "external-scratch", [f"--{self.GROUP}"], self.APIS)


if __name__ == "__main__":
    unittest.main()
