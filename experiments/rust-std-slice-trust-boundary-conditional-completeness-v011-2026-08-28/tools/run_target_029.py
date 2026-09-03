#!/usr/bin/env python3
"""Build, execute, and record the bounded target-029 evidence package."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import target_029
import target_pipeline


EVIDENCE_ROOT = (
    common.OUT / "evidence/targets" / target_029.ARTIFACT_ID
)
RESULT_STATUSES = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
}


def write_obligation(
    filename: str,
    purpose: str,
) -> tuple[Path, Path, dict[str, Any]]:
    text, metadata = target_029.obligation(purpose)
    target_029.validate_target_obligation(text, metadata)
    smt_path = EVIDENCE_ROOT / f"{filename}.smt2"
    metadata_path = EVIDENCE_ROOT / f"{filename}.metadata.json"
    smt_path.write_text(text)
    common.write_json(metadata_path, metadata)
    return smt_path, metadata_path, metadata


def run_solver(
    z3: str,
    label: str,
    smt_path: Path,
    expected: str,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        EVIDENCE_ROOT / label,
        [z3, "-smt2", str(smt_path)],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
        }
    )
    return record


def validate_crosswalk_identity() -> None:
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in rows
        if row["target"] == target_029.TARGET
        and row["input_order"] == target_029.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError("target 029 is absent or duplicated in the crosswalk")
    row = matches[0]
    if (
        row["active_contract_sha256"] != target_029.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != target_029.ACTIVE_CONTRACT_TEXT
        or row["boundary_admissibility"] != "admissible"
        or row["boundary_narrower_than_target"] != "yes"
        or row["equivalence_kind"] != "matching-index-equivalence"
    ):
        raise ValueError("target 029 crosswalk authority/boundary binding changed")


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-029 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

    validate_crosswalk_identity()
    if EVIDENCE_ROOT.exists():
        shutil.rmtree(EVIDENCE_ROOT)
    EVIDENCE_ROOT.mkdir(parents=True)

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("obligation", target_029.PRIMARY),
        ("sorted_domain_sanity", target_029.SORTED_SANITY),
        ("exact_output_obligation", target_029.EXACT_OUTPUT),
    ):
        smt_path, metadata_path, metadata = write_obligation(filename, purpose)
        solver = run_solver(
            z3,
            filename,
            smt_path,
            metadata["expected_solver_result"],
        )
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    witness_path = EVIDENCE_ROOT / "witness.json"
    common.write_json(witness_path, target_029.witness_payload())

    counterexample_path = EVIDENCE_ROOT / "counterexample_model.smt2"
    counterexample_path.write_text(
        target_029.fixed_model_text(target_029.PRIMARY)
    )
    counterexample = run_solver(
        z3,
        "counterexample_model",
        counterexample_path,
        "sat",
    )

    exact_witness_path = EVIDENCE_ROOT / "exact_output_witness.smt2"
    exact_witness_path.write_text(
        target_029.fixed_model_text(target_029.EXACT_OUTPUT)
    )
    exact_witness = run_solver(
        z3,
        "exact_output_witness",
        exact_witness_path,
        "sat",
    )

    replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_029.py"),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-029 independent witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("target-029 replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-029 replay did not report passed")
    replay["result"] = replay_result

    frozen_harness = (
        common.OUT
        / "provenance/frozen/implproof"
        / target_029.ARTIFACT_ID
        / "harness.rs"
    )
    verus = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus",
        [
            str(common.VERUS),
            str(frozen_harness),
            "--crate-type=lib",
        ],
        cwd=common.OUT,
    )
    verus_stdout = (common.OUT / verus["stdout"]).read_text()
    verus_stderr = (common.OUT / verus["stderr"]).read_text()
    if (
        verus["exit_code"] != 0
        or verus_stderr
        or "verification results:: 9 verified, 0 errors" not in verus_stdout
    ):
        raise RuntimeError("frozen target-029 Verus harness did not verify cleanly")
    verus["expected_summary"] = "verification results:: 9 verified, 0 errors"

    result = {
        "schema_version": 1,
        "target": target_029.TARGET,
        "input_order": target_029.INPUT_ORDER,
        "artifact_id": target_029.ARTIFACT_ID,
        "active_contract_sha256": target_029.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": target_029.ACTIVE_CONTRACT_TEXT,
        "bounded_domain": "length-2",
        "classification": RESULT_STATUSES,
        "classification_basis": (
            "The primary theorem is SAT, and its fixed model replay uses the "
            "nonmonotone [Greater, Less] profile. Independent replay confirms "
            "contract-valid Ok(0) and Err(0) executions with equal callback state "
            "that are not matching-index equivalent."
        ),
        "obligations": obligations,
        "counterexample_model": {
            "smt": target_pipeline.artifact_record(counterexample_path),
            "solver": counterexample,
        },
        "exact_output_witness": {
            "smt": target_pipeline.artifact_record(exact_witness_path),
            "solver": exact_witness,
        },
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay,
        "verus": {
            "harness": target_pipeline.artifact_record(frozen_harness),
            "run": verus,
        },
        "updated_crosswalk_fields": sorted(RESULT_STATUSES),
    }
    common.write_json(EVIDENCE_ROOT / "result.json", result)

    target_pipeline.update_crosswalk_result(
        target=target_029.TARGET,
        input_order=target_029.INPUT_ORDER,
        statuses=RESULT_STATUSES,
    )

    print("target_029=PASS")
    print("general_obligation=sat")
    print("sorted_domain_sanity=unsat")
    print("exact_output_witness=sat")
    print("witness_replay=passed")
    print("verus=9_verified,0_errors")


if __name__ == "__main__":
    main()
