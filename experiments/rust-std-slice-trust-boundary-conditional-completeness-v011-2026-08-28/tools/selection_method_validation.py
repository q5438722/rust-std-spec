#!/usr/bin/env python3
"""Validate the target-077 selection-method evidence increment."""

from __future__ import annotations

import json
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
import replay_target_077
import run_target_077
import target_077
import target_pipeline


def _load_json(path: Path, errors: list[str], label: str) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is unreadable: {exc}")
        return {}


def _artifact_matches(
    record: Any, path: Path, errors: list[str], label: str
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
    record: Any, expected: str, errors: list[str], label: str
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


def validate(errors: list[str]) -> None:
    root = common.OUT / "evidence/targets" / target_077.ARTIFACT_ID
    result = _load_json(root / "result.json", errors, "target-077 result")
    if (
        result.get("target") != target_077.TARGET
        or result.get("input_order") != target_077.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_077.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_077.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != run_target_077.RESULT_STATUSES
        or result.get("updated_crosswalk_fields")
        != sorted(target_pipeline.RESULT_FIELDS)
        or result.get("ledger_counts")
        != {"classified": 25, "not_run": 37}
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_077.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target-077 result identity/classification is malformed")

    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {
        (row["target"], row["input_order"]): row for row in rows
    }
    target_key = (target_077.TARGET, target_077.INPUT_ORDER)
    row = by_key.get(target_key)
    if row is None or any(
        row[field] != value
        for field, value in run_target_077.RESULT_STATUSES.items()
    ):
        errors.append("target-077 crosswalk result is missing")
    classified = {
        key
        for key, candidate in by_key.items()
        if any(
            candidate[field] != "not-run"
            for field in target_pipeline.RESULT_FIELDS
        )
    }
    callback_results = {
        ("core::slice::select_nth_unstable_by", "78"): {
            "exact_output_determinism_status": "missing-source-backed-model",
            "completeness_modulo_reviewed_equivalence_status": (
                "missing-source-backed-model"
            ),
        },
        ("core::slice::select_nth_unstable_by_key", "79"): {
            "exact_output_determinism_status": "missing-source-backed-model",
            "completeness_modulo_reviewed_equivalence_status": (
                "missing-source-backed-model"
            ),
        },
    }
    if (
        classified
        != set(run_target_077.BASELINE_RESULTS)
        | {target_key}
        | set(callback_results)
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
        or len(classified) != 62
        or len(rows) - len(classified) != 0
    ):
        errors.append("target-077 increment changed the classified target set")
    for key, expected in callback_results.items():
        candidate = next(
            (
                item
                for item in rows
                if (item["target"], item["input_order"]) == key
            ),
            None,
        )
        if candidate is None or any(
            candidate[field] != value for field, value in expected.items()
        ):
            errors.append(f"selection callback target {key} is not delivered")

    authority_path = root / "authority_bindings.json"
    authority = _load_json(
        authority_path, errors, "target-077 authority bindings"
    )
    bindings = authority.get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != target_077.ACTIVE_CONTRACT_SHA256
        or bindings.get("active_contract_text")
        != target_077.ACTIVE_CONTRACT_TEXT
        or set(bindings.get("all_trust_site_ids", "").split(";"))
        != set(target_077.ALL_AUDITED_TRUST_SITES)
        or set(bindings.get("inadmissible_trust_site_ids", "").split(";"))
        != set(target_077.EXCLUDED_RETAINED_TRUST_SITES)
        or bindings.get("source_item_sha256")
        != "dd55bbb0ec8084c8e81b3000133de113a2249b5c57d6ffa845cb5c5348909cd2"
        or bindings.get("public_docs_sha256")
        != "4aa7c4fa7c642d3384d542d278ce058e3672107098a172cd33ff05e19111051b"
    ):
        errors.append("target-077 authority bindings are stale")
    _artifact_matches(
        result.get("authority_bindings"),
        authority_path,
        errors,
        "target-077 authority bindings",
    )

    trust_path = root / "trust_site_bindings.json"
    trust = _load_json(trust_path, errors, "target-077 trust bindings")
    trust_records = {
        item.get("record_id"): item for item in trust.get("records", [])
        if isinstance(item, dict)
    }
    expected_dispositions = {
        "TS-077-D001": "context-only-specification-vocabulary",
        "TS-077-D002": "inadmissible-answer-bearing-support",
        "TS-077-D003": "admissible-source-backed-support",
        "TS-077-C001": "context-only-source-closure",
        "TS-077-E001": "inadmissible-opaque-whole-algorithm",
    }
    if (
        set(trust_records) != set(target_077.ALL_AUDITED_TRUST_SITES)
        or any(
            trust_records[record_id].get("semantic_disposition")
            != disposition
            for record_id, disposition in expected_dispositions.items()
        )
    ):
        errors.append("target-077 trust-site bindings are incomplete")
    _artifact_matches(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        "target-077 trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    boundary = _load_json(
        boundary_path, errors, "target-077 boundary manifest"
    )
    if boundary != target_077.boundary_manifest():
        errors.append("target-077 boundary manifest changed")
    _artifact_matches(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        "target-077 boundary manifest",
    )

    bound_inputs_path = root / "bound_inputs/manifest.json"
    bound_inputs = _load_json(
        bound_inputs_path, errors, "target-077 bound inputs"
    )
    if (
        bound_inputs.get("target") != target_077.TARGET
        or bound_inputs.get("active_contract_sha256")
        != target_077.ACTIVE_CONTRACT_SHA256
        or set(bound_inputs.get("files", {}))
        != {
            "generated_declaration",
            "source_item",
            "public_docs",
            "private_selection_source",
            "partition_source",
            "ord_totality_docs",
            "selection_vocabulary",
        }
        or set(bound_inputs.get("frozen_implproof", {}))
        != {
            "harness",
            "transformation_manifest",
            "dependency_manifest",
            "source_body_manifest",
        }
    ):
        errors.append("target-077 bound-input manifest is incomplete")
    for name, record in bound_inputs.get("files", {}).items():
        _artifact_matches(
            record,
            common.OUT / record.get("path", ""),
            errors,
            f"target-077 bound input {name}",
        )
    for name, record in bound_inputs.get("frozen_implproof", {}).items():
        path = common.OUT / record.get("path", "")
        if (
            not path.is_file()
            or record.get("sha256") != common.sha256(path)
        ):
            errors.append(f"target-077 frozen input {name} changed")
    _artifact_matches(
        result.get("bound_inputs"),
        bound_inputs_path,
        errors,
        "target-077 bound inputs",
    )

    obligations = result.get("obligations", {})
    purpose_files = {
        target_077.PRIMARY: "obligation",
        target_077.EXACT_OUTPUT: "exact_output_obligation",
    }
    if set(obligations) != set(purpose_files):
        errors.append("target-077 obligation result set is incomplete")
    for purpose, filename in purpose_files.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        metadata = _load_json(
            metadata_path, errors, f"target-077 {purpose} metadata"
        )
        try:
            target_077.validate_target_obligation(
                smt_path.read_text(), metadata
            )
        except Exception as exc:
            errors.append(f"target-077 {purpose} obligation rejected: {exc}")
        evidence = obligations.get(purpose, {})
        _artifact_matches(
            evidence.get("smt"),
            smt_path,
            errors,
            f"target-077 {purpose} SMT",
        )
        _artifact_matches(
            evidence.get("metadata"),
            metadata_path,
            errors,
            f"target-077 {purpose} metadata",
        )
        _solver_capture(
            evidence.get("solver"),
            metadata.get("expected_solver_result", ""),
            errors,
            f"target-077 {purpose}",
        )
    primary_metadata = _load_json(
        root / "obligation.metadata.json",
        errors,
        "target-077 primary metadata",
    )
    exact_metadata = _load_json(
        root / "exact_output_obligation.metadata.json",
        errors,
        "target-077 exact metadata",
    )
    if primary_metadata.get("domain", {}).get("bounded") is not False:
        errors.append("target-077 completeness proof is not general-domain")
    if exact_metadata.get("domain", {}).get("bounded") is not True:
        errors.append("target-077 exact witness is not marked bounded")

    exact_path = root / "exact_output_witness.smt2"
    if (
        not exact_path.is_file()
        or exact_path.read_text() != target_077.fixed_exact_model_text()
    ):
        errors.append("target-077 exact-output witness changed")
    exact_evidence = result.get("exact_output_witness", {})
    _artifact_matches(
        exact_evidence.get("smt"),
        exact_path,
        errors,
        "target-077 exact-output witness",
    )
    _solver_capture(
        exact_evidence.get("solver"),
        "sat",
        errors,
        "target-077 exact-output witness",
    )

    probes = result.get("equivalence_witnesses", {})
    if set(probes) != set(target_077.PROBE_KINDS):
        errors.append("target-077 witness probe set is incomplete")
    for kind in target_077.PROBE_KINDS:
        path = root / f"witness_{kind}.smt2"
        if (
            not path.is_file()
            or path.read_text() != target_077.witness_probe_text(kind)
        ):
            errors.append(f"target-077 {kind} witness model changed")
        evidence = probes.get(kind, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"target-077 {kind} witness model",
        )
        _solver_capture(
            evidence.get("solver"),
            "sat",
            errors,
            f"target-077 {kind} witness",
        )

    regressions = result.get("semantic_regressions", {})
    if set(regressions) != set(target_077.SEMANTIC_REGRESSION_KINDS):
        errors.append("target-077 semantic regression set is incomplete")
    for kind in target_077.SEMANTIC_REGRESSION_KINDS:
        path = root / f"regression_{kind}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != target_077.semantic_regression_probe_text(kind)
        ):
            errors.append(f"target-077 {kind} regression model changed")
        evidence = regressions.get(kind, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"target-077 {kind} regression model",
        )
        _solver_capture(
            evidence.get("solver"),
            "unsat",
            errors,
            f"target-077 {kind} regression",
        )

    witness_path = root / "witness.json"
    if _load_json(
        witness_path, errors, "target-077 witness"
    ) != target_077.witness_payload():
        errors.append("target-077 witness payload changed")
    try:
        replay = replay_target_077.replay(witness_path)
        if replay.get("status") != "passed":
            errors.append("target-077 witness replay did not pass")
    except Exception as exc:
        errors.append(f"target-077 witness replay failed: {exc}")
    _artifact_matches(
        result.get("witness"),
        witness_path,
        errors,
        "target-077 witness",
    )

    source_model = common.OUT / "proofs/077_core_slice_select_nth_unstable.rs"
    captured_model = root / "verus/selection_model.rs"
    if (
        not source_model.is_file()
        or not captured_model.is_file()
        or source_model.read_bytes() != captured_model.read_bytes()
        or "external_body" in captured_model.read_text()
    ):
        errors.append("target-077 Verus model is missing or invalid")
    verus = result.get("verus", {})
    _artifact_matches(
        verus.get("source_model"),
        source_model,
        errors,
        "target-077 source Verus model",
    )
    _artifact_matches(
        verus.get("captured_model"),
        captured_model,
        errors,
        "target-077 captured Verus model",
    )
    for key in ("typecheck", "verification"):
        record = verus.get(key, {})
        try:
            stdout = (common.OUT / record["stdout"]).read_text()
            stderr = (common.OUT / record["stderr"]).read_text()
            status = (common.OUT / record["status"]).read_text()
        except (KeyError, OSError) as exc:
            errors.append(f"target-077 Verus {key} is unreadable: {exc}")
            continue
        if record.get("exit_code") != 0 or stderr or status != "0\n":
            errors.append(f"target-077 Verus {key} failed")
        if (
            key == "verification"
            and "verification results:: 5 verified, 0 errors" not in stdout
        ):
            errors.append("target-077 Verus summary changed")

    preservation = result.get("preserved_certified_evidence", {})
    if set(preservation) != set(run_target_077.PRESERVED_ARTIFACT_IDS):
        errors.append("target-077 certified-evidence preservation is incomplete")
    else:
        for artifact_id, record in preservation.items():
            evidence_root = common.OUT / "evidence/targets" / artifact_id
            digest = (
                run_target_077.tree_digest(evidence_root)
                if evidence_root.is_dir()
                else ""
            )
            if (
                record.get("before_sha256") != digest
                or record.get("after_sha256") != digest
            ):
                errors.append(
                    f"target-077 run did not preserve {artifact_id}"
                )
    frozen = result.get("preserved_frozen_selection_inputs", {})
    if set(frozen) != set(run_target_077.FROZEN_SELECTION_DIRS):
        errors.append("target-077 frozen-input preservation is incomplete")
    else:
        for name, record in frozen.items():
            frozen_root = common.OUT / "provenance/frozen/implproof" / name
            digest = (
                run_target_077.tree_digest(frozen_root)
                if frozen_root.is_dir()
                else ""
            )
            if (
                record.get("before_sha256") != digest
                or record.get("after_sha256") != digest
            ):
                errors.append(f"target-077 run did not preserve frozen {name}")
