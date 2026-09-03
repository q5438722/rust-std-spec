#!/usr/bin/env python3
"""Validation helpers for the target-080/082 evidence increment."""

from __future__ import annotations

import json
from pathlib import Path
from types import ModuleType
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
import replay_unstable_sort_companions as replay
import run_unstable_sort_companions as runner
import target_080
import target_082
import target_077
import target_pipeline


MODULES = (target_080, target_082)
FILENAME_BY_PURPOSE = {
    target_080.PRIMARY: "obligation",
    target_080.BOUNDED_SANITY: "bounded_sanity",
    target_080.EXACT_FINAL_SLICE: "exact_final_slice_obligation",
}


def _load_json(path: Path, errors: list[str], label: str) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is unreadable: {exc}")
        return {}


def _artifact_matches(
    record: Any,
    path: Path,
    errors: list[str],
    label: str,
) -> None:
    if not isinstance(record, dict) or not path.is_file():
        errors.append(f"{label} is missing")
        return
    if (
        record.get("path") != common.relpath(path)
        or record.get("sha256") != common.sha256(path)
        or record.get("bytes") != path.stat().st_size
    ):
        errors.append(f"{label} artifact record is stale")


def _solver_capture(
    record: Any,
    expected: str,
    errors: list[str],
    label: str,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label} solver record is missing")
        return
    try:
        stdout = (common.OUT / record["stdout"]).read_text()
        stderr = (common.OUT / record["stderr"]).read_text()
        status = (common.OUT / record["status"]).read_text()
        command = (common.OUT / record["command"]).read_text()
    except (KeyError, OSError) as exc:
        errors.append(f"{label} solver capture is unreadable: {exc}")
        return
    if (
        record.get("exit_code") != 0
        or record.get("solver_result") != expected
        or record.get("expected_solver_result") != expected
        or stdout.splitlines()[:1] != [expected]
        or stderr != ""
        or status != "0\n"
        or "-smt2" not in command
    ):
        errors.append(f"{label} solver capture is invalid")


def _validate_target(
    errors: list[str],
    module: ModuleType,
    crosswalk_by_key: dict[tuple[str, str], dict[str, str]],
) -> None:
    root = common.OUT / "evidence/targets" / module.ARTIFACT_ID
    result = _load_json(root / "result.json", errors, f"{module.TARGET} result")
    expected_status = runner.COMPANION_RESULTS[
        (module.TARGET, module.INPUT_ORDER)
    ]
    if (
        result.get("target") != module.TARGET
        or result.get("input_order") != module.INPUT_ORDER
        or result.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_status
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append(f"{module.TARGET} result identity/classification is malformed")

    row = crosswalk_by_key.get((module.TARGET, module.INPUT_ORDER))
    if row is None or any(row[field] != value for field, value in expected_status.items()):
        errors.append(f"{module.TARGET} crosswalk result is missing")

    boundary_path = root / "boundary_manifest.json"
    boundary = _load_json(
        boundary_path, errors, f"{module.TARGET} boundary manifest"
    )
    if boundary != module.boundary_manifest():
        errors.append(f"{module.TARGET} boundary manifest changed")
    _artifact_matches(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{module.TARGET} boundary manifest",
    )

    trust_path = root / "trust_site_bindings.json"
    trust = _load_json(trust_path, errors, f"{module.TARGET} trust bindings")
    if {
        item.get("record_id") for item in trust.get("records", [])
    } != set(module.ALL_AUDITED_TRUST_SITES):
        errors.append(f"{module.TARGET} trust-site bindings are incomplete")
    _artifact_matches(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{module.TARGET} trust bindings",
    )

    authority_path = root / "authority_bindings.json"
    authority = _load_json(
        authority_path, errors, f"{module.TARGET} authority bindings"
    )
    bindings = authority.get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or bindings.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or set(bindings.get("all_trust_site_ids", "").split(";"))
        != set(module.ALL_AUDITED_TRUST_SITES)
        or set(bindings.get("inadmissible_trust_site_ids", "").split(";"))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append(f"{module.TARGET} authority bindings are stale")
    _artifact_matches(
        result.get("authority_bindings"),
        authority_path,
        errors,
        f"{module.TARGET} authority bindings",
    )

    bound_inputs_path = root / "bound_inputs/manifest.json"
    bound_inputs = _load_json(
        bound_inputs_path, errors, f"{module.TARGET} bound inputs"
    )
    if (
        bound_inputs.get("target") != module.TARGET
        or bound_inputs.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or set(bound_inputs.get("frozen_implproof", {}))
        != {
            "harness",
            "transformation_manifest",
            "dependency_manifest",
            "source_body_manifest",
        }
    ):
        errors.append(f"{module.TARGET} bound-input manifest is incomplete")
    _artifact_matches(
        result.get("bound_inputs"),
        bound_inputs_path,
        errors,
        f"{module.TARGET} bound inputs",
    )
    for name, record in bound_inputs.get("files", {}).items():
        path = common.OUT / record.get("path", "")
        _artifact_matches(
            record, path, errors, f"{module.TARGET} bound input {name}"
        )

    obligations = result.get("obligations", {})
    if set(obligations) != set(module.PURPOSES):
        errors.append(f"{module.TARGET} obligation result set is incomplete")
    for purpose, filename in FILENAME_BY_PURPOSE.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        metadata = _load_json(
            metadata_path,
            errors,
            f"{module.TARGET} {purpose} metadata",
        )
        if smt_path.is_file():
            try:
                module.validate_target_obligation(
                    smt_path.read_text(), metadata
                )
            except Exception as exc:
                errors.append(
                    f"{module.TARGET} {purpose} obligation rejected: {exc}"
                )
        else:
            errors.append(f"{module.TARGET} {purpose} SMT is missing")
        evidence = obligations.get(purpose, {})
        _artifact_matches(
            evidence.get("smt"),
            smt_path,
            errors,
            f"{module.TARGET} {purpose} SMT",
        )
        _artifact_matches(
            evidence.get("metadata"),
            metadata_path,
            errors,
            f"{module.TARGET} {purpose} metadata",
        )
        _solver_capture(
            evidence.get("solver"),
            metadata.get("expected_solver_result", ""),
            errors,
            f"{module.TARGET} {purpose}",
        )
    primary_metadata = _load_json(
        root / "obligation.metadata.json",
        errors,
        f"{module.TARGET} primary metadata",
    )
    if primary_metadata.get("domain", {}).get("bounded") is not False:
        errors.append(f"{module.TARGET} completeness proof is not general-domain")

    exact_path = root / "exact_final_slice_witness.smt2"
    if (
        not exact_path.is_file()
        or exact_path.read_text() != module.fixed_exact_model_text()
    ):
        errors.append(f"{module.TARGET} exact witness model changed")
    exact_evidence = result.get("exact_final_slice_witness", {})
    _artifact_matches(
        exact_evidence.get("smt"),
        exact_path,
        errors,
        f"{module.TARGET} exact witness",
    )
    _solver_capture(
        exact_evidence.get("solver"),
        "sat",
        errors,
        f"{module.TARGET} exact witness",
    )

    for polarity, positive in (("positive", True), ("negative", False)):
        path = root / f"equal_class_equivalence.{polarity}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != module.equivalence_probe_text(positive=positive)
        ):
            errors.append(
                f"{module.TARGET} {polarity} equivalence witness changed"
            )
        evidence = result.get("equivalence_witnesses", {}).get(polarity, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{module.TARGET} {polarity} equivalence witness",
        )
        _solver_capture(
            evidence.get("solver"),
            "sat",
            errors,
            f"{module.TARGET} {polarity} equivalence witness",
        )

    witness_path = root / "witness.json"
    if _load_json(
        witness_path, errors, f"{module.TARGET} witness"
    ) != module.witness_payload():
        errors.append(f"{module.TARGET} witness payload changed")
    try:
        replay_result = replay.replay(witness_path)
        if replay_result.get("status") != "passed":
            errors.append(f"{module.TARGET} witness replay did not pass")
    except Exception as exc:
        errors.append(f"{module.TARGET} witness replay failed: {exc}")
    _artifact_matches(
        result.get("witness"),
        witness_path,
        errors,
        f"{module.TARGET} witness",
    )

    source_model = common.OUT / module.CONFIG.proof_filename
    captured_model = root / "verus/contract_model.rs"
    if (
        not source_model.is_file()
        or not captured_model.is_file()
        or source_model.read_bytes() != captured_model.read_bytes()
        or "external_body" in captured_model.read_text()
    ):
        errors.append(f"{module.TARGET} Verus source/capture is invalid")
    verus = result.get("verus", {})
    _artifact_matches(
        verus.get("source_model"),
        source_model,
        errors,
        f"{module.TARGET} source Verus model",
    )
    _artifact_matches(
        verus.get("captured_model"),
        captured_model,
        errors,
        f"{module.TARGET} captured Verus model",
    )
    for key in ("typecheck", "verification"):
        record = verus.get(key, {})
        try:
            stdout = (common.OUT / record["stdout"]).read_text()
            stderr = (common.OUT / record["stderr"]).read_text()
            status = (common.OUT / record["status"]).read_text()
        except (KeyError, OSError) as exc:
            errors.append(f"{module.TARGET} Verus {key} is unreadable: {exc}")
            continue
        if record.get("exit_code") != 0 or stderr or status != "0\n":
            errors.append(f"{module.TARGET} Verus {key} failed")
        if key == "verification" and module.CONFIG.verus_expected_summary not in stdout:
            errors.append(f"{module.TARGET} Verus summary changed")


def validate(errors: list[str]) -> None:
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for module in MODULES:
        _validate_target(errors, module, by_key)

    classified = {
        key
        for key, row in by_key.items()
        if any(
            row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS
        )
    }
    target_077_key = (target_077.TARGET, target_077.INPUT_ORDER)
    expected_classified = (
        set(runner.BASELINE_RESULTS)
        | set(runner.CLUSTER_KEYS)
        | {
            target_077_key,
            ("core::slice::select_nth_unstable_by", "78"),
            ("core::slice::select_nth_unstable_by_key", "79"),
        }
        | set(constructors.TARGET_KEYS)
        | set(edge.TARGET_KEYS)
        | set(clone_cluster.TARGET_KEYS)
        | set(exact_partitions.TARGET_KEYS)
        | set(fixed_chunks.TARGET_KEYS)
        | set(split_primitives.TARGET_KEYS)
        | set(split_off.TARGET_KEYS)
        | set(raw_slice.TARGET_KEYS)
        | set(slice_trio.TARGET_KEYS)
        | set(address_pair.TARGET_KEYS)
        | set(mutable_views.TARGET_KEYS)
        | set(align_pair.TARGET_KEYS)
    )
    target_077_row = by_key.get(target_077_key)
    if (
        classified != expected_classified
        or target_077_row is None
        or target_077_row["exact_output_determinism_status"]
        != "conditional-incomplete"
        or target_077_row[
            "completeness_modulo_reviewed_equivalence_status"
        ]
        != "conditional-complete"
    ):
        errors.append(
            "unstable-sort evidence was not preserved through target 077"
        )
    if len(classified) != 62 or len(rows) - len(classified) != 0:
        errors.append(
            "downstream align-to increment did not finish at 62/0"
        )

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "unstable-sort companion manifest",
    )
    if (
        manifest.get("execution_order")
        != [module.TARGET for module in MODULES]
        or manifest.get("classified_rows") != 24
        or manifest.get("not_run_rows") != 38
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("unstable-sort companion manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(
                f"unstable-sort run did not preserve {artifact_id}"
            )
