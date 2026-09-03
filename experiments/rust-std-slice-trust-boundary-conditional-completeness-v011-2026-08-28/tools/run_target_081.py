#!/usr/bin/env python3
"""Build, execute, and record the bounded target-081 evidence package."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import target_013
import target_029
import target_081
import target_106
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/targets" / target_081.ARTIFACT_ID
SOURCE_HARNESS = common.OUT / "proofs/081_core_slice_sort_unstable_by.rs"
RESULT_STATUSES = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": (
        "conditional-incomplete"
    ),
}
PRESERVED_RESULTS = {
    (target_013.TARGET, target_013.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    },
    (target_029.TARGET, target_029.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    },
    (target_106.TARGET, target_106.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    },
}


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.is_dir():
        raise ValueError(f"required preserved evidence directory is missing: {root}")
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def write_obligation(
    filename: str,
    purpose: str,
) -> tuple[Path, Path, dict[str, Any]]:
    text, metadata = target_081.obligation(purpose)
    target_081.validate_target_obligation(text, metadata)
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


def validate_crosswalk_identity() -> dict[str, str]:
    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    matches = [
        row
        for row in rows
        if row["target"] == target_081.TARGET
        and row["input_order"] == target_081.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError("target 081 is absent or duplicated in the crosswalk")
    row = matches[0]
    if (
        row["active_contract_sha256"] != target_081.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != target_081.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != target_081.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != target_081.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(target_081.EXCLUDED_RETAINED_TRUST_SITES)
        or row["equivalence_kind"] != "equal-key-reordering-equivalence"
        or set(row["all_trust_site_ids"].split(";"))
        != set(target_081.ALL_AUDITED_TRUST_SITES)
    ):
        raise ValueError("target 081 crosswalk authority/boundary binding changed")
    return row


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-081 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_HARNESS.is_file():
        raise RuntimeError(f"target-081 Verus harness is missing: {SOURCE_HARNESS}")

    crosswalk_row = validate_crosswalk_identity()
    preserved_roots = {
        target_013.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_029.ARTIFACT_ID
        ),
        target_106.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_106.ARTIFACT_ID
        ),
    }
    preserved_before = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if EVIDENCE_ROOT.exists():
        shutil.rmtree(EVIDENCE_ROOT)
    EVIDENCE_ROOT.mkdir(parents=True)

    authority_path = EVIDENCE_ROOT / "authority_bindings.json"
    authority_fields = (
        "target",
        "input_order",
        "active_run_id",
        "active_contract_text",
        "active_contract_sha256",
        "retained_contract_text",
        "retained_contract_sha256",
        "generated_declaration_path",
        "generated_declaration_text",
        "generated_declaration_sha256",
        "source_path",
        "source_item_text",
        "source_item_sha256",
        "public_docs_reference",
        "public_docs_text",
        "public_docs_sha256",
        "frozen_harness_path",
        "harness_sha256",
        "frozen_transformation_manifest_path",
        "transformation_manifest_sha256",
        "frozen_dependency_manifest_path",
        "dependency_manifest_sha256",
        "frozen_source_body_manifest_path",
        "source_body_manifest_sha256",
        "all_trust_site_ids",
        "inadmissible_trust_site_ids",
    )
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: crosswalk_row[field] for field in authority_fields},
        },
    )
    boundary_path = EVIDENCE_ROOT / "boundary_manifest.json"
    common.write_json(boundary_path, target_081.boundary_manifest())

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("obligation", target_081.PRIMARY),
        ("total_order_sanity", target_081.TOTAL_ORDER_SANITY),
        ("exact_final_slice_obligation", target_081.EXACT_FINAL_SLICE),
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
    common.write_json(witness_path, target_081.witness_payload())

    general_model_path = EVIDENCE_ROOT / "counterexample_model.smt2"
    general_model_path.write_text(target_081.fixed_model_text(target_081.PRIMARY))
    general_model = run_solver(
        z3,
        "counterexample_model",
        general_model_path,
        "sat",
    )

    exact_model_path = EVIDENCE_ROOT / "exact_final_slice_witness.smt2"
    exact_model_path.write_text(
        target_081.fixed_model_text(target_081.EXACT_FINAL_SLICE)
    )
    exact_model = run_solver(
        z3,
        "exact_final_slice_witness",
        exact_model_path,
        "sat",
    )

    replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_081.py"),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-081 independent witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("target-081 replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-081 replay did not report passed")
    replay["result"] = replay_result

    harness_path = EVIDENCE_ROOT / "verus/contract_model.rs"
    harness_path.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE_HARNESS, harness_path)
    typecheck = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/typecheck",
        [str(common.VERUS), str(harness_path), "--crate-type=lib", "--no-verify"],
        cwd=common.OUT,
    )
    if (
        typecheck["exit_code"] != 0
        or (common.OUT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError("target-081 Verus model did not type-check cleanly")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(harness_path), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or "verification results:: 3 verified, 0 errors" not in verification_stdout
    ):
        raise RuntimeError("target-081 Verus model did not verify cleanly")

    target_pipeline.update_crosswalk_result(
        target=target_081.TARGET,
        input_order=target_081.INPUT_ORDER,
        statuses=RESULT_STATUSES,
        preserved_results=PRESERVED_RESULTS,
    )
    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError("target-081 pipeline mutated accepted target evidence")

    result = {
        "schema_version": 1,
        "target": target_081.TARGET,
        "input_order": target_081.INPUT_ORDER,
        "artifact_id": target_081.ARTIFACT_ID,
        "active_contract_sha256": target_081.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": target_081.ACTIVE_CONTRACT_TEXT,
        "bounded_domain": "length-3 distinct identities",
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": RESULT_STATUSES,
        "classification_basis": (
            "The exact-final-slice theorem is SAT for a total comparator with "
            "two equal identities. The reviewed-equivalence theorem is SAT for "
            "a fixed non-total comparator that orders the same two identities "
            "Less in both directions. Both executions satisfy exact multiplicity "
            "and comparator-sortedness under one shared boundary, while the "
            "total-order sanity theorem is UNSAT."
        ),
        "obligations": obligations,
        "general_counterexample_model": {
            "smt": target_pipeline.artifact_record(general_model_path),
            "solver": general_model,
        },
        "exact_final_slice_witness": {
            "smt": target_pipeline.artifact_record(exact_model_path),
            "solver": exact_model,
        },
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(SOURCE_HARNESS),
            "captured_model": target_pipeline.artifact_record(harness_path),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": "verification results:: 3 verified, 0 errors",
        },
        "excluded_retained_trust_site_ids": list(
            target_081.EXCLUDED_RETAINED_TRUST_SITES
        ),
        "preserved_target_evidence": {
            artifact_id: {
                "before_sha256": preserved_before[artifact_id],
                "after_sha256": preserved_after[artifact_id],
            }
            for artifact_id in sorted(preserved_roots)
        },
        "updated_crosswalk_fields": sorted(RESULT_STATUSES),
    }
    common.write_json(EVIDENCE_ROOT / "result.json", result)

    print("target_081=PASS")
    print("general_reviewed_equivalence=sat")
    print("total_order_sanity=unsat")
    print("exact_final_slice=sat")
    print("witness_replay=passed")
    print("verus=3_verified,0_errors")
    print("targets_013_029_106=preserved")


if __name__ == "__main__":
    main()
