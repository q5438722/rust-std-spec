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
    "specs/slice/raw.rs",
    "specs/slice/raw_post.rs",
    "proofs/completeness/slice/singletons.toml",
)
MUTABLE_STATE = "proofs/completeness/slice/from_mut_state.rs"


class SingletonExportCLI(unittest.TestCase):
    def copy_project(self, project):
        def copy(source, destination):
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)

        sources = [
            "scripts/export_completeness.py", "inventory/apis.tsv", "inventory/coverage.tsv",
            *COMMON_SOURCES,
            "proofs/completeness/slice/inputs/from_ref.rs",
            "proofs/completeness/slice/inputs/from_mut.rs",
        ]
        sources.extend(str(path.relative_to(ROOT)) for path in (ROOT / "proofs/completeness/slice").glob("*.rs"))
        for source in sources:
            copy(ROOT / source, project / source)
        for api, logs in export_completeness.SINGLETON_CHECKER_LOGS.items():
            for name in ("command.txt", "exit-code.txt", "stderr.log"):
                source = Path("logs/singletons/correctness") / api / name
                copy(ROOT / source, project / source)
            dependencies = [*COMMON_SOURCES, f"proofs/completeness/slice/inputs/{api}.rs"]
            if api == "from_mut":
                dependencies.append(MUTABLE_STATE)
            for phase in ("analyze", "replay"):
                report_path = ROOT / logs / f"{phase}.json"
                report = json.loads(report_path.read_text())
                run = Path(report["run_dir"])
                for source in dependencies:
                    snapshot = run / "workspace" / source
                    copy(snapshot, project / snapshot.relative_to(ROOT))
                result = report["results"][0]
                for artifact in (
                    result["baseline"]["artifact"], result["proofs"][0]["native"]["harness"],
                ):
                    path = Path(artifact)
                    copy(path, project / path.relative_to(ROOT))
                for name in (f"{phase}.json", f"{phase}.exit-code.txt", f"{phase}-command.txt"):
                    destination = project / logs / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    # Relocate recorded absolute paths; snapshots and proof/query bytes stay exact.
                    destination.write_text(
                        (ROOT / logs / name).read_text().replace(str(ROOT), str(project))
                    )

    def check_selection(self, case, arguments, selected=(), expected_code=0, stale=None):
        scratch = Path(os.environ.get("TMPDIR", ROOT / "target/singleton-writeback"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch, prefix=f"export-{case}-") as directory:
            project = Path(directory) / "project"
            self.copy_project(project)
            if stale is not None:
                dependency, phase = stale
                base = project
                if phase:
                    report = json.loads(
                        (project / export_completeness.SINGLETON_CHECKER_LOGS["from_mut"]
                         / f"{phase}.json").read_text()
                    )
                    base = Path(report["run_dir"]) / "workspace"
                path = base / dependency
                path.write_bytes(path.read_bytes() + b"\n")
            coverage = project / "inventory/coverage.tsv"
            proofs = project / "proofs/completeness/slice"
            before = coverage.read_bytes()
            proof_before = {path.name: path.read_bytes() for path in proofs.glob("*.rs")}
            command = [sys.executable, "-B", "scripts/export_completeness.py", *arguments]
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=directory)
            environment["RUSTUP_HOME"] = "/home/chentianyu/.rustup"
            result = subprocess.run(
                command, cwd=project, env=environment, capture_output=True, text=True, timeout=30,
            )
            after = coverage.read_bytes()
            proof_after = {path.name: path.read_bytes() for path in proofs.glob("*.rs")}
            rows_before = list(csv.DictReader(io.StringIO(before.decode()), delimiter="\t"))
            rows_after = list(csv.DictReader(io.StringIO(after.decode()), delimiter="\t"))
            selected_ids = {f"core::slice::{api}" for api in selected}
            changed_rows = [
                old["canonical_id"] for old, new in zip(rows_before, rows_after) if old != new
            ]
            changed_proofs = [
                name for name in sorted(proof_before.keys() | proof_after.keys())
                if proof_before.get(name) != proof_after.get(name)
            ]
            log_root = os.environ.get("SINGLETON_EXPORT_TEST_LOG_DIR")
            if log_root:
                log = ROOT / log_root / case
                log.mkdir(parents=True)
                (log / "command.txt").write_text(
                    f"cd {shlex.quote(str(project))} && "
                    "RUSTUP_HOME=/home/chentianyu/.rustup PYTHONDONTWRITEBYTECODE=1 "
                    f"TMPDIR={shlex.quote(directory)} {shlex.join(command)}\n"
                )
                (log / "stdout.log").write_text(result.stdout)
                (log / "stderr.log").write_text(result.stderr)
                (log / "exit-code.txt").write_text(f"{result.returncode}\n")
                (log / "isolation.json").write_text(json.dumps({
                    "selected": selected,
                    "stale_dependency": stale,
                    "expected_exit_code": expected_code,
                    "actual_exit_code": result.returncode,
                    "rows_before": len(rows_before),
                    "rows_after": len(rows_after),
                    "changed_rows": changed_rows,
                    "changed_proofs": changed_proofs,
                }, indent=2) + "\n")
            self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
            self.assertEqual(
                [row["canonical_id"] for row in rows_before],
                [row["canonical_id"] for row in rows_after],
            )
            self.assertEqual(len(before.splitlines()), len(rows_before) + 1)
            self.assertEqual(len(after.splitlines()), len(rows_after) + 1)
            self.assertEqual(before.splitlines(keepends=True)[0], after.splitlines(keepends=True)[0])
            for index, (old, new) in enumerate(zip(rows_before, rows_after), start=1):
                if old["canonical_id"] not in selected_ids:
                    self.assertEqual(old, new)
                    self.assertEqual(
                        before.splitlines(keepends=True)[index], after.splitlines(keepends=True)[index]
                    )
            self.assertLessEqual(set(changed_proofs), {f"{api}.rs" for api in selected})
            for api in selected:
                self.assertIn(f"{api}.rs", proof_after)
                row = next(row for row in rows_after if row["canonical_id"] == f"core::slice::{api}")
                self.assertEqual(row["correctness_target_functions"], "0")
                self.assertEqual(row["completeness_checked_goals"], "1")
            if expected_code:
                self.assertEqual(before, after)
                self.assertEqual(proof_before, proof_after)
            if stale:
                self.assertIn(f"checked snapshot: {stale[0]}", result.stderr)

    def test_valid_and_invalid_cli_selections_preserve_unselected_bytes(self):
        for case, arguments, selected, code in (
            ("from-mut", ["--singletons", "from_mut"], ("from_mut",), 0),
            ("default-singletons", ["--singletons"], ("from_ref", "from_mut"), 0),
            ("from-ref", ["--singletons", "from_ref"], ("from_ref",), 0),
            ("explicit-both", ["--singletons", "from_ref", "from_mut"], ("from_ref", "from_mut"), 0),
            ("invalid-name", ["--singletons", "default_mut"], (), 2),
            ("mixed-selectors", ["--singletons", "--defaults"], (), 2),
            ("empty-name", ["--singletons", ""], (), 2),
            ("duplicate-name", ["--singletons", "from_mut", "from_mut"], (), 2),
            ("duplicate-among-both", ["--singletons", "from_ref", "from_mut", "from_ref"], (), 2),
        ):
            with self.subTest(case=case):
                self.check_selection(case, arguments, selected, code)

    def test_stale_dependencies_fail_before_cli_writes(self):
        for dependency in (
            "proofs/completeness/slice/inputs/from_mut.rs", MUTABLE_STATE, *COMMON_SOURCES,
        ):
            case = "stale-" + Path(dependency).stem
            with self.subTest(dependency=dependency):
                self.check_selection(
                    case, ["--singletons", "from_mut"], expected_code=1, stale=(dependency, None),
                )
        self.check_selection(
            "stale-replay-state", ["--singletons", "from_mut"],
            expected_code=1, stale=(MUTABLE_STATE, "replay"),
        )


if __name__ == "__main__":
    unittest.main()
