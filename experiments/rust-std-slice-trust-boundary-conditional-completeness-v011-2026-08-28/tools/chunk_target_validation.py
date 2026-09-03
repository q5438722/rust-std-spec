#!/usr/bin/env python3
"""Independent artifact validation for the five chunk contract-drift targets."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import clone_effect_cluster as clone_cluster
import exact_mutable_iterator_partitions as exact_partitions
import mutable_edge_extraction as edge
import mutable_fixed_chunk_edges as fixed_chunks
import mutable_iterator_constructors as constructors
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import chunk_contract_drift_cluster as cluster
import replay_chunk_contract_drift
import run_chunk_contract_drift_cluster as runner
import target_pipeline


def _load(path: Path) -> Any:
    return json.loads(path.read_text())


def _artifact_valid(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    path = common.OUT / str(record.get("path", ""))
    return (
        path.is_file()
        and record.get("sha256") == common.sha256(path)
        and record.get("bytes") == path.stat().st_size
    )


def _capture_valid(record: Any, expected: str) -> bool:
    if not isinstance(record, dict) or record.get("exit_code") != 0:
        return False
    try:
        stdout = (common.OUT / record["stdout"]).read_text()
        stderr = (common.OUT / record["stderr"]).read_text()
        status = (common.OUT / record["status"]).read_text()
        command = (common.OUT / record["command"]).read_text()
    except (KeyError, OSError):
        return False
    return (
        status == "0\n"
        and not stderr
        and stdout.splitlines()
        and stdout.splitlines()[0] == expected
        and record.get("solver_result", expected) == expected
        and command.strip()
    )


def _validate_bound_inputs(
    errors: list[str],
    config: cluster.ChunkTarget,
    result: dict[str, Any],
) -> None:
    record = result.get("bound_inputs")
    if not _artifact_valid(record):
        errors.append(f"{config.artifact_id}: bound-input manifest hash is invalid")
        return
    manifest = _load(common.OUT / record["path"])
    for name, artifact in manifest.get("artifacts", {}).items():
        if not _artifact_valid(artifact):
            errors.append(f"{config.artifact_id}: bound input {name} is invalid")
    for name, source in manifest.get("canonical_sources", {}).items():
        if not _artifact_valid(source.get("artifact")):
            errors.append(
                f"{config.artifact_id}: canonical source {name} is invalid"
            )
    pointer = manifest.get("accepted_pointer_dependency", {})
    if (
        pointer.get("artifact_id") != config.pointer_dependency
        or not _artifact_valid(pointer.get("result"))
        or not _artifact_valid(pointer.get("source_model"))
        or not _artifact_valid(pointer.get("independent_review"))
        or "no returned pointer is copied into Boundary_T"
        not in pointer.get("admission_mode", "")
    ):
        errors.append(f"{config.artifact_id}: pointer dependency is invalid")
    lower = manifest.get("ordered_lower_dependency")
    if config.lower_dependency is None:
        if lower is not None:
            errors.append(
                f"{config.artifact_id}: unexpected lower dependency was recorded"
            )
    elif (
        not isinstance(lower, dict)
        or lower.get("artifact_id") != config.lower_dependency
        or not _artifact_valid(lower.get("result"))
        or not _artifact_valid(lower.get("obligation"))
        or not _artifact_valid(lower.get("source_model"))
        or "no lower output or final state enters Boundary_T"
        not in lower.get("admission_mode", "")
    ):
        errors.append(f"{config.artifact_id}: lower dependency is invalid")


def validate_target(
    errors: list[str],
    config: cluster.ChunkTarget,
    *,
    expected_not_run: int,
) -> None:
    root = common.OUT / "evidence/targets" / config.artifact_id
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append(f"{config.artifact_id}: result.json is missing")
        return
    try:
        result = _load(result_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{config.artifact_id}: unreadable result.json: {exc}")
        return
    row = cluster.authority_row(config.input_order)
    if (
        result.get("target") != config.target
        or result.get("input_order") != config.input_order
        or result.get("active_contract_sha256")
        != config.active_contract_sha256
        or result.get("active_contract_text") != row["active_contract_text"]
        or result.get("rejected_retained_contract_sha256")
        != config.retained_contract_sha256
        or result.get("classification") != config.expected_results
        or result.get("remaining_not_run") != expected_not_run
        or result.get("updated_crosswalk_fields")
        != sorted(target_pipeline.RESULT_FIELDS)
    ):
        errors.append(f"{config.artifact_id}: result identity/classification is invalid")

    for name in ("authority_bindings", "boundary_manifest"):
        if not _artifact_valid(result.get(name)):
            errors.append(f"{config.artifact_id}: {name} artifact is invalid")
    _validate_bound_inputs(errors, config, result)

    boundary_record = result.get("boundary_manifest", {})
    if _artifact_valid(boundary_record):
        boundary = _load(common.OUT / boundary_record["path"])
        selectors = {
            field["selector"]
            for field in boundary.get("shared_boundary_observations", [])
        }
        if (
            boundary.get("active_contract_sha256")
            != config.active_contract_sha256
            or boundary.get("rejected_retained_contract_sha256")
            != config.retained_contract_sha256
            or not boundary.get("boundary_narrower_than_target")
            or selectors
            != {
                field[0]
                for field in cluster._boundary_field_specs(config)
            }
            or set(boundary.get("excluded_retained_trust_site_ids", []))
            != set(config.excluded_retained_trust_sites)
        ):
            errors.append(f"{config.artifact_id}: boundary manifest is malformed")
        if config is cluster.TARGET_015 and not {
            "TS-015-D006",
            "TS-015-E002",
        } <= set(boundary.get("excluded_retained_trust_site_ids", [])):
            errors.append("target 015 reuses an answer-bearing retained helper")

    obligations = result.get("obligations", {})
    for purpose, filename in (
        (cluster.PRIMARY, "obligation"),
        (cluster.EXACT_OUTPUT, "exact_output_obligation"),
    ):
        evidence = obligations.get(purpose, {})
        smt = evidence.get("smt")
        metadata = evidence.get("metadata")
        expected = config.expected_solver_results[purpose]
        if not _artifact_valid(smt) or not _artifact_valid(metadata):
            errors.append(
                f"{config.artifact_id}: {purpose} artifacts are invalid"
            )
            continue
        text = (common.OUT / smt["path"]).read_text()
        actual_metadata = _load(common.OUT / metadata["path"])
        try:
            cluster.validate_target_obligation(
                config, text, actual_metadata
            )
        except Exception as exc:
            errors.append(
                f"{config.artifact_id}: {purpose} checker rejection: {exc}"
            )
        if not _capture_valid(evidence.get("solver"), expected):
            errors.append(
                f"{config.artifact_id}: {purpose} solver capture is invalid"
            )

    expected_probes = cluster.probe_cases(config)
    probes = result.get("satisfiability_and_rejection_probes", {})
    if set(probes) != set(expected_probes):
        errors.append(f"{config.artifact_id}: probe set is incomplete")
    for name, case in expected_probes.items():
        evidence = probes.get(name, {})
        if (
            evidence.get("kind") != case["kind"]
            or evidence.get("expected_solver_result") != case["expected"]
            or not _artifact_valid(evidence.get("smt"))
            or not _capture_valid(evidence.get("solver"), case["expected"])
        ):
            errors.append(f"{config.artifact_id}: probe {name} is invalid")
            continue
        if (
            common.OUT / evidence["smt"]["path"]
        ).read_text() != cluster.probe_text(config, name):
            errors.append(f"{config.artifact_id}: probe {name} changed")

    witness = result.get("witness")
    fixed = result.get("fixed_sat_replay")
    if config.mutable:
        if not isinstance(witness, dict) or not _artifact_valid(
            witness.get("artifact")
        ):
            errors.append(f"{config.artifact_id}: witness artifact is invalid")
        try:
            replay_record = witness["replay"]
            replay_stdout = (
                common.OUT / replay_record["stdout"]
            ).read_text()
            replay_stderr = (
                common.OUT / replay_record["stderr"]
            ).read_text()
            replay_result = json.loads(replay_stdout)
            independently_replayed = replay_chunk_contract_drift.replay(
                common.OUT / witness["artifact"]["path"]
            )
        except (KeyError, OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{config.artifact_id}: witness replay is invalid: {exc}")
        else:
            if (
                replay_record.get("exit_code") != 0
                or replay_stderr
                or replay_result != independently_replayed
                or replay_result.get("status") != "passed"
            ):
                errors.append(f"{config.artifact_id}: witness replay changed")
        if (
            not isinstance(fixed, dict)
            or not _artifact_valid(fixed.get("smt"))
            or not _capture_valid(fixed.get("solver"), "sat")
        ):
            errors.append(f"{config.artifact_id}: fixed SAT model is invalid")
        elif (
            common.OUT / fixed["smt"]["path"]
        ).read_text() != cluster.fixed_model_text(config):
            errors.append(f"{config.artifact_id}: fixed SAT model changed")
    elif witness is not None or fixed is not None:
        errors.append(f"{config.artifact_id}: immutable target carries SAT evidence")

    verus = result.get("verus", {})
    source_model = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = verus.get("captured_model")
    try:
        captured_path = common.OUT / captured["path"]
    except (KeyError, TypeError):
        captured_path = Path()
    verification = verus.get("verification", {})
    try:
        verification_stdout = (
            common.OUT / verification["stdout"]
        ).read_text()
        verification_stderr = (
            common.OUT / verification["stderr"]
        ).read_text()
    except (KeyError, OSError):
        verification_stdout = ""
        verification_stderr = "missing"
    if (
        not source_model.is_file()
        or not _artifact_valid(verus.get("source_model"))
        or not _artifact_valid(captured)
        or not captured_path.is_file()
        or source_model.read_bytes() != captured_path.read_bytes()
        or "external_body" in source_model.read_text()
        or verus.get("external_body_count") != 0
        or verus.get("verified_count", 0) <= 0
        or verification.get("exit_code") != 0
        or verification_stderr
        or not re.search(
            r"verification results::\s+[1-9]\d* verified,\s+0 errors",
            verification_stdout,
        )
    ):
        errors.append(f"{config.artifact_id}: Verus evidence is invalid")
    typecheck = verus.get("typecheck", {})
    try:
        typecheck_stderr = (common.OUT / typecheck["stderr"]).read_text()
    except (KeyError, OSError):
        typecheck_stderr = "missing"
    if typecheck.get("exit_code") != 0 or typecheck_stderr:
        errors.append(f"{config.artifact_id}: Verus type-check is invalid")

    preservation = result.get("preserved_target_evidence", {})
    for artifact_id, hashes in preservation.items():
        if (
            hashes.get("before_sha256") != hashes.get("after_sha256")
            or hashes.get("after_sha256")
            != runner.tree_digest(
                common.OUT / "evidence/targets" / artifact_id
            )
        ):
            errors.append(
                f"{config.artifact_id}: preserved evidence {artifact_id} changed"
            )


def validate_cluster(errors: list[str]) -> None:
    for index, config in enumerate(cluster.ORDERED_TARGETS, start=1):
        validate_target(errors, config, expected_not_run=48 - index)

    path = common.OUT / "logs/ordered_chunk_contract_drift_replay.json"
    try:
        manifest = _load(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ordered chunk replay manifest is unreadable: {exc}")
        return
    expected_ids = [config.artifact_id for config in cluster.ORDERED_TARGETS]
    expected_results = {
        config.artifact_id: config.expected_results
        for config in cluster.ORDERED_TARGETS
    }
    if (
        manifest.get("schema_version") != 1
        or manifest.get("status") != "passed"
        or manifest.get("ordered_artifact_ids") != expected_ids
        or manifest.get("final_cluster_results") != expected_results
        or manifest.get("classified") != 19
        or manifest.get("not_run") != 43
    ):
        errors.append("ordered chunk replay manifest is malformed")
    preservation = manifest.get("preserved_certified_evidence", {})
    if set(preservation) != set(runner.BASELINE_ARTIFACT_IDS):
        errors.append("ordered chunk replay does not cover all 14 baseline trees")
    for artifact_id, hashes in preservation.items():
        if (
            hashes.get("before_sha256") != hashes.get("after_sha256")
            or hashes.get("after_sha256")
            != runner.tree_digest(
                common.OUT / "evidence/targets" / artifact_id
            )
        ):
            errors.append(
                f"ordered chunk replay did not preserve {artifact_id}"
            )

    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    expected_classified = dict(runner.BASELINE_RESULTS)
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_results
            for config in cluster.ORDERED_TARGETS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in split_primitives.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in split_off.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in clone_cluster.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in edge.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in constructors.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in exact_partitions.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            key: {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            for key in fixed_chunks.TARGET_KEYS
        }
    )
    expected_classified.update(
        {
            ("core::slice::assume_init_drop", "25"): {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::assume_init_mut", "26"): {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
            },
            ("core::slice::write_clone_of_slice", "119"): {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
        }
    )
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in raw_slice.TARGETS
        }
    )
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in slice_trio.TARGETS
        }
    )
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in address_pair.TARGETS
        }
    )
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in mutable_views.TARGETS
        }
    )
    expected_classified.update(
        {
            (config.target, config.input_order): config.expected_classification
            for config in align_pair.TARGETS
        }
    )
    expected_classified.update(
        {
            ("core::slice::sort_unstable", "80"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::sort_unstable_by_key", "82"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::select_nth_unstable", "77"): {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
            },
            ("core::slice::select_nth_unstable_by", "78"): {
                "exact_output_determinism_status": "missing-source-backed-model",
                "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
            },
            ("core::slice::select_nth_unstable_by_key", "79"): {
                "exact_output_determinism_status": "missing-source-backed-model",
                "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
            },
        }
    )
    for key, row in by_key.items():
        actual = {
            field: row[field] for field in target_pipeline.RESULT_FIELDS
        }
        expected = expected_classified.get(key, runner.NOT_RUN)
        if actual != expected:
            errors.append(f"{key}: delivered result differs from bounded scope")
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    if len(expected_classified) != 62 or not_run != 0:
        errors.append(
            "delivered ledger did not finish at 62 classified/0 not-run"
        )
