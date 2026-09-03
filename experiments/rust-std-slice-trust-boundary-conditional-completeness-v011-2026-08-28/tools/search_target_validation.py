#!/usr/bin/env python3
"""Independent artifact validation for Slice search-wrapper targets."""

from __future__ import annotations

import csv
import io
import json
import shlex
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import chunk_contract_drift_cluster
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
from checker_guards import GuardError
import search_family
import search_target_pipeline


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _check_artifact(
    errors: list[str],
    descriptor: Any,
    path: Path,
    label: str,
) -> None:
    if not isinstance(descriptor, dict) or not path.is_file():
        errors.append(f"{label}: missing artifact or descriptor")
        return
    if (
        descriptor.get("path") != common.relpath(path)
        or descriptor.get("sha256") != common.sha256(path)
        or descriptor.get("bytes") != path.stat().st_size
    ):
        errors.append(f"{label}: artifact path/hash/size mismatch")


def _check_capture(
    errors: list[str],
    record: Any,
    expected_argv: list[str],
    expected_result: str,
    label: str,
    *,
    require_payload: bool = False,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label}: missing command capture")
        return
    paths: dict[str, Path] = {}
    for key in ("command", "stdout", "stderr", "status"):
        value = record.get(key)
        if not isinstance(value, str):
            errors.append(f"{label}: missing {key} capture path")
            return
        paths[key] = common.OUT / value
        if not paths[key].is_file():
            errors.append(f"{label}: missing {key} capture")
            return
    stdout = paths["stdout"].read_text()
    lines = stdout.splitlines()
    actual = lines[0] if lines else ""
    if (
        record.get("argv") != expected_argv
        or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or paths["status"].read_text() != "0\n"
        or paths["stderr"].read_text() != ""
        or actual != expected_result
        or record.get("solver_result") != expected_result
        or record.get("expected_solver_result") != expected_result
        or (expected_result == "unsat" and stdout != "unsat\n")
        or (require_payload and len(lines) < 2)
    ):
        errors.append(f"{label}: solver capture is not an exact clean replay")


def _validate_lower_dependency(errors: list[str], value: Any, label: str) -> None:
    try:
        expected = search_target_pipeline._lower_dependency()
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        errors.append(f"{label}: accepted lower dependency is unavailable: {exc}")
        return
    if value != expected:
        errors.append(f"{label}: accepted lower dependency binding is stale")


def validate(
    errors: list[str],
    module: ModuleType,
    replay_module: ModuleType,
    run_module: ModuleType,
    *,
    source_model: Path,
    expected_not_run: int,
) -> None:
    label = module.CONFIG.label
    root = common.OUT / "evidence/targets" / module.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append(f"{label}: result evidence is missing")
        return
    try:
        result = _load_json(result_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: result evidence is invalid JSON: {exc}")
        return
    if (
        result.get("target") != module.TARGET
        or result.get("input_order") != module.INPUT_ORDER
        or result.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != search_target_pipeline.INCOMPLETE
        or result.get("updated_crosswalk_fields")
        != sorted(search_target_pipeline.INCOMPLETE)
        or result.get("remaining_not_run") != expected_not_run
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append(f"{label}: result identity/classification is malformed")

    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    matches = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append(f"{label}: crosswalk row is absent or duplicated")
        return
    row = matches[0]
    if any(
        row[field] != value
        for field, value in search_target_pipeline.INCOMPLETE.items()
    ):
        errors.append(f"{label}: crosswalk classification changed")

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    inputs_path = root / "bound_inputs_manifest.json"
    _check_artifact(
        errors, result.get("authority_bindings"), authority_path, f"{label} authority"
    )
    _check_artifact(
        errors, result.get("boundary_manifest"), boundary_path, f"{label} boundary"
    )
    _check_artifact(
        errors, result.get("bound_inputs"), inputs_path, f"{label} inputs"
    )

    if authority_path.is_file():
        try:
            authority = _load_json(authority_path)
            expected = {
                field: row[field]
                for field in search_target_pipeline.AUTHORITY_FIELDS
            }
            if authority != {"schema_version": 1, "bindings": expected}:
                errors.append(f"{label}: authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: authority bindings are invalid JSON: {exc}")

    if boundary_path.is_file():
        try:
            boundary = _load_json(boundary_path)
            if boundary != module.boundary_manifest():
                errors.append(f"{label}: boundary manifest differs from policy")
            serialized = json.dumps(
                boundary.get("shared_boundary_observations", []),
                sort_keys=True,
            )
            for forbidden in (
                "selected index",
                "returned Result",
                "aggregate callback final state",
                "execution trace",
            ):
                if forbidden in serialized:
                    errors.append(f"{label}: boundary contains {forbidden}")
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: boundary manifest is invalid JSON: {exc}")

    if inputs_path.is_file():
        try:
            inputs = _load_json(inputs_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: bound-input manifest is invalid JSON: {exc}")
            inputs = {}
        artifacts = inputs.get("artifacts", {})
        expected_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            module.CONFIG.source_item_filename: row["source_item_sha256"],
            module.CONFIG.source_docs_filename: row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row["transformation_manifest_sha256"],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            "canonical_binary_search_by.rs": search_family.LOWER_SOURCE_SHA256,
        }
        if (
            inputs.get("schema_version") != 1
            or not isinstance(artifacts, dict)
            or set(artifacts) != set(expected_hashes)
        ):
            errors.append(f"{label}: bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_hashes.items():
            path = root / "bound_inputs" / filename
            _check_artifact(
                errors,
                artifacts.get(filename),
                path,
                f"{label} bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"{label}: bound input hash changed: {filename}")
        lower = inputs.get("canonical_lower_transition", {})
        if lower != {
            "source_path": search_family.SLICE_SOURCE_PATH,
            "source_span": (
                f"{search_family.LOWER_SOURCE_START}-"
                f"{search_family.LOWER_SOURCE_END}"
            ),
            "source_file_sha256": search_family.SLICE_SOURCE_SHA256,
            "excerpt_sha256": search_family.LOWER_SOURCE_SHA256,
            "artifact": "canonical_binary_search_by.rs",
        }:
            errors.append(f"{label}: canonical lower transition binding changed")
        _validate_lower_dependency(
            errors,
            inputs.get("accepted_lower_dependency"),
            f"{label} bound inputs",
        )

    z3 = shutil.which("z3")
    if not z3:
        errors.append(f"{label}: validation cannot locate z3")
        return
    obligation_specs = {
        module.PRIMARY: "obligation",
        module.SANITY: (
            "partitioned_domain_sanity"
            if module.CONFIG.kind == "partition"
            else "ordered_domain_sanity"
        ),
        module.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append(f"{label}: obligation result set is incomplete")
        obligations = {}
    for purpose, stem in obligation_specs.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        try:
            metadata = _load_json(metadata_path)
            module.validate_target_obligation(smt_path.read_text(), metadata)
        except (OSError, GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{label} {purpose}: checker rejected obligation: {exc}")
            continue
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            errors.append(f"{label} {purpose}: evidence descriptor is missing")
            continue
        _check_artifact(
            errors, evidence.get("smt"), smt_path, f"{label} {purpose} SMT"
        )
        _check_artifact(
            errors,
            evidence.get("metadata"),
            metadata_path,
            f"{label} {purpose} metadata",
        )
        _check_capture(
            errors,
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            metadata["expected_solver_result"],
            f"{label} {purpose}",
        )

    fixed = result.get("fixed_sat_replays")
    fixed_specs = {
        module.PRIMARY: "counterexample_model",
        module.EXACT_OUTPUT: "exact_output_witness",
    }
    if not isinstance(fixed, dict) or set(fixed) != set(fixed_specs):
        errors.append(f"{label}: fixed SAT replay set is incomplete")
        fixed = {}
    for purpose, stem in fixed_specs.items():
        path = root / f"{stem}.smt2"
        evidence = fixed.get(purpose)
        if not isinstance(evidence, dict):
            continue
        _check_artifact(
            errors, evidence.get("smt"), path, f"{label} {purpose} fixed SMT"
        )
        if path.is_file() and path.read_text() != module.fixed_model_text(purpose):
            errors.append(f"{label} {purpose}: fixed model text changed")
        _check_capture(
            errors,
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            f"{label} {purpose} fixed replay",
            require_payload=True,
        )

    witness_path = root / "witness.json"
    _check_artifact(
        errors, result.get("witness"), witness_path, f"{label} witness"
    )
    if witness_path.is_file():
        try:
            independent = replay_module.replay(witness_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: independent witness replay failed: {exc}")
            independent = None
    else:
        independent = None
    replay = result.get("witness_replay")
    replay_script = (
        common.OUT / "tools" / f"replay_target_{int(module.INPUT_ORDER):03d}.py"
    )
    expected_replay_argv = [
        sys.executable,
        str(replay_script),
        "--witness",
        str(witness_path),
    ]
    if not isinstance(replay, dict):
        errors.append(f"{label}: witness replay capture is missing")
    else:
        paths = {
            key: common.OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured = json.loads(paths.get("stdout", Path()).read_text())
        except (OSError, json.JSONDecodeError):
            captured = None
        if (
            len(paths) != 4
            or any(not path.is_file() for path in paths.values())
            or replay.get("argv") != expected_replay_argv
            or paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or paths.get("status", Path()).read_text() != "0\n"
            or paths.get("stderr", Path()).read_text() != ""
            or captured != independent
            or replay.get("result") != independent
        ):
            errors.append(f"{label}: witness replay capture is invalid")

    captured_model = root / "verus/source_transition_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append(f"{label}: Verus evidence is missing")
    else:
        _check_artifact(
            errors, verus.get("source_model"), source_model, f"{label} source model"
        )
        _check_artifact(
            errors,
            verus.get("captured_model"),
            captured_model,
            f"{label} captured model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append(f"{label}: captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append(f"{label}: Verus model contains external_body")
        for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
            record = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(record, dict):
                errors.append(f"{label}: Verus {key} capture is missing")
                continue
            paths = {
                name: common.OUT / record.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(record.get(name), str)
            }
            stdout = (
                paths.get("stdout", Path()).read_text()
                if len(paths) == 4
                and all(path.is_file() for path in paths.values())
                else ""
            )
            if (
                len(paths) != 4
                or any(not path.is_file() for path in paths.values())
                or verus.get("expected_summary")
                != module.VERUS_EXPECTED_SUMMARY
                or record.get("argv") != expected_argv
                or paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or record.get("exit_code") != 0
                or paths.get("status", Path()).read_text() != "0\n"
                or paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and module.VERUS_EXPECTED_SUMMARY not in stdout
                )
            ):
                errors.append(f"{label}: Verus {key} capture is invalid")

    _validate_lower_dependency(
        errors,
        result.get("accepted_lower_dependency"),
        f"{label} result",
    )
    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        artifact_id: common.OUT / "evidence/targets" / artifact_id
        for artifact_id in run_module.PRESERVED_ARTIFACT_IDS
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append(f"{label}: preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            current = (
                search_target_pipeline.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            record = preservation.get(artifact_id)
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current
            ):
                errors.append(f"{label}: did not preserve {artifact_id}")


def validate_cluster(
    errors: list[str],
    ordered_modules: tuple[tuple[ModuleType, ModuleType], ...],
) -> None:
    path = common.OUT / "logs/ordered_search_family_replay.json"
    try:
        record = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ordered search replay manifest is unreadable: {exc}")
        return
    expected_order = [module.ARTIFACT_ID for module, _ in ordered_modules]
    expected_results = {
        artifact_id: search_target_pipeline.INCOMPLETE
        for artifact_id in expected_order
    }
    if (
        record.get("schema_version") != 1
        or record.get("status") != "passed"
        or record.get("ordered_artifact_ids") != expected_order
        or record.get("initial_cluster_results") != expected_results
        or record.get("final_cluster_results") != expected_results
    ):
        errors.append("ordered search replay manifest is malformed")
    crosswalk = record.get("crosswalk", {})
    search_stage_rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    chunk_targets = {
        config.target for config in chunk_contract_drift_cluster.ORDERED_TARGETS
    }
    later_targets = chunk_targets | {
        "core::slice::assume_init_drop",
        "core::slice::assume_init_mut",
        "core::slice::sort_unstable",
        "core::slice::sort_unstable_by_key",
        "core::slice::select_nth_unstable",
        "core::slice::select_nth_unstable_by",
        "core::slice::select_nth_unstable_by_key",
        "core::slice::write_clone_of_slice",
    } | {
        config.target for config in constructors.TARGETS
    } | {
        config.target for config in edge.TARGETS
    } | {
        "core::slice::clone_from_slice",
        "core::slice::fill",
    } | {
        config.target for config in exact_partitions.TARGETS
    } | {
        config.target for config in fixed_chunks.TARGETS
    } | {
        config.target for config in split_primitives.TARGETS
    } | {
        config.target for config in split_off.TARGETS
    } | {
        config.target for config in raw_slice.TARGETS
    } | {
        config.target for config in slice_trio.TARGETS
    } | {
        config.target for config in address_pair.TARGETS
    } | {
        config.target for config in mutable_views.TARGETS
    } | {
        config.target for config in align_pair.TARGETS
    }
    for row in search_stage_rows:
        if row["target"] in later_targets:
            row["exact_output_determinism_status"] = "not-run"
            row["completeness_modulo_reviewed_equivalence_status"] = "not-run"
    csv_buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=list(search_stage_rows[0]),
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(search_stage_rows)
    expected_bytes = {
        "csv": csv_buffer.getvalue().encode(),
        "json": (
            json.dumps(search_stage_rows, indent=2, sort_keys=True) + "\n"
        ).encode(),
    }
    for name, target in (
        ("csv", common.OUT / "crosswalk/target_to_proof_boundary.csv"),
        ("json", common.OUT / "crosswalk/target_to_proof_boundary.json"),
    ):
        descriptor = (
            crosswalk.get(name) if isinstance(crosswalk, dict) else None
        )
        if (
            not isinstance(descriptor, dict)
            or descriptor.get("path") != common.relpath(target)
            or descriptor.get("sha256")
            != common.sha256_bytes(expected_bytes[name])
            or descriptor.get("bytes") != len(expected_bytes[name])
        ):
            errors.append(f"ordered search replay {name}: stale binding")
    preservation = record.get("preserved_certified_evidence")
    expected_ids = set(search_target_pipeline.BASELINE_ARTIFACT_IDS)
    if not isinstance(preservation, dict) or set(preservation) != expected_ids:
        errors.append("ordered search preservation record is incomplete")
        return
    for artifact_id in expected_ids:
        root = common.OUT / "evidence/targets" / artifact_id
        current = (
            search_target_pipeline.tree_digest(root) if root.is_dir() else ""
        )
        item = preservation.get(artifact_id)
        if (
            not isinstance(item, dict)
            or item.get("before_sha256") != current
            or item.get("after_sha256") != current
        ):
            errors.append(
                f"ordered search replay did not preserve {artifact_id}"
            )
