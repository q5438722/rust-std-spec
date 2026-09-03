#!/usr/bin/env python3
"""Build and retain evidence for SliceIndex targets 053 through 055."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import raw_slice_pair
import replay_slice_index_trio as replay
import run_raw_slice_pair as predecessor
import slice_index_trio as trio
import target_pipeline


NOT_RUN = {field: "not-run" for field in target_pipeline.RESULT_FIELDS}
BASELINE_RESULTS = {
    **predecessor.BASELINE_RESULTS,
    **predecessor.CLUSTER_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *predecessor.PRESERVED_ARTIFACT_IDS,
    *(config.artifact_id for config in raw_slice_pair.TARGETS),
)
CLUSTER_RESULTS = {
    (config.target, config.input_order): config.expected_classification
    for config in trio.TARGETS
}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/slice_index_trio"
FROZEN_ROOT = common.OUT / "provenance/frozen"
EXPECTED_FROZEN_FILE_COUNT = 320
AUTHORITY_FIELDS = predecessor.AUTHORITY_FIELDS


def tree_digest(root: Path) -> str:
    return predecessor.tree_digest(root)


def tree_file_count(root: Path) -> int:
    return predecessor.tree_file_count(root)


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def _load_crosswalks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    csv_rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    json_rows = json.loads(
        (common.OUT / "crosswalk/target_to_proof_boundary.json").read_text()
    )
    return csv_rows, json_rows


def _write_crosswalks(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> None:
    common.write_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv",
        csv_rows,
        list(csv_rows[0]),
    )
    common.write_json(
        common.OUT / "crosswalk/target_to_proof_boundary.json",
        json_rows,
    )


def prepare_crosswalk_reset(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(csv_rows) != 62 or len(json_rows) != 62:
        raise ValueError("crosswalk must contain exactly 62 rows")
    csv_by_key = {_row_key(row): row for row in csv_rows}
    json_by_key = {_row_key(row): row for row in json_rows}
    if (
        len(csv_by_key) != 62
        or set(csv_by_key) != set(json_by_key)
        or any(csv_by_key[key] != json_by_key[key] for key in csv_by_key)
    ):
        raise ValueError("crosswalk formats are duplicate, mismatched, or divergent")

    observed: dict[tuple[str, str], dict[str, str]] = {}
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified 51-target baseline changed")
        elif key in CLUSTER_RESULTS:
            if actual not in (NOT_RUN, CLUSTER_RESULTS[key]):
                raise ValueError(f"{key}: SliceIndex result has unexpected state")
            observed[key] = actual
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    pending = all(observed[key] == NOT_RUN for key in trio.TARGET_KEYS)
    delivered = all(
        observed[key] == CLUSTER_RESULTS[key] for key in trio.TARGET_KEYS
    )
    if not (pending or delivered):
        raise ValueError("targets 053 through 055 must be uniformly delivered")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in trio.TARGET_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(trio.TARGET_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed out-of-scope row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during SliceIndex reset")
    return reset_csv, reset_json


def _validate_crosswalk_identity(
    config: trio.SliceIndexTarget,
) -> dict[str, str]:
    matches = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/target_to_proof_boundary.csv"
        )
        if _row_key(row) == (config.target, config.input_order)
    ]
    if len(matches) != 1:
        raise ValueError(f"{config.target}: authority row absent or duplicated")
    row = matches[0]
    expected_hashes = {
        "active_contract_sha256": config.active_contract_sha256,
        "retained_contract_sha256": config.active_contract_sha256,
        "generated_declaration_sha256": config.generated_declaration_sha256,
        "source_item_sha256": config.source_item_sha256,
        "public_docs_sha256": config.public_docs_sha256,
        "harness_sha256": config.harness_sha256,
        "source_body_manifest_sha256": config.source_body_manifest_sha256,
        "transformation_manifest_sha256": (
            config.transformation_manifest_sha256
        ),
        "dependency_manifest_sha256": config.dependency_manifest_sha256,
    }
    if any(row[field] != value for field, value in expected_hashes.items()):
        raise ValueError(f"{config.target}: bound authority hash changed")
    if (
        row["active_contract_text"] != config.active_contract_text
        or row["retained_contract_text"] != config.active_contract_text
        or row["contract_drift"] != "no"
        or row["source_item_start_line"] != str(config.source_start)
        or row["source_item_end_line"] != str(config.source_end)
        or row["public_docs_start_line"] != str(config.docs_start)
        or row["public_docs_end_line"] != str(config.docs_end)
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(config.all_trust_site_ids)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(config.excluded_trust_site_ids)
    ):
        raise ValueError(f"{config.target}: authority binding changed")
    return row


def _trust_site_records(
    config: trio.SliceIndexTarget,
) -> list[dict[str, str]]:
    selected = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/trust_site_inventory.csv"
        )
        if _row_key(row) == (config.target, config.input_order)
    ]
    by_id = {row["record_id"]: row for row in selected}
    if set(by_id) != set(config.all_trust_site_ids):
        raise ValueError(f"{config.target}: trust-site inventory changed")
    for record_id, expected_hash in config.trust_hashes.items():
        if trio.canonical_json_sha256(by_id[record_id]) != expected_hash:
            raise ValueError(f"{record_id}: readable trust record changed")
    for record_id in config.context_only_trust_site_ids:
        if (
            by_id[record_id]["semantic_disposition"]
            != "context-only-specification-vocabulary"
        ):
            raise ValueError(f"{record_id}: vocabulary record was relabeled")
    expected_excluded = (
        {"TS-053-D001": "inadmissible-answer-equivalent-dependency"}
        if config.input_order == "53"
        else {
            f"TS-{int(config.input_order):03d}-D002": (
                "inadmissible-answer-bearing-support"
            ),
            f"TS-{int(config.input_order):03d}-E001": (
                "inadmissible-complete-target-postcondition"
            ),
        }
    )
    if any(
        by_id[record_id]["semantic_disposition"] != disposition
        for record_id, disposition in expected_excluded.items()
    ):
        raise ValueError(f"{config.target}: excluded trust record was relabeled")
    replacement = trio.obligation_metadata(config, trio.PRIMARY)[
        "source_backed_replacements"
    ][0]
    if set(replacement["replaces_trust_site_ids"]) != set(
        config.excluded_trust_site_ids
    ):
        raise ValueError(f"{config.target}: excluded sites lack exact replacement")
    return selected


def _write_exact(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def _copy_exact(path: Path, destination: Path, expected_sha256: str) -> None:
    if not path.is_file() or common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound source hash mismatch: {path}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, destination)
    if common.sha256(destination) != expected_sha256:
        raise RuntimeError(f"bound copy hash mismatch: {destination}")


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    return "".join(lines[start - 1 : end])


def _write_bound_inputs(
    config: trio.SliceIndexTarget,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    text_files = {
        "active_contract.txt": (
            row["active_contract_text"],
            row["active_contract_sha256"],
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            row["generated_declaration_sha256"],
        ),
        "source_item.rs": (
            row["source_item_text"],
            row["source_item_sha256"],
        ),
        "public_docs.md": (
            row["public_docs_text"],
            row["public_docs_sha256"],
        ),
    }
    records: dict[str, Any] = {}
    for filename, (text, expected_hash) in text_files.items():
        path = root / filename
        _write_exact(path, text, expected_hash)
        records[filename] = target_pipeline.artifact_record(path)

    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{config.target}: shared vocabulary changed")
    vocabulary = _source_excerpt(
        vocabulary_source, *trio.SLICE_INDEX_VOCABULARY_RANGE
    )
    vocabulary_path = root / "slice_index_vocabulary.rs"
    vocabulary_path.write_text(vocabulary)
    records[vocabulary_path.name] = {
        **target_pipeline.artifact_record(vocabulary_path),
        "canonical_path": str(vocabulary_source),
        "canonical_file_sha256": row["shared_vocabulary_sha256"],
        "source_range": (
            f"{trio.SLICE_INDEX_VOCABULARY_RANGE[0]}-"
            f"{trio.SLICE_INDEX_VOCABULARY_RANGE[1]}"
        ),
    }

    slice_index_source = common.RUST_LIBRARY / trio.SLICE_INDEX_SOURCE
    index_wrapper_source = common.RUST_LIBRARY / trio.INDEX_WRAPPER_SOURCE
    slice_index_path = root / "rust_slice_index.rs"
    index_wrapper_path = root / "rust_index_wrappers.rs"
    _copy_exact(
        slice_index_source,
        slice_index_path,
        trio.SLICE_INDEX_SOURCE_SHA256,
    )
    _copy_exact(
        index_wrapper_source,
        index_wrapper_path,
        trio.INDEX_WRAPPER_SOURCE_SHA256,
    )
    records[slice_index_path.name] = {
        **target_pipeline.artifact_record(slice_index_path),
        "canonical_path": str(slice_index_source),
        "canonical_file_sha256": trio.SLICE_INDEX_SOURCE_SHA256,
    }
    records[index_wrapper_path.name] = {
        **target_pipeline.artifact_record(index_wrapper_path),
        "canonical_path": str(index_wrapper_source),
        "canonical_file_sha256": trio.INDEX_WRAPPER_SOURCE_SHA256,
    }

    frozen_files = {
        "implproof_harness.rs": (
            row["frozen_harness_path"],
            row["harness_sha256"],
        ),
        "source_body.json": (
            row["frozen_source_body_manifest_path"],
            row["source_body_manifest_sha256"],
        ),
        "transformation_manifest.json": (
            row["frozen_transformation_manifest_path"],
            row["transformation_manifest_sha256"],
        ),
        "dependency_assumption_manifest.json": (
            row["frozen_dependency_manifest_path"],
            row["dependency_manifest_sha256"],
        ),
    }
    frozen_records: dict[str, Any] = {}
    for filename, (relative_source, expected_hash) in frozen_files.items():
        source = common.OUT / relative_source
        destination = root / filename
        _copy_exact(source, destination, expected_hash)
        frozen_records[filename] = {
            **target_pipeline.artifact_record(destination),
            "frozen_source_path": relative_source,
            "frozen_source_sha256": expected_hash,
        }

    trio.validate_source_anchors(
        config,
        (root / "source_item.rs").read_text(),
        (root / "public_docs.md").read_text(),
        vocabulary_path.read_text(),
        slice_index_path.read_text(),
        index_wrapper_path.read_text(),
    )
    manifest_path = root / "manifest.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "target": config.target,
            "input_order": config.input_order,
            "active_contract_sha256": config.active_contract_sha256,
            "files": records,
            "frozen_implproof": frozen_records,
            "trust_record_ids": list(config.all_trust_site_ids),
            "modeled_sliceindex_forms": [
                form.name for form in config.covered_forms
            ],
        },
    )
    return manifest_path


def _run_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    path: Path,
    expected: str,
    *,
    require_payload: bool = False,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
        [z3, "-smt2", str(path)],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    stdout = (common.OUT / record["stdout"]).read_text()
    if require_payload and len(stdout.splitlines()) < 2:
        raise RuntimeError(f"{label}: SAT source/witness payload is missing")
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
            "model_retained": require_payload,
        }
    )
    return record


def _run_target(
    config: trio.SliceIndexTarget,
    z3: str,
) -> dict[str, Any]:
    row = _validate_crosswalk_identity(config)
    trust_records = _trust_site_records(config)
    evidence_root = EVIDENCE_BASE / config.artifact_id
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    evidence_root.mkdir(parents=True)

    authority_path = evidence_root / "authority_bindings.json"
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: row[field] for field in AUTHORITY_FIELDS},
        },
    )
    trust_path = evidence_root / "trust_site_bindings.json"
    common.write_json(
        trust_path,
        {
            "schema_version": 1,
            "target": config.target,
            "records": trust_records,
        },
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, trio.boundary_manifest(config))
    bound_inputs_path = _write_bound_inputs(config, row, evidence_root)
    contract_audit_path = evidence_root / "contract_translation_audit.json"
    common.write_json(
        contract_audit_path,
        {
            "schema_version": 1,
            "target": config.target,
            "active_contract_sha256": config.active_contract_sha256,
            "opaque_vocabulary_is_solver_function": False,
            "canonical_source_result_conjoined_to_spec": (
                config.exhaustive_index_coverage
            ),
            "canonical_result_policy": (
                "faithful expansion of slice_index_result across all 25 sealed forms"
                if config.exhaustive_index_coverage
                else "diagnostic only; omitted from Spec_T"
            ),
            "covered_sliceindex_forms": [
                form.name for form in config.covered_forms
            ],
            "coverage_complete_for_claim": True,
            "source_backed_replacement_id": config.replacement_id,
        },
    )

    obligations: dict[str, Any] = {}
    for purpose, stem in (
        (trio.PRIMARY, "obligation"),
        (trio.EXACT_OUTPUT, "exact_output_obligation"),
    ):
        text, metadata = trio.obligation(config, purpose)
        trio.validate_target_obligation(config, text, metadata)
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        solver = _run_solver(
            z3,
            evidence_root,
            stem,
            smt_path,
            config.expected_results[purpose],
        )
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    source_instances: dict[str, Any] = {}
    for name in trio.source_cases(config):
        path = evidence_root / "source_instances" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(trio.source_instance_text(config, name))
        solver = _run_solver(
            z3,
            evidence_root,
            f"source_instances/{name}",
            path,
            "sat",
            require_payload=True,
        )
        source_instances[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    negative_probes: dict[str, Any] = {}
    for name in trio.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(trio.negative_probe_text(config, name))
        solver = _run_solver(
            z3,
            evidence_root,
            f"negative_probes/{name}",
            path,
            "unsat",
        )
        negative_probes[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    witness: dict[str, Any] | None = None
    if config.mutable:
        smt_path = evidence_root / "fixed_reference_witness.smt2"
        payload_path = evidence_root / "fixed_reference_witness.json"
        smt_path.write_text(trio.fixed_witness_text(config))
        common.write_json(payload_path, trio.witness_payload(config))
        solver = _run_solver(
            z3,
            evidence_root,
            "fixed_reference_witness",
            smt_path,
            "sat",
            require_payload=True,
        )
        witness = {
            "smt": target_pipeline.artifact_record(smt_path),
            "payload": target_pipeline.artifact_record(payload_path),
            "solver": solver,
        }

    replay_record = target_pipeline.capture_command(
        evidence_root / "solver_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_slice_index_trio.py"),
            "--evidence-root",
            str(evidence_root),
            "--z3",
            z3,
            "--artifact-id",
            config.artifact_id,
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay_record["stdout"]).read_text()
    replay_stderr = (common.OUT / replay_record["stderr"]).read_text()
    if replay_record["exit_code"] != 0 or replay_stderr:
        raise RuntimeError(f"{config.target}: independent solver replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{config.target}: replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{config.target}: replay did not report passed")
    replay_record["result"] = replay_result

    source_model = common.OUT / config.proof_filename
    captured_model = evidence_root / "verus/source_and_contract_model.rs"
    captured_model.parent.mkdir(parents=True)
    shutil.copyfile(source_model, captured_model)
    if "external_body" in captured_model.read_text():
        raise RuntimeError(f"{config.target}: Verus model contains external_body")
    typecheck = target_pipeline.capture_command(
        evidence_root / "verus/typecheck",
        [
            str(common.VERUS),
            str(captured_model),
            "--crate-type=lib",
            "--no-verify",
        ],
        cwd=common.OUT,
    )
    if (
        typecheck["exit_code"] != 0
        or (common.OUT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError(f"{config.target}: Verus model did not type-check")
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or config.verus_expected_summary not in verification_stdout
    ):
        raise RuntimeError(f"{config.target}: Verus model did not verify")

    classification_basis = (
        "Both literal theorem negations are UNSAT after source-backed "
        "normalization of all 25 sealed Rust 1.96 SliceIndex forms. Every "
        "form has a retained SAT source instance, and no uninterpreted "
        "slice_index_result function is present."
        if config.exhaustive_index_coverage
        else "Both literal theorem negations are SAT for the valid concrete "
        "usize index 0 on a length-three slice. The canonical element-0 "
        "reference and a distinct well-formed element-1 reference satisfy "
        "the same active contract, input boundary, and exact final state; "
        "the source-selected reference is not injected into Spec_T."
    )
    result = {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "artifact_id": config.artifact_id,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "classification": config.expected_classification,
        "classification_basis": classification_basis,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "trust_site_bindings": target_pipeline.artifact_record(trust_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "contract_translation_audit": target_pipeline.artifact_record(
            contract_audit_path
        ),
        "obligations": obligations,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
        "fixed_reference_witness": witness,
        "solver_replay": replay_record,
        "verus": {
            "source_model": target_pipeline.artifact_record(source_model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": config.verus_expected_summary,
        },
        "sealed_sliceindex_coverage": [
            {
                "tag": form.tag,
                "name": form.name,
                "source_reference": form.source_reference,
            }
            for form in config.covered_forms
        ],
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "context_only_trust_site_ids": list(
            config.context_only_trust_site_ids
        ),
        "remaining_not_run_rows": 8,
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
        "independent_review": "required",
        "stage_transition": "disabled",
    }
    common.write_json(evidence_root / "result.json", result)
    return result


def _update_ledgers() -> None:
    csv_rows, json_rows = _load_crosswalks()
    preserved = copy.deepcopy(BASELINE_RESULTS)
    updated_csv = csv_rows
    updated_json = json_rows
    for config in trio.TARGETS:
        statuses = CLUSTER_RESULTS[(config.target, config.input_order)]
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            updated_csv,
            updated_json,
            target=config.target,
            input_order=config.input_order,
            statuses=statuses,
            preserved_results=preserved,
        )
        preserved[(config.target, config.input_order)] = statuses
    _write_crosswalks(updated_csv, updated_json)
    classified = {
        _row_key(row)
        for row in updated_csv
        if any(
            row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS
        )
    }
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in updated_csv
    )
    if classified != set(preserved) or len(classified) != 54 or not_run != 8:
        raise RuntimeError(
            f"expected 54 classified and 8 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for SliceIndex trio evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 51 or len(PRESERVED_ARTIFACT_IDS) != 51:
        raise RuntimeError("certified predecessor baseline is not 51 targets")
    if tree_file_count(FROZEN_ROOT) != EXPECTED_FROZEN_FILE_COUNT:
        raise RuntimeError("frozen input tree does not contain exactly 320 files")
    for config in trio.TARGETS:
        if not (common.OUT / config.proof_filename).is_file():
            raise RuntimeError(f"{config.target}: Verus model is missing")

    before_csv, before_json = _load_crosswalks()
    reset_csv, reset_json = prepare_crosswalk_reset(before_csv, before_json)
    preserved_roots = {
        artifact_id: EVIDENCE_BASE / artifact_id
        for artifact_id in PRESERVED_ARTIFACT_IDS
    }
    preserved_before = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    frozen_before = tree_digest(FROZEN_ROOT)
    mutable_roots = {
        config.artifact_id: EVIDENCE_BASE / config.artifact_id
        for config in trio.TARGETS
    }
    mutable_roots["slice_index_trio"] = CLUSTER_ROOT

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".slice-index-trio-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        existing: set[str] = set()
        for name, path in mutable_roots.items():
            if path.exists():
                shutil.copytree(path, backup_root / name)
                existing.add(name)
        try:
            _write_crosswalks(reset_csv, reset_json)
            results = {
                config.artifact_id: _run_target(config, z3)
                for config in trio.TARGETS
            }
            _update_ledgers()
            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = tree_digest(FROZEN_ROOT)
            if preserved_after != preserved_before:
                raise RuntimeError("SliceIndex run mutated accepted target evidence")
            if (
                frozen_after != frozen_before
                or tree_file_count(FROZEN_ROOT) != EXPECTED_FROZEN_FILE_COUNT
            ):
                raise RuntimeError("SliceIndex run mutated frozen inputs")

            if CLUSTER_ROOT.exists():
                shutil.rmtree(CLUSTER_ROOT)
            CLUSTER_ROOT.mkdir(parents=True)
            manifest_path = CLUSTER_ROOT / "manifest.json"
            common.write_json(
                manifest_path,
                {
                    "schema_version": 1,
                    "targets": [
                        {
                            "target": config.target,
                            "input_order": config.input_order,
                            "artifact_id": config.artifact_id,
                            "classification": config.expected_classification,
                            "result": target_pipeline.artifact_record(
                                EVIDENCE_BASE
                                / config.artifact_id
                                / "result.json"
                            ),
                        }
                        for config in trio.TARGETS
                    ],
                    "preserved_target_evidence": {
                        artifact_id: {
                            "before_sha256": preserved_before[artifact_id],
                            "after_sha256": preserved_after[artifact_id],
                        }
                        for artifact_id in sorted(preserved_roots)
                    },
                    "frozen_inputs": {
                        "file_count": EXPECTED_FROZEN_FILE_COUNT,
                        "before_sha256": frozen_before,
                        "after_sha256": frozen_after,
                    },
                    "classified_rows": 54,
                    "not_run_rows": 8,
                    "independent_review": "required",
                    "stage_transition": "disabled",
                },
            )
            results["cluster_manifest"] = target_pipeline.artifact_record(
                manifest_path
            )
        except Exception:
            _write_crosswalks(before_csv, before_json)
            for name, path in mutable_roots.items():
                if path.exists():
                    shutil.rmtree(path)
                if name in existing:
                    shutil.copytree(backup_root / name, path)
            raise

    print("slice_index_trio=PASS")
    for config in trio.TARGETS:
        print(
            f"target_{config.input_order}="
            f"{config.expected_results[trio.PRIMARY]}/"
            f"{config.expected_classification['completeness_modulo_reviewed_equivalence_status']}"
        )
    print("target_054_sealed_sliceindex_forms=25")
    print("targets_053_055_concrete_reference_witnesses=sat")
    print("preserved_target_evidence=51")
    print("frozen_inputs=320")
    print("target_result_counts=54_classified,8_not-run")


if __name__ == "__main__":
    main()
