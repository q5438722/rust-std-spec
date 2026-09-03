#!/usr/bin/env python3
"""Build and replay the ordered five-target chunk contract-drift increment."""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import chunk_contract_drift_cluster as cluster
import pointer_cast_cluster
import target_pipeline


COMPLETE = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
}
EXACT_ONLY = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
}
NOT_RUN = {
    "exact_output_determinism_status": "not-run",
    "completeness_modulo_reviewed_equivalence_status": "not-run",
}
BASELINE_RESULTS = {
    ("core::slice::as_chunks_mut", "13"): EXACT_ONLY,
    ("core::slice::as_mut_ptr", "19"): COMPLETE,
    ("core::slice::as_mut_ptr_range", "20"): COMPLETE,
    ("core::slice::as_ptr", "21"): COMPLETE,
    ("core::slice::as_ptr_range", "22"): COMPLETE,
    ("core::slice::binary_search", "28"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::binary_search_by", "29"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::binary_search_by_key", "30"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::get_disjoint_mut", "51"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::get_disjoint_unchecked_mut", "52"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::partition_point", "65"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::sort_unstable_by", "81"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::splitn_mut", "106"): COMPLETE,
    ("core::slice::write_copy_of_slice", "120"): COMPLETE,
}
BASELINE_ARTIFACT_IDS = (
    "013_core_slice_as_chunks_mut",
    "019_core_slice_as_mut_ptr",
    "020_core_slice_as_mut_ptr_range",
    "021_core_slice_as_ptr",
    "022_core_slice_as_ptr_range",
    "028_core_slice_binary_search",
    "029_core_slice_binary_search_by",
    "030_core_slice_binary_search_by_key",
    "051_core_slice_get_disjoint_mut",
    "052_core_slice_get_disjoint_unchecked_mut",
    "065_core_slice_partition_point",
    "081_core_slice_sort_unstable_by",
    "106_core_slice_splitn_mut",
    "120_core_slice_write_copy_of_slice",
)
CLUSTER_KEYS = tuple(
    (config.target, config.input_order) for config in cluster.ORDERED_TARGETS
)
AUTHORITY_FIELDS = (
    "target",
    "input_order",
    "active_run_id",
    "active_contract_text",
    "active_contract_sha256",
    "retained_contract_text",
    "retained_contract_sha256",
    "contract_drift",
    "generated_declaration_path",
    "generated_declaration_start_line",
    "generated_declaration_end_line",
    "generated_declaration_text",
    "generated_declaration_sha256",
    "source_path",
    "source_item_start_line",
    "source_item_end_line",
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
    "equivalence_kind",
)


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ValueError(f"required evidence tree is missing: {root}")
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


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
        raise ValueError("crosswalk CSV/JSON are duplicate, mismatched, or divergent")

    cluster_results = {
        (config.target, config.input_order): config.expected_results
        for config in cluster.ORDERED_TARGETS
    }
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified baseline result changed")
        elif key in cluster_results:
            if actual not in (NOT_RUN, cluster_results[key]):
                raise ValueError(f"{key}: chunk result has unexpected state")
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope result is classified")

    updated_csv = copy.deepcopy(csv_rows)
    updated_json = copy.deepcopy(json_rows)
    for rows in (updated_csv, updated_json):
        by_key = {_row_key(row): row for row in rows}
        for key in CLUSTER_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, updated_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(CLUSTER_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed a non-cluster row")
    if updated_csv != updated_json:
        raise ValueError("crosswalk formats diverged during reset")
    return updated_csv, updated_json


def _write_text_with_hash(path: Path, text: str, expected: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def _copy_with_hash(path: Path, source: Path, expected: str) -> None:
    if common.sha256(source) != expected:
        raise RuntimeError(f"authority input hash mismatch: {source}")
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, path)


def _source_excerpt(
    source: Path,
    start: int,
    end: int,
    destination: Path,
) -> dict[str, Any]:
    lines = source.read_text().splitlines(keepends=True)
    destination.write_text("".join(lines[start - 1 : end]))
    return {
        "source_path": str(source),
        "source_span": f"{start}-{end}",
        "source_file_sha256": common.sha256(source),
        "artifact": target_pipeline.artifact_record(destination),
    }


def _accepted_pointer_dependency(config: cluster.ChunkTarget) -> dict[str, Any]:
    pointer_config = (
        pointer_cast_cluster.TARGET_019
        if config.mutable
        else pointer_cast_cluster.TARGET_021
    )
    root = common.OUT / "evidence/targets" / pointer_config.artifact_id
    result_path = root / "result.json"
    model_path = common.OUT / "proofs" / (
        "019_core_slice_as_mut_ptr.rs"
        if config.mutable
        else "021_core_slice_as_ptr.rs"
    )
    review_path = (
        common.OUT / "review/REVIEW_ACCEPTANCE_20260831T173550Z.md"
    )
    result = json.loads(result_path.read_text())
    if (
        result.get("target") != pointer_config.target
        or result.get("classification") != COMPLETE
        or result.get("active_contract_sha256")
        != pointer_config.active_contract_sha256
        or not model_path.is_file()
        or not review_path.is_file()
    ):
        raise RuntimeError(
            f"{config.artifact_id}: accepted pointer dependency is unavailable"
        )
    return {
        "target": pointer_config.target,
        "artifact_id": pointer_config.artifact_id,
        "active_contract_sha256": pointer_config.active_contract_sha256,
        "admission_mode": (
            "defined allocation/address/provenance cast transition only; "
            "no returned pointer is copied into Boundary_T"
        ),
        "result": target_pipeline.artifact_record(result_path),
        "source_model": target_pipeline.artifact_record(model_path),
        "independent_review": target_pipeline.artifact_record(review_path),
    }


def _ordered_lower_dependency(
    config: cluster.ChunkTarget,
) -> dict[str, Any] | None:
    if config.lower_dependency is None:
        return None
    lower_config = next(
        item
        for item in cluster.ORDERED_TARGETS
        if item.artifact_id == config.lower_dependency
    )
    root = common.OUT / "evidence/targets" / lower_config.artifact_id
    result_path = root / "result.json"
    obligation_path = root / "obligation.smt2"
    model_path = common.OUT / "proofs" / f"{lower_config.artifact_id}.rs"
    result = json.loads(result_path.read_text())
    if (
        result.get("target") != lower_config.target
        or result.get("active_contract_sha256")
        != lower_config.active_contract_sha256
        or result.get("classification") != lower_config.expected_results
    ):
        raise RuntimeError(
            f"{config.artifact_id}: ordered lower-transition evidence is invalid"
        )
    return {
        "target": lower_config.target,
        "artifact_id": lower_config.artifact_id,
        "active_contract_sha256": lower_config.active_contract_sha256,
        "admission_mode": (
            "defined lower transition composed inside TargetDefinition_T; "
            "no lower output or final state enters Boundary_T"
        ),
        "result": target_pipeline.artifact_record(result_path),
        "obligation": target_pipeline.artifact_record(obligation_path),
        "source_model": target_pipeline.artifact_record(model_path),
    }


def freeze_bound_inputs(
    config: cluster.ChunkTarget,
    evidence_root: Path,
    row: dict[str, str],
) -> dict[str, Any]:
    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    records: dict[str, Any] = {}
    text_bindings = {
        "active_contract.txt": (
            row["active_contract_text"],
            row["active_contract_sha256"],
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            row["generated_declaration_sha256"],
        ),
        "target_source_item.rs": (
            row["source_item_text"],
            row["source_item_sha256"],
        ),
        "target_public_docs.md": (
            row["public_docs_text"],
            row["public_docs_sha256"],
        ),
    }
    for filename, (text, expected) in text_bindings.items():
        path = root / filename
        _write_text_with_hash(path, text, expected)
        records[filename] = target_pipeline.artifact_record(path)

    copied = {
        "implproof_harness.rs": (
            row["frozen_harness_path"],
            row["harness_sha256"],
        ),
        "transformation_manifest.json": (
            row["frozen_transformation_manifest_path"],
            row["transformation_manifest_sha256"],
        ),
        "dependency_assumption_manifest.json": (
            row["frozen_dependency_manifest_path"],
            row["dependency_manifest_sha256"],
        ),
        "source_body.json": (
            row["frozen_source_body_manifest_path"],
            row["source_body_manifest_sha256"],
        ),
    }
    for filename, (relative, expected) in copied.items():
        destination = root / filename
        _copy_with_hash(destination, common.OUT / relative, expected)
        records[filename] = target_pipeline.artifact_record(destination)

    canonical_slice = common.RUST_LIBRARY / cluster.SLICE_SOURCE_PATH
    canonical_raw = common.RUST_LIBRARY / cluster.RAW_SOURCE_PATH
    if common.sha256(canonical_slice) != cluster.SLICE_SOURCE_SHA256:
        raise RuntimeError("canonical Rust Slice source hash changed")
    if common.sha256(canonical_raw) != cluster.RAW_SOURCE_SHA256:
        raise RuntimeError("canonical Rust raw-slice source hash changed")

    cast = (
        pointer_cast_cluster.CAST_MUT
        if config.mutable
        else pointer_cast_cluster.CAST_CONST
    )
    cast_path = root / "canonical_slice_pointer_cast.rs"
    canonical_sources = {
        "slice_pointer_cast": _source_excerpt(
            canonical_slice, cast.start, cast.end, cast_path
        )
    }
    if common.sha256(cast_path) != cast.excerpt_sha256:
        raise RuntimeError("canonical slice pointer-cast excerpt changed")

    raw_start, raw_end = (143, 196) if config.mutable else (80, 141)
    raw_path = root / (
        "canonical_from_raw_parts_mut.rs"
        if config.mutable
        else "canonical_from_raw_parts.rs"
    )
    canonical_sources["raw_slice_constructor"] = _source_excerpt(
        canonical_raw, raw_start, raw_end, raw_path
    )

    if config.has_remainder:
        if config.mutable:
            split_start, split_end = 1961, 1991
        elif config.kind == "chunks":
            split_start, split_end = 1993, 2054
        else:
            split_start, split_end = 1912, 1959
        split_path = root / "canonical_split_transition.rs"
        canonical_sources["front_rear_split"] = _source_excerpt(
            canonical_slice, split_start, split_end, split_path
        )

    return {
        "schema_version": 1,
        "artifacts": records,
        "canonical_sources": canonical_sources,
        "accepted_pointer_dependency": _accepted_pointer_dependency(config),
        "ordered_lower_dependency": _ordered_lower_dependency(config),
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
        raise RuntimeError(f"{label}: SAT evidence lacks get-value output")
    record.update(
        {
            "solver_result": target_pipeline.first_output_line(record),
            "expected_solver_result": expected,
        }
    )
    return record


def _validate_crosswalk_identity(
    config: cluster.ChunkTarget,
) -> dict[str, str]:
    row = cluster.authority_row(config.input_order)
    if (
        row["target"] != config.target
        or row["input_order"] != config.input_order
        or set(row["all_trust_site_ids"].split(";"))
        != (
            set(config.context_only_trust_sites)
            | set(config.admitted_trust_sites)
            | set(config.excluded_retained_trust_sites)
        )
    ):
        raise ValueError(f"{config.artifact_id}: trust-site binding changed")
    return row


def _verified_count(stdout: str) -> int:
    match = re.search(r"verification results::\s+(\d+) verified,\s+0 errors", stdout)
    return int(match.group(1)) if match else 0


def _run_target(
    config: cluster.ChunkTarget,
    z3: str,
    *,
    preserved_results: dict[tuple[str, str], dict[str, str]],
    preserved_artifact_ids: tuple[str, ...],
    expected_not_run: int,
) -> None:
    row = _validate_crosswalk_identity(config)
    evidence_root = common.OUT / "evidence/targets" / config.artifact_id
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
            "bindings": {field: row[field] for field in AUTHORITY_FIELDS},
        },
    )
    bound_inputs_path = evidence_root / "bound_inputs_manifest.json"
    common.write_json(
        bound_inputs_path,
        freeze_bound_inputs(config, evidence_root, row),
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, cluster.boundary_manifest(config))

    obligations: dict[str, Any] = {}
    for filename, purpose in (
        ("obligation", cluster.PRIMARY),
        ("exact_output_obligation", cluster.EXACT_OUTPUT),
    ):
        text, metadata = cluster.obligation(config, purpose)
        cluster.validate_target_obligation(config, text, metadata)
        smt_path = evidence_root / f"{filename}.smt2"
        metadata_path = evidence_root / f"{filename}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        expected = config.expected_solver_results[purpose]
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": _run_solver(
                evidence_root,
                z3,
                filename,
                smt_path,
                expected,
            ),
        }

    probes: dict[str, Any] = {}
    for name, case in cluster.probe_cases(config).items():
        path = evidence_root / "probes" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cluster.probe_text(config, name))
        probes[name] = {
            "kind": case["kind"],
            "expected_solver_result": case["expected"],
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                evidence_root,
                z3,
                f"probes/{name}",
                path,
                case["expected"],
                require_payload=case["expected"] == "sat",
            ),
        }

    witness_record: dict[str, Any] | None = None
    fixed_model_record: dict[str, Any] | None = None
    if config.mutable:
        witness_path = evidence_root / "witness.json"
        common.write_json(witness_path, cluster.witness_payload(config))
        replay = target_pipeline.capture_command(
            evidence_root / "witness_replay",
            [
                sys.executable,
                str(common.OUT / "tools/replay_chunk_contract_drift.py"),
                "--witness",
                str(witness_path),
            ],
            cwd=common.OUT,
        )
        replay_stdout = (common.OUT / replay["stdout"]).read_text()
        replay_stderr = (common.OUT / replay["stderr"]).read_text()
        if replay["exit_code"] != 0 or replay_stderr:
            raise RuntimeError(f"{config.artifact_id}: witness replay failed")
        replay_result = json.loads(replay_stdout)
        if replay_result.get("status") != "passed":
            raise RuntimeError(f"{config.artifact_id}: witness replay did not pass")
        replay["result"] = replay_result
        witness_record = {
            "artifact": target_pipeline.artifact_record(witness_path),
            "replay": replay,
        }

        model_path = evidence_root / "counterexample_model.smt2"
        model_path.write_text(cluster.fixed_model_text(config))
        fixed_model_record = {
            "smt": target_pipeline.artifact_record(model_path),
            "solver": _run_solver(
                evidence_root,
                z3,
                "counterexample_model",
                model_path,
                "sat",
                require_payload=True,
            ),
        }

    source_model = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    if not source_model.is_file() or "external_body" in source_model.read_text():
        raise RuntimeError(
            f"{config.artifact_id}: Verus source model is missing or trusted"
        )
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
        raise RuntimeError(f"{config.artifact_id}: Verus type-check failed")
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    verified = _verified_count(verification_stdout)
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or verified <= 0
        or "external_body" in captured_model.read_text()
    ):
        raise RuntimeError(f"{config.artifact_id}: Verus verification failed")

    target_pipeline.update_crosswalk_result(
        target=config.target,
        input_order=config.input_order,
        statuses=config.expected_results,
        preserved_results=preserved_results,
    )
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    classified = {
        _row_key(row)
        for row in rows
        if any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
    }
    if (
        not_run != expected_not_run
        or classified
        != set(preserved_results) | {(config.target, config.input_order)}
    ):
        raise RuntimeError(f"{config.artifact_id}: result count/scope changed")

    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError(f"{config.artifact_id}: preserved evidence changed")

    result = {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "artifact_id": config.artifact_id,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": row["active_contract_text"],
        "rejected_retained_contract_sha256": config.retained_contract_sha256,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": config.expected_results,
        "classification_basis": (
            "Both exact-output and full exact-state theorem negations are "
            "UNSAT under the source-backed transition."
            if not config.mutable
            else (
                "The exact-output theorem negation is UNSAT. The full exact "
                "theorem is SAT because the active mutable contract permits "
                "different final contents while preserving all lengths, "
                "shared-storage aliases, frames, and final subranges; the "
                "fixed witness independently replays every active conjunct."
            )
        ),
        "obligations": obligations,
        "satisfiability_and_rejection_probes": probes,
        "fixed_sat_replay": fixed_model_record,
        "witness": witness_record,
        "verus": {
            "source_model": target_pipeline.artifact_record(source_model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "verified_count": verified,
            "external_body_count": 0,
        },
        "ordered_lower_dependency": _ordered_lower_dependency(config),
        "accepted_pointer_dependency": _accepted_pointer_dependency(config),
        "excluded_retained_trust_site_ids": list(
            config.excluded_retained_trust_sites
        ),
        "preserved_target_evidence": {
            artifact_id: {
                "before_sha256": preserved_before[artifact_id],
                "after_sha256": preserved_after[artifact_id],
            }
            for artifact_id in sorted(preserved_roots)
        },
        "updated_crosswalk_fields": sorted(target_pipeline.RESULT_FIELDS),
        "remaining_not_run": expected_not_run,
    }
    common.write_json(evidence_root / "result.json", result)
    print(
        f"target_{int(config.input_order):03d}=PASS "
        f"full={config.expected_solver_results[cluster.PRIMARY]} "
        "exact=unsat "
        f"verus={verified}_verified,0_errors not_run={expected_not_run}"
    )


def _load_crosswalks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    return common.read_csv(csv_path), json.loads(json_path.read_text())


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
    cluster.authority_row.cache_clear()


def _cluster_results(rows: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    by_key = {_row_key(row): row for row in rows}
    return {
        config.artifact_id: {
            field: by_key[(config.target, config.input_order)][field]
            for field in target_pipeline.RESULT_FIELDS
        }
        for config in cluster.ORDERED_TARGETS
    }


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for the chunk drift cluster")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

    before_csv, before_json = _load_crosswalks()
    reset_csv, reset_json = prepare_crosswalk_reset(before_csv, before_json)
    baseline_roots = {
        artifact_id: common.OUT / "evidence/targets" / artifact_id
        for artifact_id in BASELINE_ARTIFACT_IDS
    }
    baseline_before = {
        artifact_id: tree_digest(root)
        for artifact_id, root in baseline_roots.items()
    }
    cluster_roots = {
        config.artifact_id: common.OUT / "evidence/targets" / config.artifact_id
        for config in cluster.ORDERED_TARGETS
    }
    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".chunk-contract-drift-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        existing = {
            artifact_id
            for artifact_id, root in cluster_roots.items()
            if root.is_dir()
        }
        for artifact_id in existing:
            shutil.copytree(
                cluster_roots[artifact_id],
                backup_root / artifact_id,
            )
        try:
            _write_crosswalks(reset_csv, reset_json)
            preserved_results = dict(BASELINE_RESULTS)
            preserved_artifacts = list(BASELINE_ARTIFACT_IDS)
            for index, config in enumerate(cluster.ORDERED_TARGETS, start=1):
                print(f"ordered_chunk_start={config.input_order}")
                _run_target(
                    config,
                    z3,
                    preserved_results=preserved_results,
                    preserved_artifact_ids=tuple(preserved_artifacts),
                    expected_not_run=48 - index,
                )
                preserved_results[
                    (config.target, config.input_order)
                ] = config.expected_results
                preserved_artifacts.append(config.artifact_id)

            after_csv, after_json = _load_crosswalks()
            expected = copy.deepcopy(before_csv)
            by_key = {_row_key(row): row for row in expected}
            for config in cluster.ORDERED_TARGETS:
                by_key[(config.target, config.input_order)].update(
                    config.expected_results
                )
            if after_csv != expected or after_json != expected:
                raise RuntimeError(
                    "ordered chunk replay changed unexpected crosswalk cells"
                )
            baseline_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in baseline_roots.items()
            }
            if baseline_after != baseline_before:
                raise RuntimeError(
                    "ordered chunk replay mutated certified baseline evidence"
                )
        except BaseException:
            _write_crosswalks(before_csv, before_json)
            for artifact_id, root in cluster_roots.items():
                if root.exists():
                    shutil.rmtree(root)
                if artifact_id in existing:
                    shutil.copytree(backup_root / artifact_id, root)
            raise

    manifest_path = common.OUT / "logs/ordered_chunk_contract_drift_replay.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "status": "passed",
            "ordered_artifact_ids": [
                config.artifact_id for config in cluster.ORDERED_TARGETS
            ],
            "initial_cluster_results": _cluster_results(before_csv),
            "final_cluster_results": _cluster_results(after_csv),
            "crosswalk": {
                "csv": target_pipeline.artifact_record(
                    common.OUT / "crosswalk/target_to_proof_boundary.csv"
                ),
                "json": target_pipeline.artifact_record(
                    common.OUT / "crosswalk/target_to_proof_boundary.json"
                ),
            },
            "preserved_certified_evidence": {
                artifact_id: {
                    "before_sha256": baseline_before[artifact_id],
                    "after_sha256": baseline_after[artifact_id],
                }
                for artifact_id in BASELINE_ARTIFACT_IDS
            },
            "classified": 19,
            "not_run": 43,
        },
    )
    print("ordered_chunk_contract_drift=PASS")
    print("order=014,015,012,023,024")
    print("classified=19 not_run=43")


if __name__ == "__main__":
    main()
