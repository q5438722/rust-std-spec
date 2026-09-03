#!/usr/bin/env python3
"""Build and retain the bounded split_off pair evidence."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import replay_split_off_pair as replay
import run_split_at_mut_primitives as predecessor
import split_at_mut_primitives as predecessor_targets
import split_off_pair as split
import target_pipeline


COMPLETE = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
}
NOT_RUN = {field: "not-run" for field in target_pipeline.RESULT_FIELDS}
BASELINE_RESULTS = {
    **predecessor.BASELINE_RESULTS,
    **predecessor.CLUSTER_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *predecessor.PRESERVED_ARTIFACT_IDS,
    *(config.artifact_id for config in predecessor_targets.TARGETS),
)
CLUSTER_RESULTS = {key: dict(COMPLETE) for key in split.TARGET_KEYS}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/split_off_pair_cluster"
FROZEN_ROOT = common.OUT / "provenance/frozen"
EXPECTED_FROZEN_FILE_COUNT = 320
AUTHORITY_FIELDS = predecessor.AUTHORITY_FIELDS


def tree_digest(root: Path) -> str:
    return predecessor.tree_digest(root)


def tree_file_count(root: Path) -> int:
    return predecessor.tree_file_count(root)


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def _load_crosswalks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    csv_rows = common.read_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    json_rows = json.loads(
        (common.OUT / "crosswalk/target_to_proof_boundary.json").read_text()
    )
    return csv_rows, json_rows


def _write_crosswalks(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> None:
    common.write_csv(
        common.OUT / "crosswalk/target_to_proof_boundary.csv",
        csv_rows,
        list(csv_rows[0]),
    )
    common.write_json(
        common.OUT / "crosswalk/target_to_proof_boundary.json",
        json_rows,
    )


def prepare_crosswalk_reset(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(csv_rows) != 62 or len(json_rows) != 62:
        raise ValueError("crosswalk must contain exactly 62 rows")
    csv_by_key = {_row_key(row): row for row in csv_rows}
    json_by_key = {_row_key(row): row for row in json_rows}
    if (
        len(csv_by_key) != 62
        or set(csv_by_key) != set(json_by_key)
        or any(csv_by_key[key] != json_by_key[key] for key in csv_by_key)
    ):
        raise ValueError("crosswalk formats are duplicate, mismatched, or divergent")

    observed: dict[tuple[str, str], dict[str, str]] = {}
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified predecessor result changed")
        elif key in CLUSTER_RESULTS:
            if actual not in (NOT_RUN, CLUSTER_RESULTS[key]):
                raise ValueError(f"{key}: split-off result has unexpected state")
            observed[key] = actual
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    pending = all(observed[key] == NOT_RUN for key in split.TARGET_KEYS)
    delivered = all(
        observed[key] == CLUSTER_RESULTS[key] for key in split.TARGET_KEYS
    )
    if not (pending or delivered):
        raise ValueError("targets 099 and 104 must be uniformly delivered")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in split.TARGET_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(split.TARGET_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed out-of-scope row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during reset")
    return reset_csv, reset_json


def _validate_crosswalk_identity(
    config: split.SplitOffTarget,
) -> dict[str, str]:
    matches = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/target_to_proof_boundary.csv"
        )
        if _row_key(row) == (config.target, config.input_order)
    ]
    if len(matches) != 1:
        raise ValueError(f"{config.target}: authority row absent or duplicated")
    row = matches[0]
    expected_hashes = {
        "active_contract_sha256": config.active_contract_sha256,
        "retained_contract_sha256": config.active_contract_sha256,
        "generated_declaration_sha256": config.generated_declaration_sha256,
        "source_file_sha256": split.SLICE_SOURCE_SHA256,
        "source_item_sha256": config.source_item_sha256,
        "harness_sha256": config.harness_sha256,
        "source_body_manifest_sha256": config.source_body_manifest_sha256,
        "transformation_manifest_sha256": config.transformation_manifest_sha256,
        "dependency_manifest_sha256": config.dependency_manifest_sha256,
    }
    if any(row[field] != value for field, value in expected_hashes.items()):
        raise ValueError(f"{config.target}: bound authority hash changed")
    if (
        row["active_contract_text"] != config.active_contract_text
        or row["retained_contract_text"] != config.active_contract_text
        or row["contract_drift"] != "no"
        or row["source_item_start_line"] != str(config.source_start)
        or row["source_item_end_line"] != str(config.source_end)
        or row["public_docs_start_line"] != str(config.docs_start)
        or row["public_docs_end_line"] != str(config.docs_end)
        or row["boundary_admissibility"] != "admissible"
        or row["boundary_narrower_than_target"] != "yes"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(config.all_trust_site_ids)
    ):
        raise ValueError(f"{config.target}: authority binding changed")
    if config.mutable and "final(ret.unwrap())@" not in row["active_contract_text"]:
        raise ValueError("split_off_mut active final-return clause is missing")
    return row


def _trust_site_records(
    config: split.SplitOffTarget,
) -> list[dict[str, str]]:
    selected = [
        row
        for row in common.read_csv(
            common.OUT / "crosswalk/trust_site_inventory.csv"
        )
        if _row_key(row) == (config.target, config.input_order)
    ]
    by_id = {row["record_id"]: row for row in selected}
    if set(by_id) != set(config.all_trust_site_ids):
        raise ValueError(f"{config.target}: trust-site inventory changed")
    for record_id, expected_hash in config.trust_hashes.items():
        if split.canonical_json_sha256(by_id[record_id]) != expected_hash:
            raise ValueError(f"{record_id}: readable trust record changed")
    if any(
        by_id[site]["semantic_disposition"]
        != "admissible-source-backed-support"
        for site in config.excluded_trust_site_ids
    ):
        raise ValueError(f"{config.target}: retained support disposition changed")
    for site in config.context_only_trust_site_ids:
        expected = (
            "context-only-source-closure"
            if site.endswith("C001")
            else "admissible-source-backed-support"
        )
        if by_id[site]["semantic_disposition"] != expected:
            raise ValueError(f"{config.target}: context record changed")
    replaced = {
        site
        for replacement in config.source_backed_replacements
        for site in replacement.replaces_trust_site_ids
    }
    if replaced != set(config.excluded_trust_site_ids):
        raise ValueError(f"{config.target}: replacement partition changed")
    return [by_id[site] for site in config.all_trust_site_ids]


def _source_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"invalid source range {path}:{start}-{end}")
    return "".join(lines[start - 1 : end])


def _write_exact(path: Path, text: str, expected_sha256: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected_sha256:
        raise RuntimeError(f"bound text hash mismatch: {path}")


def _copy_exact(source: Path, target: Path, expected_sha256: str) -> None:
    if not source.is_file() or common.sha256(source) != expected_sha256:
        raise RuntimeError(f"frozen source hash mismatch: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if common.sha256(target) != expected_sha256:
        raise RuntimeError(f"copied input hash mismatch: {target}")


def _write_bound_inputs(
    config: split.SplitOffTarget,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_source = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_source) != split.SLICE_SOURCE_SHA256:
        raise RuntimeError(f"{config.target}: canonical source changed")
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{config.target}: shared vocabulary changed")

    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    exact_text = {
        "active_contract.txt": (
            config.active_contract_text,
            config.active_contract_sha256,
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            config.generated_declaration_sha256,
        ),
        "source_item.rs": (
            row["source_item_text"],
            config.source_item_sha256,
        ),
        "public_docs.md": (
            row["public_docs_text"],
            row["public_docs_sha256"],
        ),
    }
    files: dict[str, Any] = {}
    for filename, (text, digest) in exact_text.items():
        path = root / filename
        _write_exact(path, text, digest)
        files[filename] = target_pipeline.artifact_record(path)

    vocabulary_path = root / "split_vocabulary.rs"
    vocabulary_path.write_text(
        "\n".join(
            _source_excerpt(vocabulary_source, start, end)
            for start, end in split.VOCABULARY_RANGES
        )
    )
    files[vocabulary_path.name] = {
        **target_pipeline.artifact_record(vocabulary_path),
        "canonical_path": str(vocabulary_source),
        "canonical_file_sha256": row["shared_vocabulary_sha256"],
        "source_ranges": [
            f"{start}-{end}" for start, end in split.VOCABULARY_RANGES
        ],
    }

    helper_texts: dict[str, str] = {}
    helper_records: dict[str, Any] = {}
    for source in config.helper_sources:
        text = _source_excerpt(canonical_source, source.start, source.end)
        helper_texts[source.name] = text
        path = root / source.filename
        path.write_text(text)
        helper_records[source.name] = {
            **target_pipeline.artifact_record(path),
            "canonical_path": str(canonical_source),
            "canonical_file_sha256": source.file_sha256,
            "source_lines": source.reference,
        }
    split.validate_source_anchors(
        config,
        row["source_item_text"],
        vocabulary_path.read_text(),
        helper_texts,
    )

    frozen_bindings = {
        "implproof_harness.rs": ("frozen_harness_path", config.harness_sha256),
        "source_body.json": (
            "frozen_source_body_manifest_path",
            config.source_body_manifest_sha256,
        ),
        "transformation_manifest.json": (
            "frozen_transformation_manifest_path",
            config.transformation_manifest_sha256,
        ),
        "dependency_assumption_manifest.json": (
            "frozen_dependency_manifest_path",
            config.dependency_manifest_sha256,
        ),
    }
    frozen: dict[str, Any] = {}
    for filename, (path_field, digest) in frozen_bindings.items():
        source = common.OUT / row[path_field]
        target = root / filename
        _copy_exact(source, target, digest)
        frozen[filename] = {
            **target_pipeline.artifact_record(target),
            "frozen_source_path": row[path_field],
            "frozen_source_sha256": digest,
        }

    manifest_path = root / "manifest.json"
    common.write_json(
        manifest_path,
        {
            "schema_version": 1,
            "target": config.target,
            "input_order": config.input_order,
            "active_contract_sha256": config.active_contract_sha256,
            "files": files,
            "canonical_helpers": helper_records,
            "frozen_implproof": frozen,
            "trust_record_ids": list(config.all_trust_site_ids),
        },
    )
    return manifest_path


def _write_contract_clause_audit(
    config: split.SplitOffTarget,
    evidence_root: Path,
) -> Path:
    harness = evidence_root / "bound_inputs/implproof_harness.rs"
    transformation = evidence_root / "bound_inputs/transformation_manifest.json"
    harness_text = harness.read_text()
    transformation_text = transformation.read_text()
    active_has_final = "final(ret.unwrap())@" in config.active_contract_text
    retained_has_final = "final(ret.unwrap())@" in harness_text
    substitution_recorded = (
        "Removed only the generated `final(ret.unwrap())@` partition clause"
        in transformation_text
    )
    if config.mutable:
        if not active_has_final or retained_has_final or not substitution_recorded:
            raise RuntimeError("mutable active/corrected contract audit changed")
    elif active_has_final or retained_has_final or substitution_recorded:
        raise RuntimeError("immutable contract unexpectedly records substitution")
    path = evidence_root / "active_contract_clause_audit.json"
    common.write_json(
        path,
        {
            "schema_version": 1,
            "target": config.target,
            "active_contract_sha256": config.active_contract_sha256,
            "active_has_initial_return_partition": True,
            "active_has_final_return_partition": active_has_final,
            "retained_harness_has_final_return_partition": retained_has_final,
            "retained_transformation_records_clause_removal": (
                substitution_recorded
            ),
            "model_uses_active_final_return_partition": config.mutable,
            "active_contract_substitution": "prohibited",
        },
    )
    return path


def _run_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    path: Path,
    *,
    require_model: bool = False,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
        [z3, "-smt2", str(path)],
        cwd=common.OUT,
    )
    stdout_path = common.OUT / record["stdout"]
    stderr_path = common.OUT / record["stderr"]
    stdout = stdout_path.read_text()
    stderr = stderr_path.read_text()
    lines = stdout.splitlines()
    if (
        record["exit_code"] != 0
        or stderr
        or not lines
        or lines[0] not in {"sat", "unsat", "unknown"}
        or (
            require_model
            and (
                lines[0] != "sat"
                or len(lines) < 2
                or "(x_range_kind x)" not in stdout
                or "(s_split_index s1)" not in stdout
            )
        )
    ):
        raise RuntimeError(
            f"{label}: invalid solver capture; "
            f"rc={record['exit_code']} stdout={stdout!r} stderr={stderr!r}"
        )
    if not require_model and stdout != lines[0] + "\n":
        raise RuntimeError(f"{label}: unexpected solver output")
    record.update(
        {
            "solver_result": lines[0],
            "model_retained": require_model,
            "stdout_sha256": common.sha256(stdout_path),
        }
    )
    return record


def _classification(result: str) -> str:
    if result == "unsat":
        return "conditional-complete"
    return "solver-unknown"


def _run_target(
    config: split.SplitOffTarget,
    z3: str,
) -> dict[str, Any]:
    row = _validate_crosswalk_identity(config)
    trust_records = _trust_site_records(config)
    evidence_root = EVIDENCE_BASE / config.artifact_id
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    evidence_root.mkdir(parents=True)

    authority_path = evidence_root / "authority_bindings.json"
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: row[field] for field in AUTHORITY_FIELDS},
        },
    )
    trust_path = evidence_root / "trust_site_bindings.json"
    common.write_json(
        trust_path,
        {
            "schema_version": 1,
            "target": config.target,
            "records": trust_records,
            "record_sha256": config.trust_hashes,
        },
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, split.boundary_manifest(config))
    bound_inputs_path = _write_bound_inputs(config, row, evidence_root)
    clause_audit_path = _write_contract_clause_audit(config, evidence_root)

    obligations: dict[str, Any] = {}
    statuses: dict[str, str] = {}
    for stem, purpose in (
        ("obligation", split.PRIMARY),
        ("exact_output_obligation", split.EXACT_OUTPUT),
    ):
        text, metadata = split.obligation(config, purpose)
        split.validate_target_obligation(config, text, metadata)
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        solver = _run_solver(z3, evidence_root, stem, smt_path)
        statuses[purpose] = _classification(solver["solver_result"])
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    classification = {
        "exact_output_determinism_status": statuses[split.EXACT_OUTPUT],
        "completeness_modulo_reviewed_equivalence_status": statuses[
            split.PRIMARY
        ],
    }
    if classification != COMPLETE:
        raise RuntimeError(
            f"{config.target}: theorem replay did not justify completion: "
            f"{classification}"
        )

    source_instances: dict[str, Any] = {}
    for name, case in split.SOURCE_CASES.items():
        path = evidence_root / f"source_instance_{name}.smt2"
        path.write_text(split.source_instance_text(config, case))
        solver = _run_solver(
            z3,
            evidence_root,
            f"source_instance_{name}",
            path,
            require_model=True,
        )
        if solver["solver_result"] != "sat":
            raise RuntimeError(f"{config.target} {name}: nonvacuity failed")
        source_instances[name] = {
            "length": case.length,
            "range_kind": case.range_kind,
            "range_index": case.range_index,
            "element_size": case.element_size,
            "element_alignment": case.element_alignment,
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    negative_probes: dict[str, Any] = {}
    for name in split.NEGATIVE_PROBES:
        path = evidence_root / f"negative_probe_{name}.smt2"
        path.write_text(split.negative_probe_text(config, name))
        solver = _run_solver(z3, evidence_root, f"negative_probe_{name}", path)
        if solver["solver_result"] != "unsat":
            raise RuntimeError(f"{config.target} {name}: probe was not UNSAT")
        negative_probes[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    replay_record = target_pipeline.capture_command(
        evidence_root / "solver_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_split_off_pair.py"),
            "--evidence-root",
            str(evidence_root),
            "--z3",
            z3,
            "--artifact-id",
            config.artifact_id,
        ],
        cwd=common.OUT,
    )
    replay_stdout = (common.OUT / replay_record["stdout"]).read_text()
    replay_stderr = (common.OUT / replay_record["stderr"]).read_text()
    if replay_record["exit_code"] != 0 or replay_stderr:
        raise RuntimeError(f"{config.target}: independent replay failed")
    replay_result = json.loads(replay_stdout)
    if replay_result.get("status") != "passed":
        raise RuntimeError(f"{config.target}: replay did not report passed")
    replay_record["result"] = replay_result

    proof_path = common.OUT / "proofs" / f"{config.artifact_id}.rs"
    proof_path.write_text(split.verus_text(config))
    if "external_body" in proof_path.read_text():
        raise RuntimeError(f"{config.target}: Verus model contains trusted body")
    captured_proof = evidence_root / "verus/split_off_model.rs"
    captured_proof.parent.mkdir(parents=True)
    shutil.copyfile(proof_path, captured_proof)
    typecheck = target_pipeline.capture_command(
        evidence_root / "verus/typecheck",
        [
            str(common.VERUS),
            str(captured_proof),
            "--crate-type=lib",
            "--no-verify",
        ],
        cwd=common.OUT,
    )
    typecheck_stderr = (common.OUT / typecheck["stderr"]).read_text()
    if typecheck["exit_code"] != 0 or typecheck_stderr:
        raise RuntimeError(
            f"{config.target}: Verus model did not type-check: "
            f"{typecheck_stderr.strip()}"
        )
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_proof), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    verification_stderr = (common.OUT / verification["stderr"]).read_text()
    if (
        verification["exit_code"] != 0
        or verification_stderr
        or "0 errors" not in verification_stdout
    ):
        raise RuntimeError(
            f"{config.target}: Verus model did not verify: "
            f"{verification_stderr.strip()}"
        )

    guards_path = evidence_root / "reviewed_model_guards.json"
    common.write_json(
        guards_path,
        {
            "schema_version": 1,
            "target": config.target,
            "fail_closed_mutations": [
                "direction reversal",
                "wrapping EndInclusive addition",
                "altered bounds comparison",
                "off-by-one split",
                "swapped directional branches",
                "mutated None frame",
                "lost reference identity",
                "lost mutable-borrow disjointness",
                "removed active final-return clause",
                "reversed ordered frame",
                "weakened exact equality",
                "answer-bearing boundary",
                "boundary-to-answer laundering",
                "mismatched shared input",
                "mismatched shared boundary",
                "out-of-scope ledger edit",
            ],
            "enforcement": (
                "tools/split_off_pair.py exact reviewed AST plus "
                "tests/test_split_off_pair.py"
            ),
        },
    )

    result = {
        "schema_version": 1,
        "target": config.target,
        "input_order": config.input_order,
        "artifact_id": config.artifact_id,
        "active_contract_sha256": config.active_contract_sha256,
        "active_contract_text": config.active_contract_text,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "trust_site_bindings": target_pipeline.artifact_record(trust_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "active_contract_clause_audit": target_pipeline.artifact_record(
            clause_audit_path
        ),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "reviewed_model_guards": target_pipeline.artifact_record(guards_path),
        "classification": classification,
        "classification_basis": (
            "The arbitrary-length source transition derives one-sided range "
            "direction and checked-add overflow, bounds rejection, exact "
            "front/back regions, directional returned/remaining identities, "
            "mutable take/split ownership and disjoint borrows, unchanged None "
            "frames, and ordered final composition. The exact active mutable "
            "initial and final returned-slice clauses remain live. Both literal "
            "theorem negations replay as clean UNSAT, while every required edge, "
            "one-past-end, and ZST source instance is SAT with a retained model."
        ),
        "obligations": obligations,
        "source_instances": source_instances,
        "negative_probes": negative_probes,
        "solver_replay": replay_record,
        "verus": {
            "source_model": target_pipeline.artifact_record(proof_path),
            "captured_model": target_pipeline.artifact_record(captured_proof),
            "typecheck": typecheck,
            "verification": verification,
        },
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
        "independent_review": "required",
        "stage_transition": "disabled",
    }
    result_path = evidence_root / "result.json"
    common.write_json(result_path, result)
    return result


def _update_ledgers() -> None:
    csv_rows, json_rows = _load_crosswalks()
    preserved = copy.deepcopy(BASELINE_RESULTS)
    for config in split.TARGETS:
        csv_rows, json_rows = target_pipeline.apply_crosswalk_result_update(
            csv_rows,
            json_rows,
            target=config.target,
            input_order=config.input_order,
            statuses=COMPLETE,
            preserved_results=preserved,
        )
        preserved[(config.target, config.input_order)] = dict(COMPLETE)
    _write_crosswalks(csv_rows, json_rows)
    classified = {
        _row_key(row)
        for row in csv_rows
        if any(
            row[field] != "not-run"
            for field in target_pipeline.RESULT_FIELDS
        )
    }
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in csv_rows
    )
    if classified != set(preserved) or len(classified) != 49 or not_run != 13:
        raise RuntimeError(
            f"expected 49 classified and 13 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for split-off evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 47 or len(PRESERVED_ARTIFACT_IDS) != 47:
        raise RuntimeError("certified predecessor baseline is not 47 targets")

    before_csv, before_json = _load_crosswalks()
    reset_csv, reset_json = prepare_crosswalk_reset(before_csv, before_json)
    preserved_roots = {
        artifact_id: EVIDENCE_BASE / artifact_id
        for artifact_id in PRESERVED_ARTIFACT_IDS
    }
    preserved_before = {
        artifact_id: tree_digest(root)
        for artifact_id, root in preserved_roots.items()
    }
    frozen_file_count = tree_file_count(FROZEN_ROOT)
    if frozen_file_count != EXPECTED_FROZEN_FILE_COUNT:
        raise RuntimeError(
            f"expected {EXPECTED_FROZEN_FILE_COUNT} frozen inputs, "
            f"found {frozen_file_count}"
        )
    frozen_before = tree_digest(FROZEN_ROOT)
    mutable_roots = {
        config.artifact_id: EVIDENCE_BASE / config.artifact_id
        for config in split.TARGETS
    }
    mutable_roots["split_off_pair_cluster"] = CLUSTER_ROOT
    proof_paths = {
        config.artifact_id: common.OUT / "proofs" / f"{config.artifact_id}.rs"
        for config in split.TARGETS
    }

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".split-off-pair-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        existing_roots: set[str] = set()
        existing_proofs: set[str] = set()
        for artifact_id, root in mutable_roots.items():
            if root.is_dir():
                shutil.copytree(root, backup_root / artifact_id)
                existing_roots.add(artifact_id)
        for artifact_id, path in proof_paths.items():
            if path.is_file():
                shutil.copyfile(path, backup_root / f"{artifact_id}.rs")
                existing_proofs.add(artifact_id)
        try:
            _write_crosswalks(reset_csv, reset_json)
            if CLUSTER_ROOT.exists():
                shutil.rmtree(CLUSTER_ROOT)
            CLUSTER_ROOT.mkdir(parents=True)

            target_results: dict[str, Any] = {}
            for config in split.TARGETS:
                _run_target(config, z3)
                result_path = EVIDENCE_BASE / config.artifact_id / "result.json"
                target_results[config.target] = {
                    "artifact_id": config.artifact_id,
                    "classification": dict(COMPLETE),
                    "result": target_pipeline.artifact_record(result_path),
                }

            _update_ledgers()
            after_csv, after_json = _load_crosswalks()
            expected_after = copy.deepcopy(before_csv)
            expected_by_key = {_row_key(row): row for row in expected_after}
            for key in split.TARGET_KEYS:
                expected_by_key[key].update(COMPLETE)
            if after_csv != expected_after or after_json != expected_after:
                raise RuntimeError(
                    "split-off run changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = tree_digest(FROZEN_ROOT)
            if preserved_after != preserved_before:
                raise RuntimeError("split-off run mutated certified evidence")
            if (
                frozen_after != frozen_before
                or tree_file_count(FROZEN_ROOT) != frozen_file_count
            ):
                raise RuntimeError("split-off run mutated frozen inputs")

            common.write_json(
                CLUSTER_ROOT / "manifest.json",
                {
                    "schema_version": 1,
                    "execution_order": [
                        config.target for config in split.TARGETS
                    ],
                    "targets": target_results,
                    "preserved_certified_evidence": {
                        artifact_id: {
                            "before_sha256": preserved_before[artifact_id],
                            "after_sha256": preserved_after[artifact_id],
                        }
                        for artifact_id in PRESERVED_ARTIFACT_IDS
                    },
                    "preserved_frozen_inputs": {
                        "root": {
                            "path": common.relpath(FROZEN_ROOT),
                            "file_count": frozen_file_count,
                            "before_sha256": frozen_before,
                            "after_sha256": frozen_after,
                        }
                    },
                    "classified_rows": 49,
                    "not_run_rows": 13,
                    "updated_crosswalk_fields": list(
                        target_pipeline.RESULT_FIELDS
                    ),
                    "independent_review": "required",
                    "stage_transition": "disabled",
                },
            )
        except Exception:
            _write_crosswalks(before_csv, before_json)
            for artifact_id, root in mutable_roots.items():
                if root.exists():
                    shutil.rmtree(root)
                if artifact_id in existing_roots:
                    shutil.copytree(backup_root / artifact_id, root)
            for artifact_id, path in proof_paths.items():
                if path.exists():
                    path.unlink()
                if artifact_id in existing_proofs:
                    shutil.copyfile(backup_root / f"{artifact_id}.rs", path)
            raise

    print("split_off_pair=PASS")
    print("classified=49 not_run=13")
    print("targets=" + ",".join(config.input_order for config in split.TARGETS))


if __name__ == "__main__":
    main()
