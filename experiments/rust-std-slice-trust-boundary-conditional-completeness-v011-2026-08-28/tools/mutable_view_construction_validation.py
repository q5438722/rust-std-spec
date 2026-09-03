#!/usr/bin/env python3
"""Validate mutable-view construction evidence and the delivered ledger."""

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
import mutable_view_construction_cluster as cluster
import replay_mutable_view_construction_cluster as replay
import run_mutable_view_construction_cluster as runner
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
    model_markers = (
        (
            "(s_return_final s1)",
            "(s_return_final s2)",
            "(s_input_final s1)",
            "(s_input_final s2)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else ("(y_length y1)", "(s_input_final s1)")
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
                or any(marker not in output for marker in model_markers)
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
    config: cluster.MutableViewTarget,
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
        "mutable_view_vocabulary.rs",
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
        or set(manifest.get("canonical_helpers", {}))
        != set(config.helper_names)
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

    vocabulary_path = root / "bound_inputs/mutable_view_vocabulary.rs"
    canonical_vocabulary = Path(row["shared_vocabulary_path"])
    expected_vocabulary = "\n".join(
        _source_excerpt(canonical_vocabulary, start, end)
        for start, end in cluster.VOCABULARY_RANGES
    )
    vocabulary_record = manifest.get("files", {}).get(
        "mutable_view_vocabulary.rs", {}
    )
    if (
        not vocabulary_path.is_file()
        or vocabulary_path.read_text() != expected_vocabulary
        or vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
        or vocabulary_record.get("source_ranges")
        != [
            f"{start}-{end}"
            for start, end in cluster.VOCABULARY_RANGES
        ]
    ):
        errors.append(f"{config.target} vocabulary binding changed")

    helper_texts: dict[str, str] = {}
    for source in config.helper_sources:
        canonical = common.RUST_LIBRARY / source.path
        copied = root / "bound_inputs" / source.filename
        record = manifest.get("canonical_helpers", {}).get(source.name, {})
        _artifact(
            record,
            copied,
            errors,
            f"{config.target} canonical helper {source.name}",
        )
        expected = _source_excerpt(canonical, source.start, source.end)
        if (
            not canonical.is_file()
            or common.sha256(canonical) != source.file_sha256
            or not copied.is_file()
            or copied.read_text() != expected
            or record.get("canonical_file_sha256") != source.file_sha256
            or record.get("source_lines") != source.reference
        ):
            errors.append(f"{config.target} canonical helper changed")
        if copied.is_file():
            helper_texts[source.name] = copied.read_text()
    try:
        cluster.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            (root / "bound_inputs/public_docs.md").read_text(),
            vocabulary_path.read_text(),
            helper_texts,
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
    config: cluster.MutableViewTarget,
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
        or result.get("remaining_not_run_rows") != 2
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
    trust = _load_json(
        trust_path, errors, f"{config.target} trust bindings"
    )
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
                cluster.canonical_json_sha256(records[record_id])
                != expected_hash
            ):
                errors.append(f"{record_id} trust binding changed")
        for record_id in config.excluded_trust_site_ids:
            if not records[record_id]["semantic_disposition"].startswith(
                "inadmissible"
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
    ) != cluster.boundary_manifest(config):
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
        errors.append(f"{config.target} contract translation is malformed")
    _artifact(
        result.get("contract_translation_audit"),
        translation_path,
        errors,
        f"{config.target} contract translation",
    )

    obligations = result.get("obligations", {})
    if set(obligations) != set(cluster.PURPOSES):
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
            cluster.validate_target_obligation(
                config, smt_path.read_text(), metadata
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
            config.expected_solver_results[purpose],
            errors,
            f"{config.target} {purpose} solver",
        )

    witness_smt = root / "fixed_full_state_witness.smt2"
    witness_json = root / "fixed_full_state_witness.json"
    witness_payload = _load_json(
        witness_json,
        errors,
        f"{config.target} fixed full-state witness payload",
    )
    if (
        not witness_smt.is_file()
        or witness_smt.read_text()
        != cluster.fixed_full_state_witness_text(config)
        or witness_payload != cluster.witness_payload(config)
    ):
        errors.append(f"{config.target} fixed full-state witness changed")
    witness = result.get("fixed_full_state_witness", {})
    _artifact(
        witness.get("smt"),
        witness_smt,
        errors,
        f"{config.target} fixed full-state witness SMT",
    )
    _artifact(
        witness.get("payload"),
        witness_json,
        errors,
        f"{config.target} fixed full-state witness payload",
    )
    _capture(
        witness.get("solver"),
        [z3, "-smt2", str(witness_smt)],
        "sat",
        errors,
        f"{config.target} fixed full-state witness solver",
        require_model=True,
        witness=True,
    )
    if (
        witness.get("fixed_input") is not True
        or witness.get("fixed_boundary") is not True
        or witness.get("both_specs_satisfied") is not True
    ):
        errors.append(
            f"{config.target} fixed witness lacks active-conjunct proof"
        )

    source_instances = result.get("source_instances", {})
    if set(source_instances) != set(cluster.source_cases(config)):
        errors.append(f"{config.target} source-instance set is incomplete")
    for name, case in cluster.source_cases(config).items():
        path = root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != cluster.source_instance_text(config, name)
        ):
            errors.append(f"{config.target} {name} source instance changed")
        evidence = source_instances.get(name, {})
        if (
            evidence.get("expected_source_outcome")
            != json.loads(
                json.dumps(cluster.evaluate_source(config, case))
            )
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
    if set(negative_probes) != set(cluster.negative_probe_names(config)):
        errors.append(f"{config.target} negative-probe set is incomplete")
    for name in cluster.negative_probe_names(config):
        path = root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text()
            != cluster.negative_probe_text(config, name)
        ):
            errors.append(f"{config.target} {name} negative probe changed")
        evidence = negative_probes.get(name, {})
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
            str(
                common.OUT
                / "tools/replay_mutable_view_construction_cluster.py"
            ),
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
    expected_proof = cluster.verus_text(config)
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
            if cluster.VERUS_EXPECTED_SUMMARY not in output:
                errors.append(
                    f"{config.target} Verus verification summary changed"
                )

    guards_path = root / "reviewed_model_guards.json"
    guards = _load_json(guards_path, errors, f"{config.target} guards")
    if len(guards.get("fail_closed_mutations", [])) != 17:
        errors.append(f"{config.target} reviewed guard set is incomplete")
    _artifact(
        result.get("reviewed_model_guards"),
        guards_path,
        errors,
        f"{config.target} reviewed model guards",
    )


def _validate_cluster(errors: list[str]) -> None:
    path = runner.CLUSTER_ROOT / "manifest.json"
    manifest = _load_json(path, errors, "mutable-view cluster manifest")
    targets = {
        (item.get("target"), item.get("input_order")): item
        for item in manifest.get("targets", [])
        if isinstance(item, dict)
    }
    if (
        set(targets) != set(cluster.TARGET_KEYS)
        or manifest.get("classified_rows") != 60
        or manifest.get("not_run_rows") != 2
        or manifest.get("independent_review") != "required"
        or manifest.get("stage_transition") != "disabled"
    ):
        errors.append("mutable-view cluster manifest identity is malformed")

    excerpt = (
        runner.CLUSTER_ROOT
        / "source_excerpts/core_array_from_mut_174_177.rs"
    )
    excerpt_record = manifest.get("project_local_array_from_mut_excerpt")
    _artifact(
        excerpt_record,
        excerpt,
        errors,
        "project-local core::array::from_mut excerpt",
    )
    if (
        not excerpt.is_file()
        or common.sha256(excerpt) != cluster.ARRAY_FROM_MUT_EXCERPT_SHA256
        or not isinstance(excerpt_record, dict)
        or excerpt_record.get("canonical_file_sha256")
        != cluster.ARRAY_SOURCE_SHA256
        or excerpt_record.get("source_lines")
        != "core/src/array/mod.rs:174-177"
    ):
        errors.append("project-local core::array::from_mut binding changed")

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
        errors.append("mutable-view run did not preserve frozen inputs")
    preservation = manifest.get("preserved_target_evidence")
    if not isinstance(preservation, dict) or set(preservation) != set(
        runner.PRESERVED_ARTIFACT_IDS
    ):
        errors.append("mutable-view preservation set is incomplete")
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
                    f"mutable-view run did not preserve {artifact_id}"
                )


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("mutable-view validation cannot locate z3")
        return
    rows_list = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    rows = {
        (row["target"], row["input_order"]): row for row in rows_list
    }
    classified = {
        key
        for key, row in rows.items()
        if any(
            row[field] != "not-run"
            for field in target_pipeline.RESULT_FIELDS
        )
    }
    expected = (
        set(runner.BASELINE_RESULTS)
        | set(cluster.TARGET_KEYS)
        | set(align_pair.TARGET_KEYS)
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows_list
    )
    if classified != expected or len(classified) != 62 or not_run != 0:
        errors.append(
            "mutable-view ledger expected exactly 62 classified and 0 not-run"
        )
    for config in cluster.TARGETS:
        _validate_target(config, rows, z3, errors)
    _validate_cluster(errors)


def main() -> None:
    errors: list[str] = []
    validate(errors)
    if errors:
        print("mutable_view_construction_validation=FAIL")
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    print("mutable_view_construction_validation=PASS")
    print("target_result_counts=60_classified,2_not-run")


if __name__ == "__main__":
    main()
