#!/usr/bin/env python3
"""Build and retain the exact mutable-iterator partition evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import shlex
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import exact_mutable_iterator_partitions as partitions
import replay_exact_mutable_iterator_partitions as replay
import run_clone_effect_cluster as predecessor
import target_pipeline


COMPLETE = {
    "exact_output_determinism_status": "conditional-complete",
    "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
}
NOT_RUN = {
    field: "not-run" for field in target_pipeline.RESULT_FIELDS
}
BASELINE_RESULTS = {
    **predecessor.BASELINE_RESULTS,
    **predecessor.CLUSTER_RESULTS,
}
PRESERVED_ARTIFACT_IDS = (
    *predecessor.PRESERVED_ARTIFACT_IDS,
    *(config.artifact_id for config in predecessor.cluster.TARGETS),
)
CLUSTER_RESULTS = {
    key: dict(COMPLETE) for key in partitions.TARGET_KEYS
}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/exact_mutable_iterator_partition_cluster"
FROZEN_ROOT = common.OUT / "provenance/frozen"
CANONICAL_ITER = common.RUST_LIBRARY / partitions.CANONICAL_ITER_PATH
AUTHORITY_FIELDS = predecessor.AUTHORITY_FIELDS
EXPECTED_FROZEN_FILE_COUNT = 320


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ValueError(f"required tree is missing: {root}")
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def tree_file_count(root: Path) -> int:
    if not root.is_dir():
        raise ValueError(f"required tree is missing: {root}")
    return sum(path.is_file() for path in root.rglob("*"))


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
                raise ValueError(
                    f"{key}: exact-partition result has unexpected state"
                )
            observed[key] = actual
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope target is classified")
    pending = all(observed[key] == NOT_RUN for key in partitions.TARGET_KEYS)
    delivered = all(
        observed[key] == CLUSTER_RESULTS[key]
        for key in partitions.TARGET_KEYS
    )
    if not (pending or delivered):
        raise ValueError("targets 035 and 068 must be uniformly delivered")

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in partitions.TARGET_KEYS:
            by_key[key].update(NOT_RUN)
    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in set(partitions.TARGET_KEYS) and changed:
            raise ValueError(f"{_row_key(before)}: reset changed out-of-scope row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during reset")
    return reset_csv, reset_json


def _validate_crosswalk_identity(
    config: partitions.ExactPartitionTarget,
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
    if (
        row["active_contract_sha256"] != config.active_contract_sha256
        or row["active_contract_text"] != config.active_contract_text
        or row["retained_contract_sha256"] != config.active_contract_sha256
        or row["retained_contract_text"] != config.active_contract_text
        or row["contract_drift"] != "no"
        or row["boundary_schema_id"] != "iterator_private_state_v1"
        or row["boundary_admissibility"] != "admissible"
        or row["boundary_narrower_than_target"] != "yes"
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != set(config.all_trust_site_ids)
    ):
        raise ValueError(f"{config.target}: authority binding changed")
    return row


def _trust_site_records(
    config: partitions.ExactPartitionTarget,
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
    for site in config.dependency_trust_site_ids:
        if by_id[site]["semantic_disposition"] != (
            "admissible-source-backed-support"
        ):
            raise ValueError(f"{config.target}: dependency {site} is not admitted")
    for site in config.context_only_trust_site_ids:
        if by_id[site]["semantic_disposition"] != (
            "context-only-source-closure"
        ):
            raise ValueError(f"{config.target}: source closure {site} changed")
    return selected


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
    config: partitions.ExactPartitionTarget,
    row: dict[str, str],
    evidence_root: Path,
) -> Path:
    canonical_public = Path(row["source_path"])
    vocabulary_source = Path(row["shared_vocabulary_path"])
    if common.sha256(canonical_public) != row["source_file_sha256"]:
        raise RuntimeError(f"{config.target}: canonical public source changed")
    if common.sha256(vocabulary_source) != row["shared_vocabulary_sha256"]:
        raise RuntimeError(f"{config.target}: shared vocabulary changed")
    if (
        not CANONICAL_ITER.is_file()
        or common.sha256(CANONICAL_ITER)
        != partitions.CANONICAL_ITER_SHA256
    ):
        raise RuntimeError("canonical Rust 1.96 slice/iter.rs changed")

    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    exact_text = {
        "active_contract.txt": (
            config.active_contract_text,
            config.active_contract_sha256,
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            row["generated_declaration_sha256"],
        ),
        "source_item.rs": (
            row["source_item_text"],
            row["source_item_sha256"],
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

    vocabulary_path = root / "iterator_contract_vocabulary.rs"
    vocabulary_path.write_text(
        "\n".join(
            _source_excerpt(vocabulary_source, start, end)
            for start, end in partitions.VOCABULARY_RANGES
        )
    )
    files[vocabulary_path.name] = {
        **target_pipeline.artifact_record(vocabulary_path),
        "canonical_path": str(vocabulary_source),
        "canonical_file_sha256": row["shared_vocabulary_sha256"],
        "source_ranges": [
            f"{start}-{end}" for start, end in partitions.VOCABULARY_RANGES
        ],
    }

    private_path = root / config.private_source_filename
    private_text = _source_excerpt(
        CANONICAL_ITER,
        config.private_source_start,
        config.private_source_end,
    )
    private_path.write_text(private_text)
    files["private_constructor"] = {
        **target_pipeline.artifact_record(private_path),
        "operation": config.target.rsplit("::", 1)[-1] + "::new",
        "canonical_path": str(CANONICAL_ITER),
        "canonical_file_sha256": partitions.CANONICAL_ITER_SHA256,
        "source_lines": config.private_source_reference,
    }
    partitions.validate_source_anchors(
        config,
        row["source_item_text"],
        private_text,
    )

    frozen_bindings = {
        "implproof_harness.rs": (
            "frozen_harness_path",
            "harness_sha256",
        ),
        "transformation_manifest.json": (
            "frozen_transformation_manifest_path",
            "transformation_manifest_sha256",
        ),
        "dependency_assumption_manifest.json": (
            "frozen_dependency_manifest_path",
            "dependency_manifest_sha256",
        ),
        "source_body.json": (
            "frozen_source_body_manifest_path",
            "source_body_manifest_sha256",
        ),
    }
    frozen: dict[str, Any] = {}
    for filename, (path_field, hash_field) in frozen_bindings.items():
        source = common.OUT / row[path_field]
        target = root / filename
        _copy_exact(source, target, row[hash_field])
        frozen[filename] = {
            **target_pipeline.artifact_record(target),
            "frozen_source_path": row[path_field],
            "frozen_source_sha256": row[hash_field],
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


def _run_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    path: Path,
    expected: str,
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
        or lines[0] != expected
        or (not require_model and stdout != expected + "\n")
        or (
            require_model
            and (
                len(lines) < 2
                or "(x_length x)" not in stdout
                or "(y_split_index y1)" not in stdout
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
            "expected_solver_result": expected,
            "model_retained": require_model,
            "stdout_sha256": common.sha256(stdout_path),
        }
    )
    return record


def _run_target(
    config: partitions.ExactPartitionTarget,
    z3: str,
) -> dict[str, Any]:
    row = _validate_crosswalk_identity(config)
    records = _trust_site_records(config)
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
            "records": records,
        },
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, partitions.boundary_manifest(config))
    bound_inputs_path = _write_bound_inputs(config, row, evidence_root)

    obligations: dict[str, Any] = {}
    for stem, purpose in (
        ("obligation", partitions.PRIMARY),
        ("exact_output_obligation", partitions.EXACT_OUTPUT),
    ):
        text, metadata = partitions.obligation(config, purpose)
        partitions.validate_target_obligation(config, text, metadata)
        smt_path = evidence_root / f"{stem}.smt2"
        metadata_path = evidence_root / f"{stem}.metadata.json"
        smt_path.write_text(text)
        common.write_json(metadata_path, metadata)
        obligations[purpose] = {
            "smt": target_pipeline.artifact_record(smt_path),
            "metadata": target_pipeline.artifact_record(metadata_path),
            "solver": _run_solver(
                z3,
                evidence_root,
                stem,
                smt_path,
                "unsat",
            ),
        }

    source_instances: dict[str, Any] = {}
    for name, case in partitions.SOURCE_CASES.items():
        path = evidence_root / f"source_instance_{name}.smt2"
        path.write_text(partitions.source_instance_text(config, case))
        source_instances[name] = {
            "length": case.length,
            "chunk_size": case.chunk_size,
            "element_size": case.element_size,
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                z3,
                evidence_root,
                f"source_instance_{name}",
                path,
                "sat",
                require_model=True,
            ),
        }

    negative_probes: dict[str, Any] = {}
    for name in partitions.NEGATIVE_PROBES:
        path = evidence_root / f"negative_probe_{name}.smt2"
        path.write_text(partitions.negative_probe_text(config, name))
        negative_probes[name] = {
            "smt": target_pipeline.artifact_record(path),
            "solver": _run_solver(
                z3,
                evidence_root,
                f"negative_probe_{name}",
                path,
                "unsat",
            ),
        }

    replay_record = target_pipeline.capture_command(
        evidence_root / "solver_replay",
        [
            sys.executable,
            str(
                common.OUT
                / "tools/replay_exact_mutable_iterator_partitions.py"
            ),
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
    proof_path.write_text(partitions.verus_text(config))
    if "external_body" in proof_path.read_text():
        raise RuntimeError(f"{config.target}: Verus model contains external_body")
    captured_proof = evidence_root / "verus/exact_partition_model.rs"
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
    if (
        typecheck["exit_code"] != 0
        or typecheck_stderr
    ):
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
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": COMPLETE,
        "classification_basis": (
            "For an arbitrary valid length and positive chunk size, the "
            "source transition derives len%chunk, the target-specific split "
            "index and partition orientation, both mutable region identities, "
            "raw-v provenance, parent borrow, private constructor fields, and "
            "the immediate unchanged final frame from the shared input. Both "
            "literal theorem negations replay as clean UNSAT."
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
    for config in partitions.TARGETS:
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
    if classified != set(preserved) or len(classified) != 42 or not_run != 20:
        raise RuntimeError(
            f"expected 42 classified and 20 not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for exact-partition evidence")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")
    if len(BASELINE_RESULTS) != 40 or len(PRESERVED_ARTIFACT_IDS) != 40:
        raise RuntimeError("certified predecessor baseline is not 40 targets")

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
        for config in partitions.TARGETS
    }
    mutable_roots["exact_mutable_iterator_partition_cluster"] = CLUSTER_ROOT
    proof_paths = {
        config.artifact_id: (
            common.OUT / "proofs" / f"{config.artifact_id}.rs"
        )
        for config in partitions.TARGETS
    }

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".exact-mutable-partition-backup-",
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
            for config in partitions.TARGETS:
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
            expected_by_key = {
                _row_key(row): row for row in expected_after
            }
            for key in partitions.TARGET_KEYS:
                expected_by_key[key].update(COMPLETE)
            if after_csv != expected_after or after_json != expected_after:
                raise RuntimeError(
                    "exact-partition run changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            frozen_after = tree_digest(FROZEN_ROOT)
            if preserved_after != preserved_before:
                raise RuntimeError(
                    "exact-partition run mutated certified evidence"
                )
            if (
                frozen_after != frozen_before
                or tree_file_count(FROZEN_ROOT) != frozen_file_count
            ):
                raise RuntimeError("exact-partition run mutated frozen inputs")

            common.write_json(
                CLUSTER_ROOT / "manifest.json",
                {
                    "schema_version": 1,
                    "execution_order": [
                        config.target for config in partitions.TARGETS
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
                    "classified_rows": 42,
                    "not_run_rows": 20,
                    "stage_transition": "disabled",
                    "independent_review": "required",
                },
            )
        except BaseException:
            try:
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
                        shutil.copyfile(
                            backup_root / f"{artifact_id}.rs",
                            path,
                        )
            except Exception as restore_exc:
                raise RuntimeError(
                    "exact-partition run failed and rollback was incomplete"
                ) from restore_exc
            raise

    print("exact_mutable_iterator_partition_cluster=PASS")
    print("targets=035,068")
    print("theorems=4_unsat")
    print("source_instances=12_sat_with_models")
    print("negative_probes=16_unsat")
    print("verus_models=2_clean")
    print("preserved_evidence_trees=40")
    print(f"preserved_frozen_inputs={frozen_file_count}")
    print("classified=42 not_run=20")


if __name__ == "__main__":
    main()
