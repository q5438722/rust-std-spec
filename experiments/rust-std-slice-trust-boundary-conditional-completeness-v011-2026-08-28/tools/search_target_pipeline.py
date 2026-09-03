#!/usr/bin/env python3
"""Evidence capture for the source-backed Slice search-wrapper targets."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import campaign_common as common
import search_family
import target_pipeline


INCOMPLETE = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
}
COMPLETE = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
}
BASELINE_RESULTS = {
    ("core::slice::as_chunks_mut", "13"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    },
    ("core::slice::as_mut_ptr", "19"): COMPLETE,
    ("core::slice::as_mut_ptr_range", "20"): COMPLETE,
    ("core::slice::as_ptr", "21"): COMPLETE,
    ("core::slice::as_ptr_range", "22"): COMPLETE,
    ("core::slice::binary_search_by", "29"): INCOMPLETE,
    ("core::slice::get_disjoint_mut", "51"): INCOMPLETE,
    ("core::slice::get_disjoint_unchecked_mut", "52"): INCOMPLETE,
    ("core::slice::sort_unstable_by", "81"): INCOMPLETE,
    ("core::slice::splitn_mut", "106"): COMPLETE,
    ("core::slice::write_copy_of_slice", "120"): COMPLETE,
}
BASELINE_ARTIFACT_IDS = (
    "013_core_slice_as_chunks_mut",
    "019_core_slice_as_mut_ptr",
    "020_core_slice_as_mut_ptr_range",
    "021_core_slice_as_ptr",
    "022_core_slice_as_ptr_range",
    "029_core_slice_binary_search_by",
    "051_core_slice_get_disjoint_mut",
    "052_core_slice_get_disjoint_unchecked_mut",
    "081_core_slice_sort_unstable_by",
    "106_core_slice_splitn_mut",
    "120_core_slice_write_copy_of_slice",
)
AUTHORITY_FIELDS = (
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


def validate_crosswalk_identity(module: ModuleType) -> dict[str, str]:
    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    matches = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError(f"{module.TARGET} is absent or duplicated in the crosswalk")
    row = matches[0]
    expected_equivalence = (
        "exact-principal-return-and-final-state"
        if module.CONFIG.kind == "partition"
        else "matching-index-equivalence"
    )
    if (
        row["active_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"] != expected_equivalence
        or set(row["all_trust_site_ids"].split(";"))
        != set(module.ALL_AUDITED_TRUST_SITES)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        raise ValueError(
            f"{module.TARGET}: crosswalk authority/boundary binding changed"
        )
    return row


def _write_text_with_hash(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"frozen binding hash mismatch: {path}")


def _lower_dependency() -> dict[str, Any]:
    root = common.OUT / "evidence/targets" / search_family.LOWER_ARTIFACT_ID
    result_path = root / "result.json"
    obligation_path = root / "obligation.smt2"
    metadata_path = root / "obligation.metadata.json"
    review_path = common.OUT / "review/REVIEW_ACCEPTANCE_20260831T110316Z.md"
    required = (result_path, obligation_path, metadata_path, review_path)
    if not all(path.is_file() for path in required):
        raise RuntimeError("accepted target-029 lower-transition evidence is missing")
    result = json.loads(result_path.read_text())
    if (
        result.get("target") != search_family.LOWER_TARGET
        or result.get("active_contract_sha256")
        != search_family.LOWER_ACTIVE_CONTRACT_SHA256
        or result.get("classification") != INCOMPLETE
    ):
        raise RuntimeError("target-029 lower-transition evidence is not accepted")
    return {
        "target": search_family.LOWER_TARGET,
        "artifact_id": search_family.LOWER_ARTIFACT_ID,
        "active_contract_sha256": search_family.LOWER_ACTIVE_CONTRACT_SHA256,
        "admission_mode": (
            "reviewed relational transition only; no selected index or "
            "returned Result enters Boundary_T"
        ),
        "result": target_pipeline.artifact_record(result_path),
        "obligation": target_pipeline.artifact_record(obligation_path),
        "metadata": target_pipeline.artifact_record(metadata_path),
        "independent_review": target_pipeline.artifact_record(review_path),
    }


def freeze_bound_inputs(
    module: ModuleType,
    evidence_root: Path,
    crosswalk_row: dict[str, str],
) -> dict[str, Any]:
    root = evidence_root / "bound_inputs"
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
        module.CONFIG.source_item_filename: (
            crosswalk_row["source_item_text"],
            crosswalk_row["source_item_sha256"],
        ),
        module.CONFIG.source_docs_filename: (
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

    canonical = common.RUST_LIBRARY / search_family.SLICE_SOURCE_PATH
    if common.sha256(canonical) != search_family.SLICE_SOURCE_SHA256:
        raise RuntimeError("canonical Rust Slice source hash changed")
    excerpt = "".join(
        canonical.read_text().splitlines(keepends=True)[
            search_family.LOWER_SOURCE_START - 1 : search_family.LOWER_SOURCE_END
        ]
    )
    lower_path = root / "canonical_binary_search_by.rs"
    _write_text_with_hash(
        lower_path, excerpt, search_family.LOWER_SOURCE_SHA256
    )
    records[lower_path.name] = target_pipeline.artifact_record(lower_path)
    return {
        "schema_version": 1,
        "artifacts": records,
        "canonical_lower_transition": {
            "source_path": search_family.SLICE_SOURCE_PATH,
            "source_span": (
                f"{search_family.LOWER_SOURCE_START}-"
                f"{search_family.LOWER_SOURCE_END}"
            ),
            "source_file_sha256": search_family.SLICE_SOURCE_SHA256,
            "excerpt_sha256": search_family.LOWER_SOURCE_SHA256,
            "artifact": lower_path.name,
        },
        "accepted_lower_dependency": _lower_dependency(),
    }


def _run_solver(
    evidence_root: Path,
    z3: str,
    label: str,
    smt_path: Path,
    expected: str,
    *,
    require_payload: bool = False,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
        [z3, "-smt2", str(smt_path)],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    lines = (common.OUT / record["stdout"]).read_text().splitlines()
    if require_payload and expected == "sat" and len(lines) < 2:
        raise RuntimeError(f"{label}: SAT evidence lacks concrete get-value output")
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
        }
    )
    return record


def _validate_result_counts(
    module: ModuleType,
    preserved_results: dict[tuple[str, str], dict[str, str]],
    expected_not_run: int,
) -> None:
    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    classified = {
        (row["target"], row["input_order"])
        for row in rows
        if row["exact_output_determinism_status"] != "not-run"
        or row["completeness_modulo_reviewed_equivalence_status"] != "not-run"
    }
    if classified != set(preserved_results) | {
        (module.TARGET, module.INPUT_ORDER)
    }:
        raise RuntimeError(f"{module.CONFIG.label}: classified target set changed")
    not_run = sum(
        row["exact_output_determinism_status"] == "not-run"
        and row["completeness_modulo_reviewed_equivalence_status"] == "not-run"
        for row in rows
    )
    if not_run != expected_not_run:
        raise RuntimeError(
            f"{module.CONFIG.label}: expected {expected_not_run} not-run rows, "
            f"got {not_run}"
        )


def run(
    module: ModuleType,
    replay_module: ModuleType,
    *,
    preserved_results: dict[tuple[str, str], dict[str, str]],
    preserved_artifact_ids: tuple[str, ...],
    expected_not_run: int,
    source_model: Path,
) -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for search target evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not source_model.is_file():
        raise RuntimeError(f"Verus source-transition model is missing: {source_model}")

    evidence_root = common.OUT / "evidence/targets" / module.ARTIFACT_ID
    crosswalk_row = validate_crosswalk_identity(module)
    preserved_roots = {
        artifact_id: common.OUT / "evidence/targets" / artifact_id
        for artifact_id in preserved_artifact_ids
    }
    preserved_before = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    evidence_root.mkdir(parents=True)

    authority_path = evidence_root / "authority_bindings.json"
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {
                field: crosswalk_row[field] for field in AUTHORITY_FIELDS
            },
        },
    )
    bound_inputs_path = evidence_root / "bound_inputs_manifest.json"
    common.write_json(
        bound_inputs_path,
        freeze_bound_inputs(module, evidence_root, crosswalk_row),
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, module.boundary_manifest())

    obligations: dict[str, dict[str, Any]] = {}
    obligation_specs = (
        ("obligation", module.PRIMARY),
        (
            "partitioned_domain_sanity"
            if module.CONFIG.kind == "partition"
            else "ordered_domain_sanity",
            module.SANITY,
        ),
        ("exact_output_obligation", module.EXACT_OUTPUT),
    )
    for filename, purpose in obligation_specs:
        text, metadata = module.obligation(purpose)
        module.validate_target_obligation(text, metadata)
        smt_path = evidence_root / f"{filename}.smt2"
        metadata_path = evidence_root / f"{filename}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        solver = _run_solver(
            evidence_root,
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

    witness_path = evidence_root / "witness.json"
    common.write_json(witness_path, module.witness_payload())
    fixed_models: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("counterexample_model", module.PRIMARY),
        ("exact_output_witness", module.EXACT_OUTPUT),
    ):
        path = evidence_root / f"{filename}.smt2"
        path.write_text(module.fixed_model_text(purpose))
        fixed_models[purpose] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                evidence_root,
                z3,
                filename,
                path,
                "sat",
                require_payload=True,
            ),
        }

    replay_script = (
        common.OUT / "tools" / f"replay_target_{int(module.INPUT_ORDER):03d}.py"
    )
    replay = target_pipeline.capture_command(
        evidence_root / "witness_replay",
        [
            sys.executable,
            str(replay_script),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError(f"{module.CONFIG.label}: witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"{module.CONFIG.label}: replay did not emit JSON"
        ) from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{module.CONFIG.label}: replay did not report passed")
    replay["result"] = replay_result

    captured_model = evidence_root / "verus/source_transition_model.rs"
    captured_model.parent.mkdir(parents=True)
    shutil.copyfile(source_model, captured_model)
    typecheck = target_pipeline.capture_command(
        evidence_root / "verus/typecheck",
        [str(common.VERUS), str(captured_model), "--crate-type=lib", "--no-verify"],
        cwd=common.OUT,
    )
    if (
        typecheck["exit_code"] != 0
        or (common.OUT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError(f"{module.CONFIG.label}: Verus type-check failed")
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or module.VERUS_EXPECTED_SUMMARY not in verification_stdout
        or "external_body" in captured_model.read_text()
    ):
        raise RuntimeError(f"{module.CONFIG.label}: Verus verification failed")

    target_pipeline.update_crosswalk_result(
        target=module.TARGET,
        input_order=module.INPUT_ORDER,
        statuses=INCOMPLETE,
        preserved_results=preserved_results,
    )
    _validate_result_counts(module, preserved_results, expected_not_run)
    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError(
            f"{module.CONFIG.label}: certified evidence was mutated"
        )

    result = {
        "schema_version": 1,
        "target": module.TARGET,
        "input_order": module.INPUT_ORDER,
        "artifact_id": module.ARTIFACT_ID,
        "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": module.ACTIVE_CONTRACT_TEXT,
        "bounded_domain": "length-2",
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": INCOMPLETE,
        "classification_basis": module.CONFIG.classification_basis,
        "obligations": obligations,
        "fixed_sat_replays": fixed_models,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(source_model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": module.VERUS_EXPECTED_SUMMARY,
        },
        "accepted_lower_dependency": _lower_dependency(),
        "excluded_retained_trust_site_ids": list(
            module.EXCLUDED_RETAINED_TRUST_SITES
        ),
        "preserved_target_evidence": {
            artifact_id: {
                "before_sha256": preserved_before[artifact_id],
                "after_sha256": preserved_after[artifact_id],
            }
            for artifact_id in sorted(preserved_roots)
        },
        "updated_crosswalk_fields": sorted(INCOMPLETE),
        "remaining_not_run": expected_not_run,
    }
    common.write_json(evidence_root / "result.json", result)

    print(f"target_{int(module.INPUT_ORDER):03d}=PASS")
    print("general_obligation=sat")
    print(f"{module.SANITY.replace('-', '_')}=unsat")
    print("exact_output_obligation=sat")
    print("fixed_sat_replays=passed")
    print("witness_replay=passed")
    print("verus=3_verified,0_errors")
    print(f"not_run={expected_not_run}")
