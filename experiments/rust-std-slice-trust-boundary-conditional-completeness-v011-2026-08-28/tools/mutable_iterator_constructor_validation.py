#!/usr/bin/env python3
"""Validate the seven mutable-iterator constructor evidence trees."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

import campaign_common as common
import mutable_iterator_constructors as constructors
import replay_mutable_iterator_constructors as replay
import run_mutable_iterator_constructors as runner
import target_pipeline
from checker_guards import GuardError


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
        or stderr.read_text() != ""
        or (
            expected_stdout is not None
            and stdout.read_text() != expected_stdout
        )
    ):
        errors.append(f"{label} capture is not a clean exact replay")


def _validate_bound_inputs(
    config: constructors.ConstructorTarget,
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
        "private_constructors",
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
        if name == "private_constructors":
            continue
        _artifact_matches(
            record,
            common.OUT / record.get("path", ""),
            errors,
            f"{config.target} bound input {name}",
        )
    private = manifest.get("files", {}).get("private_constructors", {})
    if set(private) != {source.filename for source in config.private_sources}:
        errors.append(f"{config.target} private constructor set changed")
    private_source_texts: dict[str, str] = {}
    for source in config.private_sources:
        record = private.get(source.filename, {})
        source_path = root / "bound_inputs" / source.filename
        _artifact_matches(
            record,
            source_path,
            errors,
            f"{config.target} private source {source.name}",
        )
        if (
            record.get("operation") != source.name
            or record.get("source_lines") != source.citation
            or record.get("canonical_file_sha256")
            != constructors.CANONICAL_ITER_SHA256
        ):
            errors.append(f"{config.target} private source citation changed")
        if source_path.is_file():
            private_source_texts[source.name] = source_path.read_text()
    try:
        constructors.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            private_source_texts,
        )
    except (GuardError, OSError) as exc:
        errors.append(f"{config.target} source semantic anchors failed: {exc}")
    for name, record in manifest.get("frozen_implproof", {}).items():
        _artifact_matches(
            record,
            root / "bound_inputs" / name,
            errors,
            f"{config.target} frozen input {name}",
        )
        if record.get("sha256") != record.get("frozen_source_sha256"):
            errors.append(f"{config.target} frozen input {name} hash diverged")
    _artifact_matches(
        result.get("bound_inputs"),
        path,
        errors,
        f"{config.target} bound-input manifest",
    )


def _validate_reconciliation(
    config: constructors.ConstructorTarget,
    result: dict[str, Any],
    root: Path,
    errors: list[str],
) -> None:
    if config.input_order != "76":
        if result.get("citation_reconciliation") is not None:
            errors.append(f"{config.target} has an unexpected reconciliation")
        return
    path = root / "trust_site_citation_reconciliation.json"
    record = _load_json(path, errors, "TS-076-C003 reconciliation")
    canonical = record.get("canonical_source", {})
    if (
        record.get("record_id") != "TS-076-C003"
        or record.get("frozen_record_preserved") is not True
        or record.get("frozen_source_lines")
        != "core/src/slice/iter.rs:1223-1225"
        or canonical.get("source_lines")
        != "core/src/slice/iter.rs:1289-1293"
        or canonical.get("file_sha256")
        != constructors.CANONICAL_ITER_SHA256
        or "GenericSplitN { iter: s, count: n }"
        not in record.get("reconciliation", "")
    ):
        errors.append("TS-076-C003 stale citation was not reconciled")
    excerpt = canonical.get("excerpt", {})
    _artifact_matches(
        excerpt,
        root / "bound_inputs/rsplitnmut_new.rs",
        errors,
        "TS-076-C003 canonical constructor",
    )
    _artifact_matches(
        result.get("citation_reconciliation"),
        path,
        errors,
        "TS-076-C003 reconciliation",
    )


def _validate_target(
    config: constructors.ConstructorTarget,
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
        authority_path, errors, f"{config.target} authority bindings"
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
    trust = _load_json(
        trust_path, errors, f"{config.target} trust bindings"
    )
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
        boundary_path, errors, f"{config.target} boundary manifest"
    ) != constructors.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact_matches(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    _validate_bound_inputs(config, result, root, errors)
    _validate_reconciliation(config, result, root, errors)

    obligations = result.get("obligations", {})
    if set(obligations) != set(constructors.PURPOSES):
        errors.append(f"{config.target} obligation result set is incomplete")
    for purpose, stem in replay.OBLIGATIONS.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        metadata = _load_json(
            metadata_path, errors, f"{config.target} {purpose} metadata"
        )
        try:
            constructors.validate_target_obligation(
                config, smt_path.read_text(), metadata
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
        errors.append(f"{config.target} source instances are incomplete")
    for name, (length, element_size) in replay.SOURCE_INSTANCES.items():
        path = root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != constructors.source_instance_text(
                config, length=length, element_size=element_size
            )
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = instances.get(name, {})
        _artifact_matches(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} source instance",
        )
        solver = evidence.get("solver", {})
        _capture(
            solver,
            [z3, "-smt2", str(path)],
            "sat\n",
            errors,
            f"{config.target} {name} solver",
        )

    try:
        independent = replay.replay(root, z3, config)
    except Exception as exc:
        errors.append(f"{config.target} independent replay failed: {exc}")
        independent = {}
    replay_record = result.get("solver_replay", {})
    expected_replay_argv = [
        sys.executable,
        str(common.OUT / "tools/replay_mutable_iterator_constructors.py"),
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
        json.dumps(independent, sort_keys=True) + "\n",
        errors,
        f"{config.target} independent replay",
    )
    if independent.get("status") != "passed":
        errors.append(f"{config.target} independent replay did not pass")

    proof_path = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = root / "verus/constructor_model.rs"
    expected_proof = constructors.verus_text(config)
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
        verification_stdout = (
            common.OUT / verification["stdout"]
        ).read_text()
    except (KeyError, OSError, TypeError):
        verification_stdout = ""
    if "0 errors" not in verification_stdout:
        errors.append(f"{config.target} Verus verification summary changed")


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("constructor validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in constructors.TARGETS:
        _validate_target(config, by_key, z3, errors)

    classified = {
        key
        for key, row in by_key.items()
        if any(
            row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS
        )
    }
    expected = set(runner.BASELINE_RESULTS) | set(constructors.TARGET_KEYS)
    if not expected <= classified:
        errors.append("certified constructor results are not preserved")

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "constructor cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in constructors.TARGETS]
        or manifest.get("classified_rows") != 34
        or manifest.get("not_run_rows") != 28
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
        or set(manifest.get("preserved_frozen_inputs", {}))
        != {config.artifact_id for config in constructors.TARGETS}
    ):
        errors.append("constructor cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"constructor run did not preserve {artifact_id}")
    for artifact_id, record in manifest.get(
        "preserved_frozen_inputs", {}
    ).items():
        root = common.OUT / "provenance/frozen/implproof" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"constructor run changed frozen {artifact_id}")
