#!/usr/bin/env python3
"""Build and capture the bounded targets 026, 119, and 025 evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
import align_to_pair as align_pair
import exact_mutable_iterator_partitions as exact_partitions
import mutable_edge_extraction as edge
import mutable_fixed_chunk_edges as fixed_chunks
import mutable_iterator_constructors as constructors
import replay_maybeuninit_lifecycle_cluster as independent_replay
import split_at_mut_primitives as split_primitives
import split_off_pair as split_off
import raw_slice_pair as raw_slice
import slice_index_trio as slice_trio
import address_observer_pair as address_pair
import mutable_view_construction_cluster as mutable_views
import target_025
import target_026
import target_119
import target_pipeline


TARGET_MODULES = (target_026, target_119, target_025)
CLUSTER_KEYS = tuple(
    (module.TARGET, module.INPUT_ORDER) for module in TARGET_MODULES
)
NOT_RUN = {
    field: "not-run" for field in target_pipeline.RESULT_FIELDS
}
DELIVERED_RESULTS = {
    (target_025.TARGET, target_025.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    (target_026.TARGET, target_026.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    (target_119.TARGET, target_119.INPUT_ORDER): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
}
EVIDENCE_BASE = common.OUT / "evidence/targets"
CLUSTER_ROOT = common.OUT / "evidence/maybeuninit_lifecycle_cluster"
SOURCE_MODELS = {
    target_025.TARGET: common.OUT / "proofs/025_core_slice_assume_init_drop.rs",
    target_026.TARGET: common.OUT / "proofs/026_core_slice_assume_init_mut.rs",
    target_119.TARGET: common.OUT
    / "proofs/119_core_slice_write_clone_of_slice.rs",
}

BASELINE_RESULTS = {
    ("core::slice::as_chunks", "12"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_chunks_mut", "13"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::as_chunks_unchecked", "14"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_chunks_unchecked_mut", "15"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::as_mut_ptr", "19"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_mut_ptr_range", "20"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_ptr", "21"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_ptr_range", "22"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_rchunks", "23"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::as_rchunks_mut", "24"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::binary_search", "28"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::binary_search_by", "29"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::binary_search_by_key", "30"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::get_disjoint_mut", "51"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::get_disjoint_unchecked_mut", "52"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::partition_point", "65"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::sort_unstable_by", "81"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-incomplete",
    },
    ("core::slice::splitn_mut", "106"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::write_copy_of_slice", "120"): {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
}
LATER_RESULTS = {
    ("core::slice::sort_unstable", "80"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::sort_unstable_by_key", "82"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::select_nth_unstable", "77"): {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": "conditional-complete",
    },
    ("core::slice::select_nth_unstable_by", "78"): {
        "exact_output_determinism_status": "missing-source-backed-model",
        "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
    },
    ("core::slice::select_nth_unstable_by_key", "79"): {
        "exact_output_determinism_status": "missing-source-backed-model",
        "completeness_modulo_reviewed_equivalence_status": "missing-source-backed-model",
    },
}
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in constructors.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in edge.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in (
            ("core::slice::clone_from_slice", "37"),
            ("core::slice::fill", "43"),
        )
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in exact_partitions.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in fixed_chunks.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in split_primitives.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        key: {
            "exact_output_determinism_status": "conditional-complete",
            "completeness_modulo_reviewed_equivalence_status": (
                "conditional-complete"
            ),
        }
        for key in split_off.TARGET_KEYS
    }
)
LATER_RESULTS.update(
    {
        (config.target, config.input_order): config.expected_classification
        for config in raw_slice.TARGETS
    }
)
LATER_RESULTS.update(
    {
        (config.target, config.input_order): config.expected_classification
        for config in slice_trio.TARGETS
    }
)
LATER_RESULTS.update(
    {
        (config.target, config.input_order): config.expected_classification
        for config in address_pair.TARGETS
    }
)
LATER_RESULTS.update(
    {
        (config.target, config.input_order): config.expected_classification
        for config in mutable_views.TARGETS
    }
)
LATER_RESULTS.update(
    {
        (config.target, config.input_order): config.expected_classification
        for config in align_pair.TARGETS
    }
)

PRESERVED_ARTIFACT_IDS = (
    "012_core_slice_as_chunks",
    "013_core_slice_as_chunks_mut",
    "014_core_slice_as_chunks_unchecked",
    "015_core_slice_as_chunks_unchecked_mut",
    "019_core_slice_as_mut_ptr",
    "020_core_slice_as_mut_ptr_range",
    "021_core_slice_as_ptr",
    "022_core_slice_as_ptr_range",
    "023_core_slice_as_rchunks",
    "024_core_slice_as_rchunks_mut",
    "028_core_slice_binary_search",
    "029_core_slice_binary_search_by",
    "030_core_slice_binary_search_by_key",
    "051_core_slice_get_disjoint_mut",
    "052_core_slice_get_disjoint_unchecked_mut",
    "065_core_slice_partition_point",
    "081_core_slice_sort_unstable_by",
    "106_core_slice_splitn_mut",
    "120_core_slice_write_copy_of_slice",
)

EXPECTED_TRUST_IDS = {
    target_025.TARGET: set(target_025.ALL_AUDITED_TRUST_SITES),
    target_026.TARGET: set(target_026.ALL_AUDITED_TRUST_SITES),
    target_119.TARGET: set(target_119.ALL_AUDITED_TRUST_SITES),
}

CANONICAL_BINDINGS = {
    target_025.TARGET: {
        "drop_in_place": {
            "path": "core/src/ptr/mod.rs",
            "start": 716,
            "end": 819,
            "file_sha256": (
                "1fd4ecb1650cfc995f29a172ad3f72ffa378702ea55493eabf6a80355b38035e"
            ),
            "excerpt_sha256": (
                "30ab288383d8f668e6c8b6a656ff9261e57cf87301d1c3b95123df31c6cbf1fc"
            ),
        }
    },
    target_026.TARGET: {
        "assume_init_mut_docs_and_item": {
            "path": "core/src/mem/maybe_uninit.rs",
            "start": 1516,
            "end": 1531,
            "file_sha256": (
                "cd1152779de3a6bc96b29997e8a95d3beb9ff1018f99223b429ed0df66baa8ef"
            ),
            "excerpt_sha256": (
                "acd9d1bba60ce94f4149f139f03c6d44279c7ca05c88cf257c912b6c2b215a1e"
            ),
        }
    },
    target_119.TARGET: {
        "guard_drop": {
            "path": "core/src/mem/maybe_uninit.rs",
            "start": 1623,
            "end": 1635,
            "file_sha256": (
                "cd1152779de3a6bc96b29997e8a95d3beb9ff1018f99223b429ed0df66baa8ef"
            ),
            "excerpt_sha256": (
                "2d2c9ce6a1e84a0c1d6feef757e8ab46380ea599f0d63c3d37165a5fafe45b30"
            ),
        },
        "clone_trait_semantics": {
            "path": "core/src/clone.rs",
            "spans": [[39, 58], [129, 153], [192, 233]],
            "file_sha256": (
                "6bfe77fc369801a72c08598ad4cda4be5ee0fc24d521dd910dfe42bd0aae97b8"
            ),
            "excerpt_sha256": (
                "64aa6c1c03f8061646315e68d196b6c908c8d2bb1e0d8e35dfa3c9ec49867c34"
            ),
        },
        "assume_init_mut_dependency": {
            "path": "core/src/mem/maybe_uninit.rs",
            "start": 1516,
            "end": 1531,
            "file_sha256": (
                "cd1152779de3a6bc96b29997e8a95d3beb9ff1018f99223b429ed0df66baa8ef"
            ),
            "excerpt_sha256": (
                "acd9d1bba60ce94f4149f139f03c6d44279c7ca05c88cf257c912b6c2b215a1e"
            ),
        },
    },
}


def tree_digest(root: Path) -> str:
    if not root.is_dir():
        raise ValueError(f"preserved evidence tree is missing: {root}")
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("target", "")), str(row.get("input_order", ""))


def _load_crosswalks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    return common.read_csv(csv_path), json.loads(json_path.read_text())


def _write_crosswalks(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> None:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    common.write_csv(csv_path, csv_rows, list(csv_rows[0]))
    common.write_json(json_path, json_rows)


def prepare_crosswalk_reset(
    csv_rows: list[dict[str, Any]],
    json_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate the delivered ledger before resetting only this cluster."""
    if len(csv_rows) != 62 or len(json_rows) != 62:
        raise ValueError("crosswalk must contain exactly 62 rows in both formats")
    csv_by_key = {_row_key(row): row for row in csv_rows}
    json_by_key = {_row_key(row): row for row in json_rows}
    if (
        len(csv_by_key) != 62
        or set(csv_by_key) != set(json_by_key)
        or any(csv_by_key[key] != json_by_key[key] for key in csv_by_key)
    ):
        raise ValueError("crosswalk formats are duplicate, mismatched, or divergent")

    cluster_keys = set(CLUSTER_KEYS)
    cluster_actual: dict[tuple[str, str], dict[str, str]] = {}
    for key, row in csv_by_key.items():
        actual = {
            field: str(row.get(field, ""))
            for field in target_pipeline.RESULT_FIELDS
        }
        if key in BASELINE_RESULTS:
            if actual != BASELINE_RESULTS[key]:
                raise ValueError(f"{key}: certified predecessor result changed")
        elif key in cluster_keys:
            if actual not in (NOT_RUN, DELIVERED_RESULTS[key]):
                raise ValueError(f"{key}: delivered cluster result changed")
            cluster_actual[key] = actual
        elif key in LATER_RESULTS:
            if actual not in (NOT_RUN, LATER_RESULTS[key]):
                raise ValueError(f"{key}: later certified result changed")
        elif actual != NOT_RUN:
            raise ValueError(f"{key}: out-of-scope result is classified")
    cluster_is_delivered = all(
        cluster_actual[key] == DELIVERED_RESULTS[key] for key in CLUSTER_KEYS
    )
    cluster_is_not_run = all(
        cluster_actual[key] == NOT_RUN for key in CLUSTER_KEYS
    )
    if not (cluster_is_delivered or cluster_is_not_run):
        raise ValueError(
            "cluster rows must be uniformly delivered or uniformly not-run"
        )

    reset_csv = copy.deepcopy(csv_rows)
    reset_json = copy.deepcopy(json_rows)
    for rows in (reset_csv, reset_json):
        by_key = {_row_key(row): row for row in rows}
        for key in CLUSTER_KEYS:
            by_key[key].update(NOT_RUN)

    for before, after in zip(csv_rows, reset_csv):
        changed = {
            field
            for field in set(before) | set(after)
            if before.get(field) != after.get(field)
        }
        if changed - set(target_pipeline.RESULT_FIELDS):
            raise ValueError(f"{_row_key(before)}: reset changed non-result data")
        if _row_key(before) not in cluster_keys and changed:
            raise ValueError(f"{_row_key(before)}: reset changed a non-cluster row")
    if reset_csv != reset_json:
        raise ValueError("crosswalk formats diverged during cluster reset")
    return reset_csv, reset_json


def write_text_with_hash(path: Path, text: str, expected: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if common.sha256(path) != expected:
        raise RuntimeError(f"frozen text binding hash mismatch: {path}")


def validate_crosswalk_identity(module: Any) -> dict[str, str]:
    rows = common.read_csv(common.OUT / "crosswalk/target_to_proof_boundary.csv")
    matches = [
        row
        for row in rows
        if row["target"] == module.TARGET
        and row["input_order"] == module.INPUT_ORDER
    ]
    if len(matches) != 1:
        raise ValueError(f"{module.TARGET}: crosswalk row is absent or duplicated")
    row = matches[0]
    expected_boundary = (
        ("admissible", "yes")
        if module is target_119
        else ("inadmissible", "no")
    )
    if (
        row["active_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["active_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["retained_contract_sha256"] != module.ACTIVE_CONTRACT_SHA256
        or row["retained_contract_text"] != module.ACTIVE_CONTRACT_TEXT
        or row["contract_drift"] != "no"
        or (
            row["boundary_admissibility"],
            row["boundary_narrower_than_target"],
        )
        != expected_boundary
        or row["equivalence_kind"]
        != "exact-principal-return-and-final-state"
        or set(row["all_trust_site_ids"].split(";"))
        != EXPECTED_TRUST_IDS[module.TARGET]
    ):
        raise ValueError(f"{module.TARGET}: authority/boundary binding changed")
    return row


def selected_trust_records(module: Any) -> list[dict[str, str]]:
    rows = common.read_csv(common.OUT / "crosswalk/trust_site_inventory.csv")
    records = [row for row in rows if row["target"] == module.TARGET]
    if {row["record_id"] for row in records} != EXPECTED_TRUST_IDS[module.TARGET]:
        raise ValueError(f"{module.TARGET}: trust-site inventory changed")
    return records


def freeze_bound_inputs(
    module: Any,
    row: dict[str, str],
    evidence_root: Path,
) -> dict[str, Any]:
    root = evidence_root / "bound_inputs"
    root.mkdir(parents=True, exist_ok=True)
    text_bindings = {
        "active_contract.txt": (
            row["active_contract_text"],
            row["active_contract_sha256"],
        ),
        "generated_declaration.rs": (
            row["generated_declaration_text"],
            row["generated_declaration_sha256"],
        ),
        "target_source_item.rs": (
            row["source_item_text"],
            row["source_item_sha256"],
        ),
        "target_public_docs.md": (
            row["public_docs_text"],
            row["public_docs_sha256"],
        ),
    }
    artifacts: dict[str, Any] = {}
    for filename, (text, expected) in text_bindings.items():
        path = root / filename
        write_text_with_hash(path, text, expected)
        artifacts[filename] = target_pipeline.artifact_record(path)

    copied_bindings = {
        "implproof_harness.rs": (
            row["frozen_harness_path"],
            row["harness_sha256"],
        ),
        "transformation_manifest.json": (
            row["frozen_transformation_manifest_path"],
            row["transformation_manifest_sha256"],
        ),
        "dependency_assumption_manifest.json": (
            row["frozen_dependency_manifest_path"],
            row["dependency_manifest_sha256"],
        ),
        "source_body.json": (
            row["frozen_source_body_manifest_path"],
            row["source_body_manifest_sha256"],
        ),
    }
    for filename, (relative_source, expected) in copied_bindings.items():
        source = common.OUT / relative_source
        if common.sha256(source) != expected:
            raise RuntimeError(f"frozen authority input changed: {source}")
        destination = root / filename
        shutil.copyfile(source, destination)
        artifacts[filename] = target_pipeline.artifact_record(destination)

    trust_path = root / "trust_site_inventory.json"
    common.write_json(
        trust_path,
        {
            "schema_version": 1,
            "target": module.TARGET,
            "records": selected_trust_records(module),
        },
    )
    artifacts[trust_path.name] = target_pipeline.artifact_record(trust_path)

    canonical: dict[str, Any] = {}
    for name, binding in CANONICAL_BINDINGS[module.TARGET].items():
        source = common.RUST_LIBRARY / str(binding["path"])
        if common.sha256(source) != binding["file_sha256"]:
            raise RuntimeError(f"canonical Rust source changed: {source}")
        lines = source.read_text().splitlines(keepends=True)
        if "spans" in binding:
            excerpt = "".join(
                "".join(lines[start - 1 : end])
                for start, end in binding["spans"]
            )
            span = ",".join(
                f"{start}-{end}" for start, end in binding["spans"]
            )
        else:
            start = int(binding["start"])
            end = int(binding["end"])
            excerpt = "".join(lines[start - 1 : end])
            span = f"{start}-{end}"
        destination = root / f"canonical_{name}.rs"
        write_text_with_hash(
            destination,
            excerpt,
            str(binding["excerpt_sha256"]),
        )
        artifacts[destination.name] = target_pipeline.artifact_record(destination)
        canonical[name] = {
            "source_path": str(binding["path"]),
            "source_span": span,
            "source_file_sha256": binding["file_sha256"],
            "excerpt_sha256": binding["excerpt_sha256"],
        }

    return {
        "schema_version": 1,
        "canonical_sources": canonical,
        "artifacts": artifacts,
    }


def capture_solver(
    z3: str,
    evidence_root: Path,
    label: str,
    smt_path: Path,
) -> dict[str, Any]:
    record = target_pipeline.capture_command(
        evidence_root / label,
        [z3, "-smt2", str(smt_path)],
        cwd=common.OUT,
    )
    stdout = (common.OUT / record["stdout"]).read_text()
    stderr = (common.OUT / record["stderr"]).read_text()
    first = stdout.splitlines()[0] if stdout else ""
    if record["exit_code"] != 0 or stderr or first not in {"sat", "unsat", "unknown"}:
        raise RuntimeError(
            f"{label}: solver failed clean-result requirement: "
            f"rc={record['exit_code']} stdout={stdout!r} stderr={stderr!r}"
        )
    record["solver_result"] = first
    return record


def write_obligation(
    module: Any,
    evidence_root: Path,
    purpose: str,
    stem: str,
) -> tuple[Path, dict[str, Any]]:
    text, metadata = module.obligation(purpose)
    module.validate_target_obligation(text, metadata)
    smt_path = evidence_root / f"{stem}.smt2"
    metadata_path = evidence_root / f"{stem}.metadata.json"
    smt_path.write_text(text)
    common.write_json(metadata_path, metadata)
    return smt_path, {
        "smt": target_pipeline.artifact_record(smt_path),
        "metadata": target_pipeline.artifact_record(metadata_path),
    }


def derive_classification(
    solver_result: str,
    *,
    sat_witness_replayed: bool,
) -> str:
    if solver_result == "unsat":
        return "conditional-complete"
    if solver_result == "sat":
        if not sat_witness_replayed:
            raise RuntimeError("SAT cannot be classified without concrete replay")
        return "conditional-incomplete"
    if solver_result == "unknown":
        return "solver-unknown"
    raise RuntimeError(f"unsupported solver result: {solver_result}")


def run_target(module: Any, z3: str) -> tuple[dict[str, str], dict[str, Any]]:
    row = validate_crosswalk_identity(module)
    evidence_root = EVIDENCE_BASE / module.ARTIFACT_ID
    if evidence_root.exists():
        shutil.rmtree(evidence_root)
    evidence_root.mkdir(parents=True)

    authority_fields = (
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
    authority_path = evidence_root / "authority_bindings.json"
    common.write_json(
        authority_path,
        {
            "schema_version": 1,
            "bindings": {field: row[field] for field in authority_fields},
        },
    )
    bound_inputs_path = evidence_root / "bound_inputs_manifest.json"
    common.write_json(
        bound_inputs_path,
        freeze_bound_inputs(module, row, evidence_root),
    )
    boundary_path = evidence_root / "boundary_manifest.json"
    common.write_json(boundary_path, module.boundary_manifest())

    obligations: dict[str, Any] = {}
    solver_results: dict[str, str] = {}
    for purpose, stem in (
        (module.PRIMARY, "obligation"),
        (module.EXACT_OUTPUT, "exact_output_obligation"),
    ):
        smt_path, record = write_obligation(
            module, evidence_root, purpose, stem
        )
        solver = capture_solver(z3, evidence_root, stem, smt_path)
        record["solver"] = solver
        obligations[purpose] = record
        solver_results[purpose] = str(solver["solver_result"])

    probes: dict[str, Any] = {}
    for name, case in module.PROBE_CASES.items():
        path = evidence_root / "probes" / f"{name}.smt2"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(module.probe_text(name))
        solver = capture_solver(
            z3, evidence_root, f"probes/{name}", path
        )
        if solver["solver_result"] != module.PROBE_EXPECTED_RESULTS[name]:
            raise RuntimeError(
                f"{module.TARGET}/{name}: expected "
                f"{module.PROBE_EXPECTED_RESULTS[name]}, got "
                f"{solver['solver_result']}"
            )
        probes[name] = {
            "kind": case["kind"],
            "expected_solver_result": module.PROBE_EXPECTED_RESULTS[name],
            "smt": target_pipeline.artifact_record(path),
            "solver": solver,
        }

    witness_replayed = False
    witness_record: dict[str, Any] | None = None
    countermodel_record: dict[str, Any] | None = None
    if module is target_026 and solver_results[module.PRIMARY] == "sat":
        witness_path = evidence_root / "witness.json"
        common.write_json(witness_path, target_026.witness_payload())
        semantic = independent_replay.replay_target_026_witness(witness_path)
        witness_replayed = semantic["status"] == "passed"
        witness_record = {
            "artifact": target_pipeline.artifact_record(witness_path),
            "semantic_replay": semantic,
        }
        countermodel_path = evidence_root / "counterexample_model.smt2"
        countermodel_path.write_text(target_026.fixed_model_text())
        countermodel_solver = capture_solver(
            z3,
            evidence_root,
            "counterexample_model",
            countermodel_path,
        )
        if countermodel_solver["solver_result"] != "sat":
            raise RuntimeError("target-026 fixed countermodel is not SAT")
        countermodel_record = {
            "smt": target_pipeline.artifact_record(countermodel_path),
            "solver": countermodel_solver,
        }
    elif solver_results[module.PRIMARY] == "sat":
        raise RuntimeError(
            f"{module.TARGET}: unexpected SAT lacks a replayable witness"
        )

    model = SOURCE_MODELS[module.TARGET]
    if not model.is_file() or "external_body" in model.read_text():
        raise RuntimeError(f"{module.TARGET}: Verus model is missing or trusted")
    captured_model = evidence_root / "verus/source_model.rs"
    captured_model.parent.mkdir(parents=True)
    shutil.copyfile(model, captured_model)
    typecheck = target_pipeline.capture_command(
        evidence_root / "verus/typecheck",
        [str(common.VERUS), str(captured_model), "--crate-type=lib", "--no-verify"],
        cwd=common.OUT,
    )
    if (
        typecheck["exit_code"] != 0
        or (common.OUT / typecheck["stderr"]).read_text()
    ):
        raise RuntimeError(f"{module.TARGET}: Verus type-check failed")
    verification = target_pipeline.capture_command(
        evidence_root / "verus/verification",
        [str(common.VERUS), str(captured_model), "--crate-type=lib"],
        cwd=common.OUT,
    )
    verification_stdout = (common.OUT / verification["stdout"]).read_text()
    if (
        verification["exit_code"] != 0
        or (common.OUT / verification["stderr"]).read_text()
        or "0 errors" not in verification_stdout
    ):
        raise RuntimeError(f"{module.TARGET}: Verus verification failed")

    primary_status = derive_classification(
        solver_results[module.PRIMARY],
        sat_witness_replayed=witness_replayed,
    )
    exact_status = derive_classification(
        solver_results[module.EXACT_OUTPUT],
        sat_witness_replayed=False,
    )
    statuses = {
        "exact_output_determinism_status": exact_status,
        "completeness_modulo_reviewed_equivalence_status": primary_status,
    }
    result: dict[str, Any] = {
        "schema_version": 1,
        "target": module.TARGET,
        "input_order": module.INPUT_ORDER,
        "artifact_id": module.ARTIFACT_ID,
        "active_contract_sha256": module.ACTIVE_CONTRACT_SHA256,
        "active_contract_text": module.ACTIVE_CONTRACT_TEXT,
        "authority_bindings": target_pipeline.artifact_record(authority_path),
        "bound_inputs": target_pipeline.artifact_record(bound_inputs_path),
        "boundary_manifest": target_pipeline.artifact_record(boundary_path),
        "classification": statuses,
        "obligations": obligations,
        "satisfiability_probes": probes,
        "verus": {
            "source_model": target_pipeline.artifact_record(model),
            "captured_model": target_pipeline.artifact_record(captured_model),
            "typecheck": typecheck,
            "verification": verification,
        },
        "updated_crosswalk_fields": list(target_pipeline.RESULT_FIELDS),
    }
    if witness_record is not None:
        result["witness"] = witness_record
    if countermodel_record is not None:
        result["counterexample_model"] = countermodel_record
    common.write_json(evidence_root / "result.json", result)
    return statuses, result


def update_ledgers_atomically(
    statuses_by_target: dict[str, dict[str, str]],
) -> None:
    csv_path = common.OUT / "crosswalk/target_to_proof_boundary.csv"
    json_path = common.OUT / "crosswalk/target_to_proof_boundary.json"
    csv_rows = common.read_csv(csv_path)
    json_rows = json.loads(json_path.read_text())
    preserved = copy.deepcopy(BASELINE_RESULTS)
    current_by_key = {_row_key(row): row for row in csv_rows}
    for key, expected in LATER_RESULTS.items():
        actual = {
            field: current_by_key[key][field]
            for field in target_pipeline.RESULT_FIELDS
        }
        if actual == expected:
            preserved[key] = expected
    updated_csv = csv_rows
    updated_json = json_rows
    for module in TARGET_MODULES:
        updated_csv, updated_json = target_pipeline.apply_crosswalk_result_update(
            updated_csv,
            updated_json,
            target=module.TARGET,
            input_order=module.INPUT_ORDER,
            statuses=statuses_by_target[module.TARGET],
            preserved_results=preserved,
        )
        preserved[(module.TARGET, module.INPUT_ORDER)] = statuses_by_target[
            module.TARGET
        ]

    common.write_csv(csv_path, updated_csv, list(updated_csv[0]))
    common.write_json(json_path, updated_json)

    classified = {
        (row["target"], row["input_order"])
        for row in updated_csv
        if any(
            row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS
        )
    }
    if classified != set(preserved):
        raise RuntimeError("cluster changed the classified target set")
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in updated_csv
    )
    expected_classified = 22 + sum(
        key in preserved for key in LATER_RESULTS
    )
    expected_not_run = 62 - expected_classified
    if len(classified) != expected_classified or not_run != expected_not_run:
        raise RuntimeError(
            f"expected {expected_classified} classified and "
            f"{expected_not_run} not-run, got "
            f"{len(classified)} and {not_run}"
        )


def main() -> None:
    z3 = shutil.which("z3")
    if not z3:
        raise RuntimeError("z3 is required for the MaybeUninit cluster")
    if not common.VERUS.is_file():
        raise RuntimeError(f"Verus executable is missing: {common.VERUS}")

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
    mutable_roots = {
        module.ARTIFACT_ID: EVIDENCE_BASE / module.ARTIFACT_ID
        for module in TARGET_MODULES
    }
    mutable_roots["maybeuninit_lifecycle_cluster"] = CLUSTER_ROOT
    for artifact_id, root in mutable_roots.items():
        if not root.is_dir():
            raise ValueError(f"delivered evidence is missing: {artifact_id}")

    (common.OUT / "logs").mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".maybeuninit-lifecycle-cluster-backup-",
        dir=common.OUT / "logs",
    ) as backup_directory:
        backup_root = Path(backup_directory)
        for artifact_id, root in mutable_roots.items():
            shutil.copytree(root, backup_root / artifact_id)
        try:
            _write_crosswalks(reset_csv, reset_json)
            shutil.rmtree(CLUSTER_ROOT)
            CLUSTER_ROOT.mkdir(parents=True)

            statuses_by_target: dict[str, dict[str, str]] = {}
            target_results: dict[str, Any] = {}
            for module in TARGET_MODULES:
                statuses, result = run_target(module, z3)
                statuses_by_target[module.TARGET] = statuses
                target_results[module.TARGET] = {
                    "artifact_id": module.ARTIFACT_ID,
                    "classification": statuses,
                    "result": target_pipeline.artifact_record(
                        EVIDENCE_BASE / module.ARTIFACT_ID / "result.json"
                    ),
                }

            replay = target_pipeline.capture_command(
                CLUSTER_ROOT / "independent_replay",
                [
                    sys.executable,
                    str(
                        common.OUT
                        / "tools/replay_maybeuninit_lifecycle_cluster.py"
                    ),
                    "--evidence-root",
                    str(EVIDENCE_BASE),
                    "--z3",
                    z3,
                ],
                cwd=common.OUT,
            )
            replay_stdout = (common.OUT / replay["stdout"]).read_text()
            replay_stderr = (common.OUT / replay["stderr"]).read_text()
            if replay["exit_code"] != 0 or replay_stderr:
                raise RuntimeError("independent cluster replay failed")
            try:
                replay_result = json.loads(replay_stdout)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    "independent replay did not emit JSON"
                ) from exc
            if replay_result.get("status") != "passed":
                raise RuntimeError("independent replay did not report passed")
            replay["result"] = replay_result

            update_ledgers_atomically(statuses_by_target)
            after_csv, after_json = _load_crosswalks()
            expected_after = copy.deepcopy(before_csv)
            expected_by_key = {
                _row_key(row): row for row in expected_after
            }
            for key in CLUSTER_KEYS:
                expected_by_key[key].update(DELIVERED_RESULTS[key])
            if (
                after_csv != expected_after
                or after_json != expected_after
            ):
                raise RuntimeError(
                    "cluster replay changed unexpected crosswalk cells"
                )

            preserved_after = {
                artifact_id: tree_digest(root)
                for artifact_id, root in preserved_roots.items()
            }
            if preserved_after != preserved_before:
                raise RuntimeError("cluster mutated a certified evidence tree")

            manifest = {
                "schema_version": 1,
                "execution_order": [
                    target_026.TARGET,
                    target_119.TARGET,
                    target_025.TARGET,
                ],
                "targets": target_results,
                "independent_solver_and_witness_replay": replay,
                "preserved_certified_evidence": {
                    artifact_id: {
                        "before_sha256": preserved_before[artifact_id],
                        "after_sha256": preserved_after[artifact_id],
                    }
                    for artifact_id in PRESERVED_ARTIFACT_IDS
                },
                "classified_rows": len(BASELINE_RESULTS)
                + len(DELIVERED_RESULTS)
                + sum(
                    key in {
                        _row_key(row)
                        for row in before_csv
                        if any(
                            row[field] != "not-run"
                            for field in target_pipeline.RESULT_FIELDS
                        )
                    }
                    for key in LATER_RESULTS
                ),
                "not_run_rows": 62
                - (
                    len(BASELINE_RESULTS)
                    + len(DELIVERED_RESULTS)
                    + sum(
                        key in {
                            _row_key(row)
                            for row in before_csv
                            if any(
                                row[field] != "not-run"
                                for field in target_pipeline.RESULT_FIELDS
                            )
                        }
                        for key in LATER_RESULTS
                    )
                ),
                "stage_transition": "not-authorized",
            }
            common.write_json(CLUSTER_ROOT / "manifest.json", manifest)
        except BaseException:
            try:
                _write_crosswalks(before_csv, before_json)
                for artifact_id, root in mutable_roots.items():
                    if root.exists():
                        shutil.rmtree(root)
                    shutil.copytree(backup_root / artifact_id, root)
            except Exception as restore_exc:
                raise RuntimeError(
                    "cluster replay failed and rollback was incomplete"
                ) from restore_exc
            raise

    print("maybeuninit_lifecycle_cluster=PASS")
    for module in TARGET_MODULES:
        statuses = statuses_by_target[module.TARGET]
        print(
            f"{module.INPUT_ORDER}_exact="
            f"{statuses['exact_output_determinism_status']}"
        )
        print(
            f"{module.INPUT_ORDER}_full="
            f"{statuses['completeness_modulo_reviewed_equivalence_status']}"
        )
    print("independent_replay=passed")
    print("verus_models=3_clean")
    print("preserved_evidence_trees=19")
    final_rows, _ = _load_crosswalks()
    final_classified = sum(
        any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in final_rows
    )
    print(f"classified={final_classified} not_run={62 - final_classified}")


if __name__ == "__main__":
    main()
