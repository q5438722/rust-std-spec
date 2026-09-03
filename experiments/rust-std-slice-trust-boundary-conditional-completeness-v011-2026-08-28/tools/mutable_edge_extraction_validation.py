#!/usr/bin/env python3
"""Validate the four mutable-edge evidence trees and final ledger."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import clone_effect_cluster as clone_cluster
import exact_mutable_iterator_partitions as exact_partitions
import mutable_edge_extraction as edge
import mutable_fixed_chunk_edges as fixed_chunks
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import replay_mutable_edge_extraction as replay
import run_mutable_edge_extraction as runner
import target_pipeline


def _load_json(path: Path, errors: list[str], label: str) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is unreadable: {exc}")
        return {}


def _artifact(
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


def _capture(
    record: Any,
    expected_argv: list[str],
    expected_stdout: str | None,
    errors: list[str],
    label: str,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label} capture is missing")
        return
    try:
        command = common.OUT / record["command"]
        stdout = common.OUT / record["stdout"]
        stderr = common.OUT / record["stderr"]
        status = common.OUT / record["status"]
    except (KeyError, TypeError):
        errors.append(f"{label} capture paths are malformed")
        return
    if not all(path.is_file() for path in (command, stdout, stderr, status)):
        errors.append(f"{label} capture files are missing")
        return
    if (
        record.get("argv") != expected_argv
        or command.read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or status.read_text() != "0\n"
        or stderr.read_text()
        or (
            expected_stdout is not None
            and stdout.read_text() != expected_stdout
        )
    ):
        errors.append(f"{label} capture is not a clean exact replay")


def _validate_bound_inputs(
    config: edge.EdgeTarget,
    result: dict[str, Any],
    root: Path,
    errors: list[str],
) -> None:
    path = root / "bound_inputs/manifest.json"
    manifest = _load_json(path, errors, f"{config.target} bound inputs")
    if (
        manifest.get("target") != config.target
        or manifest.get("input_order") != config.input_order
        or manifest.get("active_contract_sha256")
        != config.active_contract_sha256
        or set(manifest.get("files", {}))
        != {
            "active_contract.txt",
            "generated_declaration.rs",
            "source_item.rs",
            "public_docs.md",
            "slice_edge_vocabulary.rs",
        }
        or set(manifest.get("frozen_implproof", {}))
        != {
            "implproof_harness.rs",
            "source_body.json",
            "transformation_manifest.json",
            "dependency_assumption_manifest.json",
        }
        or set(manifest.get("trust_record_ids", []))
        != set(config.all_trust_site_ids)
    ):
        errors.append(f"{config.target} bound-input manifest is incomplete")
    for name, record in manifest.get("files", {}).items():
        _artifact(
            record,
            root / "bound_inputs" / name,
            errors,
            f"{config.target} bound input {name}",
        )
    vocabulary = root / "bound_inputs/slice_edge_vocabulary.rs"
    vocabulary_record = manifest.get("files", {}).get(
        "slice_edge_vocabulary.rs", {}
    )
    if (
        vocabulary_record.get("source_ranges")
        != [f"{start}-{end}" for start, end in edge.VOCABULARY_RANGES]
        or vocabulary_record.get("active_relation") != config.vocabulary_name
        or vocabulary_record.get("canonical_file_sha256")
        is None
    ):
        errors.append(f"{config.target} vocabulary binding changed")
    try:
        edge.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            vocabulary.read_text(),
        )
    except Exception as exc:
        errors.append(f"{config.target} source anchors failed: {exc}")
    for name, record in manifest.get("frozen_implproof", {}).items():
        _artifact(
            record,
            root / "bound_inputs" / name,
            errors,
            f"{config.target} frozen {name}",
        )
        if record.get("sha256") != record.get("frozen_source_sha256"):
            errors.append(f"{config.target} frozen {name} diverged")
    _artifact(
        result.get("bound_inputs"),
        path,
        errors,
        f"{config.target} bound-input manifest",
    )


def _validate_target(
    config: edge.EdgeTarget,
    rows: dict[tuple[str, str], dict[str, str]],
    z3: str,
    errors: list[str],
) -> None:
    root = common.OUT / "evidence/targets" / config.artifact_id
    result_path = root / "result.json"
    result = _load_json(result_path, errors, f"{config.target} result")
    if (
        result.get("target") != config.target
        or result.get("input_order") != config.input_order
        or result.get("active_contract_sha256")
        != config.active_contract_sha256
        or result.get("active_contract_text") != config.active_contract_text
        or result.get("classification") != runner.COMPLETE
        or result.get("updated_crosswalk_fields")
        != list(target_pipeline.RESULT_FIELDS)
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
    ):
        errors.append(f"{config.target} result identity/classification is malformed")
    row = rows.get((config.target, config.input_order))
    if row is None or any(
        row[field] != value for field, value in runner.COMPLETE.items()
    ):
        errors.append(f"{config.target} crosswalk classification is missing")

    authority_path = root / "authority_bindings.json"
    bindings = _load_json(
        authority_path,
        errors,
        f"{config.target} authority bindings",
    ).get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != config.active_contract_sha256
        or bindings.get("retained_contract_sha256")
        != config.active_contract_sha256
        or bindings.get("generated_declaration_sha256")
        != config.generated_declaration_sha256
        or bindings.get("source_item_sha256") != config.source_item_sha256
        or set(bindings.get("all_trust_site_ids", "").split(";"))
        != set(config.all_trust_site_ids)
    ):
        errors.append(f"{config.target} authority binding changed")
    _artifact(
        result.get("authority_bindings"),
        authority_path,
        errors,
        f"{config.target} authority bindings",
    )

    trust_path = root / "trust_site_bindings.json"
    records = _load_json(
        trust_path,
        errors,
        f"{config.target} trust bindings",
    ).get("records", [])
    by_id = {
        item.get("record_id"): item
        for item in records
        if isinstance(item, dict)
    }
    if set(by_id) != set(config.all_trust_site_ids) or any(
        record.get("semantic_disposition")
        != "admissible-source-backed-support"
        or record.get("target_postcondition_coverage")
        != "partial-or-lower-level"
        for record in by_id.values()
    ):
        errors.append(f"{config.target} trust bindings changed")
    _artifact(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    if _load_json(
        boundary_path,
        errors,
        f"{config.target} boundary",
    ) != edge.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    _validate_bound_inputs(config, result, root, errors)

    obligations = result.get("obligations", {})
    if set(obligations) != set(edge.PURPOSES):
        errors.append(f"{config.target} obligation set is incomplete")
    for purpose, stem in replay.OBLIGATIONS.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        metadata = _load_json(
            metadata_path,
            errors,
            f"{config.target} {purpose} metadata",
        )
        try:
            edge.validate_target_obligation(
                config,
                smt_path.read_text(),
                metadata,
            )
        except Exception as exc:
            errors.append(f"{config.target} {purpose} is rejected: {exc}")
        evidence = obligations.get(purpose, {})
        _artifact(
            evidence.get("smt"),
            smt_path,
            errors,
            f"{config.target} {purpose} SMT",
        )
        _artifact(
            evidence.get("metadata"),
            metadata_path,
            errors,
            f"{config.target} {purpose} metadata",
        )
        solver = evidence.get("solver", {})
        _capture(
            solver,
            [z3, "-smt2", str(smt_path)],
            "unsat\n",
            errors,
            f"{config.target} {purpose} solver",
        )
        if (
            solver.get("solver_result") != "unsat"
            or solver.get("expected_solver_result") != "unsat"
        ):
            errors.append(f"{config.target} {purpose} solver status changed")

    instances = result.get("source_instances", {})
    if set(instances) != set(replay.SOURCE_INSTANCES):
        errors.append(f"{config.target} source-instance set is incomplete")
    for name, (length, element_size) in replay.SOURCE_INSTANCES.items():
        path = root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != edge.source_instance_text(
                config,
                length=length,
                element_size=element_size,
            )
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = instances.get(name, {})
        _artifact(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} source instance",
        )
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat\n",
            errors,
            f"{config.target} {name} solver",
        )

    try:
        replayed = replay.replay(root, z3, config)
    except Exception as exc:
        errors.append(f"{config.target} independent replay failed: {exc}")
        replayed = {}
    replay_record = result.get("solver_replay", {})
    _capture(
        replay_record,
        [
            sys.executable,
            str(common.OUT / "tools/replay_mutable_edge_extraction.py"),
            "--evidence-root",
            str(root),
            "--z3",
            z3,
            "--artifact-id",
            config.artifact_id,
        ],
        json.dumps(replayed, sort_keys=True) + "\n",
        errors,
        f"{config.target} independent replay",
    )
    if replayed.get("status") != "passed":
        errors.append(f"{config.target} independent replay did not pass")

    proof = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = root / "verus/edge_model.rs"
    expected_proof = edge.verus_text(config)
    if (
        not proof.is_file()
        or not captured.is_file()
        or proof.read_text() != expected_proof
        or captured.read_text() != expected_proof
        or "external_body" in expected_proof
    ):
        errors.append(f"{config.target} Verus model changed")
    verus = result.get("verus", {})
    _artifact(
        verus.get("source_model"),
        proof,
        errors,
        f"{config.target} source Verus model",
    )
    _artifact(
        verus.get("captured_model"),
        captured,
        errors,
        f"{config.target} captured Verus model",
    )
    _capture(
        verus.get("typecheck"),
        [str(common.VERUS), str(captured), "--crate-type=lib", "--no-verify"],
        None,
        errors,
        f"{config.target} Verus typecheck",
    )
    verification = verus.get("verification", {})
    _capture(
        verification,
        [str(common.VERUS), str(captured), "--crate-type=lib"],
        None,
        errors,
        f"{config.target} Verus verification",
    )
    try:
        stdout = (common.OUT / verification["stdout"]).read_text()
    except (KeyError, OSError, TypeError):
        stdout = ""
    if "0 errors" not in stdout:
        errors.append(f"{config.target} Verus verification summary changed")

    guard_path = root / "reviewed_model_guards.json"
    guards = _load_json(
        guard_path,
        errors,
        f"{config.target} reviewed guards",
    )
    if len(guards.get("fail_closed_mutations", [])) != 11:
        errors.append(f"{config.target} reviewed guard set is incomplete")
    _artifact(
        result.get("reviewed_model_guards"),
        guard_path,
        errors,
        f"{config.target} reviewed guards",
    )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("mutable-edge validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in edge.TARGETS:
        _validate_target(config, by_key, z3, errors)

    classified = {
        key
        for key, row in by_key.items()
        if any(
            row[field] != "not-run"
            for field in target_pipeline.RESULT_FIELDS
        )
    }
    expected = (
        set(runner.BASELINE_RESULTS)
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
    if classified != expected or len(classified) != 62 or len(rows) - len(
        classified
    ) != 0:
        errors.append(
            "downstream align-to cluster did not finish at 62/0"
        )

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "mutable-edge cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in edge.TARGETS]
        or manifest.get("classified_rows") != 38
        or manifest.get("not_run_rows") != 24
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("mutable-edge cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"mutable-edge run did not preserve {artifact_id}")
    frozen = manifest.get("preserved_frozen_inputs", {}).get("root", {})
    current_frozen = (
        runner.tree_digest(runner.FROZEN_ROOT)
        if runner.FROZEN_ROOT.is_dir()
        else ""
    )
    if (
        frozen.get("path") != common.relpath(runner.FROZEN_ROOT)
        or frozen.get("before_sha256") != current_frozen
        or frozen.get("after_sha256") != current_frozen
    ):
        errors.append("mutable-edge run changed frozen inputs")
