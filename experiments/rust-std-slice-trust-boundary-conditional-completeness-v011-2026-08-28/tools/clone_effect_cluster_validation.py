#!/usr/bin/env python3
"""Fail-closed validation for the targets 037/043 clone-effect increment."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any

import campaign_common as common
import align_to_pair as align_pair
import clone_effect_cluster as cluster
import exact_mutable_iterator_partitions as exact_partitions
import mutable_fixed_chunk_edges as fixed_chunks
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import replay_clone_effect_cluster as replay
import run_clone_effect_cluster as runner
import target_pipeline
from checker_guards import GuardError


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
        errors.append(f"{label} path/hash/size changed")


def _capture(
    record: Any,
    argv: list[str],
    expected: str | None,
    errors: list[str],
    label: str,
    *,
    require_model: bool = False,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label} capture is missing")
        return
    paths: dict[str, Path] = {}
    for key in ("command", "stdout", "stderr", "status"):
        value = record.get(key)
        if not isinstance(value, str):
            errors.append(f"{label} {key} capture is missing")
            return
        path = common.OUT / value
        if not path.is_file():
            errors.append(f"{label} {key} file is missing")
            return
        paths[key] = path
    stdout = paths["stdout"].read_text()
    lines = stdout.splitlines()
    if (
        record.get("argv") != argv
        or paths["command"].read_text() != shlex.join(argv) + "\n"
        or record.get("exit_code") != 0
        or paths["status"].read_text() != "0\n"
        or paths["stderr"].read_text()
        or (expected is not None and (not lines or lines[0] != expected))
        or (require_model and len(lines) < 2)
    ):
        errors.append(f"{label} capture is not an exact clean replay")


def _solver_evidence(
    evidence: Any,
    path: Path,
    z3: str,
    expected: str,
    errors: list[str],
    label: str,
) -> None:
    if not isinstance(evidence, dict):
        errors.append(f"{label} evidence is missing")
        return
    _artifact(evidence.get("smt"), path, errors, f"{label} SMT")
    solver = evidence.get("solver")
    _capture(
        solver,
        [z3, "-smt2", str(path)],
        expected,
        errors,
        label,
        require_model=expected == "sat",
    )
    if isinstance(solver, dict) and (
        solver.get("solver_result") != expected
        or solver.get("expected_solver_result") != expected
        or solver.get("model_retained") is not True
    ):
        errors.append(f"{label} solver metadata changed")


def _validate_target(
    config: cluster.CloneEffectTarget,
    by_key: dict[tuple[str, str], dict[str, str]],
    z3: str,
    errors: list[str],
) -> None:
    row = by_key.get((config.target, config.input_order))
    if row is None or any(
        row[field] != value
        for field, value in runner.COMPLETE.items()
    ):
        errors.append(f"{config.target}: final ledger result is missing")

    root = runner.EVIDENCE_BASE / config.artifact_id
    result_path = root / "result.json"
    result = _load_json(result_path, errors, f"{config.target} result")
    if (
        result.get("target") != config.target
        or result.get("input_order") != config.input_order
        or result.get("artifact_id") != config.artifact_id
        or result.get("active_contract_sha256")
        != config.active_contract_sha256
        or result.get("active_contract_text") != config.active_contract_text
        or result.get("classification") != runner.COMPLETE
        or result.get("updated_crosswalk_fields")
        != list(target_pipeline.RESULT_FIELDS)
        or result.get("independent_review") != "required"
        or result.get("stage_transition") != "disabled"
    ):
        errors.append(f"{config.target}: result identity/classification changed")

    for key, filename in (
        ("authority_bindings", "authority_bindings.json"),
        ("trust_site_bindings", "trust_site_bindings.json"),
        ("boundary_manifest", "boundary_manifest.json"),
        ("reviewed_model_guards", "reviewed_model_guards.json"),
    ):
        _artifact(
            result.get(key),
            root / filename,
            errors,
            f"{config.target} {key}",
        )
    bound_manifest = root / "bound_inputs/manifest.json"
    _artifact(
        result.get("bound_inputs"),
        bound_manifest,
        errors,
        f"{config.target} bound inputs",
    )
    boundary = _load_json(
        root / "boundary_manifest.json",
        errors,
        f"{config.target} boundary manifest",
    )
    if boundary != cluster.boundary_manifest(config):
        errors.append(f"{config.target}: boundary manifest changed")
    guards = _load_json(
        root / "reviewed_model_guards.json",
        errors,
        f"{config.target} reviewed guards",
    )
    if len(guards.get("fail_closed_mutations", [])) != 10:
        errors.append(f"{config.target}: fail-closed guard set is incomplete")

    obligations = result.get("obligations")
    if not isinstance(obligations, dict):
        errors.append(f"{config.target}: theorem evidence is missing")
        obligations = {}
    for purpose, stem in replay.OBLIGATIONS.items():
        text, metadata = cluster.obligation(config, purpose)
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        if not smt_path.is_file() or smt_path.read_text() != text:
            errors.append(f"{config.target} {purpose}: SMT changed")
        observed_metadata = _load_json(
            metadata_path,
            errors,
            f"{config.target} {purpose} metadata",
        )
        if observed_metadata != metadata:
            errors.append(f"{config.target} {purpose}: metadata changed")
        else:
            try:
                cluster.validate_target_obligation(
                    config,
                    smt_path.read_text(),
                    observed_metadata,
                )
            except (GuardError, OSError, ValueError) as exc:
                errors.append(
                    f"{config.target} {purpose}: checker rejected SMT: {exc}"
                )
        evidence = obligations.get(purpose, {})
        _solver_evidence(
            evidence,
            smt_path,
            z3,
            "unsat",
            errors,
            f"{config.target} {purpose}",
        )
        if isinstance(evidence, dict):
            _artifact(
                evidence.get("metadata"),
                metadata_path,
                errors,
                f"{config.target} {purpose} metadata",
            )

    panic_path = root / "panic_prefix_obligation.smt2"
    if (
        not panic_path.is_file()
        or panic_path.read_text() != cluster.panic_obligation_text(config)
    ):
        errors.append(f"{config.target}: panic-prefix theorem changed")
    else:
        try:
            cluster.validate_panic_obligation(config, panic_path.read_text())
        except GuardError as exc:
            errors.append(f"{config.target}: panic-prefix theorem rejected: {exc}")
    _solver_evidence(
        result.get("panic_prefix_obligation"),
        panic_path,
        z3,
        "unsat",
        errors,
        f"{config.target} panic-prefix theorem",
    )

    if config.is_fill:
        if result.get("length_mismatch_obligation") is not None:
            errors.append("fill unexpectedly has a length-mismatch obligation")
    else:
        mismatch_path = root / "length_mismatch_obligation.smt2"
        if (
            not mismatch_path.is_file()
            or mismatch_path.read_text()
            != cluster.mismatch_obligation_text(config)
        ):
            errors.append("clone_from_slice mismatch theorem changed")
        _solver_evidence(
            result.get("length_mismatch_obligation"),
            mismatch_path,
            z3,
            "unsat",
            errors,
            "clone_from_slice mismatch theorem",
        )

    source_evidence = result.get("source_instances")
    if not isinstance(source_evidence, dict):
        source_evidence = {}
    expected_cases = {
        case.name: case for case in cluster.SOURCE_CASES[config.artifact_id]
    }
    if set(source_evidence) != set(expected_cases):
        errors.append(f"{config.target}: source instance set changed")
    for name, case in expected_cases.items():
        path = root / "source_instances" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != cluster.source_instance_text(config, case)
        ):
            errors.append(f"{config.target} {name}: source SMT changed")
        evidence = source_evidence.get(name)
        if (
            not isinstance(evidence, dict)
            or evidence.get("expected_intrinsic_call_count")
            != cluster.expected_intrinsic_call_count(config, case)
        ):
            errors.append(
                f"{config.target} {name}: intrinsic-call expectation changed"
            )
        _solver_evidence(
            evidence,
            path,
            z3,
            "sat",
            errors,
            f"{config.target} source {name}",
        )

    negative_evidence = result.get("negative_probes")
    if not isinstance(negative_evidence, dict):
        negative_evidence = {}
    expected_negative = set(cluster.negative_probe_names(config))
    if set(negative_evidence) != expected_negative:
        errors.append(f"{config.target}: negative probe set changed")
    for name in expected_negative:
        path = root / "negative_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != cluster.negative_probe_text(config, name)
        ):
            errors.append(f"{config.target} {name}: negative probe changed")
        _solver_evidence(
            negative_evidence.get(name),
            path,
            z3,
            "unsat",
            errors,
            f"{config.target} negative {name}",
        )

    panic_evidence = result.get("panic_probes")
    if not isinstance(panic_evidence, dict):
        panic_evidence = {}
    if set(panic_evidence) != {f"panic_at_{index}" for index in range(3)}:
        errors.append(f"{config.target}: bounded panic set changed")
    for index in range(3):
        name = f"panic_at_{index}"
        path = root / "panic_probes" / f"{name}.smt2"
        if (
            not path.is_file()
            or path.read_text() != cluster.panic_probe_text(config, index)
        ):
            errors.append(f"{config.target} {name}: panic witness changed")
        _solver_evidence(
            panic_evidence.get(name),
            path,
            z3,
            "sat",
            errors,
            f"{config.target} {name}",
        )

    mismatch_evidence = result.get("mismatch_probes")
    expected_mismatch = set() if config.is_fill else {"default", "trivial"}
    if (
        not isinstance(mismatch_evidence, dict)
        or set(mismatch_evidence) != expected_mismatch
    ):
        errors.append(f"{config.target}: mismatch witness set changed")
        mismatch_evidence = {}
    if not config.is_fill:
        for trivial in (False, True):
            name = "trivial" if trivial else "default"
            path = root / "mismatch_probes" / f"{name}.smt2"
            if (
                not path.is_file()
                or path.read_text()
                != cluster.mismatch_probe_text(config, trivial=trivial)
            ):
                errors.append(f"clone_from_slice {name} mismatch witness changed")
            _solver_evidence(
                mismatch_evidence.get(name),
                path,
                z3,
                "sat",
                errors,
                f"clone_from_slice {name} mismatch",
            )

    expected_replay_argv = [
        sys.executable,
        str(common.OUT / "tools/replay_clone_effect_cluster.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
        "--artifact-id",
        config.artifact_id,
    ]
    try:
        independent = replay.replay(root, z3, config)
    except (GuardError, OSError, TypeError, ValueError) as exc:
        errors.append(f"{config.target}: independent replay failed: {exc}")
        independent = None
    replay_record = result.get("solver_replay")
    _capture(
        replay_record,
        expected_replay_argv,
        None,
        errors,
        f"{config.target} independent replay",
    )
    if isinstance(replay_record, dict):
        try:
            captured = json.loads(
                (common.OUT / replay_record["stdout"]).read_text()
            )
        except (KeyError, OSError, json.JSONDecodeError):
            captured = None
        if (
            independent is None
            or captured != independent
            or replay_record.get("result") != independent
        ):
            errors.append(f"{config.target}: independent replay result changed")

    proof_path = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    captured_proof = root / "verus/source_model.rs"
    expected_proof = cluster.verus_text(config)
    if (
        not proof_path.is_file()
        or not captured_proof.is_file()
        or proof_path.read_text() != expected_proof
        or captured_proof.read_text() != expected_proof
        or "external_body" in expected_proof
    ):
        errors.append(f"{config.target}: trusted-free Verus model changed")
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append(f"{config.target}: Verus evidence is missing")
        verus = {}
    _artifact(
        verus.get("source_model"),
        proof_path,
        errors,
        f"{config.target} source Verus model",
    )
    _artifact(
        verus.get("captured_model"),
        captured_proof,
        errors,
        f"{config.target} captured Verus model",
    )
    _capture(
        verus.get("typecheck"),
        [
            str(common.VERUS),
            str(captured_proof),
            "--crate-type=lib",
            "--no-verify",
        ],
        None,
        errors,
        f"{config.target} Verus typecheck",
    )
    verification = verus.get("verification")
    _capture(
        verification,
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
        None,
        errors,
        f"{config.target} Verus verification",
    )
    try:
        stdout = (common.OUT / verification["stdout"]).read_text()
    except (KeyError, OSError, TypeError):
        stdout = ""
    if "0 errors" not in stdout:
        errors.append(f"{config.target}: Verus verification summary changed")


def validate(errors: list[str]) -> None:
    z3 = shutil.which("z3")
    if not z3:
        errors.append("clone-effect validation cannot locate z3")
        return
    rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    by_key = {(row["target"], row["input_order"]): row for row in rows}
    for config in cluster.TARGETS:
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
        | set(cluster.TARGET_KEYS)
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
    if (
        classified != expected
        or len(classified) != 62
        or len(rows) - len(classified) != 0
    ):
        errors.append("clone-effect downstream ledger did not finish at 62/0")

    manifest = _load_json(
        runner.CLUSTER_ROOT / "manifest.json",
        errors,
        "clone-effect cluster manifest",
    )
    if (
        manifest.get("execution_order")
        != [config.target for config in cluster.TARGETS]
        or manifest.get("classified_rows") != 40
        or manifest.get("not_run_rows") != 22
        or manifest.get("stage_transition") != "disabled"
        or manifest.get("independent_review") != "required"
        or set(manifest.get("preserved_certified_evidence", {}))
        != set(runner.PRESERVED_ARTIFACT_IDS)
    ):
        errors.append("clone-effect cluster manifest is malformed")
    for artifact_id, record in manifest.get(
        "preserved_certified_evidence", {}
    ).items():
        root = common.OUT / "evidence/targets" / artifact_id
        digest = runner.tree_digest(root) if root.is_dir() else ""
        if (
            record.get("before_sha256") != digest
            or record.get("after_sha256") != digest
        ):
            errors.append(f"clone-effect run did not preserve {artifact_id}")
    frozen = manifest.get("preserved_frozen_inputs", {}).get("root", {})
    current_frozen = (
        runner.tree_digest(runner.FROZEN_ROOT)
        if runner.FROZEN_ROOT.is_dir()
        else ""
    )
    if (
        frozen.get("before_sha256") != current_frozen
        or frozen.get("after_sha256") != current_frozen
    ):
        errors.append("clone-effect run changed frozen inputs")
