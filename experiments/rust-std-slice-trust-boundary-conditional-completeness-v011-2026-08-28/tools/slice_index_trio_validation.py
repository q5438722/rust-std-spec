#!/usr/bin/env python3
"""Validate SliceIndex trio evidence and the delivered result ledger."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import align_to_pair as align_pair
import replay_slice_index_trio as replay
import run_slice_index_trio as runner
import slice_index_trio as trio
import address_observer_pair
import mutable_view_construction_cluster as mutable_views
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


def _solver_capture(
    record: Any,
    expected_argv: list[str],
    expected: str,
    errors: list[str],
    label: str,
    *,
    require_payload: bool = False,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label} solver capture is missing")
        return
    try:
        command = common.OUT / record["command"]
        stdout = common.OUT / record["stdout"]
        stderr = common.OUT / record["stderr"]
        status = common.OUT / record["status"]
    except (KeyError, TypeError):
        errors.append(f"{label} solver capture paths are malformed")
        return
    if not all(path.is_file() for path in (command, stdout, stderr, status)):
        errors.append(f"{label} solver capture files are missing")
        return
    output = stdout.read_text()
    lines = output.splitlines()
    if (
        record.get("argv") != expected_argv
        or command.read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or status.read_text() != "0\n"
        or stderr.read_text()
        or not lines
        or lines[0] != expected
        or record.get("solver_result") != expected
        or record.get("expected_solver_result") != expected
        or record.get("model_retained") is not require_payload
        or (not require_payload and output != expected + "\n")
        or (
            require_payload
            and (
                len(lines) < 2
                or "(NormalizedStart x)" not in output
                or "(y_address y1)" not in output
            )
        )
    ):
        errors.append(f"{label} solver capture is not an exact clean replay")


def _validate_bound_inputs(
    config: trio.SliceIndexTarget,
    row: dict[str, str],
    root: Path,
    result: dict[str, Any],
    errors: list[str],
) -> None:
    manifest_path = root / "bound_inputs/manifest.json"
    manifest = _load_json(
        manifest_path, errors, f"{config.target} bound-input manifest"
    )
    expected_files = {
        "active_contract.txt",
        "generated_declaration.rs",
        "source_item.rs",
        "public_docs.md",
        "slice_index_vocabulary.rs",
        "rust_slice_index.rs",
        "rust_index_wrappers.rs",
    }
    expected_frozen = {
        "implproof_harness.rs",
        "source_body.json",
        "transformation_manifest.json",
        "dependency_assumption_manifest.json",
    }
    if (
        manifest.get("target") != config.target
        or manifest.get("input_order") != config.input_order
        or manifest.get("active_contract_sha256")
        != config.active_contract_sha256
        or set(manifest.get("files", {})) != expected_files
        or set(manifest.get("frozen_implproof", {})) != expected_frozen
        or set(manifest.get("trust_record_ids", []))
        != set(config.all_trust_site_ids)
        or manifest.get("modeled_sliceindex_forms")
        != [form.name for form in config.covered_forms]
    ):
        errors.append(f"{config.target} bound-input manifest is incomplete")

    expected_text_hashes = {
        "active_contract.txt": row["active_contract_sha256"],
        "generated_declaration.rs": row["generated_declaration_sha256"],
        "source_item.rs": row["source_item_sha256"],
        "public_docs.md": row["public_docs_sha256"],
    }
    for filename, expected_hash in expected_text_hashes.items():
        path = root / "bound_inputs" / filename
        _artifact(
            manifest.get("files", {}).get(filename),
            path,
            errors,
            f"{config.target} bound input {filename}",
        )
        if path.is_file() and common.sha256(path) != expected_hash:
            errors.append(f"{config.target} bound input hash changed: {filename}")

    vocabulary_path = root / "bound_inputs/slice_index_vocabulary.rs"
    vocabulary_record = manifest.get("files", {}).get(
        "slice_index_vocabulary.rs", {}
    )
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if vocabulary_source.is_file():
        expected_vocabulary = runner._source_excerpt(
            vocabulary_source, *trio.SLICE_INDEX_VOCABULARY_RANGE
        )
    else:
        expected_vocabulary = ""
    _artifact(
        vocabulary_record,
        vocabulary_path,
        errors,
        f"{config.target} SliceIndex vocabulary",
    )
    if (
        not vocabulary_path.is_file()
        or vocabulary_path.read_text() != expected_vocabulary
        or vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
    ):
        errors.append(f"{config.target} SliceIndex vocabulary binding changed")

    source_bindings = {
        "rust_slice_index.rs": (
            common.RUST_LIBRARY / trio.SLICE_INDEX_SOURCE,
            trio.SLICE_INDEX_SOURCE_SHA256,
        ),
        "rust_index_wrappers.rs": (
            common.RUST_LIBRARY / trio.INDEX_WRAPPER_SOURCE,
            trio.INDEX_WRAPPER_SOURCE_SHA256,
        ),
    }
    for filename, (source, expected_hash) in source_bindings.items():
        path = root / "bound_inputs" / filename
        record = manifest.get("files", {}).get(filename)
        _artifact(
            record,
            path,
            errors,
            f"{config.target} canonical {filename}",
        )
        if (
            not source.is_file()
            or common.sha256(source) != expected_hash
            or not path.is_file()
            or path.read_bytes() != source.read_bytes()
            or not isinstance(record, dict)
            or record.get("canonical_file_sha256") != expected_hash
        ):
            errors.append(f"{config.target} canonical {filename} changed")

    expected_frozen_hashes = {
        "implproof_harness.rs": row["harness_sha256"],
        "source_body.json": row["source_body_manifest_sha256"],
        "transformation_manifest.json": row[
            "transformation_manifest_sha256"
        ],
        "dependency_assumption_manifest.json": row[
            "dependency_manifest_sha256"
        ],
    }
    for filename, expected_hash in expected_frozen_hashes.items():
        path = root / "bound_inputs" / filename
        record = manifest.get("frozen_implproof", {}).get(filename)
        _artifact(
            record,
            path,
            errors,
            f"{config.target} frozen input {filename}",
        )
        if (
            path.is_file()
            and common.sha256(path) != expected_hash
            or isinstance(record, dict)
            and record.get("frozen_source_sha256") != expected_hash
        ):
            errors.append(f"{config.target} frozen input changed: {filename}")

    try:
        trio.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            (root / "bound_inputs/public_docs.md").read_text(),
            vocabulary_path.read_text(),
            (root / "bound_inputs/rust_slice_index.rs").read_text(),
            (root / "bound_inputs/rust_index_wrappers.rs").read_text(),
        )
    except (OSError, ValueError) as exc:
        errors.append(f"{config.target} source anchors failed: {exc}")
    _artifact(
        result.get("bound_inputs"),
        manifest_path,
        errors,
        f"{config.target} bound-input manifest",
    )


def _validate_target(
    config: trio.SliceIndexTarget,
    rows: dict[tuple[str, str], dict[str, str]],
    z3: str,
    errors: list[str],
) -> None:
    root = common.OUT / "evidence/targets" / config.artifact_id
    result_path = root / "result.json"
    result = _load_json(result_path, errors, f"{config.target} result")
    row = rows.get((config.target, config.input_order))
    if row is None:
        errors.append(f"{config.target} crosswalk row is missing")
        return
    if (
        result.get("target") != config.target
        or result.get("input_order") != config.input_order
        or result.get("artifact_id") != config.artifact_id
        or result.get("active_contract_sha256")
        != config.active_contract_sha256
        or result.get("active_contract_text") != config.active_contract_text
        or result.get("classification") != config.expected_classification
        or result.get("remaining_not_run_rows") != 8
        or result.get("updated_crosswalk_fields")
        != list(target_pipeline.RESULT_FIELDS)
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(config.excluded_trust_site_ids)
        or set(result.get("context_only_trust_site_ids", []))
        != set(config.context_only_trust_site_ids)
    ):
        errors.append(f"{config.target} result identity/classification is malformed")
    if any(
        row[field] != value
        for field, value in config.expected_classification.items()
    ):
        errors.append(f"{config.target} crosswalk classification is stale")

    authority_path = root / "authority_bindings.json"
    authority = _load_json(
        authority_path, errors, f"{config.target} authority bindings"
    )
    expected_bindings = {field: row[field] for field in runner.AUTHORITY_FIELDS}
    if authority.get("bindings") != expected_bindings:
        errors.append(f"{config.target} authority bindings changed")
    _artifact(
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
    if (
        set(records) != set(config.all_trust_site_ids)
        or any(
            trio.canonical_json_sha256(records[record_id])
            != config.trust_hashes[record_id]
            for record_id in records
        )
    ):
        errors.append(f"{config.target} readable trust records changed")
    _artifact(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    boundary = _load_json(
        boundary_path, errors, f"{config.target} boundary manifest"
    )
    if boundary != trio.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    observed = json.dumps(
        boundary.get("shared_boundary_observations", [])
    ).lower()
    for forbidden in (
        "returned reference",
        "selected index",
        "final receiver",
        "canonical answer",
        "execution trace",
    ):
        if forbidden in observed:
            errors.append(f"{config.target} boundary contains {forbidden}")
    _artifact(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )

    audit_path = root / "contract_translation_audit.json"
    audit = _load_json(
        audit_path, errors, f"{config.target} contract translation audit"
    )
    if (
        audit.get("opaque_vocabulary_is_solver_function") is not False
        or audit.get("canonical_source_result_conjoined_to_spec")
        is not config.exhaustive_index_coverage
        or audit.get("covered_sliceindex_forms")
        != [form.name for form in config.covered_forms]
        or audit.get("coverage_complete_for_claim") is not True
        or audit.get("source_backed_replacement_id") != config.replacement_id
    ):
        errors.append(f"{config.target} contract translation audit changed")
    _artifact(
        result.get("contract_translation_audit"),
        audit_path,
        errors,
        f"{config.target} contract translation audit",
    )
    _validate_bound_inputs(config, row, root, result, errors)

    obligation_specs = {
        trio.PRIMARY: "obligation",
        trio.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append(f"{config.target} obligation set is incomplete")
        obligations = {}
    for purpose, stem in obligation_specs.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        try:
            metadata = _load_json(
                metadata_path, errors, f"{config.target} {purpose} metadata"
            )
            trio.validate_target_obligation(
                config, smt_path.read_text(), metadata
            )
        except (OSError, ValueError) as exc:
            errors.append(f"{config.target} {purpose} checker rejection: {exc}")
            continue
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            errors.append(f"{config.target} {purpose} result is missing")
            continue
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
        _solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            config.expected_results[purpose],
            errors,
            f"{config.target} {purpose}",
        )

    source_instances = result.get("source_instances")
    expected_source_cases = trio.source_cases(config)
    if not isinstance(source_instances, dict) or set(
        source_instances
    ) != set(expected_source_cases):
        errors.append(f"{config.target} source instance set is incomplete")
        source_instances = {}
    for name in expected_source_cases:
        path = root / "source_instances" / f"{name}.smt2"
        evidence = source_instances.get(name)
        if not isinstance(evidence, dict):
            continue
        if path.is_file() and path.read_text() != trio.source_instance_text(
            config, name
        ):
            errors.append(f"{config.target} {name} source instance changed")
        _artifact(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} source instance",
        )
        _solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            errors,
            f"{config.target} {name} source instance",
            require_payload=True,
        )

    negative = result.get("negative_probes")
    expected_negative = trio.negative_probe_names(config)
    if not isinstance(negative, dict) or set(negative) != set(
        expected_negative
    ):
        errors.append(f"{config.target} negative probe set is incomplete")
        negative = {}
    for name in expected_negative:
        path = root / "negative_probes" / f"{name}.smt2"
        evidence = negative.get(name)
        if not isinstance(evidence, dict):
            continue
        if path.is_file() and path.read_text() != trio.negative_probe_text(
            config, name
        ):
            errors.append(f"{config.target} {name} negative probe changed")
        _artifact(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} negative probe",
        )
        _solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "unsat",
            errors,
            f"{config.target} {name} negative probe",
        )

    witness = result.get("fixed_reference_witness")
    if config.mutable:
        smt_path = root / "fixed_reference_witness.smt2"
        payload_path = root / "fixed_reference_witness.json"
        if not isinstance(witness, dict):
            errors.append(f"{config.target} fixed witness is missing")
        else:
            _artifact(
                witness.get("smt"),
                smt_path,
                errors,
                f"{config.target} fixed witness SMT",
            )
            _artifact(
                witness.get("payload"),
                payload_path,
                errors,
                f"{config.target} fixed witness payload",
            )
            if (
                smt_path.is_file()
                and smt_path.read_text() != trio.fixed_witness_text(config)
                or payload_path.is_file()
                and _load_json(
                    payload_path, errors, f"{config.target} witness payload"
                )
                != trio.witness_payload(config)
            ):
                errors.append(f"{config.target} fixed witness changed")
            _solver_capture(
                witness.get("solver"),
                [z3, "-smt2", str(smt_path)],
                "sat",
                errors,
                f"{config.target} fixed witness",
                require_payload=True,
            )
    elif witness is not None:
        errors.append(f"{config.target} unexpectedly retained an incompleteness witness")

    try:
        independent = replay.replay(root, z3, config)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{config.target} independent replay failed: {exc}")
        independent = None
    replay_record = result.get("solver_replay")
    expected_replay_argv = [
        sys.executable,
        str(common.OUT / "tools/replay_slice_index_trio.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
        "--artifact-id",
        config.artifact_id,
    ]
    if not isinstance(replay_record, dict):
        errors.append(f"{config.target} replay capture is missing")
    else:
        try:
            command = common.OUT / replay_record["command"]
            stdout = common.OUT / replay_record["stdout"]
            stderr = common.OUT / replay_record["stderr"]
            status = common.OUT / replay_record["status"]
            captured = json.loads(stdout.read_text())
        except (KeyError, OSError, json.JSONDecodeError):
            command = stdout = stderr = status = Path()
            captured = None
        if (
            not all(path.is_file() for path in (command, stdout, stderr, status))
            or replay_record.get("argv") != expected_replay_argv
            or command.read_text() != shlex.join(expected_replay_argv) + "\n"
            or replay_record.get("exit_code") != 0
            or status.read_text() != "0\n"
            or stderr.read_text()
            or captured != independent
            or replay_record.get("result") != independent
        ):
            errors.append(f"{config.target} replay capture is invalid")

    source_model = common.OUT / config.proof_filename
    captured_model = root / "verus/source_and_contract_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append(f"{config.target} Verus evidence is missing")
    else:
        _artifact(
            verus.get("source_model"),
            source_model,
            errors,
            f"{config.target} source Verus model",
        )
        _artifact(
            verus.get("captured_model"),
            captured_model,
            errors,
            f"{config.target} captured Verus model",
        )
        if (
            not source_model.is_file()
            or not captured_model.is_file()
            or source_model.read_bytes() != captured_model.read_bytes()
            or "external_body" in source_model.read_text()
        ):
            errors.append(f"{config.target} Verus source model changed")
        for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
            record = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(record, dict):
                errors.append(f"{config.target} Verus {key} capture is missing")
                continue
            try:
                command = common.OUT / record["command"]
                stdout = common.OUT / record["stdout"]
                stderr = common.OUT / record["stderr"]
                status = common.OUT / record["status"]
            except (KeyError, TypeError):
                errors.append(f"{config.target} Verus {key} paths are malformed")
                continue
            output = stdout.read_text() if stdout.is_file() else ""
            if (
                not all(path.is_file() for path in (command, stdout, stderr, status))
                or record.get("argv") != expected_argv
                or command.read_text() != shlex.join(expected_argv) + "\n"
                or record.get("exit_code") != 0
                or status.read_text() != "0\n"
                or stderr.read_text()
                or (
                    key == "verification"
                    and config.verus_expected_summary not in output
                )
            ):
                errors.append(f"{config.target} Verus {key} capture is invalid")


def _validate_cluster(errors: list[str]) -> None:
    path = runner.CLUSTER_ROOT / "manifest.json"
    manifest = _load_json(path, errors, "SliceIndex cluster manifest")
    targets = {
        (item.get("target"), item.get("input_order")): item
        for item in manifest.get("targets", [])
        if isinstance(item, dict)
    }
    if (
        set(targets) != set(trio.TARGET_KEYS)
        or manifest.get("classified_rows") != 54
        or manifest.get("not_run_rows") != 8
        or manifest.get("independent_review") != "required"
        or manifest.get("stage_transition") != "disabled"
    ):
        errors.append("SliceIndex cluster manifest identity is malformed")
    frozen = manifest.get("frozen_inputs", {})
    current_frozen_digest = (
        runner.tree_digest(runner.FROZEN_ROOT)
        if runner.FROZEN_ROOT.is_dir()
        else ""
    )
    if (
        frozen.get("file_count") != runner.EXPECTED_FROZEN_FILE_COUNT
        or frozen.get("before_sha256") != frozen.get("after_sha256")
        or frozen.get("after_sha256") != current_frozen_digest
        or runner.tree_file_count(runner.FROZEN_ROOT)
        != runner.EXPECTED_FROZEN_FILE_COUNT
    ):
        errors.append("SliceIndex cluster did not preserve 320 frozen inputs")
    preservation = manifest.get("preserved_target_evidence")
    if not isinstance(preservation, dict) or set(preservation) != set(
        runner.PRESERVED_ARTIFACT_IDS
    ):
        errors.append("SliceIndex cluster preservation set is incomplete")
    else:
        for artifact_id, record in preservation.items():
            root = runner.EVIDENCE_BASE / artifact_id
            current = runner.tree_digest(root) if root.is_dir() else ""
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current
            ):
                errors.append(
                    f"SliceIndex cluster did not preserve {artifact_id}"
                )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("SliceIndex validation cannot locate z3")
        return
    rows_list = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    rows = {_row_key(row): row for row in rows_list}
    classified = sum(
        any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows_list
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows_list
    )
    expected_classified = (
        set(runner.BASELINE_RESULTS)
        | set(trio.TARGET_KEYS)
        | set(address_observer_pair.TARGET_KEYS)
        | set(mutable_views.TARGET_KEYS)
        | set(align_pair.TARGET_KEYS)
    )
    observed_classified = {
        _row_key(row)
        for row in rows_list
        if any(
            row[field] != "not-run"
            for field in target_pipeline.RESULT_FIELDS
        )
    }
    if (
        classified != 62
        or not_run != 0
        or observed_classified != expected_classified
    ):
        errors.append(
            f"SliceIndex successor ledger expected 62 classified and 0 not-run, "
            f"got {classified} and {not_run}"
        )
    for config in trio.TARGETS:
        _validate_target(config, rows, z3, errors)
    _validate_cluster(errors)


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def main() -> None:
    errors: list[str] = []
    validate(errors)
    if errors:
        print("slice_index_validation=FAIL")
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    print("slice_index_validation=PASS")
    print("target_result_counts=60_classified,2_not-run")


if __name__ == "__main__":
    main()
