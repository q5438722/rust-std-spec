#!/usr/bin/env python3
"""Validate the targets 078-079 selection-callback evidence increment."""

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
import replay_selection_callback_cluster as replay
import run_selection_callback_cluster as runner
import target_078
import target_079
import target_pipeline


MODULES = (target_078, target_079)
FILENAMES = {
    target_078.PRIMARY: "obligation",
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
    expected_status = runner.CLUSTER_RESULTS[
        (module.TARGET, module.INPUT_ORDER)
    ]
    if (
        result.get("target") != module.TARGET
        or result.get("input_order") != module.INPUT_ORDER
        or result.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_status
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
        or set(result.get("admitted_trust_site_ids", []))
        != set(module.ADMITTED_TRUST_SITES)
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
        or tuple(result.get("unresolved_source_model_phases", []))
        != module.missing_source_phases()
    ):
        errors.append(f"{module.TARGET} result identity/classification is malformed")

    row = crosswalk_by_key.get((module.TARGET, module.INPUT_ORDER))
    if row is None or any(
        row[field] != value for field, value in expected_status.items()
    ):
        errors.append(f"{module.TARGET} crosswalk result is missing")

    authority_path = root / "authority_bindings.json"
    authority = _load_json(
        authority_path, errors, f"{module.TARGET} authority bindings"
    )
    bindings = authority.get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or bindings.get("active_contract_text")
        != module.ACTIVE_CONTRACT_TEXT
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

    trust_path = root / "trust_site_bindings.json"
    trust = _load_json(
        trust_path, errors, f"{module.TARGET} trust bindings"
    )
    records = {
        item.get("record_id"): item
        for item in trust.get("records", [])
        if isinstance(item, dict)
    }
    if set(records) != set(module.ALL_AUDITED_TRUST_SITES):
        errors.append(f"{module.TARGET} six trust records are incomplete")
    else:
        if (
            records[module.ADMITTED_TRUST_SITES[0]].get(
                "semantic_disposition"
            )
            != "admissible-source-backed-support"
        ):
            errors.append(f"{module.TARGET} D004 callback site is not admitted")
        for trust_site in module.EXCLUDED_RETAINED_TRUST_SITES:
            if not str(
                records[trust_site].get("semantic_disposition", "")
            ).startswith("inadmissible"):
                errors.append(f"{module.TARGET} {trust_site} was relabeled")
    _artifact_matches(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{module.TARGET} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    if _load_json(
        boundary_path, errors, f"{module.TARGET} boundary manifest"
    ) != module.boundary_manifest():
        errors.append(f"{module.TARGET} boundary manifest changed")
    _artifact_matches(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{module.TARGET} boundary manifest",
    )

    bound_inputs_path = root / "bound_inputs/manifest.json"
    bound_inputs = _load_json(
        bound_inputs_path, errors, f"{module.TARGET} bound inputs"
    )
    if (
        bound_inputs.get("target") != module.TARGET
        or bound_inputs.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or set(bound_inputs.get("files", {}))
        != {
            "generated_declaration",
            "source_item",
            "public_docs",
            "private_selection_source",
            "partition_source",
            "small_sort_source",
            "callback_vocabulary",
        }
        or set(bound_inputs.get("frozen_implproof", {}))
        != {
            "harness",
            "transformation_manifest",
            "dependency_manifest",
            "source_body_manifest",
        }
    ):
        errors.append(f"{module.TARGET} bound-input manifest is incomplete")
    for name, record in bound_inputs.get("files", {}).items():
        _artifact_matches(
            record,
            common.OUT / record.get("path", ""),
            errors,
            f"{module.TARGET} bound input {name}",
        )
    small_sort_record = bound_inputs.get("files", {}).get(
        "small_sort_source", {}
    )
    small_sort_path = common.OUT / small_sort_record.get("path", "")
    try:
        small_sort_text = small_sort_path.read_text()
    except OSError:
        small_sort_text = ""
    if (
        small_sort_record.get("source_lines")
        != module.CONFIG.small_sort_source
        or "struct CopyOnDrop" not in small_sort_text
        or "impl<T> Drop for CopyOnDrop<T>" not in small_sort_text
        or "tail = tail.add(1);" not in small_sort_text
    ):
        errors.append(
            f"{module.TARGET} small-sort panic/loop source is incomplete"
        )
    _artifact_matches(
        result.get("bound_inputs"),
        bound_inputs_path,
        errors,
        f"{module.TARGET} bound inputs",
    )

    obligations = result.get("obligations", {})
    if set(obligations) != set(module.PURPOSES):
        errors.append(f"{module.TARGET} obligation result set is incomplete")
    for purpose, filename in FILENAMES.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        metadata = _load_json(
            metadata_path, errors, f"{module.TARGET} {purpose} metadata"
        )
        try:
            module.validate_target_obligation(smt_path.read_text(), metadata)
        except Exception as exc:
            errors.append(f"{module.TARGET} {purpose} rejected: {exc}")
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
            "unsat",
            errors,
            f"{module.TARGET} {purpose}",
        )
        domain = metadata.get("domain", {})
        if (
            domain.get("bounded") is not True
            or domain.get("source_model_complete") is not False
            or metadata.get("model_status")
            != "missing-source-backed-model"
        ):
            errors.append(
                f"{module.TARGET} {purpose} overstates source-model coverage"
            )

    nonvacuity_path = root / "bounded_nonvacuity.smt2"
    if (
        not nonvacuity_path.is_file()
        or nonvacuity_path.read_text() != module.nonvacuity_text()
    ):
        errors.append(f"{module.TARGET} bounded nonvacuity changed")
    nonvacuity = result.get("bounded_nonvacuity", {})
    _artifact_matches(
        nonvacuity.get("smt"),
        nonvacuity_path,
        errors,
        f"{module.TARGET} bounded nonvacuity",
    )
    _solver_capture(
        nonvacuity.get("solver"),
        "sat",
        errors,
        f"{module.TARGET} bounded nonvacuity",
    )

    mixed_source_path = root / "mixed_source_execution.smt2"
    if (
        not mixed_source_path.is_file()
        or mixed_source_path.read_text()
        != module.mixed_source_execution_text()
    ):
        errors.append(f"{module.TARGET} mixed source execution changed")
    mixed_source = result.get("mixed_source_execution", {})
    _artifact_matches(
        mixed_source.get("smt"),
        mixed_source_path,
        errors,
        f"{module.TARGET} mixed source execution",
    )
    _solver_capture(
        mixed_source.get("solver"),
        "sat",
        errors,
        f"{module.TARGET} mixed source execution",
    )

    length_four_wrong_path = (
        root / "length_four_wrong_schedule_regression.smt2"
    )
    if (
        not length_four_wrong_path.is_file()
        or length_four_wrong_path.read_text()
        != module.length_four_wrong_schedule_text()
    ):
        errors.append(f"{module.TARGET} length-four regression changed")
    length_four_wrong = result.get(
        "length_four_wrong_schedule_regression", {}
    )
    _artifact_matches(
        length_four_wrong.get("smt"),
        length_four_wrong_path,
        errors,
        f"{module.TARGET} length-four wrong-schedule regression",
    )
    _solver_capture(
        length_four_wrong.get("solver"),
        "unsat",
        errors,
        f"{module.TARGET} length-four wrong-schedule regression",
    )

    length_four_source_path = root / "length_four_source_execution.smt2"
    if (
        not length_four_source_path.is_file()
        or length_four_source_path.read_text()
        != module.length_four_source_execution_text()
    ):
        errors.append(f"{module.TARGET} length-four source execution changed")
    length_four_source = result.get("length_four_source_execution", {})
    _artifact_matches(
        length_four_source.get("smt"),
        length_four_source_path,
        errors,
        f"{module.TARGET} length-four source execution",
    )
    _solver_capture(
        length_four_source.get("solver"),
        "sat",
        errors,
        f"{module.TARGET} length-four source execution",
    )

    regressions = result.get("small_sort_regressions", {})
    regression_cases = {
        "descending",
        "mixed",
        "tail-three-middle",
        "tail-three-front",
    }
    if set(regressions) != regression_cases:
        errors.append(f"{module.TARGET} small-sort regressions are incomplete")
    for case in sorted(regression_cases):
        path = root / f"small_sort_{case}_regression.smt2"
        if (
            not path.is_file()
            or path.read_text() != module.small_sort_regression_text(case)
        ):
            errors.append(f"{module.TARGET} {case} regression changed")
        evidence = regressions.get(case, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{module.TARGET} {case} regression",
        )
        _solver_capture(
            evidence.get("solver"),
            "unsat",
            errors,
            f"{module.TARGET} {case} regression",
        )

    panic_after_shift = result.get("panic_after_shift_regressions", {})
    if set(panic_after_shift) != {"restored", "unrestored"}:
        errors.append(
            f"{module.TARGET} panic-after-shift regressions are incomplete"
        )
    for restored, expected, label in (
        (True, "sat", "restored"),
        (False, "unsat", "unrestored"),
    ):
        path = root / f"panic_after_shift_{label}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != module.panic_after_shift_text(restored=restored)
        ):
            errors.append(
                f"{module.TARGET} panic-after-shift {label} changed"
            )
        evidence = panic_after_shift.get(label, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{module.TARGET} panic-after-shift {label}",
        )
        _solver_capture(
            evidence.get("solver"),
            expected,
            errors,
            f"{module.TARGET} panic-after-shift {label}",
        )

    panic_records = result.get("panic_prefix_probes", {})
    if set(panic_records) != set(module.panic_probe_kinds()):
        errors.append(f"{module.TARGET} panic-prefix probes are incomplete")
    for kind in module.panic_probe_kinds():
        path = root / f"panic_prefix_{kind}.smt2"
        if (
            not path.is_file()
            or path.read_text() != module.panic_probe_text(kind)
        ):
            errors.append(f"{module.TARGET} panic probe {kind} changed")
        evidence = panic_records.get(kind, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{module.TARGET} panic probe {kind}",
        )
        _solver_capture(
            evidence.get("solver"),
            "sat",
            errors,
            f"{module.TARGET} panic probe {kind}",
        )

    witness_path = root / "witness.json"
    if _load_json(
        witness_path, errors, f"{module.TARGET} witness"
    ) != module.witness_payload():
        errors.append(f"{module.TARGET} witness payload changed")
    try:
        replay_result = replay.replay(witness_path)
        observed = replay_result.get(
            "functional_boundary_diagnostic", {}
        ).get("observed", {})
        if (
            replay_result.get("status") != "passed"
            or not observed.get("execution1_is_source_reachable")
            or observed.get("execution2_is_source_reachable")
            or observed.get("reviewed_selection_equivalent")
        ):
            errors.append(f"{module.TARGET} witness replay is not decisive")
    except Exception as exc:
        errors.append(f"{module.TARGET} witness replay failed: {exc}")
    _artifact_matches(
        result.get("witness"),
        witness_path,
        errors,
        f"{module.TARGET} witness",
    )

    source_model = common.OUT / module.CONFIG.proof_filename
    captured_model = root / "verus/selection_callback_model.rs"
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
            errors.append(f"{module.TARGET} Verus {key} unreadable: {exc}")
            continue
        if record.get("exit_code") != 0 or stderr or status != "0\n":
            errors.append(f"{module.TARGET} Verus {key} failed")
        if (
            key == "verification"
            and module.CONFIG.verus_expected_summary not in stdout
        ):
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
    expected = (
        set(runner.BASELINE_RESULTS)
        | set(runner.CLUSTER_KEYS)
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
    if classified != expected or len(classified) != 62:
        errors.append("selection callback cluster changed classified target set")
    if len(rows) - len(classified) != 0:
        errors.append(
            "downstream align-to cluster did not finish at 62/0"
        )

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "selection callback cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [module.TARGET for module in MODULES]
        or manifest.get("classified_rows") != 27
        or manifest.get("not_run_rows") != 35
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
        or set(manifest.get("preserved_frozen_selection_inputs", {}))
        != set(runner.FROZEN_SELECTION_DIRS)
    ):
        errors.append("selection callback cluster manifest is malformed")
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
                f"selection callback run did not preserve {artifact_id}"
            )
    for name, record in manifest.get(
        "preserved_frozen_selection_inputs", {}
    ).items():
        root = common.OUT / "provenance/frozen/implproof" / name
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"selection callback run changed frozen {name}")
