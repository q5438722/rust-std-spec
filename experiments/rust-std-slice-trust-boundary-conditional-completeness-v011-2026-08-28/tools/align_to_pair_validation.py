#!/usr/bin/env python3
"""Validate align_to pair evidence and the final 62-row ledger."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import align_to_pair as align
import campaign_common as common
import replay_align_to_pair as replay
import run_align_to_pair as runner
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
    witness: bool = False,
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
    markers = (
        (
            "(s_final_bytes s1)",
            "(s_final_bytes s2)",
            "(s_final_middle s1)",
            "(s_final_middle s2)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else (
            "(y_branch y1)",
            "(y_middle_values y1)",
            "(s_final_source s1)",
        )
    )
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
                or any(marker not in output for marker in markers)
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


def _validate_bound_inputs(
    config: align.AlignTarget,
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
        "align_to_vocabulary.rs",
    }
    expected_helpers = {
        "ptr_align_offset_impl",
        "ptr_align_offset_docs",
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
        or set(manifest.get("canonical_helpers", {})) != expected_helpers
        or set(manifest.get("frozen_implproof", {})) != expected_frozen
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
    for name, record in manifest.get("frozen_implproof", {}).items():
        copied = root / "bound_inputs" / name
        _artifact(
            record, copied, errors, f"{config.target} frozen {name}"
        )
        if record.get("sha256") != record.get("frozen_source_sha256"):
            errors.append(f"{config.target} frozen {name} diverged")

    vocabulary_path = root / "bound_inputs/align_to_vocabulary.rs"
    canonical_vocabulary = Path(row["shared_vocabulary_path"])
    expected_vocabulary = "\n".join(
        _source_excerpt(canonical_vocabulary, start, end)
        for start, end in align.VOCABULARY_RANGES
    )
    vocabulary_record = manifest.get("files", {}).get(
        "align_to_vocabulary.rs", {}
    )
    if (
        not vocabulary_path.is_file()
        or vocabulary_path.read_text() != expected_vocabulary
        or vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
    ):
        errors.append(f"{config.target} vocabulary binding changed")

    pointer_source = common.RUST_LIBRARY / align.PTR_SOURCE_PATH
    pointer_docs = common.RUST_LIBRARY / align.PTR_DOCS_PATH
    helper_specs = {
        "ptr_align_offset_impl": (
            pointer_source,
            align.PTR_SOURCE_SHA256,
            align.PTR_SOURCE_RANGE,
        ),
        "ptr_align_offset_docs": (
            pointer_docs,
            align.PTR_DOCS_SHA256,
            align.PTR_DOCS_RANGE,
        ),
    }
    helper_texts: dict[str, str] = {}
    for name, (canonical, digest, source_range) in helper_specs.items():
        copied = root / "bound_inputs" / f"{name}.rs"
        record = manifest.get("canonical_helpers", {}).get(name, {})
        expected = _source_excerpt(canonical, *source_range)
        _artifact(
            record,
            copied,
            errors,
            f"{config.target} canonical helper {name}",
        )
        if (
            not canonical.is_file()
            or common.sha256(canonical) != digest
            or not copied.is_file()
            or copied.read_text() != expected
            or record.get("canonical_file_sha256") != digest
        ):
            errors.append(f"{config.target} canonical helper {name} changed")
        if copied.is_file():
            helper_texts[name] = copied.read_text()
    try:
        align.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            (root / "bound_inputs/public_docs.md").read_text(),
            vocabulary_path.read_text(),
            helper_texts["ptr_align_offset_impl"],
            helper_texts["ptr_align_offset_docs"],
        )
    except Exception as exc:
        errors.append(f"{config.target} source anchors failed: {exc}")
    _artifact(
        result.get("bound_inputs"),
        path,
        errors,
        f"{config.target} bound-input manifest",
    )


def _validate_target(
    config: align.AlignTarget,
    rows: dict[tuple[str, str], dict[str, str]],
    z3: str,
    errors: list[str],
) -> None:
    root = runner.EVIDENCE_BASE / config.artifact_id
    result_path = root / "result.json"
    result = _load_json(result_path, errors, f"{config.target} result")
    if (
        result.get("target") != config.target
        or result.get("input_order") != config.input_order
        or result.get("active_contract_sha256")
        != config.active_contract_sha256
        or result.get("active_contract_text") != config.active_contract_text
        or result.get("classification") != config.expected_classification
        or result.get("remaining_not_run_rows") != 0
        or result.get("updated_crosswalk_fields")
        != list(target_pipeline.RESULT_FIELDS)
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
    ):
        errors.append(f"{config.target} result identity/classification malformed")
    row = rows.get((config.target, config.input_order))
    if row is None or any(
        row[field] != value
        for field, value in config.expected_classification.items()
    ):
        errors.append(f"{config.target} crosswalk classification missing")
        row = {}

    authority_path = root / "authority_bindings.json"
    bindings = _load_json(
        authority_path, errors, f"{config.target} authority"
    ).get("bindings", {})
    if (
        bindings.get("active_contract_sha256")
        != config.active_contract_sha256
        or bindings.get("generated_declaration_sha256")
        != config.generated_declaration_sha256
        or bindings.get("source_item_sha256") != config.source_item_sha256
        or bindings.get("public_docs_sha256") != config.public_docs_sha256
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
    trust = _load_json(trust_path, errors, f"{config.target} trust")
    records = {
        record.get("record_id"): record
        for record in trust.get("records", [])
        if isinstance(record, dict)
    }
    if set(records) != set(config.all_trust_site_ids):
        errors.append(f"{config.target} trust binding set changed")
    else:
        for record_id, expected_hash in config.trust_hashes.items():
            if (
                align.canonical_json_sha256(records[record_id])
                != expected_hash
            ):
                errors.append(f"{record_id} trust binding changed")
        for record_id in config.excluded_trust_site_ids:
            disposition = records[record_id]["semantic_disposition"]
            if not (
                disposition.startswith("inadmissible")
                or disposition == "mixed-support-includes-answer-bearing-site"
            ):
                errors.append(f"{record_id} was relabeled")
    _artifact(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    if _load_json(
        boundary_path, errors, f"{config.target} boundary"
    ) != align.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    if row:
        _validate_bound_inputs(config, row, result, root, errors)

    translation_path = root / "contract_translation_audit.json"
    translation = _load_json(
        translation_path, errors, f"{config.target} translation"
    )
    if (
        translation.get("active_contract_sha256")
        != config.active_contract_sha256
        or translation.get("active_contract_preserved") is not True
        or translation.get("opaque_vocabulary_declared_to_solver") is not False
        or translation.get(
            "canonical_answer_conjoined_outside_active_contract"
        )
        is not False
        or set(translation.get("excluded_sites_replaced_not_relabeled", []))
        != set(config.excluded_trust_site_ids)
    ):
        errors.append(f"{config.target} contract translation malformed")
    _artifact(
        result.get("contract_translation_audit"),
        translation_path,
        errors,
        f"{config.target} contract translation",
    )

    obligations = result.get("obligations", {})
    if set(obligations) != set(align.PURPOSES):
        errors.append(f"{config.target} obligation set incomplete")
    for purpose, stem in replay.OBLIGATIONS.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        metadata = _load_json(
            metadata_path, errors, f"{config.target} {purpose} metadata"
        )
        try:
            align.validate_target_obligation(
                config, smt_path.read_text(), metadata
            )
        except Exception as exc:
            errors.append(f"{config.target} {purpose} rejected: {exc}")
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
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            config.expected_solver_results[purpose],
            errors,
            f"{config.target} {purpose} solver",
        )

    witness = result.get("fixed_full_state_witness")
    if config.mutable:
        witness_smt = root / "fixed_full_state_witness.smt2"
        witness_json = root / "fixed_full_state_witness.json"
        if (
            not witness_smt.is_file()
            or witness_smt.read_text()
            != align.fixed_full_state_witness_text(config)
            or _load_json(
                witness_json,
                errors,
                f"{config.target} witness payload",
            )
            != align.witness_payload(config)
        ):
            errors.append(f"{config.target} fixed witness changed")
        if not isinstance(witness, dict):
            errors.append(f"{config.target} fixed witness missing")
        else:
            _artifact(
                witness.get("smt"),
                witness_smt,
                errors,
                f"{config.target} witness SMT",
            )
            _artifact(
                witness.get("payload"),
                witness_json,
                errors,
                f"{config.target} witness payload",
            )
            _capture(
                witness.get("solver"),
                [z3, "-smt2", str(witness_smt)],
                "sat",
                errors,
                f"{config.target} witness solver",
                require_model=True,
                witness=True,
            )
            if (
                witness.get("fixed_input") is not True
                or witness.get("fixed_boundary") is not True
                or witness.get("both_specs_satisfied") is not True
            ):
                errors.append(f"{config.target} witness is not replayable")
    elif witness is not None:
        errors.append(f"{config.target} has an unexpected SAT witness")

    source_instances = result.get("source_instances", {})
    if set(source_instances) != set(align.source_cases(config)):
        errors.append(f"{config.target} source-instance set incomplete")
    for name, case in align.source_cases(config).items():
        path = root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != align.source_instance_text(config, name)
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = source_instances.get(name, {})
        if (
            evidence.get("expected_source_outcome")
            != json.loads(json.dumps(align.evaluate_source(case)))
        ):
            errors.append(f"{config.target} {name} source outcome changed")
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
            f"{config.target} {name} source solver",
            require_model=True,
        )

    negative_probes = result.get("negative_probes", {})
    if set(negative_probes) != set(align.negative_probe_names(config)):
        errors.append(f"{config.target} negative-probe set incomplete")
    for name in align.negative_probe_names(config):
        path = root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != align.negative_probe_text(config, name)
        ):
            errors.append(f"{config.target} {name} probe changed")
        evidence = negative_probes.get(name, {})
        _artifact(
            evidence.get("smt"),
            path,
            errors,
            f"{config.target} {name} probe",
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
            str(common.OUT / "tools/replay_align_to_pair.py"),
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
    captured = root / "verus/source_and_contract_model.rs"
    expected_proof = align.verus_text(config)
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
    for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
        record = verus.get(key, {})
        argv = [
            str(common.VERUS),
            str(captured),
            "--crate-type=lib",
            *extra,
        ]
        _capture(
            record, argv, None, errors, f"{config.target} Verus {key}"
        )
        if key == "verification":
            try:
                output = (common.OUT / record["stdout"]).read_text()
            except (KeyError, OSError, TypeError):
                output = ""
            if align.VERUS_EXPECTED_SUMMARY not in output:
                errors.append(
                    f"{config.target} Verus verification summary changed"
                )

    guards_path = root / "reviewed_model_guards.json"
    guards = _load_json(guards_path, errors, f"{config.target} guards")
    if len(guards.get("fail_closed_mutations", [])) != 20:
        errors.append(f"{config.target} reviewed guard set incomplete")
    _artifact(
        result.get("reviewed_model_guards"),
        guards_path,
        errors,
        f"{config.target} reviewed guards",
    )


def _validate_cluster(errors: list[str]) -> None:
    path = runner.CLUSTER_ROOT / "manifest.json"
    manifest = _load_json(path, errors, "align-to cluster manifest")
    targets = {
        (item.get("target"), item.get("input_order")): item
        for item in manifest.get("targets", [])
        if isinstance(item, dict)
    }
    preserved = manifest.get("preserved_target_evidence", {})
    frozen = manifest.get("frozen_inputs", {})
    if (
        set(targets) != set(align.TARGET_KEYS)
        or manifest.get("classified_rows") != 62
        or manifest.get("not_run_rows") != 0
        or manifest.get("independent_review") != "required"
        or manifest.get("stage_transition") != "disabled"
        or set(preserved) != set(runner.PRESERVED_ARTIFACT_IDS)
        or any(
            item.get("before_sha256") != item.get("after_sha256")
            for item in preserved.values()
        )
        or frozen.get("file_count") != runner.EXPECTED_FROZEN_FILE_COUNT
        or frozen.get("before_sha256") != frozen.get("after_sha256")
    ):
        errors.append("align-to cluster manifest is malformed")
    for config in align.TARGETS:
        item = targets.get((config.target, config.input_order), {})
        result_path = (
            runner.EVIDENCE_BASE / config.artifact_id / "result.json"
        )
        if (
            item.get("artifact_id") != config.artifact_id
            or item.get("classification") != config.expected_classification
        ):
            errors.append(f"{config.target} cluster entry changed")
        _artifact(
            item.get("result"),
            result_path,
            errors,
            f"{config.target} cluster result",
        )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("z3 is unavailable for align-to validation")
        return
    rows_list = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    rows = {
        (row["target"], row["input_order"]): row for row in rows_list
    }
    if len(rows) != 62:
        errors.append("align-to validation requires the 62-row crosswalk")
        return
    for config in align.TARGETS:
        _validate_target(config, rows, z3, errors)
    _validate_cluster(errors)
    classified = sum(
        any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows_list
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows_list
    )
    if classified != 62 or not_run != 0:
        errors.append(
            f"final ledger has {classified} classified and {not_run} not-run"
        )
    try:
        reset_csv, reset_json = runner.prepare_crosswalk_reset(
            rows_list,
            json.loads(
                (
                    common.OUT
                    / "crosswalk/target_to_proof_boundary.json"
                ).read_text()
            ),
        )
    except Exception as exc:
        errors.append(f"align-to row-reset guard failed: {exc}")
    else:
        for before, after in zip(rows_list, reset_csv):
            changed = {
                field
                for field in before
                if before[field] != after[field]
            }
            if _row_key(before) in set(align.TARGET_KEYS):
                if changed - set(target_pipeline.RESULT_FIELDS):
                    errors.append("align-to reset changed authority fields")
            elif changed:
                errors.append("align-to reset changed an out-of-scope row")
        if reset_csv != reset_json:
            errors.append("align-to reset diverged CSV and JSON")


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def main() -> None:
    errors: list[str] = []
    validate(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("align_to_pair_validation=PASS")
    print("target_result_counts=62_classified,0_not-run")


if __name__ == "__main__":
    main()
