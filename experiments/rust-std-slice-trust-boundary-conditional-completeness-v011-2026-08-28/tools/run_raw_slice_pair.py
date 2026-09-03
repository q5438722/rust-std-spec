#!/usr/bin/env python3
"""Build and retain bounded evidence for the raw slice constructors."""

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
import align_to_pair as align_pair
import raw_slice_pair as raw
import replay_raw_slice_pair as replay
import run_split_off_pair as predecessor
import split_off_pair as predecessor_targets
import target_pipeline


NOT_RUN = {field: "not-run" for field in target_pipeline.RESULT_FIELDS}
BASELINE_RESULTS = {
    **predecessor.BASELINE_RESULTS,
    **predecessor.CLUSTER_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *predecessor.PRESERVED_ARTIFACT_IDS,
    *(config.artifact_id for config in predecessor_targets.TARGETS),
)
CLUSTER_RESULTS = {
    (config.target, config.input_order): config.expected_classification
    for config in raw.TARGETS
}
SUCCESSOR_RESULTS = {
    (config.target, config.input_order): config.expected_classification
    for config in align_pair.TARGETS
}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/raw_slice_pair_cluster"
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
                raise ValueError(f"{key}: raw-slice result has unexpected state")
            observed[key] = actual
        elif key in SUCCESSOR_RESULTS:
            if actual not in (NOT_RUN, SUCCESSOR_RESULTS[key]):
                raise ValueError(f"{key}: align-to successor result changed")
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    pending = all(observed[key] == NOT_RUN for key in raw.TARGET_KEYS)
    delivered = all(
        observed[key] == CLUSTER_RESULTS[key] for key in raw.TARGET_KEYS
    )
    if not (pending or delivered):
        raise ValueError("targets 048 and 049 must be uniformly delivered")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in raw.TARGET_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(raw.TARGET_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed out-of-scope row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during reset")
    return reset_csv, reset_json


def _validate_crosswalk_identity(
    config: raw.RawSliceTarget,
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
        "source_file_sha256": raw.RAW_SOURCE_SHA256,
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
        or row["boundary_admissibility"] != "inadmissible"
        or row["boundary_narrower_than_target"] != "no"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(config.all_trust_site_ids)
    ):
        raise ValueError(f"{config.target}: authority binding changed")
    return row


def _trust_site_records(
    config: raw.RawSliceTarget,
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
        if raw.canonical_json_sha256(by_id[record_id]) != expected_hash:
            raise ValueError(f"{record_id}: readable trust record changed")
    if (
        by_id[config.context_only_trust_site_ids[0]]["semantic_disposition"]
        != "context-only-specification-vocabulary"
    ):
        raise ValueError(f"{config.target}: vocabulary record was relabeled")
    expected_dispositions = {
        config.excluded_trust_site_ids[0]: "inadmissible-answer-bearing-support",
        config.excluded_trust_site_ids[1]: (
            "inadmissible-complete-target-postcondition"
        ),
    }
    if any(
        by_id[record_id]["semantic_disposition"] != disposition
        for record_id, disposition in expected_dispositions.items()
    ):
        raise ValueError(f"{config.target}: excluded trust record was relabeled")
    replaced = {
        site
        for replacement in raw.obligation_metadata(config, raw.PRIMARY)[
            "source_backed_replacements"
        ]
        for site in replacement["replaces_trust_site_ids"]
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
    config: raw.RawSliceTarget,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_source = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_source) != raw.RAW_SOURCE_SHA256:
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

    vocabulary_path = root / "raw_slice_vocabulary.rs"
    vocabulary_path.write_text(
        "\n".join(
            _source_excerpt(vocabulary_source, start, end)
            for start, end in raw.VOCABULARY_RANGES
        )
    )
    files[vocabulary_path.name] = {
        **target_pipeline.artifact_record(vocabulary_path),
        "canonical_path": str(vocabulary_source),
        "canonical_file_sha256": row["shared_vocabulary_sha256"],
        "source_ranges": [
            f"{start}-{end}" for start, end in raw.VOCABULARY_RANGES
        ],
    }
    raw.validate_source_anchors(
        config,
        row["source_item_text"],
        row["public_docs_text"],
        vocabulary_path.read_text(),
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
            "frozen_implproof": frozen,
            "trust_record_ids": list(config.all_trust_site_ids),
        },
    )
    return manifest_path


def _write_contract_audit(
    config: raw.RawSliceTarget,
    evidence_root: Path,
) -> Path:
    harness = evidence_root / "bound_inputs/implproof_harness.rs"
    harness_text = harness.read_text()
    if (
        "#[verifier::external_body]" not in harness_text
        or "slice_from_raw_parts" not in harness_text
        or "final(ret)" in config.active_contract_text
    ):
        raise RuntimeError(f"{config.target}: retained/active contract audit changed")
    path = evidence_root / "active_contract_clause_audit.json"
    common.write_json(
        path,
        {
            "schema_version": 1,
            "target": config.target,
            "active_contract_sha256": config.active_contract_sha256,
            "active_has_raw_domain_precondition": True,
            "active_has_initial_return_relation": True,
            "active_has_final_return_relation": False,
            "retained_harness_has_external_body": True,
            "retained_external_body_admitted": False,
            "answer_bearing_sites_replaced_not_relabeled": list(
                config.excluded_trust_site_ids
            ),
            "trusted_free_verus_model_required": True,
            "mutable_final_frame_invented": False,
        },
    )
    return path


def _run_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    path: Path,
    *,
    expected: str,
    require_model: bool = False,
    witness: bool = False,
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
        record["exit_code"] != 0
        or stderr
        or not lines
        or lines[0] != expected
        or (not require_model and stdout != expected + "\n")
        or (
            require_model
            and (
                len(lines) < 2
                or any(marker not in stdout for marker in markers)
            )
        )
    ):
        raise RuntimeError(
            f"{label}: expected clean {expected}; "
            f"rc={record['exit_code']} stdout={stdout!r} stderr={stderr!r}"
        )
    record.update(
        {
            "solver_result": expected,
            "model_retained": require_model,
            "stdout_sha256": common.sha256(stdout_path),
        }
    )
    return record


def _run_target(
    config: raw.RawSliceTarget,
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
    common.write_json(boundary_path, raw.boundary_manifest(config))
    bound_inputs_path = _write_bound_inputs(config, row, evidence_root)
    clause_audit_path = _write_contract_audit(config, evidence_root)

    obligations: dict[str, Any] = {}
    solver_results: dict[str, str] = {}
    for stem, purpose in (
        ("obligation", raw.PRIMARY),
        ("exact_output_obligation", raw.EXACT_OUTPUT),
    ):
        text, metadata = raw.obligation(config, purpose)
        raw.validate_target_obligation(config, text, metadata)
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        solver = _run_solver(
            z3,
            evidence_root,
            stem,
            smt_path,
            expected=config.expected_results[purpose],
        )
        solver_results[purpose] = solver["solver_result"]
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": solver,
        }

    witness_record: dict[str, Any] | None = None
    if config.mutable:
        witness_smt = evidence_root / "fixed_full_state_witness.smt2"
        witness_json = evidence_root / "fixed_full_state_witness.json"
        witness_smt.write_text(raw.fixed_witness_text(config))
        common.write_json(witness_json, raw.witness_payload(config))
        solver = _run_solver(
            z3,
            evidence_root,
            "fixed_full_state_witness",
            witness_smt,
            expected="sat",
            require_model=True,
            witness=True,
        )
        witness_record = {
            "smt": target_pipeline.artifact_record(witness_smt),
            "payload": target_pipeline.artifact_record(witness_json),
            "solver": solver,
            "fixed_input": True,
            "fixed_boundary": True,
            "both_specs_satisfied": True,
        }

    classification = {
        "exact_output_determinism_status": (
            "conditional-complete"
            if solver_results[raw.EXACT_OUTPUT] == "unsat"
            else "solver-unknown"
        ),
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
            if solver_results[raw.PRIMARY] == "unsat"
            else (
                "conditional-incomplete"
                if (
                    config.mutable
                    and solver_results[raw.PRIMARY] == "sat"
                    and witness_record is not None
                    and witness_record["solver"]["solver_result"] == "sat"
                )
                else "solver-unknown"
            )
        ),
    }
    if classification != config.expected_classification:
        raise RuntimeError(
            f"{config.target}: solver evidence did not justify "
            f"{config.expected_classification}: {classification}"
        )

    source_instances: dict[str, Any] = {}
    for name, case in raw.source_cases(config).items():
        path = evidence_root / f"source_instance_{name}.smt2"
        path.write_text(raw.source_instance_text(config, name))
        solver = _run_solver(
            z3,
            evidence_root,
            f"source_instance_{name}",
            path,
            expected="sat",
            require_model=True,
        )
        source_instances[name] = {
            "length": case["length"],
            "element_size": case["element_size"],
            "element_alignment": case["element_alignment"],
            "allocation": case["allocation"],
            "address": case["address"],
            "provenance": case["provenance"],
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    negative_probes: dict[str, Any] = {}
    for name in raw.NEGATIVE_PROBES:
        path = evidence_root / f"negative_probe_{name}.smt2"
        path.write_text(raw.negative_probe_text(config, name))
        solver = _run_solver(
            z3,
            evidence_root,
            f"negative_probe_{name}",
            path,
            expected="unsat",
        )
        negative_probes[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    replay_record = target_pipeline.capture_command(
        evidence_root / "solver_replay",
        [
            sys.executable,
            str(common.OUT / "tools/replay_raw_slice_pair.py"),
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
    proof_path.write_text(raw.verus_text(config))
    if "external_body" in proof_path.read_text():
        raise RuntimeError(f"{config.target}: Verus model contains trusted body")
    captured_proof = evidence_root / "verus/raw_slice_model.rs"
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
        or raw.VERUS_EXPECTED_SUMMARY not in verification_stdout
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
                "null empty or ZST pointer",
                "misaligned empty or ZST pointer",
                "nonzero span without allocation/provenance",
                "multi-allocation span",
                "uninitialized addressed memory cell",
                "shared mutation alias or mutable competing alias",
                "isize multiplication overflow",
                "address wrap or allocation overrun",
                "wrong pointwise return memory, ZST stride, or empty dereference",
                "wrong return allocation/address/provenance",
                "wrong return borrow or mutability",
                "immutable memory mutation or mutable alias-frame drift",
                "invented mutable final-frame assumption",
                "answer-bearing boundary or helper laundering",
                "mismatched shared input or boundary",
                "weakened exact equality or out-of-scope ledger edit",
            ],
            "enforcement": (
                "tools/raw_slice_pair.py exact reviewed AST plus "
                "tests/test_raw_slice_pair.py"
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
            "The source UB-check, raw-fat-pointer construction, and reference "
            "dereference transitions derive the finite initial return view "
            "pointwise from address-indexed cells in one shared initial "
            "boundary, with explicit ZST and empty one-past rules. The "
            "immutable state is source-framed and both theorems are UNSAT. "
            "The mutable exact-output theorem is UNSAT, while a separately "
            "replayed fixed-input/fixed-boundary SAT witness varies only final "
            "in-range memory omitted by the active contract."
        ),
        "obligations": obligations,
        "fixed_full_state_witness": witness_record,
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
    for config in raw.TARGETS:
        statuses = config.expected_classification
        csv_rows, json_rows = target_pipeline.apply_crosswalk_result_update(
            csv_rows,
            json_rows,
            target=config.target,
            input_order=config.input_order,
            statuses=statuses,
            preserved_results=preserved,
        )
        preserved[(config.target, config.input_order)] = dict(statuses)
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
    if classified != set(preserved) or len(classified) != 51 or not_run != 11:
        raise RuntimeError(
            f"expected 51 classified and 11 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for raw-slice evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 49 or len(PRESERVED_ARTIFACT_IDS) != 49:
        raise RuntimeError("certified predecessor baseline is not 49 targets")

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
        for config in raw.TARGETS
    }
    mutable_roots["raw_slice_pair_cluster"] = CLUSTER_ROOT
    proof_paths = {
        config.artifact_id: common.OUT / "proofs" / f"{config.artifact_id}.rs"
        for config in raw.TARGETS
    }

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".raw-slice-pair-backup-",
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
            for config in raw.TARGETS:
                _run_target(config, z3)
                result_path = EVIDENCE_BASE / config.artifact_id / "result.json"
                target_results[config.target] = {
                    "artifact_id": config.artifact_id,
                    "classification": dict(config.expected_classification),
                    "result": target_pipeline.artifact_record(result_path),
                }

            _update_ledgers()
            after_csv, after_json = _load_crosswalks()
            expected_after = copy.deepcopy(before_csv)
            expected_by_key = {_row_key(row): row for row in expected_after}
            for config in raw.TARGETS:
                expected_by_key[
                    (config.target, config.input_order)
                ].update(config.expected_classification)
            if after_csv != expected_after or after_json != expected_after:
                raise RuntimeError(
                    "raw-slice run changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = tree_digest(FROZEN_ROOT)
            if preserved_after != preserved_before:
                raise RuntimeError("raw-slice run mutated certified evidence")
            if (
                frozen_after != frozen_before
                or tree_file_count(FROZEN_ROOT) != frozen_file_count
            ):
                raise RuntimeError("raw-slice run mutated frozen inputs")

            common.write_json(
                CLUSTER_ROOT / "manifest.json",
                {
                    "schema_version": 1,
                    "execution_order": [
                        config.target for config in raw.TARGETS
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
                    "classified_rows": 51,
                    "not_run_rows": 11,
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

    print("raw_slice_pair=PASS")
    print("classified=51 not_run=11")
    print("targets=" + ",".join(config.input_order for config in raw.TARGETS))


if __name__ == "__main__":
    main()
