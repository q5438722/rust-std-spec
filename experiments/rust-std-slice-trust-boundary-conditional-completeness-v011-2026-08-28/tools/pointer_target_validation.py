#!/usr/bin/env python3
"""Independent artifact validation for the slice pointer target cluster."""

from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import campaign_common as common
from checker_guards import GuardError
import pointer_target_pipeline


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _check_artifact(
    errors: list[str],
    descriptor: Any,
    path: Path,
    label: str,
) -> None:
    if not isinstance(descriptor, dict) or not path.is_file():
        errors.append(f"{label}: missing artifact or descriptor")
        return
    if (
        descriptor.get("path") != common.relpath(path)
        or descriptor.get("sha256") != common.sha256(path)
        or descriptor.get("bytes") != path.stat().st_size
    ):
        errors.append(f"{label}: artifact path/hash/size mismatch")


def _check_solver_capture(
    errors: list[str],
    record: Any,
    expected_argv: list[str],
    expected_result: str,
    label: str,
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label}: missing command capture")
        return
    paths: dict[str, Path] = {}
    for key in ("command", "stdout", "stderr", "status"):
        value = record.get(key)
        if not isinstance(value, str):
            errors.append(f"{label}: missing {key} capture path")
            return
        paths[key] = common.OUT / value
        if not paths[key].is_file():
            errors.append(f"{label}: missing {key} capture")
            return
    stdout = paths["stdout"].read_text()
    stdout_lines = stdout.splitlines()
    actual = stdout_lines[0] if stdout_lines else ""
    if (
        record.get("argv") != expected_argv
        or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
        or record.get("exit_code") != 0
        or paths["status"].read_text() != "0\n"
        or paths["stderr"].read_text() != ""
        or actual != expected_result
        or record.get("solver_result") != expected_result
        or record.get("expected_solver_result") != expected_result
        or (expected_result == "unsat" and stdout != "unsat\n")
        or (expected_result == "sat" and len(stdout_lines) < 2)
    ):
        errors.append(f"{label}: solver capture is not an exact clean replay")


def _authority_fields() -> tuple[str, ...]:
    return (
        "target",
        "input_order",
        "active_run_id",
        "active_contract_text",
        "active_contract_sha256",
        "retained_contract_text",
        "retained_contract_sha256",
        "generated_declaration_path",
        "generated_declaration_text",
        "generated_declaration_sha256",
        "source_path",
        "source_item_text",
        "source_item_sha256",
        "public_docs_reference",
        "public_docs_text",
        "public_docs_sha256",
        "frozen_harness_path",
        "harness_sha256",
        "frozen_transformation_manifest_path",
        "transformation_manifest_sha256",
        "frozen_dependency_manifest_path",
        "dependency_manifest_sha256",
        "frozen_source_body_manifest_path",
        "source_body_manifest_sha256",
        "all_trust_site_ids",
        "inadmissible_trust_site_ids",
    )


def _check_source_dependency(
    errors: list[str],
    module: ModuleType,
    descriptor: Any,
    label: str,
) -> None:
    dependency = module.CONFIG.source_dependency
    if dependency is None:
        if descriptor is not None:
            errors.append(f"{label}: unexpected source dependency")
        return
    trust_site_id, target, artifact_id = dependency
    result_path = common.OUT / "evidence/targets" / artifact_id / "result.json"
    source_model = common.OUT / "proofs/019_core_slice_as_mut_ptr.rs"
    obligation = (
        common.OUT
        / "evidence/targets"
        / artifact_id
        / "obligation.smt2"
    )
    expected = {
        "trust_site_id": trust_site_id,
        "target": target,
        "artifact_id": artifact_id,
        "admission_mode": "source-backed transition only; no target output in Boundary_T",
        "result": (
            {
                "path": common.relpath(result_path),
                "sha256": common.sha256(result_path),
                "bytes": result_path.stat().st_size,
            }
            if result_path.is_file()
            else None
        ),
        "source_model": (
            {
                "path": common.relpath(source_model),
                "sha256": common.sha256(source_model),
                "bytes": source_model.stat().st_size,
            }
            if source_model.is_file()
            else None
        ),
        "full_exact_obligation": (
            {
                "path": common.relpath(obligation),
                "sha256": common.sha256(obligation),
                "bytes": obligation.stat().st_size,
            }
            if obligation.is_file()
            else None
        ),
    }
    if descriptor != expected or None in (
        expected["result"],
        expected["source_model"],
        expected["full_exact_obligation"],
    ):
        errors.append(f"{label}: target-019 source dependency is stale or incomplete")
        return
    try:
        dependency_result = _load_json(result_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: target-019 result is unreadable: {exc}")
        return
    if (
        dependency_result.get("target") != target
        or dependency_result.get("classification")
        != pointer_target_pipeline.COMPLETE
    ):
        errors.append(f"{label}: target-019 dependency is not conditional-complete")


def validate(
    errors: list[str],
    module: ModuleType,
    replay_module: ModuleType,
    run_module: ModuleType,
    *,
    source_model: Path,
    expected_not_run: int,
) -> None:
    label = module.CONFIG.label
    root = common.OUT / "evidence/targets" / module.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append(f"{label}: result evidence is missing")
        return
    try:
        result = _load_json(result_path)
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: result evidence is invalid JSON: {exc}")
        return

    if (
        result.get("target") != module.TARGET
        or result.get("input_order") != module.INPUT_ORDER
        or result.get("active_contract_sha256")
        != module.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != module.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != pointer_target_pipeline.COMPLETE
        or result.get("updated_crosswalk_fields")
        != sorted(pointer_target_pipeline.COMPLETE)
        or result.get("remaining_not_run") != expected_not_run
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(module.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append(f"{label}: result identity/classification is malformed")

    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    matches = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append(f"{label}: crosswalk row is absent or duplicated")
        return
    row = matches[0]
    if any(row[field] != value for field, value in pointer_target_pipeline.COMPLETE.items()):
        errors.append(f"{label}: crosswalk classification is not conditional-complete")

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    bound_inputs_path = root / "bound_inputs_manifest.json"
    _check_artifact(
        errors, result.get("authority_bindings"), authority_path, f"{label} authority"
    )
    _check_artifact(
        errors, result.get("boundary_manifest"), boundary_path, f"{label} boundary"
    )
    _check_artifact(
        errors, result.get("bound_inputs"), bound_inputs_path, f"{label} inputs"
    )

    if authority_path.is_file():
        try:
            authority = _load_json(authority_path)
            expected = {field: row[field] for field in _authority_fields()}
            if (
                authority != {"schema_version": 1, "bindings": expected}
                or expected["active_contract_sha256"]
                != module.ACTIVE_CONTRACT_SHA256
                or expected["retained_contract_sha256"]
                != module.ACTIVE_CONTRACT_SHA256
                or set(expected["all_trust_site_ids"].split(";"))
                != set(module.ALL_AUDITED_TRUST_SITES)
            ):
                errors.append(f"{label}: authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: authority bindings are invalid JSON: {exc}")

    if boundary_path.is_file():
        try:
            boundary = _load_json(boundary_path)
            if boundary != module.boundary_manifest():
                errors.append(f"{label}: boundary manifest differs from policy")
            if set(boundary.get("admitted_boundary_trust_site_ids", [])) & set(
                module.EXCLUDED_RETAINED_TRUST_SITES
            ):
                errors.append(f"{label}: excluded retained site was relabeled")
            shared = json.dumps(
                boundary.get("shared_boundary_observations", []),
                sort_keys=True,
            )
            for forbidden in (
                "returned pointer",
                "returned endpoint",
                "aggregate final state",
                "execution trace",
            ):
                if forbidden in shared:
                    errors.append(f"{label}: boundary contains {forbidden}")
            dependency = boundary.get("source_backed_target_dependency")
            if module.CONFIG.source_dependency is None:
                if dependency is not None:
                    errors.append(f"{label}: unexpected boundary dependency")
            elif (
                not isinstance(dependency, dict)
                or dependency.get("trust_site_id") != "TS-020-D002"
                or dependency.get("target") != "core::slice::as_mut_ptr"
                or "no returned pointer" not in dependency.get("admission", "")
            ):
                errors.append(
                    f"{label}: TS-020-D002 is not limited to target-019 semantics"
                )
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: boundary manifest is invalid JSON: {exc}")

    if bound_inputs_path.is_file():
        try:
            manifest = _load_json(bound_inputs_path)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: bound-input manifest is invalid JSON: {exc}")
            manifest = {}
        canonical = {
            binding.name: {
                "source_path": binding.path,
                "source_span": f"{binding.start}-{binding.end}",
                "source_file_sha256": binding.file_sha256,
                "excerpt_sha256": binding.excerpt_sha256,
                "artifact": binding.filename,
            }
            for binding in module.CANONICAL_SOURCE_BINDINGS
        }
        if (
            manifest.get("schema_version") != 1
            or manifest.get("canonical_sources") != canonical
        ):
            errors.append(f"{label}: canonical source bindings are malformed")
        expected_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            module.CONFIG.source_item_filename: row["source_item_sha256"],
            module.CONFIG.source_docs_filename: row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row["transformation_manifest_sha256"],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            **{
                binding.filename: binding.excerpt_sha256
                for binding in module.CANONICAL_SOURCE_BINDINGS
            },
        }
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != set(expected_hashes):
            errors.append(f"{label}: bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_hashes.items():
            path = root / "bound_inputs" / filename
            _check_artifact(
                errors,
                artifacts.get(filename),
                path,
                f"{label} bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"{label}: bound input hash changed: {filename}")
        for binding in module.CANONICAL_SOURCE_BINDINGS:
            source = common.RUST_LIBRARY / binding.path
            frozen = root / "bound_inputs" / binding.filename
            if not source.is_file() or common.sha256(source) != binding.file_sha256:
                errors.append(f"{label}: canonical source changed: {binding.path}")
                continue
            expected_bytes = "".join(
                source.read_text().splitlines(keepends=True)[
                    binding.start - 1 : binding.end
                ]
            ).encode()
            if not frozen.is_file() or frozen.read_bytes() != expected_bytes:
                errors.append(f"{label}: canonical source excerpt differs: {binding.name}")
        _check_source_dependency(
            errors,
            module,
            manifest.get("source_dependency"),
            f"{label} bound inputs",
        )

    z3 = shutil.which("z3")
    if not z3:
        errors.append(f"{label}: validation cannot locate z3")
        return
    obligations = result.get("obligations")
    obligation_specs = {
        module.PRIMARY: "obligation",
        module.EXACT_OUTPUT: "exact_output_obligation",
    }
    if not isinstance(obligations, dict) or set(obligations) != set(obligation_specs):
        errors.append(f"{label}: obligation result set is incomplete")
        obligations = {}
    for purpose, stem in obligation_specs.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"{label} {purpose}: obligation files are missing")
            continue
        try:
            metadata = _load_json(metadata_path)
            module.validate_target_obligation(smt_path.read_text(), metadata)
            scope = metadata.get("boundary_scope", {})
            admitted = set(scope.get("admitted_trust_site_ids", []))
            excluded = set(scope.get("excluded_retained_trust_site_ids", []))
            context_only = set(scope.get("context_only_trust_site_ids", []))
            audited = set(scope.get("all_audited_trust_site_ids", []))
            authority_sites = {
                site for site in row["all_trust_site_ids"].split(";") if site
            }
            inadmissible_sites = {
                site
                for site in row["inadmissible_trust_site_ids"].split(";")
                if site
            }
            if (
                audited != authority_sites
                or admitted | excluded | context_only != audited
                or admitted & excluded
                or admitted & context_only
                or excluded & context_only
                or admitted & inadmissible_sites
                or not inadmissible_sites <= excluded
            ):
                errors.append(
                    f"{label} {purpose}: boundary backing is not authority-bound"
                )
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{label} {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        _check_artifact(
            errors, evidence.get("smt"), smt_path, f"{label} {purpose} SMT"
        )
        _check_artifact(
            errors,
            evidence.get("metadata"),
            metadata_path,
            f"{label} {purpose} metadata",
        )
        _check_solver_capture(
            errors,
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "unsat",
            f"{label} {purpose}",
        )

    probes = result.get("satisfiability_and_rejection_probes")
    if not isinstance(probes, dict) or set(probes) != set(module.PROBE_CASES):
        errors.append(f"{label}: probe result set is incomplete")
        probes = {}
    for name, case in module.PROBE_CASES.items():
        path = root / "probes" / f"{name}.smt2"
        evidence = probes.get(name)
        if not isinstance(evidence, dict):
            continue
        if (
            evidence.get("kind") != case["kind"]
            or evidence.get("case") != case["values"]
            or evidence.get("expected_solver_result")
            != case["expected_solver_result"]
        ):
            errors.append(f"{label} {name}: probe description changed")
        _check_artifact(
            errors, evidence.get("smt"), path, f"{label} {name} probe SMT"
        )
        if path.is_file() and path.read_text() != module.probe_text(name):
            errors.append(f"{label} {name}: probe differs from reviewed text")
        _check_solver_capture(
            errors,
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            case["expected_solver_result"],
            f"{label} {name}",
        )

    replay = result.get("solver_replay")
    replay_script = common.OUT / "tools" / f"replay_target_{int(module.INPUT_ORDER):03d}.py"
    expected_replay_argv = [
        sys.executable,
        str(replay_script),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent = replay_module.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: independent replay failed: {exc}")
        independent = None
    if not isinstance(replay, dict):
        errors.append(f"{label}: solver replay capture is missing")
    else:
        paths = {
            key: common.OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured = json.loads(paths.get("stdout", Path()).read_text())
        except (OSError, json.JSONDecodeError):
            captured = None
        if (
            len(paths) != 4
            or any(not path.is_file() for path in paths.values())
            or replay.get("argv") != expected_replay_argv
            or paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or paths.get("status", Path()).read_text() != "0\n"
            or paths.get("stderr", Path()).read_text() != ""
            or captured != independent
            or replay.get("result") != independent
        ):
            errors.append(f"{label}: independent solver replay capture is invalid")

    captured_model = root / "verus/source_transition_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append(f"{label}: Verus evidence is missing")
    else:
        _check_artifact(
            errors, verus.get("source_model"), source_model, f"{label} source model"
        )
        _check_artifact(
            errors,
            verus.get("captured_model"),
            captured_model,
            f"{label} captured model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append(f"{label}: captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append(f"{label}: Verus model contains external_body")
        for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
            record = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(record, dict):
                errors.append(f"{label}: Verus {key} capture is missing")
                continue
            paths = {
                name: common.OUT / record.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(record.get(name), str)
            }
            stdout = (
                paths.get("stdout", Path()).read_text()
                if len(paths) == 4
                and all(path.is_file() for path in paths.values())
                else ""
            )
            if (
                len(paths) != 4
                or any(not path.is_file() for path in paths.values())
                or verus.get("expected_summary")
                != pointer_target_pipeline.VERUS_EXPECTED_SUMMARY
                or record.get("argv") != expected_argv
                or paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or record.get("exit_code") != 0
                or paths.get("status", Path()).read_text() != "0\n"
                or paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and pointer_target_pipeline.VERUS_EXPECTED_SUMMARY
                    not in stdout
                )
            ):
                errors.append(f"{label}: Verus {key} capture is invalid")

    _check_source_dependency(
        errors,
        module,
        result.get("source_dependency"),
        f"{label} result",
    )
    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        artifact_id: common.OUT / "evidence/targets" / artifact_id
        for artifact_id in run_module.PRESERVED_ARTIFACT_IDS
    }
    if not isinstance(preservation, dict) or set(preservation) != set(expected_roots):
        errors.append(f"{label}: preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                pointer_target_pipeline.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(f"{label}: did not preserve {artifact_id}")
