#!/usr/bin/env python3
"""Validate raw-slice pair evidence and the delivered result ledger."""

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
import raw_slice_pair as raw
import replay_raw_slice_pair as replay
import run_raw_slice_pair as runner
import slice_index_trio as slice_trio
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
            "(y_return_memory y1)",
            "(s_final_memory s1)",
            "(Equivalent_T x b y1 s1 y2 s2)",
            "false",
        )
        if witness
        else (
            "(y_return_address y1)",
            "(s_final_memory s1)",
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
    config: raw.RawSliceTarget,
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
        "raw_slice_vocabulary.rs",
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
    vocabulary_path = root / "bound_inputs/raw_slice_vocabulary.rs"
    vocabulary_record = manifest.get("files", {}).get(
        "raw_slice_vocabulary.rs", {}
    )
    canonical_vocabulary = Path(row["shared_vocabulary_path"])
    expected_vocabulary = "\n".join(
        _source_excerpt(canonical_vocabulary, start, end)
        for start, end in raw.VOCABULARY_RANGES
    )
    if (
        not vocabulary_path.is_file()
        or vocabulary_path.read_text() != expected_vocabulary
        or vocabulary_record.get("canonical_file_sha256")
        != row["shared_vocabulary_sha256"]
        or vocabulary_record.get("source_ranges")
        != [f"{start}-{end}" for start, end in raw.VOCABULARY_RANGES]
    ):
        errors.append(f"{config.target} vocabulary binding changed")
    try:
        raw.validate_source_anchors(
            config,
            (root / "bound_inputs/source_item.rs").read_text(),
            (root / "bound_inputs/public_docs.md").read_text(),
            vocabulary_path.read_text(),
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
    config: raw.RawSliceTarget,
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
        or result.get("classification") != config.expected_classification
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
    trust = _load_json(
        trust_path,
        errors,
        f"{config.target} trust bindings",
    )
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
        errors.append(f"{config.target} trust bindings changed")
    for record_id, expected_hash in config.trust_hashes.items():
        if (
            record_id not in by_id
            or raw.canonical_json_sha256(by_id[record_id]) != expected_hash
        ):
            errors.append(f"{record_id} readable trust record changed")
    if any(
        by_id.get(site, {}).get("semantic_disposition", "").startswith(
            "admissible"
        )
        for site in config.excluded_trust_site_ids
    ):
        errors.append(f"{config.target} answer-bearing trust site was relabeled")
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
    ) != raw.boundary_manifest(config):
        errors.append(f"{config.target} boundary manifest changed")
    _artifact(
        result.get("boundary_manifest"),
        boundary_path,
        errors,
        f"{config.target} boundary manifest",
    )
    if row:
        _validate_bound_inputs(config, row, result, root, errors)

    clause_path = root / "active_contract_clause_audit.json"
    clause = _load_json(clause_path, errors, f"{config.target} clause audit")
    if (
        clause.get("active_has_final_return_relation") is not False
        or clause.get("retained_external_body_admitted") is not False
        or clause.get("answer_bearing_sites_replaced_not_relabeled")
        != list(config.excluded_trust_site_ids)
        or clause.get("mutable_final_frame_invented") is not False
    ):
        errors.append(f"{config.target} active-contract clause audit changed")
    _artifact(
        result.get("active_contract_clause_audit"),
        clause_path,
        errors,
        f"{config.target} clause audit",
    )

    obligations = result.get("obligations", {})
    if set(obligations) != set(raw.PURPOSES):
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
            raw.validate_target_obligation(
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
        expected = config.expected_results[purpose]
        _capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            expected,
            errors,
            f"{config.target} {purpose} solver",
        )

    source_instances = result.get("source_instances", {})
    if set(source_instances) != set(raw.source_cases(config)):
        errors.append(f"{config.target} source-instance set is incomplete")
    for name in raw.source_cases(config):
        path = root / f"source_instance_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != raw.source_instance_text(config, name)
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
    if set(probes) != set(raw.NEGATIVE_PROBES):
        errors.append(f"{config.target} negative-probe set is incomplete")
    for name in raw.NEGATIVE_PROBES:
        path = root / f"negative_probe_{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != raw.negative_probe_text(config, name)
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

    witness = result.get("fixed_full_state_witness")
    if config.mutable:
        witness_smt = root / "fixed_full_state_witness.smt2"
        witness_json = root / "fixed_full_state_witness.json"
        if (
            not witness_smt.is_file()
            or witness_smt.read_text() != raw.fixed_witness_text(config)
            or _load_json(
                witness_json,
                errors,
                f"{config.target} witness payload",
            )
            != raw.witness_payload(config)
        ):
            errors.append(f"{config.target} fixed witness changed")
        if not isinstance(witness, dict):
            errors.append(f"{config.target} fixed witness record is missing")
            witness = {}
        _artifact(
            witness.get("smt"),
            witness_smt,
            errors,
            f"{config.target} fixed witness SMT",
        )
        _artifact(
            witness.get("payload"),
            witness_json,
            errors,
            f"{config.target} fixed witness payload",
        )
        _capture(
            witness.get("solver"),
            [z3, "-smt2", str(witness_smt)],
            "sat",
            errors,
            f"{config.target} fixed witness solver",
            require_model=True,
            witness=True,
        )
        if (
            witness.get("fixed_input") is not True
            or witness.get("fixed_boundary") is not True
            or witness.get("both_specs_satisfied") is not True
        ):
            errors.append(f"{config.target} fixed witness lacks active-conjunct proof")
    elif witness is not None:
        errors.append(f"{config.target} unexpectedly has an incompleteness witness")

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
            str(common.OUT / "tools/replay_raw_slice_pair.py"),
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
    captured = root / "verus/raw_slice_model.rs"
    expected_proof = raw.verus_text(config)
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
    if raw.VERUS_EXPECTED_SUMMARY not in verification_stdout:
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
        errors.append("raw-slice validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in raw.TARGETS:
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
        | set(raw.TARGET_KEYS)
        | set(slice_trio.TARGET_KEYS)
        | set(address_observer_pair.TARGET_KEYS)
        | set(mutable_views.TARGET_KEYS)
        | set(align_pair.TARGET_KEYS)
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    if classified != expected or len(classified) != 62 or not_run != 0:
        errors.append("raw-slice successor 62/0 result ledger is not preserved")

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "raw-slice cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in raw.TARGETS]
        or manifest.get("classified_rows") != 51
        or manifest.get("not_run_rows") != 11
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("raw-slice cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"raw-slice run did not preserve {artifact_id}")
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
        errors.append("raw-slice run did not preserve frozen inputs")


def main() -> None:
    errors: list[str] = []
    validate(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("raw_slice_pair_validation=PASS")
    print("classified=51 not_run=11")


if __name__ == "__main__":
    main()
