#!/usr/bin/env python3
"""Build and capture targets 080 and 082 unstable-sort evidence."""

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
import run_maybeuninit_lifecycle_cluster as accepted_baseline
import target_080
import target_082
import target_pipeline


TARGET_MODULES = (target_080, target_082)
CLUSTER_KEYS = tuple(
    (module.TARGET, module.INPUT_ORDER) for module in TARGET_MODULES
)
NOT_RUN = {
    field: "not-run" for field in target_pipeline.RESULT_FIELDS
}
COMPANION_RESULTS = {
    (module.TARGET, module.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    }
    for module in TARGET_MODULES
}
BASELINE_RESULTS = {
    **accepted_baseline.BASELINE_RESULTS,
    **accepted_baseline.DELIVERED_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *accepted_baseline.PRESERVED_ARTIFACT_IDS,
    "025_core_slice_assume_init_drop",
    "026_core_slice_assume_init_mut",
    "119_core_slice_write_clone_of_slice",
)
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/unstable_sort_companions"
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
    "shared_vocabulary_path",
    "shared_vocabulary_sha256",
    "source_reference",
    "source_path",
    "source_file_sha256",
    "source_item_start_line",
    "source_item_end_line",
    "source_item_text",
    "source_item_sha256",
    "public_docs_reference",
    "public_docs_start_line",
    "public_docs_end_line",
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
    "equivalence_policy",
    "equivalence_source_citation",
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
        raise ValueError("crosswalk CSV/JSON are duplicate, mismatched, or divergent")

    observed_companions: dict[tuple[str, str], dict[str, str]] = {}
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified predecessor result changed")
        elif key in COMPANION_RESULTS:
            if actual not in (NOT_RUN, COMPANION_RESULTS[key]):
                raise ValueError(f"{key}: delivered companion result changed")
            observed_companions[key] = actual
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope result is classified")
    delivered = all(
        observed_companions[key] == COMPANION_RESULTS[key]
        for key in CLUSTER_KEYS
    )
    pending = all(
        observed_companions[key] == NOT_RUN for key in CLUSTER_KEYS
    )
    if not (delivered or pending):
        raise ValueError(
            "companion rows must be uniformly delivered or uniformly not-run"
        )

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
            raise ValueError(f"{_row_key(before)}: reset changed a non-cluster row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during reset")
    return reset_csv, reset_json


def _write_text_with_hash(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def validate_crosswalk_identity(module: ModuleType) -> dict[str, str]:
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError(f"{module.TARGET}: crosswalk row is absent or duplicated")
    row = matches[0]
    if (
        row["active_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"] != "equal-key-reordering-equivalence"
        or set(row["all_trust_site_ids"].split(";"))
        != set(module.ALL_AUDITED_TRUST_SITES)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        raise ValueError(
            f"{module.TARGET}: crosswalk authority/boundary binding changed"
        )
    return row


def _trust_site_records(module: ModuleType) -> list[dict[str, str]]:
    rows = common.read_csv(common.OUT / "crosswalk/trust_site_inventory.csv")
    selected = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if {row["record_id"] for row in selected} != set(
        module.ALL_AUDITED_TRUST_SITES
    ):
        raise ValueError(f"{module.TARGET}: trust-site inventory changed")
    return selected


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    return "".join(lines[start - 1 : end])


def write_bound_inputs(
    module: ModuleType,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_source = Path(row["source_path"])
    if common.sha256(canonical_source) != row["source_file_sha256"]:
        raise RuntimeError(f"{module.TARGET}: canonical source file changed")
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{module.TARGET}: shared vocabulary changed")
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
        if common.sha256(frozen) != row[hash_field]:
            raise RuntimeError(
                f"{module.TARGET}: frozen input hash changed: {frozen}"
            )

    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True)
    generated = root / "generated_declaration.rs"
    source_item = root / "source_item.rs"
    public_docs = root / "public_docs.md"
    _write_text_with_hash(
        generated,
        row["generated_declaration_text"],
        row["generated_declaration_sha256"],
    )
    _write_text_with_hash(
        source_item,
        row["source_item_text"],
        row["source_item_sha256"],
    )
    _write_text_with_hash(
        public_docs,
        row["public_docs_text"],
        row["public_docs_sha256"],
    )

    ord_source = common.RUST_LIBRARY / "core/src/cmp.rs"
    ord_excerpt = root / "ord_totality_docs.rs"
    ord_excerpt.write_text(_source_excerpt(ord_source, 733, 761))
    vocabulary_excerpt = root / "ord_observation_vocabulary.rs"
    vocabulary_excerpt.write_text(
        _source_excerpt(vocabulary_source, 330, 379)
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
                "ord_totality_docs": {
                    **target_pipeline.artifact_record(ord_excerpt),
                    "canonical_path": str(ord_source),
                    "canonical_file_sha256": common.sha256(ord_source),
                    "source_lines": "core/src/cmp.rs:733-761",
                },
                "ord_observation_vocabulary": {
                    **target_pipeline.artifact_record(vocabulary_excerpt),
                    "canonical_path": str(vocabulary_source),
                    "canonical_file_sha256": common.sha256(vocabulary_source),
                    "source_lines": (
                        "specs/slice_shared_vocabulary.rs:330-379"
                    ),
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
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
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


def _write_obligation(
    module: ModuleType,
    evidence_root: Path,
    filename: str,
    purpose: str,
) -> tuple[Path, Path, dict[str, Any]]:
    text, metadata = module.obligation(purpose)
    module.validate_target_obligation(text, metadata)
    smt_path = evidence_root / f"{filename}.smt2"
    metadata_path = evidence_root / f"{filename}.metadata.json"
    smt_path.write_text(text)
    common.write_json(metadata_path, metadata)
    return smt_path, metadata_path, metadata


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
    for filename, purpose in (
        ("obligation", module.PRIMARY),
        ("bounded_sanity", module.BOUNDED_SANITY),
        ("exact_final_slice_obligation", module.EXACT_FINAL_SLICE),
    ):
        smt_path, metadata_path, metadata = _write_obligation(
            module, evidence_root, filename, purpose
        )
        solver = _run_solver(
            z3,
            evidence_root,
            filename,
            smt_path,
            metadata["expected_solver_result"],
        )
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    exact_model_path = evidence_root / "exact_final_slice_witness.smt2"
    exact_model_path.write_text(module.fixed_exact_model_text())
    exact_model = _run_solver(
        z3,
        evidence_root,
        "exact_final_slice_witness",
        exact_model_path,
        "sat",
    )
    equivalence_probes: dict[str, Any] = {}
    for polarity, positive in (("positive", True), ("negative", False)):
        path = evidence_root / f"equal_class_equivalence.{polarity}.smt2"
        path.write_text(module.equivalence_probe_text(positive=positive))
        solver = _run_solver(
            z3,
            evidence_root,
            f"equal_class_equivalence.{polarity}",
            path,
            "sat",
        )
        equivalence_probes[polarity] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    witness_path = evidence_root / "witness.json"
    common.write_json(witness_path, module.witness_payload())
    replay = target_pipeline.capture_command(
        evidence_root / "witness_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_unstable_sort_companions.py"),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError(f"{module.TARGET}: witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"{module.TARGET}: witness replay did not emit JSON"
        ) from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{module.TARGET}: witness replay did not pass")
    replay["result"] = replay_result

    source_model = common.OUT / module.CONFIG.proof_filename
    captured_model = evidence_root / "verus/contract_model.rs"
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
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or module.CONFIG.verus_expected_summary not in verification_stdout
    ):
        raise RuntimeError(f"{module.TARGET}: Verus model did not verify")

    statuses = COMPANION_RESULTS[(module.TARGET, module.INPUT_ORDER)]
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
            "The arbitrary-length, arbitrary-position reviewed-equivalence "
            "theorem is real UNSAT under the source-backed Ord total-order "
            "semantics. Exact final-slice determinism is SAT with two distinct "
            "equal-class permutations that satisfy the exact active contract "
            "under one input and boundary. The bounded UNSAT result is retained "
            "as sanity evidence only."
        ),
        "obligations": obligations,
        "exact_final_slice_witness": {
            "smt": target_pipeline.artifact_record(exact_model_path),
            "solver": exact_model,
        },
        "equivalence_witnesses": equivalence_probes,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay,
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
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
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
    if classified != set(preserved) or len(classified) != 24 or not_run != 38:
        raise RuntimeError(
            f"expected 24 classified and 38 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for unstable-sort evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 22 or len(PRESERVED_ARTIFACT_IDS) != 22:
        raise RuntimeError("the certified predecessor baseline is not 22 targets")

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
    mutable_roots = {
        module.ARTIFACT_ID: EVIDENCE_BASE / module.ARTIFACT_ID
        for module in TARGET_MODULES
    }
    mutable_roots["unstable_sort_companions"] = CLUSTER_ROOT

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".unstable-sort-companions-backup-",
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
                        EVIDENCE_BASE / module.ARTIFACT_ID / "result.json"
                    ),
                }

            update_ledgers_atomically(statuses_by_target)
            after_csv, after_json = _load_crosswalks()
            expected_after = copy.deepcopy(before_csv)
            expected_by_key = {
                _row_key(row): row for row in expected_after
            }
            for key in CLUSTER_KEYS:
                expected_by_key[key].update(COMPANION_RESULTS[key])
            if after_csv != expected_after or after_json != expected_after:
                raise RuntimeError(
                    "companion run changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            if preserved_after != preserved_before:
                raise RuntimeError("companion run mutated certified evidence")

            manifest = {
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
                "classified_rows": 24,
                "not_run_rows": 38,
                "stage_transition": "disabled",
                "independent_review": "required",
            }
            common.write_json(CLUSTER_ROOT / "manifest.json", manifest)
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
                    "companion run failed and rollback was incomplete"
                ) from restore_exc
            raise

    print("unstable_sort_companions=PASS")
    print("080_exact=conditional-incomplete")
    print("080_modulo_equal_ord=conditional-complete")
    print("082_exact=conditional-incomplete")
    print("082_modulo_equal_key=conditional-complete")
    print("general_obligations=2_unsat")
    print("bounded_sanity=2_unsat")
    print("exact_witnesses=2_sat")
    print("verus_models=2_clean")
    print("preserved_evidence_trees=22")
    print("classified=24 not_run=38")


if __name__ == "__main__":
    main()
