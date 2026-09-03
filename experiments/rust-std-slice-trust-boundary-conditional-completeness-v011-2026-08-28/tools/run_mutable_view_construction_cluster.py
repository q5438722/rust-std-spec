#!/usr/bin/env python3
"""Build and retain the bounded mutable-view construction evidence."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import address_observer_pair as predecessor_targets
import align_to_pair as align_pair
import campaign_common as common
import mutable_view_construction_cluster as cluster
import replay_mutable_view_construction_cluster as replay
import run_address_observer_pair as predecessor
import target_pipeline


NOT_RUN = {field: "not-run" for field in target_pipeline.RESULT_FIELDS}
BASELINE_RESULTS = {
    **predecessor.BASELINE_RESULTS,
    **predecessor.CLUSTER_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *predecessor.PRESERVED_ARTIFACT_IDS,
    *(config.artifact_id for config in predecessor_targets.TARGETS),
)
CLUSTER_RESULTS = {
    (config.target, config.input_order): config.expected_classification
    for config in cluster.TARGETS
}
SUPERSEDED_CLUSTER_RESULTS = {
    key: {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    }
    for key in CLUSTER_RESULTS
}
SUCCESSOR_RESULTS = {
    (config.target, config.input_order): config.expected_classification
    for config in align_pair.TARGETS
}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/mutable_view_construction_cluster"
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
                raise ValueError(f"{key}: certified 56-target baseline changed")
        elif key in CLUSTER_RESULTS:
            if actual not in (
                NOT_RUN,
                CLUSTER_RESULTS[key],
                SUPERSEDED_CLUSTER_RESULTS[key],
            ):
                raise ValueError(
                    f"{key}: mutable-view result has unexpected state"
                )
            observed[key] = actual
        elif key in SUCCESSOR_RESULTS:
            if actual not in (NOT_RUN, SUCCESSOR_RESULTS[key]):
                raise ValueError(f"{key}: align-to successor result changed")
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    pending = all(
        observed[key] == NOT_RUN for key in cluster.TARGET_KEYS
    )
    delivered = all(
        observed[key] == CLUSTER_RESULTS[key] for key in cluster.TARGET_KEYS
    )
    superseded = all(
        observed[key] == SUPERSEDED_CLUSTER_RESULTS[key]
        for key in cluster.TARGET_KEYS
    )
    if not (pending or delivered or superseded):
        raise ValueError("mutable-view targets must be uniformly delivered")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in cluster.TARGET_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed authority data")
        if _row_key(before) not in set(cluster.TARGET_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed out-of-scope row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during reset")
    return reset_csv, reset_json


def _validate_crosswalk_identity(
    config: cluster.MutableViewTarget,
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
        "generated_declaration_sha256": (
            config.generated_declaration_sha256
        ),
        "source_file_sha256": config.source_file_sha256,
        "source_item_sha256": config.source_item_sha256,
        "public_docs_sha256": config.public_docs_sha256,
        "harness_sha256": config.harness_sha256,
        "source_body_manifest_sha256": (
            config.source_body_manifest_sha256
        ),
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
        raise ValueError(f"{config.target}: readable authority binding changed")
    return row


def _trust_site_records(
    config: cluster.MutableViewTarget,
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
        if cluster.canonical_json_sha256(by_id[record_id]) != expected_hash:
            raise ValueError(f"{record_id}: readable trust record changed")
    for record_id in config.context_only_trust_site_ids:
        if not by_id[record_id]["semantic_disposition"].startswith(
            "context-only"
        ):
            raise ValueError(f"{record_id}: context-only site was relabeled")
    for record_id in config.admitted_trust_site_ids:
        if not by_id[record_id]["semantic_disposition"].startswith(
            "admissible"
        ):
            raise ValueError(f"{record_id}: lower site was relabeled")
    for record_id in config.excluded_trust_site_ids:
        if not by_id[record_id]["semantic_disposition"].startswith(
            "inadmissible"
        ):
            raise ValueError(f"{record_id}: answer-bearing site was relabeled")
    replacement = cluster.obligation_metadata(config, cluster.PRIMARY)[
        "source_backed_replacements"
    ][0]
    if set(replacement["replaces_trust_site_ids"]) != set(
        config.excluded_trust_site_ids
    ):
        raise ValueError(f"{config.target}: replacement partition changed")
    return [by_id[site] for site in config.all_trust_site_ids]


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"invalid source range {path}:{start}-{end}")
    return "".join(lines[start - 1 : end])


def _write_exact(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def _copy_exact(source: Path, target: Path, expected_sha256: str) -> None:
    if not source.is_file() or common.sha256(source) != expected_sha256:
        raise RuntimeError(f"frozen source hash mismatch: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if common.sha256(target) != expected_sha256:
        raise RuntimeError(f"copied input hash mismatch: {target}")


def _write_bound_inputs(
    config: cluster.MutableViewTarget,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_source = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_source) != config.source_file_sha256:
        raise RuntimeError(f"{config.target}: canonical source changed")
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{config.target}: shared vocabulary changed")

    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    exact_text = {
        "active_contract.txt": (
            config.active_contract_text,
            config.active_contract_sha256,
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            config.generated_declaration_sha256,
        ),
        "source_item.rs": (
            row["source_item_text"],
            config.source_item_sha256,
        ),
        "public_docs.md": (
            row["public_docs_text"],
            config.public_docs_sha256,
        ),
    }
    files: dict[str, Any] = {}
    for filename, (text, digest) in exact_text.items():
        path = root / filename
        _write_exact(path, text, digest)
        files[filename] = target_pipeline.artifact_record(path)

    vocabulary_path = root / "mutable_view_vocabulary.rs"
    vocabulary_path.write_text(
        "\n".join(
            _source_excerpt(vocabulary_source, start, end)
            for start, end in cluster.VOCABULARY_RANGES
        )
    )
    files[vocabulary_path.name] = {
        **target_pipeline.artifact_record(vocabulary_path),
        "canonical_path": str(vocabulary_source),
        "canonical_file_sha256": row["shared_vocabulary_sha256"],
        "source_ranges": [
            f"{start}-{end}" for start, end in cluster.VOCABULARY_RANGES
        ],
    }

    helper_texts: dict[str, str] = {}
    helper_records: dict[str, Any] = {}
    for source in config.helper_sources:
        canonical = common.RUST_LIBRARY / source.path
        if (
            not canonical.is_file()
            or common.sha256(canonical) != source.file_sha256
        ):
            raise RuntimeError(
                f"{config.target}: canonical helper changed: {source.path}"
            )
        text = _source_excerpt(canonical, source.start, source.end)
        helper_texts[source.name] = text
        path = root / source.filename
        path.write_text(text)
        helper_records[source.name] = {
            **target_pipeline.artifact_record(path),
            "canonical_path": str(canonical),
            "canonical_file_sha256": source.file_sha256,
            "source_lines": source.reference,
        }
    cluster.validate_source_anchors(
        config,
        row["source_item_text"],
        row["public_docs_text"],
        vocabulary_path.read_text(),
        helper_texts,
    )

    frozen_bindings = {
        "implproof_harness.rs": ("frozen_harness_path", config.harness_sha256),
        "source_body.json": (
            "frozen_source_body_manifest_path",
            config.source_body_manifest_sha256,
        ),
        "transformation_manifest.json": (
            "frozen_transformation_manifest_path",
            config.transformation_manifest_sha256,
        ),
        "dependency_assumption_manifest.json": (
            "frozen_dependency_manifest_path",
            config.dependency_manifest_sha256,
        ),
    }
    frozen: dict[str, Any] = {}
    for filename, (path_field, digest) in frozen_bindings.items():
        source = common.OUT / row[path_field]
        target = root / filename
        _copy_exact(source, target, digest)
        frozen[filename] = {
            **target_pipeline.artifact_record(target),
            "frozen_source_path": row[path_field],
            "frozen_source_sha256": digest,
        }

    manifest_path = root / "manifest.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "target": config.target,
            "input_order": config.input_order,
            "active_contract_sha256": config.active_contract_sha256,
            "files": files,
            "canonical_helpers": helper_records,
            "frozen_implproof": frozen,
            "trust_record_ids": list(config.all_trust_site_ids),
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
    require_model: bool = False,
    witness: bool = False,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
        [z3, "-smt2", str(path)],
        cwd=common.OUT,
    )
    target_pipeline.require_clean_result(record, expected, label=label)
    stdout = (common.OUT / record["stdout"]).read_text()
    markers = (
        (
            "(s_return_final s1)",
            "(s_return_final s2)",
            "(s_input_final s1)",
            "(s_input_final s2)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else ("(y_length y1)", "(s_input_final s1)")
    )
    if require_model and (
        len(stdout.splitlines()) < 2
        or any(marker not in stdout for marker in markers)
    ):
        raise RuntimeError(f"{label}: SAT source model was not retained")
    if not require_model and stdout != expected + "\n":
        raise RuntimeError(f"{label}: solver stdout was not exact")
    record.update(
        {
            "solver_result": expected,
            "expected_solver_result": expected,
            "model_retained": require_model,
            "stdout_sha256": common.sha256(common.OUT / record["stdout"]),
        }
    )
    return record


def _run_target(
    config: cluster.MutableViewTarget,
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
            "record_sha256": config.trust_hashes,
        },
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, cluster.boundary_manifest(config))
    bound_inputs_path = _write_bound_inputs(config, row, evidence_root)

    translation_path = evidence_root / "contract_translation_audit.json"
    metadata = cluster.obligation_metadata(config, cluster.PRIMARY)
    common.write_json(
        translation_path,
        {
            "schema_version": 1,
            "target": config.target,
            "active_contract_sha256": config.active_contract_sha256,
            "active_contract_preserved": True,
            "opaque_vocabulary_declared_to_solver": False,
            "canonical_answer_conjoined_outside_active_contract": False,
            "source_flow": metadata["contract_translation"]["source_flow"],
            "excluded_sites_replaced_not_relabeled": list(
                config.excluded_trust_site_ids
            ),
        },
    )

    obligations: dict[str, Any] = {}
    solver_results: dict[str, str] = {}
    for purpose, stem in (
        (cluster.PRIMARY, "obligation"),
        (cluster.EXACT_OUTPUT, "exact_output_obligation"),
    ):
        text, obligation_metadata = cluster.obligation(config, purpose)
        cluster.validate_target_obligation(config, text, obligation_metadata)
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, obligation_metadata)
        solver = _run_solver(
            z3,
            evidence_root,
            stem,
            smt_path,
            config.expected_solver_results[purpose],
        )
        solver_results[purpose] = solver["solver_result"]
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    witness_smt = evidence_root / "fixed_full_state_witness.smt2"
    witness_json = evidence_root / "fixed_full_state_witness.json"
    witness_smt.write_text(cluster.fixed_full_state_witness_text(config))
    common.write_json(witness_json, cluster.witness_payload(config))
    witness_solver = _run_solver(
        z3,
        evidence_root,
        "fixed_full_state_witness",
        witness_smt,
        "sat",
        require_model=True,
        witness=True,
    )
    witness_record = {
        "smt": target_pipeline.artifact_record(witness_smt),
        "payload": target_pipeline.artifact_record(witness_json),
        "solver": witness_solver,
        "fixed_input": True,
        "fixed_boundary": True,
        "both_specs_satisfied": True,
    }

    classification = {
        "exact_output_determinism_status": (
            "conditional-complete"
            if solver_results[cluster.EXACT_OUTPUT] == "unsat"
            else "solver-unknown"
        ),
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
            if (
                solver_results[cluster.PRIMARY] == "sat"
                and witness_solver["solver_result"] == "sat"
            )
            else "solver-unknown"
        ),
    }
    if classification != config.expected_classification:
        raise RuntimeError(
            f"{config.target}: solver evidence did not justify "
            f"{config.expected_classification}: {classification}"
        )

    source_instances: dict[str, Any] = {}
    for name, case in cluster.source_cases(config).items():
        path = evidence_root / "source_instances" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cluster.source_instance_text(config, name))
        source_instances[name] = {
            "input": {
                field: list(value) if isinstance(value, tuple) else value
                for field, value in vars(case).items()
            },
            "expected_source_outcome": cluster.evaluate_source(config, case),
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                z3,
                evidence_root,
                f"source_instances/{name}",
                path,
                "sat",
                require_model=True,
            ),
        }

    negative_probes: dict[str, Any] = {}
    for name in cluster.negative_probe_names(config):
        path = evidence_root / "negative_probes" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cluster.negative_probe_text(config, name))
        negative_probes[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                z3,
                evidence_root,
                f"negative_probes/{name}",
                path,
                "unsat",
            ),
        }

    replay_record = target_pipeline.capture_command(
        evidence_root / "solver_replay",
        [
            sys.executable,
            str(
                common.OUT
                / "tools/replay_mutable_view_construction_cluster.py"
            ),
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
    replay_result = json.loads(replay_stdout)
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{config.target}: replay did not report passed")
    replay_record["result"] = replay_result

    source_model = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    source_model.write_text(cluster.verus_text(config))
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
        or cluster.VERUS_EXPECTED_SUMMARY not in verification_stdout
    ):
        raise RuntimeError(f"{config.target}: Verus model did not verify")

    guards_path = evidence_root / "reviewed_model_guards.json"
    common.write_json(
        guards_path,
        {
            "schema_version": 1,
            "target": config.target,
            "fail_closed_mutations": [
                "opaque functionality relation",
                "answer-bearing boundary role",
                "affine answer laundering through a boundary field",
                "canonical answer outside the active contract",
                "strengthened semantic Requires_T precondition",
                "weakened output or final-state equality",
                "wrong checked multiplication or overflow panic",
                "invalid unchecked multiplication",
                "wrong option branch",
                "wrong returned range or projection",
                "lost mutable pointer address/allocation/provenance",
                "lost root-borrow identity or exclusivity",
                "wrong singleton array-to-slice unsizing",
                "wrong borrow-lifetime length or receiver reconstruction",
                "wrong outside-memory frame",
                "null, misaligned, allocation, provenance, alias, or borrow input",
                "out-of-scope crosswalk update",
            ],
            "enforcement": (
                "tools/mutable_view_construction_cluster.py exact reviewed "
                "obligation plus tests/test_mutable_view_construction_cluster.py"
            ),
        },
    )

    result = {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "artifact_id": config.artifact_id,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "classification": classification,
        "classification_basis": (
            "The exact-output theorem negation replays UNSAT. The full-state "
            "negation and a concrete fixed-input/fixed-boundary witness replay "
            "SAT because legal returned-borrow writes remain free at the exact "
            "returned length. Receiver/return reconstruction, prefix suffix, "
            "outside frame, and backing identity/provenance remain enforced."
        ),
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "trust_site_bindings": target_pipeline.artifact_record(trust_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "contract_translation_audit": target_pipeline.artifact_record(
            translation_path
        ),
        "reviewed_model_guards": target_pipeline.artifact_record(guards_path),
        "obligations": obligations,
        "fixed_full_state_witness": witness_record,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
        "solver_replay": replay_record,
        "verus": {
            "source_model": target_pipeline.artifact_record(source_model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
            "expected_summary": cluster.VERUS_EXPECTED_SUMMARY,
        },
        "excluded_retained_trust_site_ids": list(
            config.excluded_trust_site_ids
        ),
        "remaining_not_run_rows": 2,
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
        "independent_review": "required",
        "stage_transition": "disabled",
    }
    result_path = evidence_root / "result.json"
    common.write_json(result_path, result)
    return result


def _update_ledgers() -> None:
    csv_rows, json_rows = _load_crosswalks()
    preserved = copy.deepcopy(BASELINE_RESULTS)
    updated_csv = csv_rows
    updated_json = json_rows
    for config in cluster.TARGETS:
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
    if classified != set(preserved) or len(classified) != 60 or not_run != 2:
        raise RuntimeError(
            f"expected 60 classified and 2 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def _write_array_from_mut_excerpt() -> dict[str, Any]:
    source = common.RUST_LIBRARY / cluster.ARRAY_SOURCE_PATH
    if common.sha256(source) != cluster.ARRAY_SOURCE_SHA256:
        raise RuntimeError("canonical core::array source changed")
    text = _source_excerpt(source, 174, 177)
    path = CLUSTER_ROOT / "source_excerpts/core_array_from_mut_174_177.rs"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != cluster.ARRAY_FROM_MUT_EXCERPT_SHA256:
        raise RuntimeError("core::array::from_mut excerpt changed")
    return {
        **target_pipeline.artifact_record(path),
        "canonical_path": str(source),
        "canonical_file_sha256": cluster.ARRAY_SOURCE_SHA256,
        "source_lines": "core/src/array/mod.rs:174-177",
    }


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for mutable-view evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 56 or len(PRESERVED_ARTIFACT_IDS) != 56:
        raise RuntimeError("certified predecessor baseline is not 56 targets")
    if tree_file_count(FROZEN_ROOT) != EXPECTED_FROZEN_FILE_COUNT:
        raise RuntimeError("frozen input tree does not contain exactly 320 files")

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
        for config in cluster.TARGETS
    }
    mutable_roots["mutable_view_construction_cluster"] = CLUSTER_ROOT
    proof_paths = {
        config.artifact_id: common.OUT / "proofs" / f"{config.artifact_id}.rs"
        for config in cluster.TARGETS
    }

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".mutable-view-construction-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        existing_roots: set[str] = set()
        existing_proofs: set[str] = set()
        for name, path in mutable_roots.items():
            if path.is_dir():
                shutil.copytree(path, backup_root / name)
                existing_roots.add(name)
        for artifact_id, path in proof_paths.items():
            if path.is_file():
                shutil.copyfile(path, backup_root / f"{artifact_id}.rs")
                existing_proofs.add(artifact_id)
        try:
            _write_crosswalks(reset_csv, reset_json)
            results = {
                config.artifact_id: _run_target(config, z3)
                for config in cluster.TARGETS
            }
            _update_ledgers()

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = tree_digest(FROZEN_ROOT)
            if preserved_after != preserved_before:
                raise RuntimeError(
                    "mutable-view run mutated certified target evidence"
                )
            if (
                frozen_after != frozen_before
                or tree_file_count(FROZEN_ROOT)
                != EXPECTED_FROZEN_FILE_COUNT
            ):
                raise RuntimeError("mutable-view run mutated frozen inputs")

            if CLUSTER_ROOT.exists():
                shutil.rmtree(CLUSTER_ROOT)
            CLUSTER_ROOT.mkdir(parents=True)
            array_excerpt = _write_array_from_mut_excerpt()
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
                        for config in cluster.TARGETS
                    ],
                    "project_local_array_from_mut_excerpt": array_excerpt,
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
                    "classified_rows": 60,
                    "not_run_rows": 2,
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
                if name in existing_roots:
                    shutil.copytree(backup_root / name, path)
            for artifact_id, path in proof_paths.items():
                if path.exists():
                    path.unlink()
                if artifact_id in existing_proofs:
                    shutil.copyfile(
                        backup_root / f"{artifact_id}.rs",
                        path,
                    )
            raise

    print("mutable_view_construction_cluster=PASS")
    for config in cluster.TARGETS:
        print(
            f"target_{config.input_order}="
            "unsat/conditional-complete_exact,"
            "sat/conditional-incomplete_full"
        )
    print("preserved_target_evidence=56")
    print("frozen_inputs=320")
    print("target_result_counts=60_classified,2_not-run")


if __name__ == "__main__":
    main()
