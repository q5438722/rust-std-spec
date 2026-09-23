from contextlib import contextmanager
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
from unittest import mock

from scripts import export_completeness as export
import test_endpoint_export_cli as endpoint_tests
import test_mutable_endpoint_export_cli as mutable_endpoint_tests


ROOT = Path(__file__).resolve().parents[1]
APIS = export.MUTABLE_SPLITS
CHECKER_LOGS = Path(export.MUTABLE_SPLIT_CHECKER_LOGS)
SOURCE_LOGS = Path("logs/mutable-splits/correctness")
STATE_LOGS = Path(export.MUTABLE_SPLIT_STATE_LOGS)
COMPARISON_LOGS = Path("logs/mutable-splits-proposal/compiled-comparisons")
BEFORE = Path(export.MUTABLE_SPLIT_BEFORE)
DEPENDENCIES = export.MUTABLE_SPLIT_DEPENDENCIES
POST = export.MUTABLE_SPLIT_POST
STATE = export.MUTABLE_SPLIT_STATE
BINDING = export.MUTABLE_SPLIT_BINDING
LAST_SOURCE = "proofs/correctness/slice/split_last_mut.rs"
LAST_INPUT = "proofs/completeness/slice/inputs/split_last_mut.rs"


class MutableSplitExportCLI(unittest.TestCase):
    set_json = staticmethod(mutable_endpoint_tests.MutableEndpointExportCLI.set_json)
    table = staticmethod(endpoint_tests.EndpointExportCLI.table)

    @staticmethod
    def copy_project(project, foundation=False):
        def copy(path, relocate=False):
            source = ROOT / path
            destination = project / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if relocate:
                destination.write_text(source.read_text().replace(str(ROOT), str(project)))
            else:
                shutil.copyfile(source, destination)

        def compilation(logs, dependencies=(), source_run=False):
            copy(logs / ("command.json" if source_run else "result.json"), relocate=True)
            for path in (ROOT / logs).glob("*.rlib"):
                copy(path)
            for path in (ROOT / logs / "queries").glob("*.smt*"):
                copy(path)
            for path in dependencies:
                copy(logs / "inputs" / path)
            for name in (
                ("verus.log", "verus.stdout", "verus.stderr", "verus.exit-code.txt")
                if source_run else ("verus.log",)
            ):
                copy(logs / name)

        if foundation:
            endpoint_tests.EndpointExportCLI().copy_project(project, foundation=True)
        for path in (
            "scripts/export_completeness.py", "inventory/apis.tsv", *DEPENDENCIES, BINDING,
            *[BEFORE / path for path in (POST, STATE, BINDING, "inventory/coverage.tsv")],
            *[path for path in (ROOT / "proofs/completeness/slice").glob("*.rs")
              if path.stem not in APIS],
            *(ROOT / "proofs/completeness/slice/history").glob("*.rs"),
            *(ROOT / "proofs/correctness/slice").glob("*.rs"),
        ):
            copy(path)
        shutil.copyfile(ROOT / BEFORE / "inventory/coverage.tsv", project / "inventory/coverage.tsv")
        compilation(STATE_LOGS / "state", (STATE, POST))
        for api in APIS:
            source = f"proofs/correctness/slice/{api}.rs"
            analysis = f"proofs/completeness/slice/inputs/{api}.rs"
            for path in (
                source, analysis, BEFORE / source, BEFORE / analysis,
                f"proofs/correctness/slice/proposals/{api}.rs",
                f"logs/mutable-splits-proposal/correctness/initial/original/{api}/verus.log",
            ):
                copy(path)
            compilation(SOURCE_LOGS / api, (source, POST), source_run=True)
            compilation(STATE_LOGS / api, (analysis, STATE, POST))
            compilation(COMPARISON_LOGS / api)
            for phase in ("analyze", "replay"):
                logs = CHECKER_LOGS / api
                report = json.loads((ROOT / logs / f"{phase}.json").read_text())
                run = Path(report["run_dir"])
                for path in (analysis, *DEPENDENCIES):
                    copy(run / "workspace" / path)
                for name in ("manifest.json", "effective-config.json"):
                    copy(run / name, relocate=True)
                result = report["results"][0]
                proof = result["proofs"][0]
                native = proof["native"]
                attempt = Path(proof["artifact"])
                for path in (
                    result["baseline"]["artifact"], native["harness"], native["source"],
                    *[Path(native["worktree"]) / dependency for dependency in DEPENDENCIES],
                    Path(native["logs"]) / "root.smt2",
                    Path(native["logs"]) / "root.smt_transcript",
                    attempt / "verifier/stdout.txt", attempt / "verifier/stderr.txt",
                ):
                    copy(path)
                for path in (
                    attempt / "query/baseline.json", attempt / "verifier/process.json",
                    logs / f"{phase}.json", logs / f"{phase}-command.json", logs / f"{phase}.stderr",
                ):
                    copy(path, relocate=True)
            (project / f"proofs/completeness/slice/{api}.rs").unlink(missing_ok=True)

    @contextmanager
    def project(self, case, foundation=False):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/mutable-splits/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix=f"{case}-") as directory:
            project = Path(directory) / "project"
            self.copy_project(project, foundation)
            yield project

    def invoke(self, project, case, arguments, selected=(), expected_code=0, default=False):
        def contents():
            return {
                str(path.relative_to(project)): path.read_bytes()
                for path in project.rglob("*") if path.is_file()
            }

        def directories():
            return {str(path.relative_to(project)) for path in project.rglob("*") if path.is_dir()}

        before, dirs_before = contents(), directories()
        command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
        result = subprocess.run(
            command, cwd=project, capture_output=True, text=True, timeout=30,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(project.parent)),
        )
        after, dirs_after = contents(), directories()
        changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
        log_root = os.environ.get("MUTABLE_SPLIT_EXPORT_TEST_LOG_DIR")
        if log_root:
            log = ROOT / log_root / "cli" / case
            log.mkdir(parents=True, exist_ok=False)
            (log / "command.txt").write_text(
                f"cd {shlex.quote(str(project))} && PYTHONDONTWRITEBYTECODE=1 "
                f"TMPDIR={shlex.quote(str(project.parent))} {shlex.join(command)}\n"
            )
            (log / "stdout.log").write_text(result.stdout)
            (log / "stderr.log").write_text(result.stderr)
            (log / "result.json").write_text(json.dumps({
                "returncode": result.returncode, "expected_returncode": expected_code,
                "selected": selected, "default_export": default, "changed_files": changed,
                "preexisting_files": len(before), "new_directories": sorted(dirs_after - dirs_before),
            }, indent=2) + "\n")
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        self.assertEqual(dirs_before, dirs_after)
        if expected_code:
            self.assertEqual(before, after)
            return
        allowed = {"inventory/coverage.tsv", *[
            f"proofs/completeness/slice/{api}.rs"
            for api in (("len", "is_empty") if default else selected)
        ]}
        self.assertLessEqual(set(changed), allowed)
        self.assertEqual(before.keys() - allowed, after.keys() - allowed)
        for path in before.keys() - allowed:
            self.assertEqual(before[path], after[path], path)
        fields, rows, records = self.table(before["inventory/coverage.tsv"])
        new_fields, new_rows, new_records = self.table(after["inventory/coverage.tsv"])
        self.assertEqual(fields, new_fields)
        self.assertEqual(list(rows), list(new_rows))
        self.assertEqual(len(rows), 331)
        self.assertEqual(records["header"], new_records["header"])
        selected_ids = {f"<[T]>::{api}" for api in (export.APIS if default else selected)}
        for identity in rows:
            if identity not in selected_ids:
                self.assertEqual(records[identity], new_records[identity], identity)
            else:
                for field in fields[:4]:
                    self.assertEqual(rows[identity][field], new_rows[identity][field])
        for api in selected:
            row = new_rows[f"<[T]>::{api}"]
            self.assertEqual(row["specification"], f"{POST}::{api}_post")
            self.assertEqual(row["correctness_proof"], f"proofs/correctness/slice/{api}.rs")
            self.assertEqual(row["correctness_log"], f"{SOURCE_LOGS}/{api}/verus.stdout")
            self.assertEqual(row["correctness_target_functions"], "1")
            self.assertIn("--compile --no-cheating", row["correctness_command"])
            self.assertIn("1 target + 0 imported proof functions", row["correctness_result"])
            self.assertIn("length/index-update/split_at_mut contracts and Seq view", row["correctness_result"])
            self.assertIn("final implementation review pending", row["correctness_result"])
            self.assertEqual(row["completeness_checked_goals"], "1")
            for observation in (
                "entire initial remainder Seq<T>", "entire final owner Seq<T>",
                "caller element/remainder contents independent", "all 19 search guards off",
                "9 compiled comparison functions are not source targets",
                "unchanged analysis/reexecution retained",
            ):
                self.assertIn(observation, row["completeness_result"])
            self.assertEqual(row["issues"], "issues/V-SLICE-PATTERN.md;issues/S-MUT-RETURN.md")
            self.assertEqual(row["independent_review"], "pending")
            self.assertEqual(row["mission_scope"], "slice_mutable_splits")
            text = after[row["completeness_proof"]].decode()
            _, report = self.report(project, api=api)
            original = Path(report["results"][0]["proofs"][0]["native"]["harness"]).read_text()
            self.assertEqual(
                "\n".join(text.splitlines()[3:]) + "\n",
                original.replace('#[path = "../mutable_splits_state.rs"]',
                                 '#[path = "mutable_splits_state.rs"]', 1),
            )
        self.assertIn(
            "Exported 2 native completeness harnesses" if default else
            f"Exported {len(selected)} checked mutable split proofs", result.stdout,
        )

    def check_case(self, case, change=None, arguments=None, selected=(), expected_code=1):
        with self.subTest(case=case), self.project(case) as project:
            if change is not None:
                change(project)
            self.invoke(
                project, case, ["--mutable-splits"] if arguments is None else arguments,
                selected, expected_code,
            )

    @staticmethod
    def report(project, phase="analyze", api="split_last_mut"):
        path = project / CHECKER_LOGS / api / f"{phase}.json"
        return path, json.loads(path.read_text())

    @classmethod
    def alter_report(cls, project, keys, value, phase="analyze"):
        cls.set_json(project / CHECKER_LOGS / "split_last_mut" / f"{phase}.json", keys, value)

    @classmethod
    def location(cls, project, kind, phase="analyze"):
        _, report = cls.report(project, phase)
        result = report["results"][0]
        if kind == "query":
            return Path(result["baseline"]["artifact"])
        if kind == "attempt":
            return Path(result["proofs"][0]["artifact"])
        if kind in ("harness", "source", "worktree", "logs"):
            return Path(result["proofs"][0]["native"][kind])
        return Path(report["run_dir"]) / kind

    @classmethod
    def alter_command(cls, project, edit, phase="source"):
        path = (
            project / SOURCE_LOGS / "split_last_mut/command.json" if phase == "source" else
            project / CHECKER_LOGS / "split_last_mut" / f"{phase}-command.json"
        )
        data = json.loads(path.read_text())
        edit(data["command"])
        path.write_text(json.dumps(data) + "\n")

    def test_selections_duplicates_invalid_names_and_exclusive_groups(self):
        flag = "--mutable-splits"
        for case, arguments, selected, code in (
            ("first", [flag, APIS[0]], APIS[:1], 0),
            ("last", [flag, APIS[1]], APIS[1:], 0),
            ("both", [flag], APIS, 0),
            ("explicit-both", [flag, *APIS], APIS, 0),
            ("reverse", [flag, *APIS[::-1]], APIS[::-1], 0),
            ("wrong", [flag, "split_first"], (), 2),
            ("empty", [flag, ""], (), 2),
            ("duplicate-first", [flag, APIS[0], APIS[0]], (), 2),
            ("duplicate-last", [flag, APIS[1], APIS[1]], (), 2),
            ("duplicate-both", [flag, *APIS, APIS[0]], (), 2),
            *[(f"mixed-{other}", [flag, "--" + other], (), 2)
              for other in ("defaults", "singletons", "ascii-case", "endpoints", "splits", "mutable-endpoints")],
        ):
            self.check_case(case, arguments=arguments, selected=selected, expected_code=code)

    def test_partial_and_repeated_exports_are_byte_identical(self):
        with self.project("partial") as project:
            self.invoke(project, "partial-first", ["--mutable-splits", APIS[0]], APIS[:1])
            self.assertFalse((project / f"proofs/completeness/slice/{APIS[1]}.rs").exists())
            self.invoke(project, "partial-last", ["--mutable-splits", APIS[1]], APIS[1:])
            coverage = (project / "inventory/coverage.tsv").read_bytes()
            for case, arguments in (
                ("partial-repeat", ["--mutable-splits"]),
                ("partial-repeat-reverse", ["--mutable-splits", *APIS[::-1]]),
            ):
                self.invoke(project, case, arguments, APIS)
                self.assertEqual(coverage, (project / "inventory/coverage.tsv").read_bytes())
            (project / SOURCE_LOGS / APIS[1] / "verus.exit-code.txt").write_text("1\n")
            self.invoke(project, "partial-rejected-repeat", ["--mutable-splits"], expected_code=1)

    def test_unselected_sources_and_evidence_are_not_required(self):
        for selected, unselected in (APIS, APIS[::-1]):
            def remove(project, unselected=unselected):
                for logs in (SOURCE_LOGS, CHECKER_LOGS, STATE_LOGS, COMPARISON_LOGS):
                    shutil.rmtree(project / logs / unselected)
                (project / f"proofs/correctness/slice/{unselected}.rs").unlink()
                (project / f"proofs/completeness/slice/inputs/{unselected}.rs").unlink()
                if unselected == "split_last_mut":
                    (project / BINDING).unlink()
            self.check_case(
                f"only-{selected}-evidence", remove, ["--mutable-splits", selected], (selected,), 0,
            )

    def test_default_export_preserves_partial_and_complete_mutable_split_records(self):
        with self.project("default", foundation=True) as project:
            self.invoke(project, "default-prepare", [], default=True)
            for api in APIS:
                self.invoke(project, f"default-select-{api}", ["--mutable-splits", api], (api,))
                before = (project / "inventory/coverage.tsv").read_bytes()
                self.invoke(project, f"default-preserve-{api}", [], default=True)
                self.assertEqual(before, (project / "inventory/coverage.tsv").read_bytes())
            shutil.rmtree(project / CHECKER_LOGS)
            shutil.rmtree(project / SOURCE_LOGS)
            self.invoke(project, "default-keeps-unselected-evidence", [], default=True)
            self.assertEqual(before, (project / "inventory/coverage.tsv").read_bytes())

    def test_source_failures_do_not_partially_export_the_other_selected_api(self):
        for case, name, value in (
            ("exit", "verus.exit-code.txt", "1\n"),
            ("failure", "verus.stdout", "verification results:: 0 verified, 1 errors\n"),
            ("zero", "verus.stdout", "verification results:: 0 verified, 0 errors\n"),
            ("imported-only", "verus.stdout", "verification results:: 7 verified, 0 errors\n"),
            ("comparison-count", "verus.stdout", "verification results:: 9 verified, 0 errors\n"),
            ("partial", "verus.stdout", "verification results:: 1 verified, 0 errors (partial verification)\n"),
            ("stderr", "verus.stderr", "error: failed\n"),
            ("combined-log", "verus.log", "verification results:: 0 verified, 0 errors\n"),
            ("empty-library", "libslice_split_last_mut.rlib", ""),
            ("empty-query", "queries/root.smt2", ""),
            ("unknown", "queries/root.smt_transcript", "(check-sat)\nunknown\n"),
            ("sat", "queries/root.smt_transcript", "(check-sat)\nsat\n"),
            ("empty-transcript", "queries/root.smt_transcript", ""),
            ("imported-proof", "queries/contracts.smt2", ";; Function-Def imported\n"),
        ):
            self.check_case(
                "source-" + case,
                lambda project, n=name, v=value: (project / SOURCE_LOGS / "split_last_mut" / n).write_text(v),
            )
        for name in ("command.json", "libslice_split_last_mut.rlib", "queries/root.smt2",
                     "queries/root.smt_transcript", "verus.exit-code.txt"):
            self.check_case(
                "source-missing-" + name.replace("/", "-"),
                lambda project, n=name: (project / SOURCE_LOGS / "split_last_mut" / n).unlink(),
            )
        for case, edit in (
            ("no-compile", lambda command: command.remove("--compile")),
            ("no-no-cheating", lambda command: command.remove("--no-cheating")),
            ("wrong-source", lambda command: command.__setitem__(1, STATE)),
            ("wrong-verus", lambda command: command.__setitem__(0, "/wrong/verus")),
            ("wrong-crate", lambda command: command.__setitem__(5, "state")),
            ("verify-root", lambda command: command.extend(["--verify-root"])),
            ("wrong-thread-count", lambda command: command.__setitem__(9, "2")),
        ):
            self.check_case("source-command-" + case, lambda project, e=edit: self.alter_command(project, e))
        self.check_case(
            "source-receipt-failure", lambda project: self.set_json(
                project / SOURCE_LOGS / "split_last_mut/command.json", ["returncode"], 1,
            ),
        )
        def wrong_target(project):
            path = project / SOURCE_LOGS / "split_last_mut/queries/root.smt2"
            path.write_text(path.read_text().replace(
                ";; Function-Def slice_split_last_mut::split_last_mut",
                ";; Function-Def slice_split_last_mut::contracts::helper",
            ))
        self.check_case("source-wrong-obligation", wrong_target)

    def test_current_compiled_and_frozen_inputs_must_match_by_content(self):
        for location in ("current", "compiled"):
            for source in (LAST_SOURCE, POST):
                def stale(project, source=source, location=location):
                    base = project if location == "current" else project / SOURCE_LOGS / "split_last_mut/inputs"
                    path = base / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(f"stale-source-{location}-{Path(source).name}", stale)
        for location in ("current", "analyze", "replay", "native-analyze", "native-replay"):
            for source in (LAST_INPUT, *DEPENDENCIES):
                if location.startswith("native-") and source == LAST_INPUT:
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
                self.check_case(f"stale-checker-{location}-{Path(source).name}", stale)
        for label, logs, dependencies in (
            ("state", STATE_LOGS / "state", (STATE, POST)),
            ("adapter", STATE_LOGS / APIS[1], (LAST_INPUT, STATE, POST)),
            ("before", BEFORE, (LAST_INPUT, STATE, POST, BINDING, LAST_SOURCE)),
        ):
            for source in dependencies:
                def stale(project, source=source, logs=logs, label=label):
                    path = project / logs / ("" if label == "before" else "inputs") / source
                    path.write_bytes(path.read_bytes() + b"\n")
                self.check_case(f"stale-{label}-{source.replace('/', '-')}", stale)

    def test_only_the_permitted_source_body_and_unchanged_binding_can_export(self):
        for case, before, after in (
            ("ghost-removed", "            vstd::slice::mut_ref_slice_len_eq(&init);\n", ""),
            ("swapped-return", "Some((&mut last[0], init))", "Some((&mut init[0], last))"),
            ("target-call", "Some((&mut last[0], init))", "slice.split_last_mut()"),
            ("contract-final-owner", "final(slice)@", "old(slice)@"),
            ("header", "body:262-264.", "body:262-263."),
            ("import", "../../../specs/slice/mutable_splits_post.rs", "../../../specs/slice/mod.rs"),
        ):
            def change(project, before=before, after=after):
                for base in (project, project / SOURCE_LOGS / "split_last_mut/inputs"):
                    path = base / LAST_SOURCE
                    self.assertIn(before, path.read_text())
                    path.write_text(path.read_text().replace(before, after, 1))
            self.check_case("candidate-" + case, change)
        for source in (LAST_SOURCE, POST, STATE, BINDING):
            self.check_case("candidate-missing-" + Path(source).name, lambda project, p=source: (project / p).unlink())
        for case, before, after in (
            ("duplicate-first", "<[T]>::split_last_mut", "<[T]>::split_first_mut"),
            ("wrong-post", "post::split_last_mut_post", "post::split_first_mut_post"),
            ("frozen-element", "*final(value)", "*value"),
            ("frozen-remainder", "final(remainder)@", "remainder@"),
            ("swapped-order", "(*value, remainder@)", "(remainder@, *value)"),
            ("missing-unwind", "    no_unwind\n", ""),
        ):
            def change(project, before=before, after=after):
                path = project / BINDING
                self.assertIn(before, path.read_text())
                path.write_text(path.read_text().replace(before, after, 1))
            self.check_case("binding-" + case, change)

    def test_state_adapter_and_comparison_compilations_are_real_nonzero_evidence(self):
        for label, logs, crate in (
            ("state", STATE_LOGS / "state", "state"),
            ("adapter", STATE_LOGS / APIS[1], APIS[1]),
            ("comparison", COMPARISON_LOGS / APIS[1], f"{APIS[1]}_comparison"),
        ):
            for case, name, text in (
                ("zero", "verus.log", "verification results:: 0 verified, 0 errors\n"),
                ("failure", "verus.log", "verification results:: 7 verified, 1 errors\n"),
                ("wrong-count", "verus.log", "verification results:: 1 verified, 0 errors\n"),
                ("empty-library", f"lib{crate}.rlib", ""),
                ("empty-query", "queries/root.smt2", ""),
                ("unknown", "queries/root.smt_transcript", "(check-sat)\nunknown\n"),
            ):
                self.check_case(
                    f"{label}-{case}",
                    lambda project, d=logs, n=name, t=text: (project / d / n).write_text(t),
                )
            for name in ("result.json", f"lib{crate}.rlib", "queries/root.smt_transcript"):
                self.check_case(
                    f"{label}-missing-{name.replace('/', '-')}",
                    lambda project, d=logs, n=name: (project / d / n).unlink(),
                )
            self.check_case(
                f"{label}-nonzero-exit",
                lambda project, d=logs: self.set_json(project / d / "result.json", ["exit_code"], 1),
            )
            for flag in ("--compile", *(("--no-cheating",) if label != "comparison" else ())):
                def remove(project, logs=logs, flag=flag):
                    path = project / logs / "result.json"
                    data = json.loads(path.read_text())
                    data["command"].remove(flag)
                    path.write_text(json.dumps(data) + "\n")
                self.check_case(f"{label}-without-{flag[2:]}", remove)
        self.check_case(
            "comparison-wrong-source", lambda project: self.set_json(
                project / COMPARISON_LOGS / APIS[1] / "result.json", ["command", 1], LAST_SOURCE,
            ),
        )

    def test_checker_failures_unknown_and_zero_targets_or_generated_goals_are_rejected(self):
        prefix = ["results", 0]
        native = prefix + ["proofs", 0, "native"]
        for phase in ("analyze", "replay"):
            for case, keys, value in (
                ("exit", ["exit_code"], 1),
                ("failed", ["status"], "failed"),
                ("unknown", ["counts"], {"unknown": 1}),
                ("diagnostic", ["diagnostics"], [{"message": "failed"}]),
                ("no-targets", ["targets"], []),
                ("no-results", ["results"], []),
                ("target-failed", prefix + ["status"], "failed"),
                ("target-unknown", prefix + ["verdict"], "unknown"),
                ("target-diagnostic", prefix + ["diagnostics"], [{"message": "failed"}]),
                ("baseline-unknown", prefix + ["baseline", "status"], "unknown"),
                ("baseline-sat", prefix + ["baseline", "status"], "sat"),
                ("baseline-constrained", prefix + ["baseline", "constraints"], ["nonempty"]),
                ("missing-baseline", prefix + ["baseline"], None),
                ("no-proofs", prefix + ["proofs"], []),
                ("zero-goals", prefix + ["proofs", 0, "verified_goals"], 0),
                ("extra-goals", prefix + ["proofs", 0, "verified_goals"], 2),
                ("proof-failed", prefix + ["proofs", 0, "status"], "failed"),
                ("not-baseline", native + ["baseline"], False),
                ("wrong-target", prefix + ["target", "name"], "split_first_mut_observation"),
                ("wrong-line", prefix + ["target", "line"], 8),
                ("ignored-remainder", prefix + ["coverage", "ignored_dimensions"], ["return.0.Some.1"]),
                ("ignored-owner", prefix + ["coverage", "ignored_dimensions"], ["return.1"]),
                ("native-failed", native + ["invocations", 0, "process", "returncode"], 1),
                ("native-zero", native + ["invocations", 0, "verified_goals"], 0),
                ("native-timeout", native + ["invocations", 0, "process", "timed_out"], True),
                ("native-wrong-target", native + ["invocations", 0, "function"], "state::caller_domain"),
                ("native-wrong-source", native + ["source"], LAST_INPUT),
                ("native-no-invocations", native + ["invocations"], []),
            ):
                self.check_case(
                    f"{phase}-{case}",
                    lambda project, k=keys, v=value, p=phase: self.alter_report(project, k, v, p),
                )
            for key in ("results", "proofs"):
                def duplicate(project, phase=phase, key=key):
                    _, report = self.report(project, phase)
                    keys = ["results"] if key == "results" else prefix + ["proofs"]
                    values = report["results"] if key == "results" else report["results"][0]["proofs"]
                    self.alter_report(project, keys, values * 2, phase)
                self.check_case(f"{phase}-duplicate-{key}", duplicate)

    def test_comparison_includes_variant_ordered_initial_pair_and_entire_final_owner(self):
        for phase in ("analyze", "replay"):
            for case, before, after in (
                ("variant", "(((r1)@.0 is Some) == ((r2)@.0 is Some))", "true"),
                ("element", "((r1)@.0->Some_0.0 == (r2)@.0->Some_0.0)", "true"),
                ("initial-remainder", "((r1)@.0->Some_0.1 =~= (r2)@.0->Some_0.1)", "true"),
                ("final-owner", "((r1)@.1 =~= (r2)@.1)", "true"),
                ("remainder-length", "((r1)@.0->Some_0.1 =~= (r2)@.0->Some_0.1)",
                 "((r1)@.0->Some_0.1.len() == (r2)@.0->Some_0.1.len())"),
                ("owner-length", "((r1)@.1 =~= (r2)@.1)", "((r1)@.1.len() == (r2)@.1.len())"),
                ("swapped-order", "(r1)@.0->Some_0.0 == (r2)@.0->Some_0.0",
                 "(r1)@.0->Some_0.1 == (r2)@.0->Some_0.0"),
            ):
                def change(project, phase=phase, before=before, after=after):
                    _, report = self.report(project, phase)
                    text = report["results"][0]["proofs"][0]["native"]["det_spec"]["equal_fn_def"]
                    self.assertIn(before, text)
                    self.alter_report(
                        project, ["results", 0, "proofs", 0, "native", "det_spec", "equal_fn_def"],
                        text.replace(before, after, 1), phase,
                    )
                self.check_case(f"{phase}-comparison-{case}", change)
            for case, before, after in (
                ("frozen-element", "caller_final@, r2@", "Some((input_initial@[0], caller_final@.unwrap().1)), r2@"),
                ("frozen-remainder", "caller_final@, r2@", "Some((caller_final@.unwrap().0, input_initial@)), r2@"),
                ("owner-preinput", "caller_final: Ghost<Option<(T, Seq<T>)>>,",
                 "caller_final: Ghost<Option<(T, Seq<T>)>>, final_owner: Ghost<Seq<T>>,"),
                ("same-result", "caller_final@, r2@", "caller_final@, r1@"),
                ("constrained-writes", "written_remainder.len() + 1 == input_initial@.len()",
                 "written_remainder == input_initial@"),
            ):
                def change(project, phase=phase, before=before, after=after):
                    _, report = self.report(project, phase)
                    text = report["results"][0]["proofs"][0]["native"]["det_spec"]["det_check_template"]
                    self.assertIn(before, text)
                    self.alter_report(
                        project, ["results", 0, "proofs", 0, "native", "det_spec", "det_check_template"],
                        text.replace(before, after, 1), phase,
                    )
                self.check_case(f"{phase}-premise-{case}", change)
            for kind in ("harness", "source"):
                def change(project, phase=phase, kind=kind):
                    path = self.location(project, kind, phase)
                    path.write_text(path.read_text().replace("caller_final@, r2@", "caller_final@, r1@", 1))
                self.check_case(f"{phase}-actual-{kind}", change)

    def test_written_components_cannot_be_frozen_or_swapped_in_the_analysis_body(self):
        for case, replacement in (
            ("frozen-element", "written_remainder + seq![input_initial@[0]]"),
            ("frozen-remainder", "input_initial@.subrange(0, input_initial@.len() - 1) + seq![written]"),
            ("swapped-order", "seq![written] + written_remainder"),
        ):
            def change(project, replacement=replacement):
                paths = {
                    project / LAST_INPUT,
                    project / STATE_LOGS / APIS[1] / "inputs" / LAST_INPUT,
                    *[self.location(project, "workspace", phase) / LAST_INPUT
                      for phase in ("analyze", "replay")],
                    *[self.location(project, kind, phase)
                      for phase in ("analyze", "replay") for kind in ("harness", "source")],
                }
                for path in paths:
                    text = path.read_text()
                    self.assertIn("written_remainder + seq![written]", text)
                    path.write_text(text.replace("written_remainder + seq![written]", replacement, 1))
            self.check_case("analysis-body-" + case, change)

    def test_all_nineteen_original_query_guards_and_native_obligations_are_checked(self):
        for phase in ("analyze", "replay"):
            query = self.location(ROOT, "query", phase).read_text()
            guards = re.findall(r"^\(declare-fun (g_\S+)! \(\) Bool\)$", query, re.MULTILINE)
            self.assertEqual(len(guards), 19)
            for guard in guards:
                def constrain(project, phase=phase, guard=guard):
                    path = self.location(project, "query", phase)
                    text = path.read_text()
                    self.assertIn(f"(not {guard}!)", text)
                    path.write_text(text.replace(f"(not {guard}!)", f"{guard}!", 1))
                self.check_case(f"{phase}-enabled-{guard}", constrain)
            for case, extra in (
                ("extra-constraint", "(assert false)\n"),
                ("extra-guard", "(declare-fun g_extra! () Bool)\n"),
                ("extra-check", "(check-sat)\n"),
            ):
                def change(project, phase=phase, extra=extra):
                    path = self.location(project, "query", phase)
                    path.write_text(path.read_text() + extra)
                self.check_case(f"{phase}-query-{case}", change)
            for name, text in (
                ("root.smt2", ""), ("root.smt_transcript", "(check-sat)\nunknown\n"),
            ):
                self.check_case(
                    f"{phase}-native-{name}",
                    lambda project, p=phase, n=name, t=text: (self.location(project, "logs", p) / n).write_text(t),
                )
            for case, keys, value in (
                ("unknown", ["evidence", "status"], "unknown"),
                ("wrong-source", ["source_transcript"], "/wrong/query"),
                ("enabled-guard", ["guard_assignments", "g_neq_tuple"], True),
            ):
                self.check_case(
                    f"{phase}-baseline-artifact-{case}",
                    lambda project, p=phase, k=keys, v=value: self.set_json(
                        self.location(project, "attempt", p) / "query/baseline.json", ["payload", *k], v,
                    ),
                )
        def wrong_target(project):
            for phase in ("analyze", "replay"):
                _, report = self.report(project, phase, APIS[0])
                query = Path(report["results"][0]["baseline"]["artifact"])
                self.location(project, "query", phase).write_bytes(query.read_bytes())
        self.check_case("both-phases-wrong-original-target", wrong_target)
        def extra_constraint(project):
            for phase in ("analyze", "replay"):
                path = self.location(project, "query", phase)
                path.write_text(path.read_text() + "(assert false)\n")
        self.check_case("both-phases-extra-original-constraint", extra_constraint)

    def test_selectors_reexecution_and_actual_process_receipts_cannot_be_replaced(self):
        for phase in ("analyze", "replay"):
            for case, keys, value in (
                ("selector", ["selectors"], []),
                ("assistance", ["assistance"], {"mode": "live"}),
                ("wrong-verus", ["toolchain", "executable"], "/wrong/verus"),
                ("partial-verification", ["toolchain", "extra_args"], ["--verify-root"]),
                ("extra-build-flags", ["build", "extra_args"], ["--crate-type", "lib", "--compile"]),
            ):
                self.check_case(
                    f"{phase}-config-{case}", lambda project, p=phase, k=keys, v=value: self.set_json(
                        self.location(project, "effective-config.json", p), ["payload", *k], v,
                    ),
                )
            self.check_case(
                f"{phase}-command-exit", lambda project, p=phase: self.set_json(
                    project / CHECKER_LOGS / APIS[1] / f"{p}-command.json", ["returncode"], 1,
                ),
            )
            for name in ("stdout.txt", "stderr.txt"):
                self.check_case(
                    f"{phase}-process-{name}", lambda project, p=phase, n=name:
                    (self.location(project, "attempt", p) / "verifier" / n).write_text("wrong execution\n"),
                )
            self.check_case(
                f"{phase}-process-receipt", lambda project, p=phase: self.set_json(
                    self.location(project, "attempt", p) / "verifier/process.json",
                    ["payload", "returncode"], 1,
                ),
            )
        for case, edit in (
            ("no-reexecute", lambda command: command.remove("--reexecute")),
            ("wrong-run", lambda command: command.__setitem__(3, "/wrong/run")),
            ("config-override", lambda command: command.extend(["--config", "specdet.toml"])),
        ):
            self.check_case(f"replay-{case}", lambda project, e=edit: self.alter_command(project, e, "replay"))
        self.check_case(
            "analyze-wrong-selector", lambda project: self.alter_command(
                project, lambda command: command.__setitem__(command.index("--target") + 1, "*"), "analyze",
            ),
        )
        self.check_case(
            "replay-wrong-parent", lambda project: self.set_json(
                self.location(project, "manifest.json", "replay"), ["payload", "parent_run"], "/wrong/run",
            ),
        )

    def test_missing_duplicate_or_invalid_records_and_existing_proofs_are_not_changed(self):
        self.check_case("no-coverage", lambda project: (project / "inventory/coverage.tsv").unlink())
        for name in ("apis.tsv", "coverage.tsv"):
            def duplicate(project, name=name):
                path = project / "inventory" / name
                lines = path.read_bytes().splitlines(keepends=True)
                path.write_bytes(b"".join(lines + [lines[1]]))
            self.check_case("duplicate-" + name, duplicate)
        def missing(project):
            for name in ("apis.tsv", "coverage.tsv"):
                path = project / "inventory" / name
                path.write_bytes(b"".join(
                    line for line in path.read_bytes().splitlines(keepends=True)
                    if not line.startswith(b"<[T]>::split_last_mut\t")
                ))
        self.check_case("missing-selected-identity", missing)
        def reviewed(project):
            path = project / "inventory/coverage.tsv"
            path.write_bytes(b"".join(
                line.replace(b"\tnot_evaluated_in_this_mission\t", b"\tapproved\t")
                if line.startswith(b"<[T]>::split_last_mut\t") else line
                for line in path.read_bytes().splitlines(keepends=True)
            ))
        self.check_case("unexpected-independent-review", reviewed)
        self.check_case(
            "different-existing-proof",
            lambda project: (project / "proofs/completeness/slice/split_last_mut.rs").write_text("// other work\n"),
        )

    def test_raw_unselected_lines_and_source_metadata_cells_are_preserved(self):
        with self.project("raw-tsv") as project:
            path = project / "inventory/coverage.tsv"
            raw = path.read_bytes().replace(b"\tpending\t", b'\t"pending"\t')
            raw = raw.replace(b"\tmissing\t", b'\t"missing"\t').replace(b"\n", b"\r\n")
            path.write_bytes(raw)
            self.invoke(project, "raw-tsv", ["--mutable-splits"], APIS)
            self.assertEqual(raw.count(b"\r\n"), path.read_bytes().count(b"\r\n"))
            self.assertEqual(raw.count(b'\t"missing"\t'), path.read_bytes().count(b'\t"missing"\t'))

    def test_external_scratch_respects_tmpdir(self):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/mutable-splits/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix="external-scratch-") as directory:
            with mock.patch.dict(os.environ, {"TMPDIR": directory}):
                with self.project("external") as project:
                    self.assertTrue(project.is_relative_to(Path(directory)))
                    self.invoke(project, "external", ["--mutable-splits"], APIS)


if __name__ == "__main__":
    unittest.main()
