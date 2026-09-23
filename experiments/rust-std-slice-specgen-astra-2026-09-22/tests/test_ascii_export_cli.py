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

from scripts import export_completeness


ROOT = Path(__file__).resolve().parents[1]
COMMON_SOURCES = (
    "specs/slice/ascii.rs", "specs/slice/ascii_post.rs",
    "proofs/completeness/slice/ascii_state.rs", "proofs/completeness/slice/ascii.toml",
)


class AsciiExportCLI(unittest.TestCase):
    def copy_project(self, project):
        def copy(source, destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

        sources = [
            "scripts/export_completeness.py", "inventory/apis.tsv", "inventory/coverage.tsv",
            *COMMON_SOURCES,
            *export_completeness.ASCII_CORRECTNESS_DEPENDENCIES,
            *(f"proofs/correctness/slice/{api}.rs"
              for api in export_completeness.ASCII_CHECKER_LOGS),
            *(f"proofs/completeness/slice/inputs/{api}.rs"
              for api in export_completeness.ASCII_CHECKER_LOGS),
        ]
        sources.extend(
            str(path.relative_to(ROOT)) for path in (ROOT / "proofs/completeness/slice").glob("*.rs")
        )
        for source in sources:
            copy(ROOT / source, project / source)
        for api, logs in export_completeness.ASCII_CHECKER_LOGS.items():
            for name in ("command.txt", "exit-code.txt", "verus.log"):
                source = Path("logs/ascii-case/correctness") / api / name
                copy(ROOT / source, project / source)
            correctness = Path(export_completeness.ASCII_CORRECTNESS_LOGS[api])
            for name in ("command.txt", "exit-code.txt", "verus.stdout", "verus.stderr"):
                copy(ROOT / correctness / name, project / correctness / name)
            for source in (
                f"proofs/correctness/slice/{api}.rs",
                *export_completeness.ASCII_CORRECTNESS_DEPENDENCIES,
            ):
                snapshot = correctness / "inputs" / source
                copy(ROOT / snapshot, project / snapshot)
            for phase in ("analyze", "replay"):
                report = json.loads((ROOT / logs / f"{phase}.json").read_text())
                run = Path(report["run_dir"])
                for source in (
                    *COMMON_SOURCES,
                    f"proofs/completeness/slice/inputs/{api}.rs",
                ):
                    snapshot = run / "workspace" / source
                    copy(snapshot, project / snapshot.relative_to(ROOT))
                for result in report["results"]:
                    for artifact in (
                        result["baseline"]["artifact"], result["proofs"][0]["native"]["harness"],
                    ):
                        path = Path(artifact)
                        copy(path, project / path.relative_to(ROOT))
                for name in (f"{phase}.json", f"{phase}.exit-code.txt", f"{phase}-command.txt"):
                    destination = project / logs / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(
                        (ROOT / logs / name).read_text().replace(str(ROOT), str(project))
                    )

    def check_selection(self, case, arguments, selected=(), expected_code=0, tamper=None):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/ascii-case/export-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix=f"export-{case}-") as directory:
            project = Path(directory) / "project"
            self.copy_project(project)
            expected_error = None
            if tamper:
                kind, path, phase = tamper
                logs = project / export_completeness.ASCII_CHECKER_LOGS["make_ascii_lowercase"]
                report_phase = phase if kind in ("source", "comparison", "premise", "guard") else None
                report_path = logs / f"{report_phase or 'analyze'}.json"
                report = json.loads(report_path.read_text())
                result = next(
                    result for result in report["results"]
                    if result["target"]["name"] == "make_ascii_lowercase_observation"
                )
                if kind == "source":
                    base = Path(report["run_dir"]) / "workspace" if phase else project
                    source = base / path
                    source.write_bytes(source.read_bytes() + b"\n")
                    expected_error = f"checked snapshot: {path}"
                elif kind == "comparison":
                    result["proofs"][0]["native"]["det_spec"]["equal_fn_def"] = "true"
                    report_path.write_text(json.dumps(report))
                    expected_error = "complete final byte sequence is not compared"
                elif kind == "premise":
                    result["proofs"][0]["native"]["det_spec"]["det_check_template"] += "\nrequires false"
                    report_path.write_text(json.dumps(report))
                    expected_error = "Unexpected premises"
                elif kind == "guard":
                    query = Path(result["baseline"]["artifact"])
                    query.write_text(
                        query.read_text().replace("(not g__initial___0__eq!)", "g__initial___0__eq!")
                    )
                    expected_error = "did not disable every search guard"
                elif kind == "source-proof":
                    base = (
                        project / export_completeness.ASCII_CORRECTNESS_LOGS["make_ascii_lowercase"]
                        / "inputs" if phase == "snapshot" else project
                    )
                    source = base / path
                    source.write_bytes(source.read_bytes() + b"\n")
                    expected_error = "differs from the checked source proof"
                elif kind == "proof-result":
                    correctness = project / export_completeness.ASCII_CORRECTNESS_LOGS[
                        "make_ascii_lowercase"
                    ]
                    (correctness / path).write_text(phase)
                    expected_error = "No successful compiled ASCII source proof"
                else:
                    self.fail(f"Unknown test modification: {kind}")
            coverage = project / "inventory/coverage.tsv"
            proofs = project / "proofs/completeness/slice"
            before = coverage.read_bytes()
            proof_before = {path.name: path.read_bytes() for path in proofs.glob("*.rs")}
            original_logs = project / "logs/ascii-case/correctness"
            original_before = {
                path.relative_to(original_logs): path.read_bytes()
                for path in original_logs.rglob("*") if path.is_file()
            }
            command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
            result = subprocess.run(
                command, cwd=project,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=directory),
                capture_output=True, text=True, timeout=30,
            )
            after = coverage.read_bytes()
            proof_after = {path.name: path.read_bytes() for path in proofs.glob("*.rs")}
            self.assertEqual(original_before, {
                path.relative_to(original_logs): path.read_bytes()
                for path in original_logs.rglob("*") if path.is_file()
            })
            rows_before = list(csv.DictReader(io.StringIO(before.decode()), delimiter="\t"))
            rows_after = list(csv.DictReader(io.StringIO(after.decode()), delimiter="\t"))
            selected_ids = {f"<[u8]>::{api}" for api in selected}
            changed_rows = [
                old["canonical_id"] for old, new in zip(rows_before, rows_after) if old != new
            ]
            changed_proofs = [
                name for name in sorted(proof_before.keys() | proof_after.keys())
                if proof_before.get(name) != proof_after.get(name)
            ]
            log_root = os.environ.get("ASCII_EXPORT_TEST_LOG_DIR")
            if log_root:
                log = ROOT / log_root / case
                log.mkdir(parents=True)
                (log / "command.txt").write_text(
                    f"cd {shlex.quote(str(project))} && {shlex.join(command)}\n"
                )
                (log / "stdout.log").write_text(result.stdout)
                (log / "stderr.log").write_text(result.stderr)
                (log / "exit-code.txt").write_text(f"{result.returncode}\n")
                (log / "isolation.json").write_text(json.dumps({
                    "selected": selected, "modification": tamper,
                    "expected_exit_code": expected_code, "actual_exit_code": result.returncode,
                    "rows_before": len(rows_before), "rows_after": len(rows_after),
                    "changed_rows": changed_rows, "changed_proofs": changed_proofs,
                }, indent=2) + "\n")
            self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
            self.assertEqual(len(rows_before), 331)
            self.assertEqual(
                [row["canonical_id"] for row in rows_before],
                [row["canonical_id"] for row in rows_after],
            )
            self.assertEqual(before.splitlines()[0], after.splitlines()[0])
            for index, (old, new) in enumerate(zip(rows_before, rows_after), start=1):
                if old["canonical_id"] not in selected_ids:
                    self.assertEqual(old, new)
                    self.assertEqual(
                        before.splitlines(keepends=True)[index], after.splitlines(keepends=True)[index],
                    )
            self.assertLessEqual(set(changed_proofs), {f"{api}.rs" for api in selected})
            for api in selected:
                self.assertIn(f"{api}.rs", proof_after)
                row = next(row for row in rows_after if row["canonical_id"] == f"<[u8]>::{api}")
                self.assertEqual(row["correctness_target_functions"], "1")
                self.assertIn("1 target + 6 scalar source functions", row["correctness_result"])
                self.assertIn("13 verified obligations", row["correctness_result"])
                self.assertIn("--compile --no-cheating", row["correctness_command"])
                self.assertEqual(
                    row["correctness_log"],
                    f"{export_completeness.ASCII_CORRECTNESS_LOGS[api]}/verus.stdout",
                )
                self.assertEqual(row["completeness_checked_goals"], "1")
                self.assertIn("full final Seq<u8>", row["completeness_result"])
            if expected_code:
                self.assertEqual(before, after)
                self.assertEqual(proof_before, proof_after)
            if expected_error:
                self.assertIn(expected_error, result.stderr)

    def test_real_selected_default_and_invalid_exports(self):
        for case, arguments, selected, code in (
            ("uppercase", ["--ascii-case", "make_ascii_uppercase"], ("make_ascii_uppercase",), 0),
            ("lowercase", ["--ascii-case", "make_ascii_lowercase"], ("make_ascii_lowercase",), 0),
            ("both", ["--ascii-case"], tuple(export_completeness.ASCII_CHECKER_LOGS), 0),
            ("explicit-both", ["--ascii-case", "make_ascii_lowercase", "make_ascii_uppercase"],
             ("make_ascii_lowercase", "make_ascii_uppercase"), 0),
            ("wrong-name", ["--ascii-case", "from_mut"], (), 2),
            ("mixed-defaults", ["--ascii-case", "--defaults"], (), 2),
            ("mixed-singletons", ["--ascii-case", "--singletons"], (), 2),
            ("duplicate", ["--ascii-case", "make_ascii_uppercase", "make_ascii_uppercase"], (), 2),
        ):
            with self.subTest(case=case):
                self.check_selection(case, arguments, selected, code)

    def test_stale_current_and_reexecuted_inputs_do_not_export(self):
        for path in (
            *COMMON_SOURCES, "proofs/completeness/slice/inputs/make_ascii_lowercase.rs",
        ):
            with self.subTest(path=path):
                case = "stale-" + path.replace("/", "-")
                self.check_selection(
                    case, ["--ascii-case", "make_ascii_lowercase"],
                    expected_code=1, tamper=("source", path, None),
                )
        self.check_selection(
            "stale-replay-state", ["--ascii-case", "make_ascii_lowercase"], expected_code=1,
            tamper=("source", "proofs/completeness/slice/ascii_state.rs", "replay"),
        )

    def test_unit_only_comparison_extra_premises_and_search_limits_do_not_export(self):
        for kind in ("comparison", "premise", "guard"):
            with self.subTest(kind=kind):
                self.check_selection(
                    kind, ["--ascii-case", "make_ascii_lowercase"], expected_code=1,
                    tamper=(kind, None, "analyze"),
                )

    def test_changed_source_proof_or_dependency_does_not_export(self):
        for path in (
            "proofs/correctness/slice/make_ascii_lowercase.rs",
            *export_completeness.ASCII_CORRECTNESS_DEPENDENCIES,
        ):
            with self.subTest(path=path):
                self.check_selection(
                    "stale-proof-" + path.replace("/", "-"),
                    ["--ascii-case", "make_ascii_lowercase"], expected_code=1,
                    tamper=("source-proof", path, "snapshot" if path in COMMON_SOURCES else None),
                )

    def test_failed_empty_or_incomplete_source_proof_does_not_export(self):
        for case, path, value in (
            ("source-failed", "exit-code.txt", "1\n"),
            ("source-empty", "verus.stdout", "verification results:: 0 verified, 0 errors\n"),
            ("source-partial", "verus.stdout", "verification results:: 12 verified, 0 errors\n"),
            ("source-error", "verus.stderr", "error: source compilation failed\n"),
        ):
            with self.subTest(case=case):
                self.check_selection(
                    case, ["--ascii-case", "make_ascii_lowercase"], expected_code=1,
                    tamper=("proof-result", path, value),
                )


if __name__ == "__main__":
    unittest.main()
