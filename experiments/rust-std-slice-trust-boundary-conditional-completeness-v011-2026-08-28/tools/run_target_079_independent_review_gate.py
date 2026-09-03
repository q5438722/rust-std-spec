#!/usr/bin/env python3
"""Capture the independent target-079 replay and acceptance gate."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import target_pipeline


ROOT = common.OUT
EVIDENCE = (
    ROOT / "evidence/target_079_operational_v1/independent_review_gate"
)
VERUS_PROOF = (
    ROOT
    / "proofs/079_core_slice_select_nth_unstable_by_key_operational_v1.rs"
)


def _capture(
    name: str,
    argv: list[str],
    *,
    timeout: int = 300,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        EVIDENCE / name,
        argv,
        cwd=ROOT,
        timeout=timeout,
    )
    if record["exit_code"] != 0:
        raise RuntimeError(
            f"{name}: command exited {record['exit_code']}"
        )
    return record


def _require_line(
    name: str,
    record: dict[str, Any],
    expected: str,
) -> None:
    target_pipeline.require_clean_result(
        record, expected, label=name
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args()
    z3 = shutil.which("z3")
    if z3 is None:
        raise RuntimeError("z3 is required")

    EVIDENCE.mkdir(parents=True, exist_ok=True)
    records: dict[str, Any] = {}
    manifest_path = EVIDENCE / "manifest.json"
    try:
        records["python_compile"] = _capture(
            "python_compile",
            [
                sys.executable,
                "-m",
                "compileall",
                "-q",
                "tools",
                "tests",
            ],
        )
        records["ground_truth"] = _capture(
            "ground_truth",
            [
                sys.executable,
                "tools/run_target_079_ground_truth.py",
            ],
        )
        records["target_runner"] = _capture(
            "target_runner",
            [
                sys.executable,
                "tools/run_target_079_operational_v1.py",
            ],
            timeout=600,
        )
        target_stdout = (
            ROOT / records["target_runner"]["stdout"]
        ).read_text()
        if "target_079_operational_v1=PASS" not in target_stdout:
            raise RuntimeError("target runner did not report PASS")

        records["focused_execution_tests"] = _capture(
            "focused_execution_tests",
            [
                sys.executable,
                "tests/test_target_079_operational_v1.py",
                "-q",
            ],
        )
        records["focused_artifact_tests"] = _capture(
            "focused_artifact_tests",
            [
                sys.executable,
                "tests/test_target_079_operational_artifacts_v1.py",
                "-q",
            ],
            timeout=300,
        )

        for label, filename, expected in (
            (
                "z3_exact_output",
                "exact_output_obligation.smt2",
                "unsat",
            ),
            ("z3_completeness", "obligation.smt2", "unsat"),
            ("z3_nonvacuity", "nonvacuity.smt2", "sat"),
        ):
            record = _capture(
                label,
                [
                    z3,
                    "-smt2",
                    str(
                        ROOT
                        / "evidence/target_079_operational_v1"
                        / filename
                    ),
                ],
            )
            _require_line(label, record, expected)
            records[label] = record

        records["verus_typecheck"] = _capture(
            "verus_typecheck",
            [
                str(common.VERUS),
                str(VERUS_PROOF),
                "--crate-type=lib",
                "--no-verify",
            ],
        )
        records["verus_verification"] = _capture(
            "verus_verification",
            [
                str(common.VERUS),
                str(VERUS_PROOF),
                "--crate-type=lib",
            ],
        )
        verification_stdout = (
            ROOT / records["verus_verification"]["stdout"]
        ).read_text()
        if (
            "verification results:: 7 verified, 0 errors"
            not in verification_stdout
        ):
            raise RuntimeError("Verus verification summary changed")

        records["complete_unit_suite"] = _capture(
            "complete_unit_suite",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ],
            timeout=900,
        )
        records["acceptance"] = _capture(
            "acceptance",
            [sys.executable, "tools/run_acceptance.py"],
            timeout=1800,
        )
        acceptance_stdout = (
            ROOT / records["acceptance"]["stdout"]
        ).read_text()
        if "acceptance=PASS" not in acceptance_stdout:
            raise RuntimeError("acceptance runner did not report PASS")
    except Exception as error:
        common.write_json(
            manifest_path,
            {
                "schema_version": 1,
                "status": "failed",
                "task_id": args.task_id,
                "error": str(error),
                "commands": records,
            },
        )
        raise

    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "status": "passed",
            "task_id": args.task_id,
            "target": "core::slice::select_nth_unstable_by_key",
            "input_order": "79",
            "commands": records,
            "direct_solver_results": {
                "exact_output": "unsat",
                "completeness": "unsat",
                "nonvacuity": "sat",
            },
            "verus_summary": (
                "verification results:: 7 verified, 0 errors"
            ),
        },
    )
    print("target_079_independent_review_gate=PASS")
    print(f"commands={len(records)}")


if __name__ == "__main__":
    main()
