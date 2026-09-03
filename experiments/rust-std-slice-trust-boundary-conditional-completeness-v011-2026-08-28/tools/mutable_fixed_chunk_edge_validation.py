#!/usr/bin/env python3
"""Validate mutable fixed-chunk evidence and the delivered ledger."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import mutable_fixed_chunk_edges as fixed
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import replay_mutable_fixed_chunk_edges as replay
import run_mutable_fixed_chunk_edges as runner
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
    expected: str | None,
    errors: list[str],
    label: str,
    *,
    require_model: bool = False,
    expected_stdout: str | None = None,
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
    output = stdout.read_text()
    lines = output.splitlines()
    if (
        record.get("argv") != expected_argv
        or command.read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or status.read_text() != "0\n"
        or stderr.read_text()
        or (expected is not None and (not lines or lines[0] != expected))
        or (
            expected is not None
            and not require_model
            and output != expected + "\n"
        )
        or (
            require_model
            and (
                len(lines) < 2
                or "(x_n x)" not in output
                or "(y_split_index y1)" not in output
                or record.get("model_retained") is not True
            )
        )
        or (
            expected_stdout is not None
            and output != expected_stdout
        )
    ):
        errors.append(f"{label} capture is not a clean exact replay")


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    return "".join(lines[start - 1 : end])


def _canonical_path(
    source: fixed.CanonicalSource,
    row: dict[str, str],
) -> Path:
    if source.path == fixed.SLICE_SOURCE_PATH:
        return Path(row["source_path"])
    return common.RUST_LIBRARY / source.path


def _validate_bound_inputs(
    config: fixed.FixedChunkTarget,
    row: dict[str, str],
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
        "fixed_chunk_vocabulary.rs",
    }
    if (
        manifest.get("target") != config.target
        or manifest.get("input_order") != config.input_order
        or manifest.get("active_contract_sha256")
        != config.active_contract_sha256
        or set(manifest.get("files", {})) != expected_files
        or set(manifest.get("canonical_helpers", {}))
        != set(config.helper_names)
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
    vocabulary_path = root / "bound_inputs/fixed_chunk_vocabulary.rs"
    vocabulary_record = manifest.get("files", {}).get(
        "fixed_chunk_vocabulary.rs", {}
    )
    if (
        vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
        or vocabulary_record.get("source_ranges")
        != [f"{start}-{end}" for start, end in fixed.VOCABULARY_RANGES]
    ):
        errors.append(f"{config.target} vocabulary binding changed")

    helper_texts: dict[str, str] = {}
    for source in config.helper_sources:
        copied = root / "bound_inputs" / source.filename
        record = manifest.get("canonical_helpers", {}).get(source.name)
        _artifact(
            record,
            copied,
            errors,
            f"{config.target} canonical helper {source.name}",
        )
        canonical = _canonical_path(source, row)
        if (
            not canonical.is_file()
            or common.sha256(canonical) != source.file_sha256
            or not copied.is_file()
            or copied.read_text()
            != _source_excerpt(canonical, source.start, source.end)
            or record.get("canonical_file_sha256") != source.file_sha256
            or record.get("source_lines") != source.reference
        ):
            errors.append(f"{config.target} canonical helper {source.name} changed")
        if copied.is_file():
            helper_texts[source.name] = copied.read_text()
    try:
        fixed.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            vocabulary_path.read_text(),
            helper_texts,
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
    config: fixed.FixedChunkTarget,
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
        row = {}

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
    if set(by_id) != set(config.all_trust_site_ids):
        errors.append(f"{config.target} trust bindings changed")
    else:
        for site in config.context_only_trust_site_ids:
            expected = (
                "context-only-specification-vocabulary"
                if site.endswith("D001")
                else "context-only-source-closure"
            )
            if by_id[site].get("semantic_disposition") != expected:
                errors.append(f"{config.target} context trust site {site} changed")
        for site in config.excluded_trust_site_ids:
            if (
                by_id[site].get("target_postcondition_coverage")
                != "partial-or-lower-level"
            ):
                errors.append(f"{config.target} lower trust site {site} changed")
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
    ) != fixed.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    if row:
        _validate_bound_inputs(config, row, result, root, errors)

    obligations = result.get("obligations", {})
    if set(obligations) != set(fixed.PURPOSES):
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
            fixed.validate_target_obligation(
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
            "unsat",
            errors,
            f"{config.target} {purpose} solver",
        )
        if solver.get("solver_result") != "unsat":
            errors.append(f"{config.target} {purpose} solver status changed")

    source_instances = result.get("source_instances", {})
    if set(source_instances) != set(fixed.SOURCE_CASES):
        errors.append(f"{config.target} source-instance set is incomplete")
    for name, case in fixed.SOURCE_CASES.items():
        path = root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != fixed.source_instance_text(config, case)
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = source_instances.get(name, {})
        _artifact(
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
    if set(probes) != set(fixed.NEGATIVE_PROBES):
        errors.append(f"{config.target} negative-probe set is incomplete")
    for name in fixed.NEGATIVE_PROBES:
        path = root / f"negative_probe_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != fixed.negative_probe_text(config, name)
        ):
            errors.append(f"{config.target} {name} negative probe changed")
        evidence = probes.get(name, {})
        _artifact(
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
            str(common.OUT / "tools/replay_mutable_fixed_chunk_edges.py"),
            "--evidence-root",
            str(root),
            "--z3",
            z3,
            "--artifact-id",
            config.artifact_id,
        ],
        None,
        errors,
        f"{config.target} independent replay",
        expected_stdout=json.dumps(replayed, sort_keys=True) + "\n",
    )
    if replayed.get("status") != "passed":
        errors.append(f"{config.target} independent replay did not pass")

    proof = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = root / "verus/fixed_chunk_model.rs"
    expected_proof = fixed.verus_text(config)
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
    )
    if "0 errors" not in verification_stdout:
        errors.append(f"{config.target} Verus verification summary changed")

    guards_path = root / "reviewed_model_guards.json"
    guards = _load_json(
        guards_path,
        errors,
        f"{config.target} reviewed guards",
    )
    if len(guards.get("fail_closed_mutations", [])) != 16:
        errors.append(f"{config.target} reviewed guard set is incomplete")
    _artifact(
        result.get("reviewed_model_guards"),
        guards_path,
        errors,
        f"{config.target} reviewed guards",
    )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("fixed-chunk validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in fixed.TARGETS:
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
        | set(fixed.TARGET_KEYS)
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
        errors.append("fixed-chunk downstream 62/0 result ledger is not preserved")

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "fixed-chunk cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in fixed.TARGETS]
        or manifest.get("classified_rows") != 45
        or manifest.get("not_run_rows") != 17
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("fixed-chunk cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"fixed-chunk run did not preserve {artifact_id}")
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
        errors.append("fixed-chunk run did not preserve frozen inputs")
