#!/usr/bin/env python3
"""Validate the exact mutable-iterator partition evidence trees."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import exact_mutable_iterator_partitions as partitions
import mutable_fixed_chunk_edges as fixed_chunks
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import replay_exact_mutable_iterator_partitions as replay
import run_exact_mutable_iterator_partitions as runner
import target_pipeline
from checker_guards import GuardError


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


def _capture(
    record: Any,
    expected_argv: list[str],
    expected_result: str | None,
    errors: list[str],
    label: str,
    *,
    expected_stdout: str | None = None,
    require_model: bool = False,
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
    out = stdout.read_text()
    lines = out.splitlines()
    if (
        record.get("argv") != expected_argv
        or command.read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or status.read_text() != "0\n"
        or stderr.read_text() != ""
        or (
            expected_stdout is not None
            and out != expected_stdout
        )
        or (
            expected_stdout is None
            and (
                expected_result is None
                or not lines
                or lines[0] != expected_result
            )
        )
        or (
            expected_stdout is None
            and not require_model
            and out != expected_result + "\n"
        )
        or (
            require_model
            and (
                len(lines) < 2
                or "(x_length x)" not in out
                or "(y_split_index y1)" not in out
                or record.get("model_retained") is not True
            )
        )
    ):
        errors.append(f"{label} capture is not a clean exact replay")


def _validate_bound_inputs(
    config: partitions.ExactPartitionTarget,
    result: dict[str, Any],
    root: Path,
    errors: list[str],
) -> None:
    path = root / "bound_inputs/manifest.json"
    manifest = _load_json(path, errors, f"{config.target} bound inputs")
    expected_files = {
        "active_contract.txt",
        "generated_declaration.rs",
        "source_item.rs",
        "public_docs.md",
        "iterator_contract_vocabulary.rs",
        "private_constructor",
    }
    if (
        manifest.get("target") != config.target
        or manifest.get("input_order") != config.input_order
        or manifest.get("active_contract_sha256")
        != config.active_contract_sha256
        or set(manifest.get("files", {})) != expected_files
        or set(manifest.get("frozen_implproof", {}))
        != {
            "implproof_harness.rs",
            "transformation_manifest.json",
            "dependency_assumption_manifest.json",
            "source_body.json",
        }
        or set(manifest.get("trust_record_ids", []))
        != set(config.all_trust_site_ids)
    ):
        errors.append(f"{config.target} bound-input manifest is incomplete")
    for name, record in manifest.get("files", {}).items():
        filename = (
            config.private_source_filename
            if name == "private_constructor"
            else name
        )
        _artifact_matches(
            record,
            root / "bound_inputs" / filename,
            errors,
            f"{config.target} bound input {name}",
        )
    private = manifest.get("files", {}).get("private_constructor", {})
    private_path = root / "bound_inputs" / config.private_source_filename
    if (
        private.get("source_lines") != config.private_source_reference
        or private.get("canonical_file_sha256")
        != partitions.CANONICAL_ITER_SHA256
    ):
        errors.append(f"{config.target} private constructor citation changed")
    try:
        partitions.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            private_path.read_text(),
        )
    except (GuardError, OSError) as exc:
        errors.append(f"{config.target} source semantic anchors failed: {exc}")
    for filename, record in manifest.get("frozen_implproof", {}).items():
        _artifact_matches(
            record,
            root / "bound_inputs" / filename,
            errors,
            f"{config.target} frozen input {filename}",
        )
        if record.get("sha256") != record.get("frozen_source_sha256"):
            errors.append(f"{config.target} frozen input {filename} diverged")
    _artifact_matches(
        result.get("bound_inputs"),
        path,
        errors,
        f"{config.target} bound-input manifest",
    )


def _validate_target(
    config: partitions.ExactPartitionTarget,
    by_key: dict[tuple[str, str], dict[str, str]],
    z3: str,
    errors: list[str],
) -> None:
    root = common.OUT / "evidence/targets" / config.artifact_id
    result = _load_json(root / "result.json", errors, f"{config.target} result")
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
    row = by_key.get((config.target, config.input_order))
    if row is None or any(
        row[field] != value for field, value in runner.COMPLETE.items()
    ):
        errors.append(f"{config.target} crosswalk classification is missing")

    authority_path = root / "authority_bindings.json"
    authority = _load_json(
        authority_path,
        errors,
        f"{config.target} authority bindings",
    ).get("bindings", {})
    if (
        authority.get("active_contract_sha256")
        != config.active_contract_sha256
        or authority.get("active_contract_text") != config.active_contract_text
        or authority.get("retained_contract_sha256")
        != config.active_contract_sha256
        or set(authority.get("all_trust_site_ids", "").split(";"))
        != set(config.all_trust_site_ids)
    ):
        errors.append(f"{config.target} authority binding changed")
    _artifact_matches(
        result.get("authority_bindings"),
        authority_path,
        errors,
        f"{config.target} authority bindings",
    )

    trust_path = root / "trust_site_bindings.json"
    trust = _load_json(trust_path, errors, f"{config.target} trust bindings")
    records = {
        item.get("record_id"): item
        for item in trust.get("records", [])
        if isinstance(item, dict)
    }
    if set(records) != set(config.all_trust_site_ids):
        errors.append(f"{config.target} trust record set changed")
    else:
        for site in config.dependency_trust_site_ids:
            if records[site].get("semantic_disposition") != (
                "admissible-source-backed-support"
            ):
                errors.append(f"{config.target} dependency {site} changed")
        for site in config.context_only_trust_site_ids:
            if records[site].get("semantic_disposition") != (
                "context-only-source-closure"
            ):
                errors.append(f"{config.target} source closure {site} changed")
    _artifact_matches(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    if _load_json(
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    ) != partitions.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact_matches(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    _validate_bound_inputs(config, result, root, errors)

    obligations = result.get("obligations", {})
    if set(obligations) != set(partitions.PURPOSES):
        errors.append(f"{config.target} obligation result set is incomplete")
    for purpose, stem in replay.OBLIGATIONS.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        metadata = _load_json(
            metadata_path,
            errors,
            f"{config.target} {purpose} metadata",
        )
        try:
            partitions.validate_target_obligation(
                config,
                smt_path.read_text(),
                metadata,
            )
        except Exception as exc:
            errors.append(f"{config.target} {purpose} is rejected: {exc}")
        evidence = obligations.get(purpose, {})
        _artifact_matches(
            evidence.get("smt"),
            smt_path,
            errors,
            f"{config.target} {purpose} SMT",
        )
        _artifact_matches(
            evidence.get("metadata"),
            metadata_path,
            errors,
            f"{config.target} {purpose} metadata",
        )
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "unsat",
            errors,
            f"{config.target} {purpose} solver",
        )

    instances = result.get("source_instances", {})
    if set(instances) != set(partitions.SOURCE_CASES):
        errors.append(f"{config.target} source instances are incomplete")
    for name, case in partitions.SOURCE_CASES.items():
        path = root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != partitions.source_instance_text(config, case)
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = instances.get(name, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} source instance",
        )
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            errors,
            f"{config.target} {name} solver",
            require_model=True,
        )

    probes = result.get("negative_probes", {})
    if set(probes) != set(partitions.NEGATIVE_PROBES):
        errors.append(f"{config.target} negative probes are incomplete")
    for name in partitions.NEGATIVE_PROBES:
        path = root / f"negative_probe_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != partitions.negative_probe_text(config, name)
        ):
            errors.append(f"{config.target} {name} negative probe changed")
        evidence = probes.get(name, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} negative probe",
        )
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "unsat",
            errors,
            f"{config.target} {name} negative probe solver",
        )

    try:
        independent = replay.replay(root, z3, config)
    except Exception as exc:
        errors.append(f"{config.target} independent replay failed: {exc}")
        independent = {}
    replay_record = result.get("solver_replay", {})
    expected_replay_argv = [
        sys.executable,
        str(
            common.OUT
            / "tools/replay_exact_mutable_iterator_partitions.py"
        ),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
        "--artifact-id",
        config.artifact_id,
    ]
    _capture(
        replay_record,
        expected_replay_argv,
        None,
        errors,
        f"{config.target} independent replay",
        expected_stdout=json.dumps(independent, sort_keys=True) + "\n",
    )
    if independent.get("status") != "passed":
        errors.append(f"{config.target} independent replay did not pass")

    proof_path = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = root / "verus/exact_partition_model.rs"
    expected_proof = partitions.verus_text(config)
    if (
        not proof_path.is_file()
        or not captured.is_file()
        or proof_path.read_text() != expected_proof
        or captured.read_text() != expected_proof
        or "external_body" in expected_proof
    ):
        errors.append(f"{config.target} Verus model changed")
    verus = result.get("verus", {})
    _artifact_matches(
        verus.get("source_model"),
        proof_path,
        errors,
        f"{config.target} source Verus model",
    )
    _artifact_matches(
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
        expected_stdout="",
    )
    verification = verus.get("verification", {})
    try:
        verification_stdout = (
            common.OUT / verification["stdout"]
        ).read_text()
    except (KeyError, OSError, TypeError):
        verification_stdout = ""
    _capture(
        verification,
        [str(common.VERUS), str(captured), "--crate-type=lib"],
        None,
        errors,
        f"{config.target} Verus verification",
        expected_stdout=verification_stdout,
    )
    if "0 errors" not in verification_stdout:
        errors.append(f"{config.target} Verus verification summary changed")


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("exact-partition validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in partitions.TARGETS:
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
        | set(partitions.TARGET_KEYS)
        | set(fixed_chunks.TARGET_KEYS)
        | set(split_primitives.TARGET_KEYS)
        | set(split_off.TARGET_KEYS)
        | set(raw_slice.TARGET_KEYS)
        | set(slice_trio.TARGET_KEYS)
        | set(address_pair.TARGET_KEYS)
        | set(mutable_views.TARGET_KEYS)
        | set(align_pair.TARGET_KEYS)
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    if classified != expected or len(classified) != 62 or not_run != 0:
        errors.append("exact-partition downstream 62/0 ledger is not preserved")

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "exact-partition cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in partitions.TARGETS]
        or manifest.get("classified_rows") != 42
        or manifest.get("not_run_rows") != 20
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("exact-partition cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence",
        {},
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(
                f"exact-partition run did not preserve {artifact_id}"
            )
    frozen = manifest.get("preserved_frozen_inputs", {}).get("root", {})
    frozen_digest = (
        runner.tree_digest(runner.FROZEN_ROOT)
        if runner.FROZEN_ROOT.is_dir()
        else ""
    )
    if (
        frozen.get("file_count") != runner.EXPECTED_FROZEN_FILE_COUNT
        or runner.tree_file_count(runner.FROZEN_ROOT)
        != runner.EXPECTED_FROZEN_FILE_COUNT
        or frozen.get("before_sha256") != frozen_digest
        or frozen.get("after_sha256") != frozen_digest
    ):
        errors.append("exact-partition run did not preserve frozen inputs")
