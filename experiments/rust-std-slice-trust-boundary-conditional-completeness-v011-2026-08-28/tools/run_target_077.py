#!/usr/bin/env python3
"""Build, execute, and record target-077 selection evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_target_077
import run_unstable_sort_companions as accepted_baseline
import target_077
import target_pipeline


EVIDENCE_ROOT = common.OUT / "evidence/targets" / target_077.ARTIFACT_ID
SOURCE_MODEL = common.OUT / "proofs/077_core_slice_select_nth_unstable.rs"
RESULT_STATUSES = {
    "exact_output_determinism_status": "conditional-incomplete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
}
BASELINE_RESULTS = {
    **accepted_baseline.BASELINE_RESULTS,
    **accepted_baseline.COMPANION_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *accepted_baseline.PRESERVED_ARTIFACT_IDS,
    "080_core_slice_sort_unstable",
    "082_core_slice_sort_unstable_by_key",
)
FROZEN_SELECTION_DIRS = (
    "077_core_slice_select_nth_unstable",
    "078_core_slice_select_nth_unstable_by",
    "079_core_slice_select_nth_unstable_by_key",
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
    "proof_boundary_assumption",
    "boundary_model_requirement",
)


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ValueError(f"required preserved directory is missing: {root}")
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


def validate_crosswalk_state() -> tuple[dict[str, str], list[dict[str, Any]]]:
    csv_rows, json_rows = _load_crosswalks()
    if len(csv_rows) != 62 or csv_rows != json_rows:
        raise ValueError("crosswalk formats are not the same 62-row ledger")
    by_key = {_row_key(row): row for row in csv_rows}
    if len(by_key) != 62:
        raise ValueError("crosswalk contains duplicate target identities")
    target_key = (target_077.TARGET, target_077.INPUT_ORDER)
    row = by_key.get(target_key)
    if row is None:
        raise ValueError("target 077 is absent from the crosswalk")
    if (
        row["active_contract_sha256"] != target_077.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != target_077.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != target_077.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != target_077.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(target_077.ALL_AUDITED_TRUST_SITES)
        or set(row["inadmissible_trust_site_ids"].split(";"))
        != set(target_077.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        raise ValueError("target-077 authority or retained-boundary binding changed")

    not_run = {
        field: "not-run" for field in target_pipeline.RESULT_FIELDS
    }
    actual_target = {
        field: row[field] for field in target_pipeline.RESULT_FIELDS
    }
    if actual_target not in (not_run, RESULT_STATUSES):
        raise ValueError("target-077 result fields have an unexpected state")
    for key, candidate in by_key.items():
        actual = {
            field: candidate[field] for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified result changed")
        elif key == target_key:
            continue
        elif actual != not_run:
            raise ValueError(f"{key}: out-of-scope target is classified")
    for order in ("78", "79"):
        candidate = next(row for row in csv_rows if row["input_order"] == order)
        if any(candidate[field] != "not-run" for field in target_pipeline.RESULT_FIELDS):
            raise ValueError(f"target {order} must remain not-run")
    return row, csv_rows


def _trust_site_records() -> list[dict[str, str]]:
    rows = common.read_csv(common.OUT / "crosswalk/trust_site_inventory.csv")
    selected = [
        row
        for row in rows
        if row["target"] == target_077.TARGET
        and row["input_order"] == target_077.INPUT_ORDER
    ]
    by_id = {row["record_id"]: row for row in selected}
    if set(by_id) != set(target_077.ALL_AUDITED_TRUST_SITES):
        raise ValueError("target-077 trust-site inventory changed")
    if (
        by_id["TS-077-D003"]["semantic_disposition"]
        != "admissible-source-backed-support"
        or by_id["TS-077-D002"]["semantic_disposition"]
        != "inadmissible-answer-bearing-support"
        or by_id["TS-077-E001"]["semantic_disposition"]
        != "inadmissible-opaque-whole-algorithm"
        or by_id["TS-077-D001"]["semantic_disposition"]
        != "context-only-specification-vocabulary"
        or by_id["TS-077-C001"]["semantic_disposition"]
        != "context-only-source-closure"
    ):
        raise ValueError("target-077 trust-site dispositions changed")
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


def write_bound_inputs(row: dict[str, str]) -> Path:
    canonical_source = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_source) != row["source_file_sha256"]:
        raise RuntimeError("canonical target source changed")
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError("generated shared vocabulary changed")
    for path_field, hash_field in (
        ("frozen_harness_path", "harness_sha256"),
        (
            "frozen_transformation_manifest_path",
            "transformation_manifest_sha256",
        ),
        ("frozen_dependency_manifest_path", "dependency_manifest_sha256"),
        ("frozen_source_body_manifest_path", "source_body_manifest_sha256"),
    ):
        path = common.OUT / row[path_field]
        if not path.is_file() or common.sha256(path) != row[hash_field]:
            raise RuntimeError(f"frozen target-077 input changed: {path}")

    root = EVIDENCE_ROOT / "bound_inputs"
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
    ord_source = common.RUST_LIBRARY / "core/src/cmp.rs"
    ord_excerpt = root / "ord_totality_docs.rs"
    ord_excerpt.write_text(_source_excerpt(ord_source, 733, 761))
    vocabulary_excerpt = root / "selection_vocabulary.rs"
    vocabulary_excerpt.write_text(
        _source_excerpt(vocabulary_source, 316, 379)
        + "\n"
        + _source_excerpt(vocabulary_source, 759, 770)
    )

    manifest_path = root / "manifest.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "target": target_077.TARGET,
            "input_order": target_077.INPUT_ORDER,
            "active_contract_sha256": target_077.ACTIVE_CONTRACT_SHA256,
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
                    "source_lines": target_077.SELECT_SOURCE,
                },
                "partition_source": {
                    **target_pipeline.artifact_record(partition_excerpt),
                    "canonical_path": str(partition_source),
                    "canonical_file_sha256": common.sha256(partition_source),
                    "source_lines": target_077.PARTITION_SOURCE,
                },
                "ord_totality_docs": {
                    **target_pipeline.artifact_record(ord_excerpt),
                    "canonical_path": str(ord_source),
                    "canonical_file_sha256": common.sha256(ord_source),
                    "source_lines": target_077.ORD_SOURCE,
                },
                "selection_vocabulary": {
                    **target_pipeline.artifact_record(vocabulary_excerpt),
                    "canonical_path": str(vocabulary_source),
                    "canonical_file_sha256": common.sha256(vocabulary_source),
                    "source_lines": target_077.VOCABULARY_SOURCE,
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
    z3: str, label: str, smt_path: Path, expected: str
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


def _write_obligation(
    filename: str, purpose: str
) -> tuple[Path, Path, dict[str, Any]]:
    text, metadata = target_077.obligation(purpose)
    target_077.validate_target_obligation(text, metadata)
    smt_path = EVIDENCE_ROOT / f"{filename}.smt2"
    metadata_path = EVIDENCE_ROOT / f"{filename}.metadata.json"
    smt_path.write_text(text)
    common.write_json(metadata_path, metadata)
    return smt_path, metadata_path, metadata


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for target-077 evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if not SOURCE_MODEL.is_file():
        raise RuntimeError(f"target-077 Verus model is missing: {SOURCE_MODEL}")
    if len(BASELINE_RESULTS) != 24 or len(PRESERVED_ARTIFACT_IDS) != 24:
        raise RuntimeError("target-077 predecessor baseline is not 24 targets")

    row, before_rows = validate_crosswalk_state()
    trust_sites = _trust_site_records()
    preserved_roots = {
        artifact_id: common.OUT / "evidence/targets" / artifact_id
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

    if EVIDENCE_ROOT.exists():
        shutil.rmtree(EVIDENCE_ROOT)
    EVIDENCE_ROOT.mkdir(parents=True)

    authority_path = EVIDENCE_ROOT / "authority_bindings.json"
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: row[field] for field in AUTHORITY_FIELDS},
        },
    )
    trust_path = EVIDENCE_ROOT / "trust_site_bindings.json"
    common.write_json(
        trust_path,
        {
            "schema_version": 1,
            "target": target_077.TARGET,
            "records": trust_sites,
        },
    )
    boundary_path = EVIDENCE_ROOT / "boundary_manifest.json"
    common.write_json(boundary_path, target_077.boundary_manifest())
    bound_inputs_path = write_bound_inputs(row)

    obligations: dict[str, dict[str, Any]] = {}
    for filename, purpose in (
        ("obligation", target_077.PRIMARY),
        ("exact_output_obligation", target_077.EXACT_OUTPUT),
    ):
        smt_path, metadata_path, metadata = _write_obligation(
            filename, purpose
        )
        solver = _run_solver(
            z3, filename, smt_path, metadata["expected_solver_result"]
        )
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    exact_model_path = EVIDENCE_ROOT / "exact_output_witness.smt2"
    exact_model_path.write_text(target_077.fixed_exact_model_text())
    exact_model = _run_solver(
        z3, "exact_output_witness", exact_model_path, "sat"
    )

    probes: dict[str, Any] = {}
    for kind in target_077.PROBE_KINDS:
        path = EVIDENCE_ROOT / f"witness_{kind}.smt2"
        path.write_text(target_077.witness_probe_text(kind))
        solver = _run_solver(z3, f"witness_{kind}", path, "sat")
        probes[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    semantic_regressions: dict[str, Any] = {}
    for kind in target_077.SEMANTIC_REGRESSION_KINDS:
        path = EVIDENCE_ROOT / f"regression_{kind}.smt2"
        path.write_text(target_077.semantic_regression_probe_text(kind))
        solver = _run_solver(z3, f"regression_{kind}", path, "unsat")
        semantic_regressions[kind] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    witness_path = EVIDENCE_ROOT / "witness.json"
    common.write_json(witness_path, target_077.witness_payload())
    replay = target_pipeline.capture_command(
        EVIDENCE_ROOT / "witness_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_target_077.py"),
            "--witness",
            str(witness_path),
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay["stdout"]).read_text()
    replay_stderr = (common.OUT / replay["stderr"]).read_text()
    if replay["exit_code"] != 0 or replay_stderr:
        raise RuntimeError("target-077 witness replay failed")
    try:
        replay_result = json.loads(replay_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("target-077 witness replay did not emit JSON") from exc
    if replay_result.get("status") != "passed":
        raise RuntimeError("target-077 witness replay did not pass")
    replay["result"] = replay_result

    captured_model = EVIDENCE_ROOT / "verus/selection_model.rs"
    captured_model.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE_MODEL, captured_model)
    if "external_body" in captured_model.read_text():
        raise RuntimeError("target-077 Verus model contains a trusted body")
    typecheck = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/typecheck",
        [
            str(common.VERUS),
            str(captured_model),
            "--crate-type=lib",
            "--no-verify",
        ],
        cwd=common.OUT,
    )
    if typecheck["exit_code"] != 0 or (common.OUT / typecheck["stderr"]).read_text():
        raise RuntimeError("target-077 Verus model did not type-check")
    verification = target_pipeline.capture_command(
        EVIDENCE_ROOT / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or "verification results:: 5 verified, 0 errors"
        not in verification_stdout
    ):
        raise RuntimeError("target-077 Verus model did not verify")

    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    csv_backup = csv_path.read_bytes()
    json_backup = json_path.read_bytes()
    try:
        target_pipeline.update_crosswalk_result(
            target=target_077.TARGET,
            input_order=target_077.INPUT_ORDER,
            statuses=RESULT_STATUSES,
            preserved_results=BASELINE_RESULTS,
        )
        after_csv, after_json = _load_crosswalks()
        expected_after = copy.deepcopy(before_rows)
        target_after = next(
            candidate
            for candidate in expected_after
            if _row_key(candidate)
            == (target_077.TARGET, target_077.INPUT_ORDER)
        )
        target_after.update(RESULT_STATUSES)
        if after_csv != expected_after or after_json != expected_after:
            raise RuntimeError("target-077 pipeline changed non-result ledger data")
        classified = {
            _row_key(candidate)
            for candidate in after_csv
            if any(
                candidate[field] != "not-run"
                for field in target_pipeline.RESULT_FIELDS
            )
        }
        if (
            classified
            != set(BASELINE_RESULTS)
            | {(target_077.TARGET, target_077.INPUT_ORDER)}
            or len(classified) != 25
            or len(after_csv) - len(classified) != 37
        ):
            raise RuntimeError("target-077 pipeline did not finish at 25/37")
    except Exception:
        csv_path.write_bytes(csv_backup)
        json_path.write_bytes(json_backup)
        raise

    preserved_after = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    frozen_after = {
        name: tree_digest(root) for name, root in frozen_roots.items()
    }
    if preserved_after != preserved_before:
        raise RuntimeError("target-077 pipeline mutated certified evidence")
    if frozen_after != frozen_before:
        raise RuntimeError("target-077 pipeline mutated frozen selection inputs")

    result = {
        "schema_version": 1,
        "target": target_077.TARGET,
        "input_order": target_077.INPUT_ORDER,
        "artifact_id": target_077.ARTIFACT_ID,
        "active_contract_sha256": target_077.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": target_077.ACTIVE_CONTRACT_TEXT,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "trust_site_bindings": target_pipeline.artifact_record(trust_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": RESULT_STATUSES,
        "classification_basis": (
            "The arbitrary-length shared-input/shared-Ord-boundary theorem is "
            "real UNSAT modulo the source-documented selection relation. A "
            "fixed-input, fixed-boundary SAT witness reorders both unsorted "
            "sides while satisfying every active contract conjunct, so exact "
            "return/final-state determinism is conditionally incomplete."
        ),
        "obligations": obligations,
        "exact_output_witness": {
            "smt": target_pipeline.artifact_record(exact_model_path),
            "solver": exact_model,
        },
        "equivalence_witnesses": probes,
        "semantic_regressions": semantic_regressions,
        "witness": target_pipeline.artifact_record(witness_path),
        "witness_replay": replay,
        "verus": {
            "source_model": target_pipeline.artifact_record(SOURCE_MODEL),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": "verification results:: 5 verified, 0 errors",
        },
        "excluded_retained_trust_site_ids": list(
            target_077.EXCLUDED_RETAINED_TRUST_SITES
        ),
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
        "updated_crosswalk_fields": sorted(RESULT_STATUSES),
        "ledger_counts": {"classified": 25, "not_run": 37},
        "independent_review": "required",
        "stage_transition": "disabled",
    }
    common.write_json(EVIDENCE_ROOT / "result.json", result)

    print("target_077=PASS")
    print("reviewed_selection_equivalence=unsat")
    print("exact_output_and_final_state=sat")
    print("witness_replay=passed")
    print("verus=5_verified_0_errors")
    print("ledger=25_classified,37_not-run")
    print("certified_evidence=24_preserved")
    print("targets_078_079=not-run")


if __name__ == "__main__":
    main()
