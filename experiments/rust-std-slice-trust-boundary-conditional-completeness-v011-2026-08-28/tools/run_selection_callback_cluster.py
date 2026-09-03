#!/usr/bin/env python3
"""Build and capture targets 078-079 selection-callback evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_selection_callback_cluster as replay
import run_target_077 as accepted_baseline
import target_077
import target_078
import target_079
import target_pipeline


TARGET_MODULES = (target_078, target_079)
CLUSTER_KEYS = tuple(
    (module.TARGET, module.INPUT_ORDER) for module in TARGET_MODULES
)
NOT_RUN = {
    field: "not-run" for field in target_pipeline.RESULT_FIELDS
}
CLUSTER_RESULTS = {
    key: {
        "exact_output_determinism_status": "missing-source-backed-model",
        "completeness_modulo_reviewed_equivalence_status": (
            "missing-source-backed-model"
        ),
    }
    for key in CLUSTER_KEYS
}
CANDIDATE_BOUNDARY_RESULTS = {
    key: {
        "exact_output_determinism_status": "boundary-insufficient",
        "completeness_modulo_reviewed_equivalence_status": (
            "boundary-insufficient"
        ),
    }
    for key in CLUSTER_KEYS
}
REJECTED_CLUSTER_RESULTS = {
    key: {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    for key in CLUSTER_KEYS
}
BASELINE_RESULTS = {
    **accepted_baseline.BASELINE_RESULTS,
    (target_077.TARGET, target_077.INPUT_ORDER): (
        accepted_baseline.RESULT_STATUSES
    ),
}
PRESERVED_ARTIFACT_IDS = (
    *accepted_baseline.PRESERVED_ARTIFACT_IDS,
    target_077.ARTIFACT_ID,
)
FROZEN_SELECTION_DIRS = accepted_baseline.FROZEN_SELECTION_DIRS
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/selection_callback_cluster"
AUTHORITY_FIELDS = accepted_baseline.AUTHORITY_FIELDS


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

    observed_cluster: dict[tuple[str, str], dict[str, str]] = {}
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified predecessor result changed")
        elif key in CLUSTER_RESULTS:
            if actual not in (
                NOT_RUN,
                CLUSTER_RESULTS[key],
                CANDIDATE_BOUNDARY_RESULTS[key],
                REJECTED_CLUSTER_RESULTS[key],
            ):
                raise ValueError(f"{key}: cluster result has unexpected state")
            observed_cluster[key] = actual
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    delivered = all(
        observed_cluster[key] == CLUSTER_RESULTS[key] for key in CLUSTER_KEYS
    )
    pending = all(observed_cluster[key] == NOT_RUN for key in CLUSTER_KEYS)
    rejected = all(
        observed_cluster[key] == REJECTED_CLUSTER_RESULTS[key]
        for key in CLUSTER_KEYS
    )
    candidate_boundary = all(
        observed_cluster[key] == CANDIDATE_BOUNDARY_RESULTS[key]
        for key in CLUSTER_KEYS
    )
    if not (delivered or pending or rejected or candidate_boundary):
        raise ValueError("targets 078-079 must be uniformly delivered or not-run")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in CLUSTER_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(CLUSTER_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed non-cluster row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during cluster reset")
    return reset_csv, reset_json


def validate_crosswalk_identity(module: ModuleType) -> dict[str, str]:
    matches = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/target_to_proof_boundary.csv"
        )
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError(f"{module.TARGET}: authority row absent or duplicated")
    row = matches[0]
    if (
        row["active_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(module.ALL_AUDITED_TRUST_SITES)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        raise ValueError(f"{module.TARGET}: authority binding changed")
    return row


def _trust_site_records(module: ModuleType) -> list[dict[str, str]]:
    selected = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/trust_site_inventory.csv"
        )
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    by_id = {row["record_id"]: row for row in selected}
    if set(by_id) != set(module.ALL_AUDITED_TRUST_SITES):
        raise ValueError(f"{module.TARGET}: six trust records changed")
    expected = {
        module.ALL_AUDITED_TRUST_SITES[0]: (
            "context-only-specification-vocabulary"
        ),
        module.ALL_AUDITED_TRUST_SITES[1]: (
            "inadmissible-answer-bearing-support"
        ),
        module.ALL_AUDITED_TRUST_SITES[2]: (
            "inadmissible-answer-bearing-support"
        ),
        module.ALL_AUDITED_TRUST_SITES[3]: (
            "admissible-source-backed-support"
        ),
        module.ALL_AUDITED_TRUST_SITES[4]: "context-only-source-closure",
        module.ALL_AUDITED_TRUST_SITES[5]: (
            "inadmissible-opaque-whole-algorithm"
        ),
    }
    if any(
        by_id[record_id]["semantic_disposition"] != disposition
        for record_id, disposition in expected.items()
    ):
        raise ValueError(f"{module.TARGET}: trust dispositions changed")
    return selected


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    return "".join(lines[start - 1 : end])


def _write_bound_text(
    path: Path, text: str, expected_sha256: str | None = None
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if expected_sha256 is not None and common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def write_bound_inputs(
    module: ModuleType,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_source = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_source) != row["source_file_sha256"]:
        raise RuntimeError(f"{module.TARGET}: canonical source changed")
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{module.TARGET}: vocabulary changed")
    for path_field, hash_field in (
        ("frozen_harness_path", "harness_sha256"),
        (
            "frozen_transformation_manifest_path",
            "transformation_manifest_sha256",
        ),
        ("frozen_dependency_manifest_path", "dependency_manifest_sha256"),
        ("frozen_source_body_manifest_path", "source_body_manifest_sha256"),
    ):
        frozen = common.OUT / row[path_field]
        if not frozen.is_file() or common.sha256(frozen) != row[hash_field]:
            raise RuntimeError(f"{module.TARGET}: frozen input changed: {frozen}")

    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True)
    generated = root / "generated_declaration.rs"
    source_item = root / "source_item.rs"
    public_docs = root / "public_docs.md"
    _write_bound_text(
        generated,
        row["generated_declaration_text"],
        row["generated_declaration_sha256"],
    )
    _write_bound_text(
        source_item, row["source_item_text"], row["source_item_sha256"]
    )
    _write_bound_text(
        public_docs, row["public_docs_text"], row["public_docs_sha256"]
    )

    select_source = common.RUST_LIBRARY / "core/src/slice/sort/select.rs"
    select_copy = root / "select.rs"
    shutil.copyfile(select_source, select_copy)
    partition_source = (
        common.RUST_LIBRARY / "core/src/slice/sort/unstable/quicksort.rs"
    )
    partition_excerpt = root / "partition.rs"
    partition_excerpt.write_text(_source_excerpt(partition_source, 93, 137))
    small_sort_source = (
        common.RUST_LIBRARY / "core/src/slice/sort/shared/smallsort.rs"
    )
    small_sort_excerpt = root / "smallsort.rs"
    small_sort_excerpt.write_text(
        _source_excerpt(small_sort_source, 295, 309)
        + "\n"
        + _source_excerpt(small_sort_source, 542, 607)
    )
    vocabulary_excerpt = root / "callback_vocabulary.rs"
    ranges = (
        ((664, 749), (768, 776))
        if module.CONFIG.mode == "compare"
        else ((316, 379), (590, 610), (778, 788))
    )
    vocabulary_excerpt.write_text(
        "\n".join(
            _source_excerpt(vocabulary_source, start, end)
            for start, end in ranges
        )
    )

    manifest_path = root / "manifest.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "target": module.TARGET,
            "input_order": module.INPUT_ORDER,
            "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
            "files": {
                "generated_declaration": target_pipeline.artifact_record(
                    generated
                ),
                "source_item": target_pipeline.artifact_record(source_item),
                "public_docs": target_pipeline.artifact_record(public_docs),
                "private_selection_source": {
                    **target_pipeline.artifact_record(select_copy),
                    "canonical_path": str(select_source),
                    "canonical_file_sha256": common.sha256(select_source),
                    "source_lines": module.CONFIG.selection_source,
                },
                "partition_source": {
                    **target_pipeline.artifact_record(partition_excerpt),
                    "canonical_path": str(partition_source),
                    "canonical_file_sha256": common.sha256(partition_source),
                    "source_lines": module.CONFIG.partition_source,
                },
                "small_sort_source": {
                    **target_pipeline.artifact_record(small_sort_excerpt),
                    "canonical_path": str(small_sort_source),
                    "canonical_file_sha256": common.sha256(
                        small_sort_source
                    ),
                    "source_lines": module.CONFIG.small_sort_source,
                },
                "callback_vocabulary": {
                    **target_pipeline.artifact_record(vocabulary_excerpt),
                    "canonical_path": str(vocabulary_source),
                    "canonical_file_sha256": common.sha256(vocabulary_source),
                    "source_lines": module.CONFIG.vocabulary_source,
                },
            },
            "frozen_implproof": {
                "harness": {
                    "path": row["frozen_harness_path"],
                    "sha256": row["harness_sha256"],
                },
                "transformation_manifest": {
                    "path": row["frozen_transformation_manifest_path"],
                    "sha256": row["transformation_manifest_sha256"],
                },
                "dependency_manifest": {
                    "path": row["frozen_dependency_manifest_path"],
                    "sha256": row["dependency_manifest_sha256"],
                },
                "source_body_manifest": {
                    "path": row["frozen_source_body_manifest_path"],
                    "sha256": row["source_body_manifest_sha256"],
                },
            },
        },
    )
    return manifest_path


def _run_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    smt_path: Path,
    expected: str,
    *,
    solver_timeout_seconds: int | None = None,
) -> dict[str, Any]:
    argv = [z3]
    if solver_timeout_seconds is not None:
        argv.append(f"-T:{solver_timeout_seconds}")
    argv.extend(("-smt2", str(smt_path)))
    record = target_pipeline.capture_command(
        evidence_root / label,
        argv,
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


def run_target(
    module: ModuleType,
    z3: str,
) -> tuple[dict[str, str], dict[str, Any]]:
    row = validate_crosswalk_identity(module)
    trust_sites = _trust_site_records(module)
    evidence_root = EVIDENCE_BASE / module.ARTIFACT_ID
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
            "target": module.TARGET,
            "records": trust_sites,
        },
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, module.boundary_manifest())
    bound_inputs_path = write_bound_inputs(module, row, evidence_root)

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (("obligation", module.PRIMARY),):
        text, metadata = module.obligation(purpose)
        module.validate_target_obligation(text, metadata)
        smt_path = evidence_root / f"{filename}.smt2"
        metadata_path = evidence_root / f"{filename}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        solver = _run_solver(
            z3,
            evidence_root,
            filename,
            smt_path,
            metadata["expected_solver_result"],
            solver_timeout_seconds=15,
        )
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    nonvacuity_path = evidence_root / "bounded_nonvacuity.smt2"
    nonvacuity_path.write_text(module.nonvacuity_text())
    nonvacuity_solver = _run_solver(
        z3,
        evidence_root,
        "bounded_nonvacuity",
        nonvacuity_path,
        "sat",
    )

    mixed_source_path = evidence_root / "mixed_source_execution.smt2"
    mixed_source_path.write_text(module.mixed_source_execution_text())
    mixed_source_solver = _run_solver(
        z3,
        evidence_root,
        "mixed_source_execution",
        mixed_source_path,
        "sat",
    )

    length_four_wrong_path = (
        evidence_root / "length_four_wrong_schedule_regression.smt2"
    )
    length_four_wrong_path.write_text(
        module.length_four_wrong_schedule_text()
    )
    length_four_wrong_solver = _run_solver(
        z3,
        evidence_root,
        "length_four_wrong_schedule_regression",
        length_four_wrong_path,
        "unsat",
    )

    length_four_source_path = (
        evidence_root / "length_four_source_execution.smt2"
    )
    length_four_source_path.write_text(
        module.length_four_source_execution_text()
    )
    length_four_source_solver = _run_solver(
        z3,
        evidence_root,
        "length_four_source_execution",
        length_four_source_path,
        "sat",
    )

    small_sort_regressions: dict[str, Any] = {}
    for case in (
        "descending",
        "mixed",
        "tail-three-middle",
        "tail-three-front",
    ):
        path = evidence_root / f"small_sort_{case}_regression.smt2"
        path.write_text(module.small_sort_regression_text(case))
        solver = _run_solver(
            z3,
            evidence_root,
            f"small_sort_{case}_regression",
            path,
            "unsat",
        )
        small_sort_regressions[case] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    panic_after_shift: dict[str, Any] = {}
    for restored, expected, label in (
        (True, "sat", "restored"),
        (False, "unsat", "unrestored"),
    ):
        path = evidence_root / f"panic_after_shift_{label}.smt2"
        path.write_text(module.panic_after_shift_text(restored=restored))
        solver = _run_solver(
            z3,
            evidence_root,
            f"panic_after_shift_{label}",
            path,
            expected,
        )
        panic_after_shift[label] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    panic_probes: dict[str, Any] = {}
    for kind in module.panic_probe_kinds():
        path = evidence_root / f"panic_prefix_{kind}.smt2"
        path.write_text(module.panic_probe_text(kind))
        solver = _run_solver(
            z3, evidence_root, f"panic_prefix_{kind}", path, "sat"
        )
        panic_probes[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    witness_path = evidence_root / "witness.json"
    common.write_json(witness_path, module.witness_payload())
    replay_record = target_pipeline.capture_command(
        evidence_root / "witness_replay",
        [
            sys.executable,
            str(
                common.OUT
                / "tools/replay_selection_callback_cluster.py"
            ),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay_record["stdout"]).read_text()
    replay_stderr = (common.OUT / replay_record["stderr"]).read_text()
    if replay_record["exit_code"] != 0 or replay_stderr:
        raise RuntimeError(f"{module.TARGET}: witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"{module.TARGET}: witness replay did not emit JSON"
        ) from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{module.TARGET}: witness replay did not pass")
    replay_record["result"] = replay_result

    source_model = common.OUT / module.CONFIG.proof_filename
    captured_model = evidence_root / "verus/selection_callback_model.rs"
    captured_model.parent.mkdir(parents=True)
    shutil.copyfile(source_model, captured_model)
    if "external_body" in captured_model.read_text():
        raise RuntimeError(f"{module.TARGET}: Verus model contains external_body")
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
        raise RuntimeError(f"{module.TARGET}: Verus model did not type-check")
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (
        common.OUT / verification["stdout"]
    ).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or module.CONFIG.verus_expected_summary not in verification_stdout
    ):
        raise RuntimeError(f"{module.TARGET}: Verus model did not verify")

    statuses = CLUSTER_RESULTS[(module.TARGET, module.INPUT_ORDER)]
    result = {
        "schema_version": 1,
        "target": module.TARGET,
        "input_order": module.INPUT_ORDER,
        "artifact_id": module.ARTIFACT_ID,
        "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": module.ACTIVE_CONTRACT_TEXT,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "trust_site_bindings": target_pipeline.artifact_record(trust_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": statuses,
        "classification_basis": (
            "The bounded source model executes the literal length-four "
            "insertion-sort path: tails one, two, and three thread exact "
            "callback states and intermediate sequence rotations. It rejects "
            "the former one/two-adapter all-equal traces, admits the canonical "
            "three-adapter trace, and rejects wrong descending and mixed "
            "post-states. Panic probes execute source-valid prefixes through "
            "the same adapter and gap-guard rotation definitions. The model "
            "does not encode choose_pivot, lower-partition mutations and "
            "callbacks, introselect narrowing, the 16-step fallback, or their "
            "panic prefixes for arbitrary lengths. The retained whole-helper "
            "sites therefore remain unresolved and both results are "
            "missing-source-backed-model, not boundary-insufficient."
            + (
                " Target 079 also leaves temporary key Drop order, "
                "callback-visible state, and panic unmodeled."
                if module.CONFIG.mode == "key"
                else ""
            )
        ),
        "obligations": obligations,
        "bounded_nonvacuity": {
            "smt": target_pipeline.artifact_record(nonvacuity_path),
            "solver": nonvacuity_solver,
        },
        "mixed_source_execution": {
            "smt": target_pipeline.artifact_record(mixed_source_path),
            "solver": mixed_source_solver,
        },
        "length_four_wrong_schedule_regression": {
            "smt": target_pipeline.artifact_record(length_four_wrong_path),
            "solver": length_four_wrong_solver,
        },
        "length_four_source_execution": {
            "smt": target_pipeline.artifact_record(length_four_source_path),
            "solver": length_four_source_solver,
        },
        "small_sort_regressions": small_sort_regressions,
        "panic_after_shift_regressions": panic_after_shift,
        "unresolved_source_model_phases": list(
            module.missing_source_phases()
        ),
        "panic_prefix_probes": panic_probes,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay_record,
        "verus": {
            "source_model": target_pipeline.artifact_record(source_model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": module.CONFIG.verus_expected_summary,
        },
        "excluded_retained_trust_site_ids": list(
            module.EXCLUDED_RETAINED_TRUST_SITES
        ),
        "admitted_trust_site_ids": list(module.ADMITTED_TRUST_SITES),
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
        "independent_review": "required",
        "stage_transition": "disabled",
    }
    common.write_json(evidence_root / "result.json", result)
    return statuses, result


def update_ledgers_atomically(
    statuses_by_target: dict[str, dict[str, str]],
) -> None:
    csv_rows, json_rows = _load_crosswalks()
    preserved = copy.deepcopy(BASELINE_RESULTS)
    updated_csv = csv_rows
    updated_json = json_rows
    for module in TARGET_MODULES:
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            updated_csv,
            updated_json,
            target=module.TARGET,
            input_order=module.INPUT_ORDER,
            statuses=statuses_by_target[module.TARGET],
            preserved_results=preserved,
        )
        preserved[(module.TARGET, module.INPUT_ORDER)] = statuses_by_target[
            module.TARGET
        ]
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
    if classified != set(preserved) or len(classified) != 27 or not_run != 35:
        raise RuntimeError(
            f"expected 27 classified and 35 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for selection callback evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 25 or len(PRESERVED_ARTIFACT_IDS) != 25:
        raise RuntimeError("certified predecessor baseline is not 25 targets")

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
    frozen_roots = {
        name: common.OUT / "provenance/frozen/implproof" / name
        for name in FROZEN_SELECTION_DIRS
    }
    frozen_before = {
        name: tree_digest(root) for name, root in frozen_roots.items()
    }
    mutable_roots = {
        module.ARTIFACT_ID: EVIDENCE_BASE / module.ARTIFACT_ID
        for module in TARGET_MODULES
    }
    mutable_roots["selection_callback_cluster"] = CLUSTER_ROOT

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".selection-callback-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        existing_roots: set[str] = set()
        for artifact_id, root in mutable_roots.items():
            if root.is_dir():
                shutil.copytree(root, backup_root / artifact_id)
                existing_roots.add(artifact_id)
        try:
            _write_crosswalks(reset_csv, reset_json)
            if CLUSTER_ROOT.exists():
                shutil.rmtree(CLUSTER_ROOT)
            CLUSTER_ROOT.mkdir(parents=True)

            statuses_by_target: dict[str, dict[str, str]] = {}
            target_results: dict[str, Any] = {}
            for module in TARGET_MODULES:
                statuses, result = run_target(module, z3)
                statuses_by_target[module.TARGET] = statuses
                target_results[module.TARGET] = {
                    "artifact_id": module.ARTIFACT_ID,
                    "classification": statuses,
                    "result": target_pipeline.artifact_record(
                        EVIDENCE_BASE
                        / module.ARTIFACT_ID
                        / "result.json"
                    ),
                }

            update_ledgers_atomically(statuses_by_target)
            after_csv, after_json = _load_crosswalks()
            expected_after = copy.deepcopy(before_csv)
            expected_by_key = {
                _row_key(row): row for row in expected_after
            }
            for key in CLUSTER_KEYS:
                expected_by_key[key].update(CLUSTER_RESULTS[key])
            if after_csv != expected_after or after_json != expected_after:
                raise RuntimeError(
                    "selection callback run changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = {
                name: tree_digest(root) for name, root in frozen_roots.items()
            }
            if preserved_after != preserved_before:
                raise RuntimeError("selection callback run mutated certified evidence")
            if frozen_after != frozen_before:
                raise RuntimeError("selection callback run mutated frozen inputs")

            common.write_json(
                CLUSTER_ROOT / "manifest.json",
                {
                    "schema_version": 1,
                    "execution_order": [
                        module.TARGET for module in TARGET_MODULES
                    ],
                    "targets": target_results,
                    "preserved_certified_evidence": {
                        artifact_id: {
                            "before_sha256": preserved_before[artifact_id],
                            "after_sha256": preserved_after[artifact_id],
                        }
                        for artifact_id in PRESERVED_ARTIFACT_IDS
                    },
                    "preserved_frozen_selection_inputs": {
                        name: {
                            "before_sha256": frozen_before[name],
                            "after_sha256": frozen_after[name],
                        }
                        for name in FROZEN_SELECTION_DIRS
                    },
                    "classified_rows": 27,
                    "not_run_rows": 35,
                    "stage_transition": "disabled",
                    "independent_review": "required",
                },
            )
        except BaseException:
            try:
                _write_crosswalks(before_csv, before_json)
                for artifact_id, root in mutable_roots.items():
                    if root.exists():
                        shutil.rmtree(root)
                    if artifact_id in existing_roots:
                        shutil.copytree(backup_root / artifact_id, root)
            except Exception as restore_exc:
                raise RuntimeError(
                    "selection callback run failed and rollback was incomplete"
                ) from restore_exc
            raise

    print("selection_callback_cluster=PASS")
    print("078_exact=missing-source-backed-model")
    print("078_reviewed=missing-source-backed-model")
    print("079_exact=missing-source-backed-model")
    print("079_reviewed=missing-source-backed-model")
    print("bounded_obligations=2_unsat")
    print("bounded_nonvacuity=4_sat")
    print("length_four_wrong_schedule_regressions=2_unsat")
    print("length_four_source_executions=2_sat")
    print("small_sort_mutation_regressions=8_unsat")
    print("panic_after_shift=2_sat,2_unsat")
    print("verus_models=2_clean")
    print("preserved_evidence_trees=25")
    print("classified=27 not_run=35")


if __name__ == "__main__":
    main()
