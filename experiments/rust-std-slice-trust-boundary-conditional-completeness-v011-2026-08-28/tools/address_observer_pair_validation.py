#!/usr/bin/env python3
"""Validate the delivered address-observer evidence and result ledger."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import address_observer_pair as pair
import campaign_common as common
import align_to_pair as align_pair
import replay_address_observer_pair as replay
import run_address_observer_pair as runner
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
                or "(y_return y1)" not in output
                or "(WrappingByteOffset x b)" not in output
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
    config: pair.AddressObserverTarget,
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
        "address_observer_vocabulary.rs",
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
        _artifact(
            record,
            root / "bound_inputs" / name,
            errors,
            f"{config.target} frozen {name}",
        )
        if record.get("sha256") != record.get("frozen_source_sha256"):
            errors.append(f"{config.target} frozen {name} diverged")

    vocabulary_path = root / "bound_inputs/address_observer_vocabulary.rs"
    canonical_vocabulary = Path(row["shared_vocabulary_path"])
    expected_vocabulary = "\n".join(
        _source_excerpt(canonical_vocabulary, start, end)
        for start, end in pair.VOCABULARY_RANGES
    )
    vocabulary_record = manifest.get("files", {}).get(
        "address_observer_vocabulary.rs", {}
    )
    if (
        not vocabulary_path.is_file()
        or vocabulary_path.read_text() != expected_vocabulary
        or vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
        or vocabulary_record.get("source_ranges")
        != [f"{start}-{end}" for start, end in pair.VOCABULARY_RANGES]
    ):
        errors.append(f"{config.target} vocabulary binding changed")
    try:
        pair.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            (root / "bound_inputs/public_docs.md").read_text(),
            vocabulary_path.read_text(),
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
    config: pair.AddressObserverTarget,
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
        or result.get("remaining_not_run_rows") != 6
        or result.get("updated_crosswalk_fields")
        != list(target_pipeline.RESULT_FIELDS)
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
    ):
        errors.append(f"{config.target} result identity/classification is malformed")

    row = rows.get((config.target, config.input_order))
    if row is None or any(
        row[field] != value
        for field, value in config.expected_classification.items()
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
    trust = _load_json(trust_path, errors, f"{config.target} trust bindings")
    records = trust.get("records", [])
    by_id = {
        item.get("record_id"): item
        for item in records
        if isinstance(item, dict)
    }
    if (
        set(by_id) != set(config.all_trust_site_ids)
        or trust.get("record_sha256") != config.trust_hashes
    ):
        errors.append(f"{config.target} trust binding set changed")
    for record_id, expected_hash in config.trust_hashes.items():
        if (
            record_id not in by_id
            or pair.canonical_json_sha256(by_id[record_id]) != expected_hash
        ):
            errors.append(f"{record_id} readable trust record changed")
    if any(
        not by_id.get(site, {}).get(
            "semantic_disposition", ""
        ).startswith("inadmissible")
        for site in config.excluded_trust_site_ids
    ):
        errors.append(f"{config.target} answer-bearing site was relabeled")
    _artifact(
        result.get("trust_site_bindings"),
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )

    boundary_path = root / "boundary_manifest.json"
    if _load_json(
        boundary_path, errors, f"{config.target} boundary"
    ) != pair.boundary_manifest(config):
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
        translation_path,
        errors,
        f"{config.target} contract translation",
    )
    if (
        translation.get("active_contract_preserved") is not True
        or translation.get("opaque_vocabulary_declared_to_solver") is not False
        or translation.get(
            "canonical_answer_conjoined_outside_active_contract"
        )
        is not False
        or translation.get("zst_panic_is_separate_outcome") is not True
        or translation.get("excluded_sites_replaced_not_relabeled")
        != list(config.excluded_trust_site_ids)
    ):
        errors.append(f"{config.target} contract translation audit changed")
    _artifact(
        result.get("contract_translation_audit"),
        translation_path,
        errors,
        f"{config.target} contract translation audit",
    )

    obligations = result.get("obligations", {})
    if set(obligations) != set(pair.PURPOSES):
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
            pair.validate_target_obligation(
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
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            config.expected_results[purpose],
            errors,
            f"{config.target} {purpose} solver",
        )

    source_instances = result.get("source_instances", {})
    if set(source_instances) != set(pair.source_cases(config)):
        errors.append(f"{config.target} source-instance set is incomplete")
    for name, case in pair.source_cases(config).items():
        path = root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != pair.source_instance_text(config, name)
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = source_instances.get(name, {})
        if evidence.get("expected_source_outcome") != pair.evaluate_source(
            config, case
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

    probes = result.get("negative_probes", {})
    if set(probes) != set(pair.negative_probe_names(config)):
        errors.append(f"{config.target} negative-probe set is incomplete")
    for name in pair.negative_probe_names(config):
        path = root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != pair.negative_probe_text(config, name)
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
            f"{config.target} {name} negative solver",
        )

    false_positive = result.get("empty_subslice_false_positives")
    if config.kind == "subslice":
        path = root / "empty_subslice_false_positives.json"
        if _load_json(
            path,
            errors,
            f"{config.target} empty false positives",
        ) != pair.false_positive_assessment(config):
            errors.append(f"{config.target} false-positive assessment changed")
        _artifact(
            false_positive,
            path,
            errors,
            f"{config.target} false-positive assessment",
        )
    elif false_positive is not None:
        errors.append(f"{config.target} unexpectedly has subslice evidence")

    try:
        replayed = replay.replay(root, z3, config)
    except Exception as exc:
        errors.append(f"{config.target} independent replay failed: {exc}")
        replayed = {}
    replay_record = result.get("solver_replay", {})
    expected_replay_argv = [
        sys.executable,
        str(common.OUT / "tools/replay_address_observer_pair.py"),
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
        expected_stdout=json.dumps(replayed, sort_keys=True) + "\n",
    )
    if replayed.get("status") != "passed":
        errors.append(f"{config.target} independent replay did not pass")

    proof = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured = root / "verus/source_and_contract_model.rs"
    expected_proof = pair.verus_text(config)
    if (
        not proof.is_file()
        or not captured.is_file()
        or proof.read_text() != expected_proof
        or captured.read_text() != expected_proof
        or "external_body" in expected_proof
    ):
        errors.append(f"{config.target} trusted-free Verus model changed")
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
            record,
            argv,
            None,
            errors,
            f"{config.target} Verus {key}",
        )
        if key == "verification":
            try:
                output = (common.OUT / record["stdout"]).read_text()
            except (KeyError, OSError, TypeError):
                output = ""
            if pair.VERUS_EXPECTED_SUMMARY not in output:
                errors.append(
                    f"{config.target} Verus verification summary changed"
                )

    guards_path = root / "reviewed_model_guards.json"
    guards = _load_json(guards_path, errors, f"{config.target} guards")
    if len(guards.get("fail_closed_mutations", [])) != 14:
        errors.append(f"{config.target} reviewed guard set is incomplete")
    _artifact(
        result.get("reviewed_model_guards"),
        guards_path,
        errors,
        f"{config.target} reviewed model guards",
    )


def _validate_cluster(errors: list[str]) -> None:
    path = runner.CLUSTER_ROOT / "manifest.json"
    manifest = _load_json(path, errors, "address-observer cluster manifest")
    targets = {
        (item.get("target"), item.get("input_order")): item
        for item in manifest.get("targets", [])
        if isinstance(item, dict)
    }
    if (
        set(targets) != set(pair.TARGET_KEYS)
        or manifest.get("classified_rows") != 56
        or manifest.get("not_run_rows") != 6
        or manifest.get("independent_review") != "required"
        or manifest.get("stage_transition") != "disabled"
    ):
        errors.append("address-observer cluster manifest identity is malformed")
    frozen = manifest.get("frozen_inputs", {})
    current_frozen = (
        runner.tree_digest(runner.FROZEN_ROOT)
        if runner.FROZEN_ROOT.is_dir()
        else ""
    )
    if (
        frozen.get("file_count") != runner.EXPECTED_FROZEN_FILE_COUNT
        or frozen.get("before_sha256") != frozen.get("after_sha256")
        or frozen.get("after_sha256") != current_frozen
        or runner.tree_file_count(runner.FROZEN_ROOT)
        != runner.EXPECTED_FROZEN_FILE_COUNT
    ):
        errors.append("address-observer run did not preserve frozen inputs")
    preservation = manifest.get("preserved_target_evidence")
    if not isinstance(preservation, dict) or set(preservation) != set(
        runner.PRESERVED_ARTIFACT_IDS
    ):
        errors.append("address-observer preservation set is incomplete")
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
                    f"address-observer run did not preserve {artifact_id}"
                )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("address-observer validation cannot locate z3")
        return
    rows_list = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    rows = {
        (row["target"], row["input_order"]): row
        for row in rows_list
    }
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
            f"address-observer successor ledger expected 62 classified and 0 not-run, "
            f"got {classified} and {not_run}"
        )
    for config in pair.TARGETS:
        _validate_target(config, rows, z3, errors)
    _validate_cluster(errors)


def main() -> None:
    errors: list[str] = []
    validate(errors)
    if errors:
        print("address_observer_validation=FAIL")
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    print("address_observer_validation=PASS")
    print("target_result_counts=60_classified,2_not-run")


if __name__ == "__main__":
    main()
