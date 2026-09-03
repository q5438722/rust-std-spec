#!/usr/bin/env python3
"""Build, execute, and record the bounded target-106 evidence package."""

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
import target_106
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/targets" / target_106.ARTIFACT_ID
SOURCE_HARNESS = common.OUT / "proofs/106_core_slice_splitn_mut.rs"
RESULT_STATUSES = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
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
    text, metadata = target_106.obligation(purpose)
    target_106.validate_target_obligation(text, metadata)
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
        if row["target"] == target_106.TARGET
        and row["input_order"] == target_106.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError("target 106 is absent or duplicated in the crosswalk")
    row = matches[0]
    if (
        row["active_contract_sha256"] != target_106.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != target_106.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != target_106.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != target_106.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "admissible"
        or row["boundary_narrower_than_target"] != "yes"
        or row["equivalence_kind"] != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(target_106.boundary_manifest()["all_audited_trust_site_ids"])
    ):
        raise ValueError("target 106 crosswalk authority/boundary binding changed")
    return row


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-106 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_HARNESS.is_file():
        raise RuntimeError(f"target-106 Verus harness is missing: {SOURCE_HARNESS}")

    crosswalk_row = validate_crosswalk_identity()
    preserved_roots = {
        target_013.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_029.ARTIFACT_ID
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
    )
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: crosswalk_row[field] for field in authority_fields},
        },
    )
    boundary_path = EVIDENCE_ROOT / "boundary_manifest.json"
    common.write_json(boundary_path, target_106.boundary_manifest())

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("obligation", target_106.PRIMARY),
        ("exact_output_obligation", target_106.EXACT_OUTPUT),
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

    replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "solver_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_106.py"),
            "--evidence-root",
            str(EVIDENCE_ROOT),
            "--z3",
            z3,
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-106 independent solver replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("target-106 replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-106 replay did not report passed")
    replay["result"] = replay_result

    harness_path = EVIDENCE_ROOT / "verus/constructor_harness.rs"
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
        raise RuntimeError("target-106 Verus harness did not type-check cleanly")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(harness_path), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or "0 errors" not in verification_stdout
    ):
        raise RuntimeError("target-106 constructor Verus harness did not verify cleanly")

    target_pipeline.update_crosswalk_result(
        target=target_106.TARGET,
        input_order=target_106.INPUT_ORDER,
        statuses=RESULT_STATUSES,
        preserved_results=PRESERVED_RESULTS,
    )
    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError("target-106 pipeline mutated accepted target evidence")

    result = {
        "schema_version": 1,
        "target": target_106.TARGET,
        "input_order": target_106.INPUT_ORDER,
        "artifact_id": target_106.ARTIFACT_ID,
        "active_contract_sha256": target_106.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": target_106.ACTIVE_CONTRACT_TEXT,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": RESULT_STATUSES,
        "classification_basis": (
            "Both exact-output and full exact-state theorem negations are "
            "UNSAT. The source constructor chain fixes the complete returned "
            "iterator/private state, inner mutable-reference identity, stored "
            "predicate and unchanged callback state, and unchanged final state "
            "from one shared input while the boundary carries only input identities."
        ),
        "obligations": obligations,
        "solver_replay": replay,
        "verus": {
            "harness": target_pipeline.artifact_record(harness_path),
            "source_harness": target_pipeline.artifact_record(SOURCE_HARNESS),
            "typecheck": typecheck,
            "verification": verification,
        },
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

    print("target_106=PASS")
    print("full_exact_obligation=unsat")
    print("exact_output_obligation=unsat")
    print("solver_replay=passed")
    print("verus=constructor_model_verified")
    print("targets_013_029=preserved")


if __name__ == "__main__":
    main()
