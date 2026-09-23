from contextlib import contextmanager
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts import export_completeness as export
import test_endpoint_export_cli as endpoint_tests


ROOT = Path(__file__).resolve().parents[1]
APIS = export.SPLIT_OFF_ENDPOINTS
BEFORE = Path(export.SPLIT_OFF_BEFORE)
CHECKER_LOGS = Path(export.SPLIT_OFF_CHECKER_LOGS)
POST = export.SPLIT_OFF_POST
STATE = export.SPLIT_OFF_STATE
BINDING = export.SPLIT_OFF_BINDING
LAST_SOURCE = "proofs/correctness/slice/split_off_last.rs"
LAST_INPUT = "proofs/completeness/slice/inputs/split_off_last.rs"
LAST_LOGS = Path(export.SPLIT_OFF_SOURCE_LOGS[APIS[1]])


class SplitOffExportCLI(unittest.TestCase):
    table = staticmethod(endpoint_tests.EndpointExportCLI.table)

    @staticmethod
    def copy_project(project):
        def copy(path, relocate=False):
            source = ROOT / path
            destination = project / source.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if relocate:
                destination.write_text(source.read_text().replace(str(ROOT), str(project)))
            else:
                shutil.copyfile(source, destination)

        def compilation(logs, dependencies=(), text_receipt=False):
            name = "command.txt" if text_receipt else "command.json"
            copy(logs / name, relocate=True)
            if text_receipt:
                copy(logs / "exit-code.txt")
                command = shlex.split((ROOT / logs / name).read_text())
            else:
                command = json.loads((ROOT / logs / name).read_text())["command"]
            copy(command[-1])
            copy(logs / "verus.log")
            for path in (ROOT / logs / "queries").glob("*.smt*"):
                copy(path)
            for path in dependencies:
                copy(logs / "source" / path)

        for path in (
            "scripts/export_completeness.py", "inventory/apis.tsv",
            *export.SPLIT_OFF_DEPENDENCIES, STATE, BINDING,
            "proofs/correctness/slice/split_last.rs",
            *[BEFORE / path for path in (
                POST, STATE, BINDING, "specs/slice/mod.rs",
                "proofs/correctness/slice/split_last.rs",
            )],
            *(ROOT / BEFORE / "proofs/completeness/slice").glob("*.rs"),
        ):
            copy(path)
        for path in (ROOT / BEFORE / "proofs/completeness/slice").glob("*.rs"):
            destination = project / path.relative_to(ROOT / BEFORE)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
        shutil.copyfile(ROOT / BEFORE / "inventory/coverage.tsv", project / "inventory/coverage.tsv")
        compilation(Path("logs/split-off-endpoints/value-state/state"), (STATE, POST))
        for api in APIS:
            source = f"proofs/correctness/slice/{api}.rs"
            analysis = f"proofs/completeness/slice/inputs/{api}.rs"
            for path in (source, analysis, BEFORE / source, BEFORE / analysis):
                copy(path)
            dependencies = [source, POST]
            if api == "split_off_last":
                dependencies += ["proofs/correctness/slice/split_last.rs", "specs/slice/mod.rs"]
            compilation(Path(export.SPLIT_OFF_SOURCE_LOGS[api]), dependencies, text_receipt=True)
            compilation(Path("logs/split-off-endpoints/compiled-comparisons") / api)
            for phase in ("analyze", "replay"):
                logs = CHECKER_LOGS / api
                report = json.loads((ROOT / logs / f"{phase}.json").read_text())
                run = Path(report["run_dir"])
                result = report["results"][0]
                native = result["proofs"][0]["native"]
                attempt = Path(result["proofs"][0]["artifact"])
                for path in (analysis, *export.SPLIT_OFF_DEPENDENCIES):
                    copy(run / "workspace" / path)
                for path in (
                    result["baseline"]["artifact"], native["harness"], native["source"],
                    *[Path(native["worktree"]) / path for path in export.SPLIT_OFF_DEPENDENCIES],
                    Path(native["logs"]) / "root.smt2", Path(native["logs"]) / "root.smt_transcript",
                    attempt / "verifier/stdout.txt", attempt / "verifier/stderr.txt",
                ):
                    copy(path)
                for path in (
                    run / "manifest.json", run / "effective-config.json",
                    attempt / "query/baseline.json", attempt / "verifier/process.json",
                    logs / f"{phase}.json", logs / f"{phase}-command.json", logs / f"{phase}.stderr",
                ):
                    copy(path, relocate=True)

    @contextmanager
    def project(self, case):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/split-off-endpoints/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=f"{case}-", dir=scratch) as directory:
            project = Path(directory) / "project"
            self.copy_project(project)
            yield project

    @staticmethod
    def set_json(path, keys, value):
        data = json.loads(path.read_text())
        target = data
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        path.write_text(json.dumps(data) + "\n")

    @staticmethod
    def report(project, phase="analyze", api="split_off_last"):
        path = project / CHECKER_LOGS / api / f"{phase}.json"
        return path, json.loads(path.read_text())

    @classmethod
    def location(cls, project, kind, phase="analyze"):
        _, report = cls.report(project, phase)
        result = report["results"][0]
        if kind == "query":
            return Path(result["baseline"]["artifact"])
        if kind == "attempt":
            return Path(result["proofs"][0]["artifact"])
        if kind in ("source", "harness", "worktree", "logs"):
            return Path(result["proofs"][0]["native"][kind])
        return Path(report["run_dir"]) / kind

    def invoke(self, project, case, arguments, selected=(), expected_code=0):
        def contents():
            return {
                str(path.relative_to(project)): path.read_bytes()
                for path in project.rglob("*") if path.is_file()
            }

        before = contents()
        directories = {str(path.relative_to(project)) for path in project.rglob("*") if path.is_dir()}
        command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
        result = subprocess.run(
            command, cwd=project, text=True, capture_output=True, timeout=30,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(project.parent)},
        )
        after = contents()
        changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
        if directory := os.environ.get("SPLIT_OFF_EXPORT_TEST_LOG_DIR"):
            log = ROOT / directory / "cli" / case
            log.mkdir(parents=True, exist_ok=False)
            (log / "command.txt").write_text(
                f"cd {shlex.quote(str(project))} && PYTHONDONTWRITEBYTECODE=1 {shlex.join(command)}\n"
            )
            (log / "stdout.log").write_text(result.stdout)
            (log / "stderr.log").write_text(result.stderr)
            (log / "result.json").write_text(json.dumps({
                "returncode": result.returncode, "expected_returncode": expected_code,
                "selected": selected, "changed_files": changed,
            }, indent=2) + "\n")
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        self.assertEqual(
            directories, {str(path.relative_to(project)) for path in project.rglob("*") if path.is_dir()},
        )
        if expected_code:
            self.assertEqual(before, after)
            return
        allowed = {"inventory/coverage.tsv", *[f"proofs/completeness/slice/{api}.rs" for api in selected]}
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
        for identity in rows:
            if identity not in {f"<[T]>::{api}" for api in selected}:
                self.assertEqual(records[identity], new_records[identity], identity)
            else:
                for field in fields[:4]:
                    self.assertEqual(rows[identity][field], new_rows[identity][field])
        for api in selected:
            row = new_rows[f"<[T]>::{api}"]
            self.assertEqual(row["specification"], f"{POST}::{api}_post")
            self.assertEqual(row["correctness_proof"], f"proofs/correctness/slice/{api}.rs")
            self.assertEqual(row["correctness_target_functions"], "1")
            self.assertIn("--compile --no-cheating --num-threads 1", row["correctness_command"])
            self.assertIn("final implementation review pending", row["correctness_result"])
            self.assertIn(
                "1 target + 1 shared split dependency + 2 imported consistency lemmas"
                if api == "split_off_last" else "1 target + 0 imported project proof functions",
                row["correctness_result"],
            )
            self.assertEqual(row["completeness_checked_goals"], "1")
            for observation in (
                "Option variant/full element", "entire call-return remaining Seq<T>",
                "two independent post-slot observations", "no caller-final input",
                "6 state lemmas", "all 11 search guards off",
                "unchanged analysis/reexecution retained",
            ):
                self.assertIn(observation, row["completeness_result"])
            self.assertEqual(row["independent_review"], "pending")
            self.assertEqual(row["mission_scope"], "slice_shared_split_off_endpoints")
            self.assertEqual(
                row["issues"], "issues/V-ASCII-CALL-BINDING.md" if api == "split_off_last" else "",
            )
            _, report = self.report(project, api=api)
            native = report["results"][0]["proofs"][0]["native"]
            self.assertEqual(
                "\n".join(after[row["completeness_proof"]].decode().splitlines()[3:]) + "\n",
                Path(native["harness"]).read_text().replace(
                    '#[path = "../../../../specs/slice/split_off_post.rs"]',
                    '#[path = "../../../specs/slice/split_off_post.rs"]', 1,
                ),
            )
        self.assertIn(f"Exported {len(selected)} checked split-off proofs", result.stdout)

    def case(self, name, change=None, arguments=None, selected=(), expected_code=1):
        with self.subTest(case=name), self.project(name) as project:
            if change:
                change(project)
            self.invoke(
                project, name, ["--split-off-endpoints"] if arguments is None else arguments,
                selected, expected_code,
            )

    def test_single_joint_reverse_invalid_duplicate_and_exclusive_selections(self):
        flag = "--split-off-endpoints"
        for name, arguments, selected, code in (
            ("first", [flag, APIS[0]], APIS[:1], 0),
            ("last", [flag, APIS[1]], APIS[1:], 0),
            ("both", [flag], APIS, 0),
            ("both-explicit", [flag, *APIS], APIS, 0),
            ("reverse", [flag, *APIS[::-1]], APIS[::-1], 0),
            ("wrong-api", [flag, "split_last"], (), 2),
            ("empty-name", [flag, ""], (), 2),
            ("duplicate-first", [flag, APIS[0], APIS[0]], (), 2),
            ("duplicate-last", [flag, APIS[1], APIS[1]], (), 2),
            *[(f"exclusive-{other}", [flag, "--" + other], (), 2) for other in (
                "defaults", "singletons", "ascii-case", "endpoints", "splits",
                "mutable-endpoints", "mutable-splits",
            )],
        ):
            self.case(name, arguments=arguments, selected=selected, expected_code=code)

    def test_partial_exports_and_repeats_preserve_bytes(self):
        with self.project("partial") as project:
            for api in APIS:
                self.invoke(project, f"partial-{api}", ["--split-off-endpoints", api], (api,))
            before = (project / "inventory/coverage.tsv").read_bytes()
            self.invoke(project, "repeat-both", ["--split-off-endpoints"], APIS)
            self.assertEqual(before, (project / "inventory/coverage.tsv").read_bytes())
            (project / LAST_LOGS / "exit-code.txt").write_text("1\n")
            self.invoke(project, "repeat-now-failed", ["--split-off-endpoints"], expected_code=1)

    def test_only_selected_api_evidence_is_required(self):
        for selected, unselected in (APIS, APIS[::-1]):
            def remove(project, unselected=unselected):
                for path in (
                    export.SPLIT_OFF_SOURCE_LOGS[unselected],
                    f"{CHECKER_LOGS}/{unselected}",
                    f"logs/split-off-endpoints/compiled-comparisons/{unselected}",
                ):
                    shutil.rmtree(project / path)
                (project / f"proofs/correctness/slice/{unselected}.rs").unlink()
                (project / f"proofs/completeness/slice/inputs/{unselected}.rs").unlink()
            self.case(
                f"only-{selected}", remove, ["--split-off-endpoints", selected], (selected,), 0,
            )

    def test_failed_or_zero_source_proofs_never_partially_export(self):
        for name, path, value in (
            ("failed-source-exit", "exit-code.txt", "1\n"),
            ("zero-source", "verus.log", "verification results:: 0 verified, 0 errors\n"),
            ("failed-source", "verus.log", "verification results:: 0 verified, 1 errors\n"),
            ("dependency-only", "verus.log", "verification results:: 3 verified, 0 errors\n"),
            ("empty-source-library", "libsplit_off_last.rlib", ""),
            ("empty-source-query", "queries/root.smt2", ""),
            ("unknown-source", "queries/root.smt_transcript", "(check-sat)\nunknown\n"),
            ("sat-source", "queries/root.smt_transcript", "(check-sat)\nsat\n"),
        ):
            self.case(name, lambda project, p=path, v=value: (project / LAST_LOGS / p).write_text(v))
        for flag in ("--compile", "--no-cheating"):
            def remove(project, flag=flag):
                path = project / LAST_LOGS / "command.txt"
                path.write_text(path.read_text().replace(flag, "", 1))
            self.case("source-missing-" + flag[2:], remove)
        self.case("missing-source-receipt", lambda project: (project / LAST_LOGS / "command.txt").unlink())

    def test_only_the_approved_current_body_can_be_exported(self):
        for name, before, after in (
            ("unadopted", "split_dependency::split_last(*slice)", "slice.split_last()"),
            ("wrong-slot", "*slice = rem;", "*slice = *slice;"),
            ("target-call", "split_dependency::split_last(*slice)", "slice.split_off_last()"),
            ("old-post-slot", "(*final(slice))@", "(*old(slice))@"),
        ):
            def alter(project, before=before, after=after):
                for root in (project, project / LAST_LOGS / "source"):
                    path = root / LAST_SOURCE
                    self.assertIn(before, path.read_text())
                    path.write_text(path.read_text().replace(before, after, 1))
            self.case("source-" + name, alter)

    def test_current_compiled_reviewed_and_analyzed_inputs_must_match(self):
        for path in (POST, STATE, BINDING, LAST_SOURCE, LAST_INPUT, "proofs/correctness/slice/split_last.rs"):
            self.case(
                "current-stale-" + path.replace("/", "-"),
                lambda project, p=path: (project / p).write_bytes((project / p).read_bytes() + b"\n"),
            )
        for path in (POST, LAST_SOURCE, "proofs/correctness/slice/split_last.rs", "specs/slice/mod.rs"):
            self.case(
                "compiled-stale-" + Path(path).name,
                lambda project, p=path: (project / LAST_LOGS / "source" / p).write_bytes(
                    (project / LAST_LOGS / "source" / p).read_bytes() + b"\n"
                ),
            )
        for phase in ("analyze", "replay"):
            for location in ("workspace", "worktree"):
                paths = (*export.SPLIT_OFF_DEPENDENCIES, *((LAST_INPUT,) if location == "workspace" else ()))
                for path in paths:
                    def stale(project, path=path, phase=phase, location=location):
                        file = self.location(project, location, phase) / path
                        file.write_bytes(file.read_bytes() + b"\n")
                    self.case(f"stale-{phase}-{location}-{Path(path).name}", stale)
        self.case(
            "changed-pre-adoption", lambda project: (project / BEFORE / LAST_SOURCE).write_text("changed\n"),
        )

    def test_checker_failure_unknown_zero_goals_and_ignored_remaining_are_rejected(self):
        prefix = ["results", 0]
        for phase in ("analyze", "replay"):
            for name, keys, value in (
                ("failed", ["status"], "failed"), ("exit", ["exit_code"], 1),
                ("unknown-count", ["counts"], {"unknown": 1}),
                ("no-targets", ["targets"], []), ("no-results", ["results"], []),
                ("target-unknown", prefix + ["verdict"], "unknown"),
                ("baseline-unknown", prefix + ["baseline", "status"], "unknown"),
                ("baseline-missing", prefix + ["baseline"], None),
                ("baseline-constrained", prefix + ["baseline", "constraints"], ["nonempty"]),
                ("no-proofs", prefix + ["proofs"], []),
                ("zero-goals", prefix + ["proofs", 0, "verified_goals"], 0),
                ("extra-goals", prefix + ["proofs", 0, "verified_goals"], 2),
                ("proof-failed", prefix + ["proofs", 0, "status"], "failed"),
                ("ignored-remaining", prefix + ["coverage", "ignored_dimensions"], ["post.slice"]),
                ("slot-not-modeled", prefix + ["coverage", "mutable_parameter_poststates"], "not_modeled"),
            ):
                self.case(
                    f"{phase}-{name}", lambda project, k=keys, v=value, p=phase:
                    self.set_json(project / CHECKER_LOGS / APIS[1] / f"{p}.json", k, v),
                )

    def test_full_variant_value_and_remaining_comparison_cannot_be_reduced(self):
        prefix = ["results", 0, "proofs", 0, "native", "det_spec"]
        for phase in ("analyze", "replay"):
            for name, before, after in (
                ("variant", "(r1 is Some) == (r2 is Some)", "true"),
                ("value", "r1->Some_0 == r2->Some_0", "true"),
                ("remaining", "post1_slice =~= post2_slice", "true"),
            ):
                def reduce(project, before=before, after=after, phase=phase):
                    path, report = self.report(project, phase)
                    equal = report["results"][0]["proofs"][0]["native"]["det_spec"]["equal_fn_def"]
                    self.assertIn(before, equal)
                    self.set_json(path, prefix + ["equal_fn_def"], equal.replace(before, after, 1))
                self.case(f"comparison-{phase}-{name}", reduce)
            self.case(
                f"comparison-{phase}-only-return", lambda project, p=phase: self.set_json(
                    self.report(project, p)[0], prefix + ["equal_arg_pairs"], [{"lhs": "r1", "rhs": "r2"}],
                ),
            )
            def freeze(project, phase=phase):
                path, report = self.report(project, phase)
                template = report["results"][0]["proofs"][0]["native"]["det_spec"]["det_check_template"]
                self.set_json(path, prefix + ["det_check_template"], template.replace("post2_slice", "post1_slice"))
            self.case(f"comparison-{phase}-same-post-slot", freeze)
            for kind in ("harness", "source"):
                def reduce_file(project, kind=kind, phase=phase):
                    path = self.location(project, kind, phase)
                    path.write_text(path.read_text().replace("post1_slice =~= post2_slice", "true", 1))
                self.case(f"comparison-{phase}-actual-{kind}", reduce_file)

    def test_every_actual_search_guard_must_be_disabled(self):
        for phase in ("analyze", "replay"):
            for guard in ("g_pre_slice_leneq", "g_r1_is_Some", "g_post1_slice_leneq", "g_post2_slice_lenrng", "g_neq_tuple"):
                def enable(project, guard=guard, phase=phase):
                    path = self.location(project, "query", phase)
                    before = f"(not {guard}!)"
                    self.assertIn(before, path.read_text())
                    path.write_text(path.read_text().replace(before, f"{guard}!", 1))
                self.case(f"guard-{phase}-{guard}", enable)
            self.case(
                f"guard-{phase}-record", lambda project, p=phase: self.set_json(
                    self.location(project, "attempt", p) / "query/baseline.json",
                    ["payload", "guard_assignments", "g_post1_slice_leneq"], True,
                ),
            )

    def test_reexecution_and_exact_single_target_selection_are_required(self):
        self.case(
            "wrong-declaration-line", lambda project: self.set_json(
                self.report(project)[0], ["results", 0, "target", "line"], 6,
            ),
        )
        for name, file, keys, value in (
            ("replay-selector", "effective-config.json", ["payload", "selectors"], []),
            ("replay-parent", "manifest.json", ["payload", "parent_run"], ""),
            ("assisted", "effective-config.json", ["payload", "assistance"], {"mode": "live"}),
        ):
            self.case(
                name, lambda project, f=file, k=keys, v=value:
                self.set_json(self.location(project, f, "replay"), k, v),
            )
        for name, edit in (
            ("no-reexecute", lambda command: command.remove("--reexecute")),
            ("replay-config-override", lambda command: command.extend(["--config", "specdet.toml"])),
        ):
            def change(project, edit=edit):
                path = project / CHECKER_LOGS / APIS[1] / "replay-command.json"
                data = json.loads(path.read_text())
                edit(data["command"])
                path.write_text(json.dumps(data) + "\n")
            self.case(name, change)

    def test_actual_verifier_and_separate_compilations_must_succeed(self):
        for name, keys, value in (
            ("native-failed", ["process", "returncode"], 1),
            ("native-timeout", ["process", "timed_out"], True),
            ("native-zero", ["verified_goals"], 0),
        ):
            self.case(
                name, lambda project, k=keys, v=value: self.set_json(
                    self.report(project)[0], ["results", 0, "proofs", 0, "native", "invocations", 0, *k], v,
                ),
            )
        self.case(
            "native-unknown-transcript", lambda project:
            (self.location(project, "logs") / "root.smt_transcript").write_text("(check-sat)\nunknown\n"),
        )
        for label, logs, output in (
            ("state", Path("logs/split-off-endpoints/value-state/state"), "target/split-off-endpoints/libstate.rlib"),
            ("comparison", Path("logs/split-off-endpoints/compiled-comparisons/split_off_last"),
             "target/split-off-endpoints/libsplit_off_last_comparison.rlib"),
        ):
            for name, change in (
                ("zero", lambda project, d=logs: (project / d / "verus.log").write_text(
                    "verification results:: 0 verified, 0 errors\n"
                )),
                ("empty-library", lambda project, p=output: (project / p).write_bytes(b"")),
                ("failed-receipt", lambda project, d=logs: self.set_json(
                    project / d / "command.json", ["returncode"], 1,
                )),
                ("no-receipt", lambda project, d=logs: (project / d / "command.json").unlink()),
            ):
                self.case(f"{label}-{name}", change)

    def test_existing_different_comparison_is_not_overwritten(self):
        def conflict(project):
            (project / f"proofs/completeness/slice/{APIS[1]}.rs").write_text("previous result\n")
        self.case("different-export", conflict)


if __name__ == "__main__":
    unittest.main()
