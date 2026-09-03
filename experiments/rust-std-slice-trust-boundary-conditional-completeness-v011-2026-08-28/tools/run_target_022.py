#!/usr/bin/env python3
"""Build, execute, and record the bounded target-022 evidence package."""

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
import target_022
import target_029
import target_081
import target_106
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/targets" / target_022.ARTIFACT_ID
SOURCE_MODEL = common.OUT / "proofs/022_core_slice_as_ptr_range.rs"
PTR_SOURCE = common.RUST_LIBRARY / "core/src/ptr/const_ptr.rs"
PTR_DOCS = common.RUST_LIBRARY / "core/src/ptr/docs/add.md"
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
    (target_081.TARGET, target_081.INPUT_ORDER): {
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
    text, metadata = target_022.obligation(purpose)
    target_022.validate_target_obligation(text, metadata)
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
        if row["target"] == target_022.TARGET
        and row["input_order"] == target_022.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError("target 022 is absent or duplicated in the crosswalk")
    row = matches[0]
    if (
        row["active_contract_sha256"] != target_022.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != target_022.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != target_022.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != target_022.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"] != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(target_022.ALL_AUDITED_TRUST_SITES)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != {"TS-022-D004", "TS-022-E001"}
    ):
        raise ValueError("target 022 crosswalk authority/boundary binding changed")
    return row


def _write_text_with_hash(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"frozen binding hash mismatch: {path}")


def freeze_bound_inputs(crosswalk_row: dict[str, str]) -> dict[str, Any]:
    root = EVIDENCE_ROOT / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    text_bindings = {
        "active_contract.txt": (
            crosswalk_row["active_contract_text"],
            crosswalk_row["active_contract_sha256"],
        ),
        "generated_declaration.rs": (
            crosswalk_row["generated_declaration_text"],
            crosswalk_row["generated_declaration_sha256"],
        ),
        "slice_as_ptr_range_item.rs": (
            crosswalk_row["source_item_text"],
            crosswalk_row["source_item_sha256"],
        ),
        "slice_as_ptr_range_docs.md": (
            crosswalk_row["public_docs_text"],
            crosswalk_row["public_docs_sha256"],
        ),
    }
    records: dict[str, Any] = {}
    for filename, (text, expected_hash) in text_bindings.items():
        path = root / filename
        _write_text_with_hash(path, text, expected_hash)
        records[filename] = target_pipeline.artifact_record(path)

    copied_bindings = {
        "implproof_harness.rs": (
            crosswalk_row["frozen_harness_path"],
            crosswalk_row["harness_sha256"],
        ),
        "transformation_manifest.json": (
            crosswalk_row["frozen_transformation_manifest_path"],
            crosswalk_row["transformation_manifest_sha256"],
        ),
        "dependency_assumption_manifest.json": (
            crosswalk_row["frozen_dependency_manifest_path"],
            crosswalk_row["dependency_manifest_sha256"],
        ),
        "source_body.json": (
            crosswalk_row["frozen_source_body_manifest_path"],
            crosswalk_row["source_body_manifest_sha256"],
        ),
    }
    for filename, (relative_source, expected_hash) in copied_bindings.items():
        source = common.OUT / relative_source
        if common.sha256(source) != expected_hash:
            raise RuntimeError(f"authority input hash mismatch: {source}")
        destination = root / filename
        shutil.copyfile(source, destination)
        records[filename] = target_pipeline.artifact_record(destination)

    if common.sha256(PTR_SOURCE) != target_022.CANONICAL_PTR_SOURCE_SHA256:
        raise RuntimeError("canonical const_ptr.rs changed")
    ptr_lines = PTR_SOURCE.read_text().splitlines(keepends=True)
    ptr_item = root / "canonical_const_ptr_add.rs"
    ptr_item.write_text("".join(ptr_lines[810:864]))
    if common.sha256(ptr_item) != target_022.CANONICAL_PTR_ADD_ITEM_SHA256:
        raise RuntimeError("canonical ptr::add item span changed")
    if common.sha256(PTR_DOCS) != target_022.CANONICAL_PTR_ADD_DOCS_SHA256:
        raise RuntimeError("canonical ptr::add safety documentation changed")
    ptr_docs = root / "canonical_ptr_add_safety.md"
    shutil.copyfile(PTR_DOCS, ptr_docs)
    records["canonical_const_ptr_add.rs"] = target_pipeline.artifact_record(
        ptr_item
    )
    records["canonical_ptr_add_safety.md"] = target_pipeline.artifact_record(
        ptr_docs
    )
    return {
        "schema_version": 1,
        "canonical_sources": {
            "slice_cast": target_022.CANONICAL_SLICE_CAST_REFERENCE,
            "ptr_add": target_022.CANONICAL_PTR_ADD_REFERENCE,
            "ptr_add_safety": target_022.CANONICAL_PTR_ADD_DOCS_REFERENCE,
            "const_ptr_source_sha256": target_022.CANONICAL_PTR_SOURCE_SHA256,
        },
        "artifacts": records,
    }


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-022 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_MODEL.is_file():
        raise RuntimeError(f"target-022 Verus model is missing: {SOURCE_MODEL}")

    crosswalk_row = validate_crosswalk_identity()
    preserved_roots = {
        target_013.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_029.ARTIFACT_ID
        ),
        target_081.ARTIFACT_ID: (
            common.OUT / "evidence/targets" / target_081.ARTIFACT_ID
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
    bound_inputs_path = EVIDENCE_ROOT / "bound_inputs_manifest.json"
    common.write_json(bound_inputs_path, freeze_bound_inputs(crosswalk_row))
    boundary_path = EVIDENCE_ROOT / "boundary_manifest.json"
    common.write_json(boundary_path, target_022.boundary_manifest())

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("obligation", target_022.PRIMARY),
        ("exact_output_obligation", target_022.EXACT_OUTPUT),
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

    probes: dict[str, Any] = {}
    for name, case in target_022.PROBE_CASES.items():
        path = EVIDENCE_ROOT / "probes" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(target_022.probe_text(name))
        solver = run_solver(
            z3,
            f"probes/{name}",
            path,
            target_022.PROBE_EXPECTED_RESULTS[name],
        )
        probes[name] = {
            "case": case,
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "solver_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_022.py"),
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
        raise RuntimeError("target-022 independent solver replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("target-022 replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-022 replay did not report passed")
    replay["result"] = replay_result

    model_path = EVIDENCE_ROOT / "verus/source_transition_model.rs"
    model_path.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE_MODEL, model_path)
    typecheck = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/typecheck",
        [str(common.VERUS), str(model_path), "--crate-type=lib", "--no-verify"],
        cwd=common.OUT,
    )
    if typecheck["exit_code"] != 0 or (common.OUT / typecheck["stderr"]).read_text():
        raise RuntimeError("target-022 Verus model did not type-check cleanly")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(model_path), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or "verification results:: 2 verified, 0 errors" not in verification_stdout
        or "external_body" in model_path.read_text()
    ):
        raise RuntimeError("target-022 source-transition model did not verify cleanly")

    target_pipeline.update_crosswalk_result(
        target=target_022.TARGET,
        input_order=target_022.INPUT_ORDER,
        statuses=RESULT_STATUSES,
        preserved_results=PRESERVED_RESULTS,
    )
    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError("target-022 pipeline mutated accepted target evidence")

    result = {
        "schema_version": 1,
        "target": target_022.TARGET,
        "input_order": target_022.INPUT_ORDER,
        "artifact_id": target_022.ARTIFACT_ID,
        "active_contract_sha256": target_022.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": target_022.ACTIVE_CONTRACT_TEXT,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": RESULT_STATUSES,
        "classification_basis": (
            "The exact-output and full exact-state theorem negations are UNSAT. "
            "The source transition derives the thin start pointer from the input "
            "allocation/address/provenance and derives the end with mathematical "
            "len * element_size pointer addition under explicit isize-fit, "
            "non-null/alignment and no-wrap requirements. Allocation provenance "
            "and in-allocation one-past constraints apply only when the byte "
            "offset is nonzero."
        ),
        "obligations": obligations,
        "satisfiability_probes": probes,
        "solver_replay": replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(SOURCE_MODEL),
            "captured_model": target_pipeline.artifact_record(model_path),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": "verification results:: 2 verified, 0 errors",
        },
        "excluded_retained_trust_site_ids": list(
            target_022.EXCLUDED_RETAINED_TRUST_SITES
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

    print("target_022=PASS")
    print("full_exact_obligation=unsat")
    print("exact_output_obligation=unsat")
    print(
        "domain_probes="
        + ",".join(
            f"{name}:{target_022.PROBE_EXPECTED_RESULTS[name]}"
            for name in target_022.PROBE_CASES
        )
    )
    print("solver_replay=passed")
    print("verus=2_verified,0_errors")
    print("targets_013_029_081_106=preserved")


if __name__ == "__main__":
    main()
