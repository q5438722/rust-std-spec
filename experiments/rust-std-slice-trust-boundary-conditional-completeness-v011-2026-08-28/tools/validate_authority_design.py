#!/usr/bin/env python3
"""Independently validate the bounded Slice UNKNOWN authority/design package."""

from __future__ import annotations

import copy
import csv
import io
import json
import re
import shlex
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import campaign_common as common
from checker_guards import GuardError, example_obligation, validate_obligation
import pointer_target_pipeline
import pointer_target_validation
import search_target_validation
import chunk_target_validation
import chunk_contract_drift_cluster
import clone_effect_cluster
import clone_effect_cluster_validation
import exact_mutable_iterator_partition_validation
import exact_mutable_iterator_partitions
import maybeuninit_lifecycle_validation
import mutable_edge_extraction
import mutable_edge_extraction_validation
import mutable_fixed_chunk_edge_validation
import mutable_fixed_chunk_edges
import mutable_iterator_constructor_validation
import mutable_iterator_constructors
import split_at_mut_primitive_validation
import split_at_mut_primitives
import split_off_pair
import split_off_pair_validation
import raw_slice_pair
import raw_slice_pair_validation
import slice_index_trio
import slice_index_trio_validation
import address_observer_pair
import address_observer_pair_validation
import mutable_view_construction_cluster
import mutable_view_construction_validation
import align_to_pair
import align_to_pair_validation
import selection_method_validation
import selection_callback_validation
import unstable_sort_companion_validation
import replay_target_028
import replay_target_030
import replay_target_065
import replay_target_019
import replay_target_020
import replay_target_021
import replay_target_013
import replay_target_022
import replay_target_029
import replay_target_051
import replay_target_052
import replay_target_081
import replay_target_106
import replay_target_120
import run_target_013
import run_target_019
import run_target_020
import run_target_022
import run_target_021
import run_target_051
import run_target_052
import run_target_081
import run_target_106
import run_target_120
import run_search_family_cluster
import run_target_028
import run_target_030
import run_target_065
import target_pipeline
import target_013
import target_019
import target_020
import target_022
import target_021
import target_029
import target_051
import target_052
import target_081
import target_080
import target_082
import target_106
import target_120
import target_025
import target_026
import target_119
import target_028
import target_030
import target_065
import target_077
import target_078
import target_079


OUT = common.OUT
EXPECTED_REASON_COUNTS = {
    "iterator-or-subslice-state-boundary": 24,
    "raw-pointer-provenance-boundary": 13,
    "mutable-reference-view-boundary": 7,
    "unstable-sort-or-selection-boundary": 6,
    "duplicate-or-callback-search-boundary": 4,
    "maybeuninit-storage-boundary": 4,
    "clone-or-callback-effect-boundary": 2,
    "disjoint-mutable-alias-boundary": 2,
}
REQUIRED_LOGS = (
    "01_compileall",
    "02_unit_tests",
    "03_builder",
    "04_theorem_template_z3",
    "05_target_029_pipeline",
    "06_target_013_pipeline",
    "07_target_106_pipeline",
    "08_target_081_pipeline",
    "09_target_022_pipeline",
    "10_target_120_pipeline",
    "16_target_051_pipeline",
    "17_target_052_pipeline",
    "18_target_019_pipeline",
    "19_target_021_pipeline",
    "20_target_020_pipeline",
    "21_pointer_cast_cluster_replay",
    "23_target_028_pipeline",
    "24_target_030_pipeline",
    "25_target_065_pipeline",
    "26_search_family_cluster_replay",
    "27_chunk_contract_drift_cluster_replay",
    "28_maybeuninit_lifecycle_cluster",
    "29_unstable_sort_companions",
    "30_target_077_pipeline",
    "31_selection_callback_cluster",
    "32_mutable_iterator_constructor_cluster",
    "33_mutable_edge_extraction_cluster",
    "34_clone_effect_cluster",
    "35_exact_mutable_iterator_partition_cluster",
    "36_mutable_fixed_chunk_edge_cluster",
    "37_split_at_mut_primitive_cluster",
    "38_split_off_pair_cluster",
    "39_raw_slice_pair_cluster",
    "40_slice_index_trio",
    "41_address_observer_pair",
    "42_mutable_view_construction_cluster",
    "43_align_to_pair",
    "11_slice_inventory",
    "12_slice_catalog",
    "13_slice_contracts",
    "14_slice_provenance",
    "15_implproof_aggregate",
)
EXPECTED_DEPENDENCY_AUDIT_SHA256 = (
    "af4c1296d61382a5ea3fbe6377ee85785321afbde5cc770d6637952507fb1495"
)
EXPECTED_EXTERNAL_AUDIT_SHA256 = (
    "f05a969973f468d656c3f7e63a681dde9ea7761aceb5896d65f4004b1c56cc89"
)
EXPECTED_EXTERNAL_CATEGORY_RECORD_IDS = {
    "complete-target-postcondition": frozenset(
        """
TS-048-E001 TS-049-E001 TS-054-E001 TS-055-E001 TS-026-E001 TS-025-E001
TS-047-E001 TS-052-E001 TS-086-E002 TS-015-E002 TS-017-E004
""".split()
    ),
    "complete-branch-postcondition": frozenset(
        """
TS-008-E005 TS-008-E006 TS-009-E003 TS-009-E004 TS-018-E002 TS-046-E002
TS-085-E002 TS-051-E002 TS-039-E003 TS-039-E004 TS-039-E005 TS-111-E002
TS-111-E003 TS-111-E004
""".split()
    ),
    "answer-equivalent-result": frozenset(
        """
TS-022-E001 TS-020-E001 TS-028-E001 TS-028-E003 TS-030-E001 TS-030-E002
TS-065-E001 TS-051-E001 TS-120-E005
""".split()
    ),
    "opaque-whole-algorithm": frozenset(
        """
TS-077-E001 TS-078-E001 TS-079-E001 TS-080-E001 TS-081-E001 TS-082-E001
""".split()
    ),
    "pointer-layout-provenance-transition": frozenset(
        """
TS-008-E003 TS-009-E002 TS-014-E001 TS-014-E002 TS-015-E001 TS-017-E003
TS-018-E001 TS-046-E001 TS-090-E003 TS-039-E002 TS-120-E002 TS-120-E003
TS-120-E004 TS-120-E001
""".split()
    ),
    "intermediate-raw-slice-constructor": frozenset(
        "TS-012-E001 TS-013-E001 TS-085-E001 TS-086-E001 TS-090-E001".split()
    ),
    "intermediate-subrange-split": frozenset(
        "TS-012-E002 TS-013-E002 TS-090-E002".split()
    ),
    "derived-borrow-source-callee": frozenset(
        """
TS-012-E003 TS-013-E003 TS-023-E001 TS-024-E001 TS-062-E001 TS-090-E004
TS-096-E001 TS-119-E003 TS-120-E006 TS-008-E004
""".split()
    ),
    "arithmetic-or-offset-fact": frozenset(
        "TS-008-E001 TS-009-E001 TS-008-E002 TS-017-E002".split()
    ),
    "panic-edge": frozenset(
        "TS-017-E001 TS-039-E001 TS-111-E001".split()
    ),
    "callback-or-element-effect": frozenset(
        """
TS-028-E002 TS-029-E001 TS-029-E002 TS-037-E001 TS-043-E001 TS-119-E001
TS-119-E002
""".split()
    ),
}
EXPECTED_INADMISSIBLE_EXTERNAL_CATEGORIES = {
    "complete-target-postcondition",
    "complete-branch-postcondition",
    "answer-equivalent-result",
    "opaque-whole-algorithm",
}
EXPECTED_EXTERNAL_POLICY = {
    "complete-target-postcondition": (
        "inadmissible-complete-target-postcondition",
        "complete-target",
    ),
    "complete-branch-postcondition": (
        "inadmissible-complete-branch-postcondition",
        "complete-on-target-branch",
    ),
    "answer-equivalent-result": (
        "inadmissible-answer-equivalent-result",
        "answer-equivalent",
    ),
    "opaque-whole-algorithm": (
        "inadmissible-opaque-whole-algorithm",
        "complete-target-or-final-state",
    ),
    "pointer-layout-provenance-transition": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "intermediate-raw-slice-constructor": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "intermediate-subrange-split": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "derived-borrow-source-callee": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "arithmetic-or-offset-fact": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "panic-edge": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
    "callback-or-element-effect": (
        "admissible-source-backed-lower-boundary",
        "partial-or-lower-level",
    ),
}
EXPECTED_EXTERNAL_CATEGORY_COUNTS = {
    category: len(record_ids)
    for category, record_ids in EXPECTED_EXTERNAL_CATEGORY_RECORD_IDS.items()
}

TARGET_RESULT_LABELS = (
    "013_exact-output-complete/full-incomplete",
    "019_conditional-complete",
    "020_conditional-complete",
    "021_conditional-complete",
    "022_conditional-complete",
    "029_conditional-incomplete",
    "051_conditional-incomplete",
    "052_conditional-incomplete",
    "028_conditional-incomplete",
    "030_conditional-incomplete",
    "065_conditional-incomplete",
    "012_conditional-complete",
    "014_conditional-complete",
    "015_exact-output-complete/full-incomplete",
    "023_conditional-complete",
    "024_exact-output-complete/full-incomplete",
    "081_conditional-incomplete",
    "106_conditional-complete",
    "077_exact-incomplete/modulo-selection-complete",
    "078_missing-source-backed-model",
    "079_missing-source-backed-model",
    "080_exact-incomplete/modulo-equal-Ord-complete",
    "082_exact-incomplete/modulo-equal-key-complete",
    "120_conditional-complete",
    "025_conditional-complete",
    "026_exact-output-complete/full-incomplete",
    "119_conditional-complete",
    "032_conditional-complete",
    "036_conditional-complete",
    "069_conditional-complete",
    "074_conditional-complete",
    "076_conditional-complete",
    "093_conditional-complete",
    "098_conditional-complete",
    "091_conditional-complete",
    "097_conditional-complete",
    "101_conditional-complete",
    "103_conditional-complete",
    "037_conditional-complete",
    "043_conditional-complete",
    "035_conditional-complete",
    "068_conditional-complete",
    "062_conditional-complete",
    "090_conditional-complete",
    "096_conditional-complete",
    "085_conditional-complete",
    "086_conditional-complete",
    "099_conditional-complete",
    "104_conditional-complete",
    "048_conditional-complete",
    "049_exact-output-complete/full-incomplete",
    "053_conditional-incomplete",
    "054_conditional-complete",
    "055_conditional-incomplete",
    "039_conditional-complete",
    "111_conditional-complete",
    "017_exact-output-complete/full-incomplete",
    "018_exact-output-complete/full-incomplete",
    "046_exact-output-complete/full-incomplete",
    "047_exact-output-complete/full-incomplete",
    "008_conditional-complete",
    "009_exact-output-complete/full-incomplete",
)


def target_result_counts(
    rows: list[dict[str, str]],
) -> tuple[int, int]:
    classified = sum(
        any(row[field] != "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    not_run = sum(
        all(row[field] == "not-run" for field in target_pipeline.RESULT_FIELDS)
        for row in rows
    )
    return classified, not_run


def target_results_summary(rows: list[dict[str, str]]) -> str:
    _, not_run = target_result_counts(rows)
    return f"target_results={','.join(TARGET_RESULT_LABELS)},{not_run}_not-run"


def target_result_count_summary(rows: list[dict[str, str]]) -> str:
    classified, not_run = target_result_counts(rows)
    return f"target_result_counts={classified}_classified,{not_run}_not-run"
EXPECTED_EXTERNAL_CATEGORY_BY_RECORD_ID = {
    record_id: category
    for category, record_ids in EXPECTED_EXTERNAL_CATEGORY_RECORD_IDS.items()
    for record_id in record_ids
}
EXPECTED_INTRINSIC_DEPENDENCIES = {
    "TS-019-D001": (
        "core::slice::as_mut_ptr",
        "self as *mut [T] as *mut T",
    ),
    "TS-021-D001": (
        "core::slice::as_ptr",
        "self as *const [T] as *const T",
    ),
    "TS-053-D001": ("core::slice::get_mut", ""),
}
EXPECTED_INADMISSIBLE_TARGETS = {
    "core::slice::align_to",
    "core::slice::align_to_mut",
    "core::slice::as_chunks_unchecked_mut",
    "core::slice::as_flattened_mut",
    "core::slice::as_mut_array",
    "core::slice::as_mut_ptr",
    "core::slice::as_mut_ptr_range",
    "core::slice::as_ptr",
    "core::slice::as_ptr_range",
    "core::slice::assume_init_drop",
    "core::slice::assume_init_mut",
    "core::slice::binary_search",
    "core::slice::binary_search_by_key",
    "core::slice::element_offset",
    "core::slice::first_chunk_mut",
    "core::slice::from_mut",
    "core::slice::from_raw_parts",
    "core::slice::from_raw_parts_mut",
    "core::slice::get_disjoint_mut",
    "core::slice::get_disjoint_unchecked_mut",
    "core::slice::get_mut",
    "core::slice::get_unchecked",
    "core::slice::get_unchecked_mut",
    "core::slice::partition_point",
    "core::slice::select_nth_unstable",
    "core::slice::select_nth_unstable_by",
    "core::slice::select_nth_unstable_by_key",
    "core::slice::sort_unstable",
    "core::slice::sort_unstable_by",
    "core::slice::sort_unstable_by_key",
    "core::slice::split_at_mut_checked",
    "core::slice::split_at_mut_unchecked",
    "core::slice::subslice_range",
    "core::slice::write_copy_of_slice",
}
REQUIRED_ANSWER_BEARING_FRAGMENTS = {
    "TS-048-E001": "slice_from_raw_parts_result",
    "TS-049-E001": "slice_from_raw_parts_mut_result",
    "TS-054-E001": "slice_index_result",
    "TS-055-E001": "slice_index_mut_frame",
    "TS-008-E005": "slice_align_to_result",
    "TS-009-E003": "slice_align_to_mut_result",
    "TS-039-E003": "slice_element_offset_option_result",
    "TS-111-E002": "slice_subslice_range_option_result",
    "TS-077-E001": "slice_select_partition_ord",
    "TS-080-E001": "slice_sorted_by_ord",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def independently_derive(errors: list[str]) -> dict[str, Any]:
    manifest = load_json(common.LATEST_MANIFEST)
    catalog = read_csv(common.CATALOG)
    proof = [
        row for row in read_csv(common.TARGETS_180) if row.get("module") == "slice"
    ]
    order = [
        row for row in read_csv(common.PROOF_ORDER) if row.get("module") == "slice"
    ]
    manifest_rows = manifest.get("results", [])
    catalog_by_target = {row["target"]: row for row in catalog}
    proof_by_target = {row["target"]: row for row in proof}
    order_by_target = {row["target"]: row for row in order}
    generated = {
        row["target"] for row in catalog if row["status"] == common.GENERATED_STATUS
    }
    exact_vstd = {
        row["target"] for row in catalog if row["status"] == common.EXACT_VSTD_STATUS
    }
    manifest_targets = {row["target"] for row in manifest_rows}
    r0_counts = Counter(row.get("r0_z3") for row in manifest_rows)
    selected_rows = [
        row
        for row in manifest_rows
        if row.get("r0_z3") == "unknown"
        and row["target"] in generated
        and catalog_by_target[row["target"]]["status"] == common.GENERATED_STATUS
    ]
    selected_rows.sort(key=lambda row: int(proof_by_target[row["target"]]["input_order"]))
    selected = {row["target"] for row in selected_rows}
    unsat = {
        row["target"] for row in manifest_rows if row.get("r0_z3") == "unsat"
    }

    if len(catalog) != 132:
        errors.append(f"catalog total is {len(catalog)}, expected 132")
    if Counter(row["status"] for row in catalog) != Counter(
        {common.GENERATED_STATUS: 120, common.EXACT_VSTD_STATUS: 12}
    ):
        errors.append("catalog is not 120 generated plus 12 exact-vstd rows")
    if len(manifest_rows) != 120 or manifest_targets != generated:
        errors.append("active manifest does not equal the 120 generated catalog rows")
    if r0_counts != Counter({"unknown": 62, "unsat": 58}):
        errors.append(f"active R0 split is {dict(r0_counts)}, expected 62/58")
    if manifest.get("r0_z3_counts") != dict(r0_counts):
        errors.append("manifest headline R0 counts do not match independently counted rows")
    if len(selected) != 62 or len(selected_rows) != 62:
        errors.append("selected active UNKNOWN set is not 62 unique targets")
    if selected & unsat or selected & exact_vstd:
        errors.append("selected targets overlap UNSAT or exact-vstd rows")
    if any(not target.startswith("core::slice::") for target in selected):
        errors.append("selected target set contains a non-core::slice namespace")
    if any(
        token in target
        for target in selected
        for token in ("alloc::vec", "Array", "Option", "String")
    ):
        errors.append("selected target set leaks an excluded family")
    if not selected <= set(proof_by_target) or not selected <= set(order_by_target):
        errors.append("selected targets are missing proof inventory/order bindings")
    if Counter(row["unknown_reason_class"] for row in selected_rows) != Counter(
        EXPECTED_REASON_COUNTS
    ):
        errors.append("selected reason-class partition differs from active 62-row split")
    return {
        "manifest": manifest,
        "manifest_rows": manifest_rows,
        "catalog": catalog,
        "catalog_by_target": catalog_by_target,
        "proof_by_target": proof_by_target,
        "order_by_target": order_by_target,
        "selected_rows": selected_rows,
        "selected": selected,
        "generated": generated,
        "exact_vstd": exact_vstd,
        "unsat": unsat,
    }


def independently_scan_external_bodies(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text().splitlines()
    sites: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        if not re.search(r"#\s*\[\s*verifier::external_body\s*\]", line):
            continue
        found = None
        for cursor in range(index + 1, min(len(lines), index + 50)):
            match = re.search(r"\bfn\s+([A-Za-z_][A-Za-z0-9_]*)", lines[cursor])
            if match:
                found = {
                    "attribute_line": index + 1,
                    "declaration_line": cursor + 1,
                    "symbol": match.group(1),
                }
                break
        if found is None:
            raise ValueError(f"{path}:{index + 1}: unresolved external_body")
        declaration_index = found["declaration_line"] - 1
        contract_lines: list[str] = []
        contract_end_line: int | None = None
        contract_clause_seen = False
        for cursor in range(declaration_index, min(len(lines), declaration_index + 120)):
            line = lines[cursor]
            code = line.split("//", 1)[0]
            stripped = code.strip()
            if stripped.startswith(
                ("requires", "recommends", "ensures", "returns", "decreases")
            ):
                contract_clause_seen = True
            body_opens = (
                "{" in code
                and (
                    cursor == declaration_index
                    or stripped.startswith("{")
                    or not contract_clause_seen
                )
            )
            if body_opens:
                prefix = line[: line.index("{")].rstrip()
                if prefix:
                    contract_lines.append(prefix)
                contract_end_line = cursor + 1
                break
            contract_lines.append(line.rstrip())
        if contract_end_line is None:
            raise ValueError(
                f"{path}:{declaration_index + 1}: external_body contract has no body"
            )
        found["contract_end_line"] = contract_end_line
        found["contract_text"] = "\n".join(contract_lines).strip() + "\n"
        sites.append(found)
    return sites


def validate_parallel_formats(
    errors: list[str],
    csv_path: Path,
    json_path: Path,
    label: str,
) -> list[dict[str, str]]:
    csv_rows = read_csv(csv_path)
    json_rows = load_json(json_path)
    if csv_rows != json_rows:
        errors.append(f"{label} CSV and JSON are not identical ordered scalar rows")
    return csv_rows


def validate_crosswalk(
    errors: list[str],
    authority: dict[str, Any],
    rows: list[dict[str, str]],
    trust_rows: list[dict[str, str]],
) -> None:
    targets = [row.get("target", "") for row in rows]
    if len(rows) != 62 or len(set(targets)) != 62:
        errors.append("crosswalk does not contain 62 unique target rows")
    if set(targets) != authority["selected"]:
        errors.append("crosswalk target set differs from independently selected UNKNOWN set")

    trust_by_id = {row["record_id"]: row for row in trust_rows}
    if len(trust_by_id) != len(trust_rows):
        errors.append("trust-site inventory contains duplicate record IDs")
    declarations = common.bind_generated_declarations(authority["catalog"])
    weak_targets: dict[str, set[str]] = {
        "matching-index-equivalence": set(),
        "equal-key-reordering-equivalence": set(),
    }
    observed_drifts: set[str] = set()
    observed_external_audit_ids: set[str] = set()

    for row in rows:
        target = row["target"]
        if target not in authority["selected"]:
            continue
        active = authority["catalog_by_target"][target]
        proof = authority["proof_by_target"][target]
        order = int(proof["input_order"])
        manifest_row = next(
            item for item in authority["selected_rows"] if item["target"] == target
        )
        paths = common.proof_paths(target, order)

        if row["input_order"] != proof["input_order"]:
            errors.append(f"{target}: input_order mismatch")
        if row["module"] != "slice" or row["abcd_status"] != "B":
            errors.append(f"{target}: expected module=slice and abcd_status=B")
        if row["catalog_status"] != common.GENERATED_STATUS:
            errors.append(f"{target}: selected row is not generated")
        if row["active_r0_z3"] != "unknown":
            errors.append(f"{target}: selected row does not retain active UNKNOWN")
        if row["active_unknown_reason_class"] != manifest_row["unknown_reason_class"]:
            errors.append(f"{target}: unknown reason class mismatch")
        if row["active_contract_text"] != active["contract_text"]:
            errors.append(f"{target}: crosswalk does not carry verbatim active contract")
        if row["active_contract_sha256"] != common.sha256_text(active["contract_text"]):
            errors.append(f"{target}: active contract hash mismatch")
        if row["retained_contract_text"] != proof["contract_text"]:
            errors.append(f"{target}: retained proof contract mismatch")
        if row["retained_contract_sha256"] != proof["contract_sha256"]:
            errors.append(f"{target}: retained proof contract hash mismatch")
        drifted = active["contract_text"] != proof["contract_text"]
        if row["contract_drift"] != ("yes" if drifted else "no"):
            errors.append(f"{target}: contract drift flag mismatch")
        if drifted:
            observed_drifts.add(target)

        declaration = declarations[target]
        source_lines = common.GENERATED_SPECS.read_text().splitlines()
        exact_declaration = (
            "\n".join(
                source_lines[
                    declaration["start_line"] - 1 : declaration["end_line"]
                ]
            )
            + "\n"
        )
        if (
            row["generated_declaration_text"] != exact_declaration
            or row["generated_declaration_sha256"]
            != common.sha256_text(exact_declaration)
            or common.canonical_contract(exact_declaration)
            != common.canonical_contract(active["contract_text"])
        ):
            errors.append(f"{target}: executable generated declaration binding mismatch")

        for key, field, hash_field in (
            ("harness", "harness_path", "harness_sha256"),
            (
                "source_body",
                "source_body_manifest_path",
                "source_body_manifest_sha256",
            ),
            (
                "transformation",
                "transformation_manifest_path",
                "transformation_manifest_sha256",
            ),
            (
                "dependency",
                "dependency_manifest_path",
                "dependency_manifest_sha256",
            ),
        ):
            if row[field] != str(paths[key]) or common.sha256(paths[key]) != row[hash_field]:
                errors.append(f"{target}: {key} path/hash binding mismatch")

        source_body = load_json(paths["source_body"])
        transformation = load_json(paths["transformation"])
        dependency = load_json(paths["dependency"])
        if any(
            payload.get("target") != target
            for payload in (source_body, transformation, dependency)
        ):
            errors.append(f"{target}: a proof manifest binds another target")
        source = common.canonical_source_record(source_body)
        if (
            row["source_path"] != str(source["path"])
            or row["source_file_sha256"] != source["source_file_sha256"]
            or row["source_item_text"] != source["source_item_text"]
            or row["source_item_sha256"] != source["source_item_sha256"]
            or row["public_docs_reference"] != source["public_docs_reference"]
            or row["public_docs_text"] != source["public_docs_text"]
            or row["public_docs_sha256"] != source["public_docs_sha256"]
            or not source["public_docs_text"]
        ):
            errors.append(f"{target}: canonical source item/docs binding mismatch")
        if (
            source["source_file_sha256"] != source_body["source_file_sha256"]
            or source["source_item_sha256"] != source_body["source_item_sha256"]
        ):
            errors.append(f"{target}: proof source hashes differ from Rust 1.96")

        dependency_items = dependency.get("assumptions_and_boundaries", [])
        closure_items = dependency.get("private_helper_callee_closure", [])
        dependency_ids = [
            item for item in row["dependency_record_ids"].split(";") if item
        ]
        closure_ids = [
            item for item in row["private_helper_record_ids"].split(";") if item
        ]
        external_ids = [
            item for item in row["external_body_site_ids"].split(";") if item
        ]
        all_ids = [item for item in row["all_trust_site_ids"].split(";") if item]
        if int(row["dependency_record_count"]) != len(dependency_items):
            errors.append(f"{target}: dependency record count mismatch")
        if int(row["private_helper_record_count"]) != len(closure_items):
            errors.append(f"{target}: private-helper closure count mismatch")
        if all_ids != dependency_ids + closure_ids + external_ids:
            errors.append(f"{target}: all-trust-site ID ordering mismatch")
        if any(identifier not in trust_by_id for identifier in all_ids):
            errors.append(f"{target}: crosswalk references a missing trust-site record")
        if any(identifier not in row["proof_boundary_assumption"] for identifier in all_ids):
            errors.append(f"{target}: proof-boundary statement omits a trust-site ID")

        for index, item in enumerate(dependency_items, start=1):
            identifier = f"TS-{order:03d}-D{index:03d}"
            trust = trust_by_id.get(identifier)
            if (
                trust is None
                or trust["record_type"] != "dependency-manifest-record"
                or load_json_text(trust["raw_record_json"]) != item
            ):
                errors.append(f"{target}: dependency record {index} not expanded exactly")
        for index, item in enumerate(closure_items, start=1):
            identifier = f"TS-{order:03d}-C{index:03d}"
            trust = trust_by_id.get(identifier)
            if (
                trust is None
                or trust["record_type"] != "private-helper-callee"
                or load_json_text(trust["raw_record_json"]) != item
            ):
                errors.append(f"{target}: private helper record {index} mismatch")

        live_external = independently_scan_external_bodies(paths["harness"])
        if int(row["external_body_count"]) != len(live_external):
            errors.append(f"{target}: external-body count mismatch")
        for index, item in enumerate(live_external, start=1):
            identifier = f"TS-{order:03d}-E{index:03d}"
            trust = trust_by_id.get(identifier)
            if (
                trust is None
                or trust["record_type"] != "harness-external-body"
                or trust["name"] != item["symbol"]
                or trust["attribute_line"] != str(item["attribute_line"])
                or trust["declaration_line"] != str(item["declaration_line"])
                or trust["contract_end_line"] != str(item["contract_end_line"])
                or trust["contract_text"] != item["contract_text"]
                or trust["contract_sha256"]
                != common.sha256_text(item["contract_text"])
            ):
                errors.append(f"{target}: external-body site {index} mismatch")
                continue
            dependency_links = [
                value
                for value in trust["matching_dependency_record_ids"].split(";")
                if value
            ]
            if not dependency_links:
                errors.append(f"{target}: {identifier} has no dependency binding")
            for dependency_id in dependency_links:
                dependency_trust = trust_by_id.get(dependency_id)
                if (
                    dependency_trust is None
                    or dependency_trust["target"] != target
                    or dependency_trust["record_type"]
                    != "dependency-manifest-record"
                ):
                    errors.append(
                        f"{target}: {identifier} has invalid dependency link "
                        f"{dependency_id}"
                    )
            if not trust["adjudication_source_citations"]:
                errors.append(f"{target}: {identifier} lacks adjudication citations")
            site_key = (target, item["symbol"])
            observed_external_audit_ids.add(identifier)
            expected_category = EXPECTED_EXTERNAL_CATEGORY_BY_RECORD_ID.get(
                identifier
            )
            if expected_category is None:
                errors.append(
                    f"{target}: {identifier} is absent from the independent "
                    "exhaustive external-site audit"
                )
                continue
            expected_disposition, expected_coverage = EXPECTED_EXTERNAL_POLICY[
                expected_category
            ]
            if (
                trust["semantic_audit_version"]
                != common.TRUST_SEMANTIC_AUDIT_VERSION
                or trust["semantic_audit_category"] != expected_category
                or trust["semantic_disposition"] != expected_disposition
                or trust["target_postcondition_coverage"] != expected_coverage
                or common.EXTERNAL_SITE_SEMANTIC_AUDIT.get(site_key)
                != expected_category
            ):
                errors.append(
                    f"{target}: {identifier} differs from the independently "
                    "enumerated semantic audit"
                )
            expected_fragment = REQUIRED_ANSWER_BEARING_FRAGMENTS.get(identifier)
            if (
                expected_fragment is not None
                and expected_fragment not in item["contract_text"]
            ):
                errors.append(
                    f"{target}: {identifier} no longer contains audited "
                    f"answer-bearing fragment {expected_fragment}"
                )
        target_leaf = target.rsplit("::", 1)[-1]
        common_external = common.external_body_sites(paths["harness"])
        if common.target_function_is_external(
            paths["harness"], target_leaf, common_external
        ):
            errors.append(f"{target}: public target itself is external_body")

        target_trust = [
            trust_by_id[identifier]
            for identifier in all_ids
            if identifier in trust_by_id
        ]
        inadmissible_ids = [
            item["record_id"]
            for item in target_trust
            if item["semantic_disposition"].startswith("inadmissible-")
            or item["semantic_disposition"].startswith("mixed-")
        ]
        context_ids = [
            item["record_id"]
            for item in target_trust
            if item["semantic_disposition"].startswith("context-only-")
        ]
        if int(row["semantically_adjudicated_trust_site_count"]) != len(all_ids):
            errors.append(f"{target}: not every trust-site row was adjudicated")
        if (
            int(row["admissible_boundary_site_count"])
            != len(all_ids) - len(inadmissible_ids) - len(context_ids)
            or int(row["context_only_site_count"]) != len(context_ids)
            or int(row["inadmissible_boundary_site_count"])
            != len(inadmissible_ids)
            or [
                value
                for value in row["inadmissible_trust_site_ids"].split(";")
                if value
            ]
            != inadmissible_ids
        ):
            errors.append(f"{target}: semantic disposition counts/IDs mismatch")
        if row["unlinked_external_body_count"] != "0":
            errors.append(f"{target}: unresolved external-body dependency link")
        expected_admissible = target not in EXPECTED_INADMISSIBLE_TARGETS
        if (
            row["boundary_admissibility"]
            != ("admissible" if expected_admissible else "inadmissible")
            or row["boundary_narrower_than_target"]
            != ("yes" if expected_admissible else "no")
            or not row["boundary_admissibility_rationale"]
            or not row["boundary_narrowness_rationale"]
        ):
            errors.append(f"{target}: incorrect semantic admissibility/narrowness")
        pointer_expectations = {
            identifier: cast
            for identifier, (expected_target, cast) in (
                EXPECTED_INTRINSIC_DEPENDENCIES.items()
            )
            if expected_target == target and cast
        }
        for identifier, canonical_cast in pointer_expectations.items():
            if (
                identifier not in inadmissible_ids
                or canonical_cast not in row["source_item_text"]
                or row["boundary_admissibility"] != "inadmissible"
                or row["boundary_narrower_than_target"] != "no"
            ):
                errors.append(
                    f"{target}: synthetic pointer dependency is not blocked "
                    "against the canonical Rust cast"
                )

        schema = common.BOUNDARY_SCHEMAS[manifest_row["unknown_reason_class"]]
        if (
            row["boundary_schema_id"] != schema["schema_id"]
            or load_json_text(row["boundary_allowed_observations_json"])
            != schema["allowed_observations"]
            or row["boundary_model_requirement"] != schema["model_requirement"]
            or not row["proof_boundary_assumption"].startswith(schema["assumption"])
        ):
            errors.append(f"{target}: boundary schema/assumption mismatch")

        equivalence = common.equivalence_for_target(target)
        if (
            row["equivalence_kind"] != equivalence["kind"]
            or row["equivalence_policy"] != equivalence["exact_observation_policy"]
            or row["equivalence_positive_witness"] != equivalence["positive_witness"]
            or row["equivalence_negative_witness"] != equivalence["negative_witness"]
        ):
            errors.append(f"{target}: equivalence policy mismatch")
        if equivalence["kind"] in weak_targets:
            weak_targets[equivalence["kind"]].add(target)
            if not row["equivalence_source_citation"]:
                errors.append(f"{target}: weak equivalence lacks a source citation")
        elif row["equivalence_source_citation"]:
            errors.append(f"{target}: exact equivalence unexpectedly has weak citation")
        if target in common.SELECTION_TARGETS and row["equivalence_kind"] != (
            "exact-principal-return-and-final-state"
        ):
            errors.append(f"{target}: selection API was weakened")
        expected_results = (
            next(
                config.expected_classification
                for config in align_to_pair.TARGETS
                if config.target == target
            )
            if target in {config.target for config in align_to_pair.TARGETS}
            else
            next(
                config.expected_classification
                for config in address_observer_pair.TARGETS
                if config.target == target
            )
            if target
            in {
                config.target
                for config in address_observer_pair.TARGETS
            }
            else
            next(
                config.expected_classification
                for config in slice_index_trio.TARGETS
                if config.target == target
            )
            if target in {config.target for config in slice_index_trio.TARGETS}
            else
            next(
                config.expected_classification
                for config in raw_slice_pair.TARGETS
                if config.target == target
            )
            if target in {config.target for config in raw_slice_pair.TARGETS}
            else
            next(
                config.expected_classification
                for config in mutable_view_construction_cluster.TARGETS
                if config.target == target
            )
            if target
            in {
                config.target
                for config in mutable_view_construction_cluster.TARGETS
            }
            else
            {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target
            in {
                config.target
                for config in mutable_iterator_constructors.TARGETS
            }
            | {config.target for config in mutable_edge_extraction.TARGETS}
            | {config.target for config in clone_effect_cluster.TARGETS}
            | {
                config.target
                for config in exact_mutable_iterator_partitions.TARGETS
            }
            | {
                config.target
                for config in mutable_fixed_chunk_edges.TARGETS
            }
            | {
                config.target
                for config in split_at_mut_primitives.TARGETS
            }
            | {config.target for config in split_off_pair.TARGETS}
            else
            {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target == target_077.TARGET
            else
            {
                "exact_output_determinism_status": "missing-source-backed-model",
                "completeness_modulo_reviewed_equivalence_status": (
                    "missing-source-backed-model"
                ),
            }
            if target in {target_078.TARGET, target_079.TARGET}
            else
            {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target == target_029.TARGET
            else {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target == target_013.TARGET
            else {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target == target_106.TARGET
            else {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target == target_081.TARGET
            else {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target in {target_080.TARGET, target_082.TARGET}
            else {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target == target_022.TARGET
            else {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target == target_120.TARGET
            else {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target == target_051.TARGET
            else {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target == target_052.TARGET
            else {
                "exact_output_determinism_status": "conditional-complete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-complete"
                ),
            }
            if target
            in {
                target_019.TARGET,
                target_020.TARGET,
                target_021.TARGET,
            }
            else {
                "exact_output_determinism_status": "conditional-incomplete",
                "completeness_modulo_reviewed_equivalence_status": (
                    "conditional-incomplete"
                ),
            }
            if target
            in {
                target_028.TARGET,
                target_030.TARGET,
                target_065.TARGET,
            }
            else chunk_contract_drift_cluster.TARGET_BY_ORDER[
                next(
                    config.input_order
                    for config in chunk_contract_drift_cluster.ORDERED_TARGETS
                    if config.target == target
                )
            ].expected_results
            if target
            in {
                config.target
                for config in chunk_contract_drift_cluster.ORDERED_TARGETS
            }
            else maybeuninit_lifecycle_validation.EXPECTED_RESULTS[target]
            if target
            in {
                target_025.TARGET,
                target_026.TARGET,
                target_119.TARGET,
            }
            else {
                "exact_output_determinism_status": "not-run",
                "completeness_modulo_reviewed_equivalence_status": "not-run",
            }
        )
        if any(row[field] != value for field, value in expected_results.items()):
            errors.append(f"{target}: target result fields do not match campaign scope")

    not_run_count = sum(
        row["exact_output_determinism_status"] == "not-run"
        and row["completeness_modulo_reviewed_equivalence_status"] == "not-run"
        for row in rows
    )
    if not_run_count != 0:
        errors.append(f"crosswalk has {not_run_count} not-run rows instead of 0")

    if observed_drifts != common.EXPECTED_DRIFT_TARGETS:
        errors.append("crosswalk does not reconcile exactly the six active contract drifts")
    if weak_targets["matching-index-equivalence"] != common.BINARY_SEARCH_TARGETS:
        errors.append("matching-index equivalence target set is not the three searches")
    if weak_targets["equal-key-reordering-equivalence"] != common.UNSTABLE_SORT_TARGETS:
        errors.append("equal-key equivalence target set is not the three unstable sorts")
    if observed_external_audit_ids != set(
        EXPECTED_EXTERNAL_CATEGORY_BY_RECORD_ID
    ):
        errors.append("exhaustive external-body semantic audit is incomplete")


def load_json_text(text: str) -> Any:
    return json.loads(text)


def validate_trust_inventory(
    errors: list[str],
    authority: dict[str, Any],
    rows: list[dict[str, str]],
) -> None:
    counts = Counter(row["record_type"] for row in rows)
    live_dependency_count = 0
    live_closure_count = 0
    live_external_count = 0
    live_external_harnesses = 0
    dependency_audit_payload: list[dict[str, Any]] = []
    external_audit_payload: list[dict[str, Any]] = []
    for selected_row in authority["selected_rows"]:
        target = selected_row["target"]
        proof = authority["proof_by_target"][target]
        order = int(proof["input_order"])
        paths = common.proof_paths(target, order)
        dependency = load_json(paths["dependency"])
        dependency_items = dependency.get("assumptions_and_boundaries", [])
        live_dependency_count += len(dependency_items)
        live_closure_count += len(dependency.get("private_helper_callee_closure", []))
        external = independently_scan_external_bodies(paths["harness"])
        live_external_count += len(external)
        live_external_harnesses += bool(external)
        dependency_audit_payload.extend(
            {
                "record_id": f"TS-{order:03d}-D{index:03d}",
                "target": target,
                "record": item,
            }
            for index, item in enumerate(dependency_items, start=1)
        )
        external_audit_payload.extend(
            {
                "record_id": f"TS-{order:03d}-E{index:03d}",
                "target": target,
                "symbol": item["symbol"],
                "contract_text": item["contract_text"],
            }
            for index, item in enumerate(external, start=1)
        )
    if live_dependency_count != 232:
        errors.append(f"live selected dependency record count is {live_dependency_count}")
    if live_external_harnesses != 43:
        errors.append(f"live external-body harness count is {live_external_harnesses}")
    if counts["dependency-manifest-record"] != live_dependency_count:
        errors.append("trust inventory does not expand every dependency record")
    if counts["private-helper-callee"] != live_closure_count:
        errors.append("trust inventory does not expand every private helper closure")
    if counts["harness-external-body"] != live_external_count:
        errors.append("trust inventory does not enumerate every external-body site")
    required_semantic_fields = (
        "semantic_role",
        "semantic_audit_category",
        "semantic_audit_version",
        "semantic_disposition",
        "target_postcondition_coverage",
        "adjudication_rationale",
        "adjudication_source_citations",
    )
    if any(
        not row["name"]
        or not row["rationale"]
        or any(not row[field] for field in required_semantic_fields)
        for row in rows
    ):
        errors.append("a normalized trust-site row lacks semantic adjudication")

    external_rows = [
        row for row in rows if row["record_type"] == "harness-external-body"
    ]
    external_by_key = {
        (row["target"], row["name"]): row for row in external_rows
    }
    if len(external_by_key) != len(external_rows):
        errors.append("external-body target/symbol pairs are not unique")
    if any(
        not row["matching_dependency_record_ids"]
        or not row["contract_text"]
        or row["contract_sha256"] != common.sha256_text(row["contract_text"])
        for row in external_rows
    ):
        errors.append("an external-body site lacks linkage or full contract evidence")
    if len(common.PREVIOUSLY_UNLINKED_EXTERNAL_SITES) != 14 or any(
        key not in external_by_key
        or not external_by_key[key]["matching_dependency_record_ids"]
        for key in common.PREVIOUSLY_UNLINKED_EXTERNAL_SITES
    ):
        errors.append("the 14 former external-body linkage gaps are not resolved")
    get_disjoint_link = external_by_key.get(
        ("core::slice::get_disjoint_mut", "get_disjoint_check_valid")
    )
    if (
        get_disjoint_link is None
        or get_disjoint_link["matching_dependency_record_ids"] != "TS-051-D002"
    ):
        errors.append("get_disjoint_check_valid is not linked to its source helper")

    dependency_rows = [
        row for row in rows if row["record_type"] == "dependency-manifest-record"
    ]
    dependency_by_id = {row["record_id"]: row for row in dependency_rows}
    live_dependency_ids = set(dependency_by_id)
    audited_dependency_sets = (
        set(common.DEPENDENCY_CONTEXT_ONLY_RECORD_IDS),
        set(common.DEPENDENCY_ADMISSIBLE_RECORD_IDS),
        set(common.DEPENDENCY_INTRINSIC_INADMISSIBLE),
    )
    if sum(map(len, audited_dependency_sets)) != len(
        set().union(*audited_dependency_sets)
    ):
        errors.append("dependency semantic-audit categories overlap")
    if set().union(*audited_dependency_sets) != live_dependency_ids:
        errors.append("dependency semantic audit does not cover exactly the live IDs")
    if set(common.DEPENDENCY_INTRINSIC_INADMISSIBLE) != set(
        EXPECTED_INTRINSIC_DEPENDENCIES
    ):
        errors.append(
            "intrinsic dependency audit is not the three independently "
            "reviewed answer-equivalent records"
        )
    for identifier, (target, _) in EXPECTED_INTRINSIC_DEPENDENCIES.items():
        row = dependency_by_id.get(identifier)
        if row is None or row["target"] != target:
            errors.append(
                f"{identifier}: intrinsic dependency is not bound to {target}"
            )
    independently_context_only = {
        row["record_id"]
        for row in dependency_rows
        if row["kind"] in {"shared_model_helper", "shared_contract_vocabulary"}
    }
    if independently_context_only != set(
        common.DEPENDENCY_CONTEXT_ONLY_RECORD_IDS
    ):
        errors.append("context-only dependency audit differs from live semantic kinds")

    external_by_dependency: dict[str, list[dict[str, str]]] = {
        identifier: [] for identifier in live_dependency_ids
    }
    for external in external_rows:
        for identifier in external["matching_dependency_record_ids"].split(";"):
            if identifier:
                external_by_dependency.setdefault(identifier, []).append(external)
    for identifier, row in dependency_by_id.items():
        if identifier in common.DEPENDENCY_CONTEXT_ONLY_RECORD_IDS:
            expected = "context-only-specification-vocabulary"
            expected_category = "specification-vocabulary"
        elif identifier in common.DEPENDENCY_INTRINSIC_INADMISSIBLE:
            expected = "inadmissible-answer-equivalent-dependency"
            expected_category = "answer-equivalent-target-dependency"
        else:
            linked = external_by_dependency.get(identifier, [])
            has_inadmissible = any(
                item["semantic_disposition"].startswith("inadmissible-")
                for item in linked
            )
            has_admissible = any(
                item["semantic_disposition"]
                == "admissible-source-backed-lower-boundary"
                for item in linked
            )
            expected_category = "source-backed-support"
            if has_inadmissible and has_admissible:
                expected = "mixed-support-includes-answer-bearing-site"
            elif has_inadmissible:
                expected = "inadmissible-answer-bearing-support"
            else:
                expected = "admissible-source-backed-support"
        if (
            row["semantic_audit_version"]
            != common.TRUST_SEMANTIC_AUDIT_VERSION
            or row["semantic_audit_category"] != expected_category
            or row["semantic_disposition"] != expected
        ):
            errors.append(
                f"{identifier}: dependency disposition does not follow the "
                "exhaustive audit and external linkage"
            )

    dependency_audit_sha256 = common.sha256_text(
        common.json_compact(dependency_audit_payload)
    )
    external_audit_sha256 = common.sha256_text(
        common.json_compact(external_audit_payload)
    )
    if (
        dependency_audit_sha256 != EXPECTED_DEPENDENCY_AUDIT_SHA256
        or common.DEPENDENCY_AUDIT_INPUT_SHA256
        != EXPECTED_DEPENDENCY_AUDIT_SHA256
    ):
        errors.append("dependency audit is not bound to the reviewed frozen input")
    if (
        external_audit_sha256 != EXPECTED_EXTERNAL_AUDIT_SHA256
        or common.EXTERNAL_AUDIT_INPUT_SHA256 != EXPECTED_EXTERNAL_AUDIT_SHA256
    ):
        errors.append("external audit is not bound to complete reviewed contracts")

    expected_dispositions = Counter(
        {
            "context-only-specification-vocabulary": 46,
            "context-only-source-closure": 91,
            "admissible-source-backed-support": 144,
            "admissible-source-backed-lower-boundary": 46,
            "inadmissible-complete-target-postcondition": 11,
            "inadmissible-complete-branch-postcondition": 14,
            "inadmissible-answer-equivalent-result": 9,
            "inadmissible-opaque-whole-algorithm": 6,
            "inadmissible-answer-bearing-support": 34,
            "mixed-support-includes-answer-bearing-site": 5,
            "inadmissible-answer-equivalent-dependency": 3,
        }
    )
    actual_dispositions = Counter(row["semantic_disposition"] for row in rows)
    if actual_dispositions != expected_dispositions:
        errors.append(
            "trust-site semantic disposition partition differs from the "
            "independently expected 409-row adjudication"
        )


def validate_drifts(
    errors: list[str],
    rows: list[dict[str, str]],
) -> None:
    if len(rows) != 6 or {row["target"] for row in rows} != common.EXPECTED_DRIFT_TARGETS:
        errors.append("contract drift table is not exactly the reviewed six targets")
    for row in rows:
        if row["active_contract_text"] == row["retained_contract_text"]:
            errors.append(f"{row['target']}: drift row has equal contracts")
        if "active catalog" not in row["resolution"]:
            errors.append(f"{row['target']}: drift resolution does not name active authority")


def validate_provenance(errors: list[str]) -> None:
    rows = load_json(OUT / "provenance/input_provenance.json")
    allowed_roots = (
        common.SPECGEN.resolve(),
        common.IMPLPROOF.resolve(),
        common.RUST_LIBRARY.resolve(),
    )
    seen: set[tuple[str, str]] = set()
    for row in rows:
        source = Path(row["source_path"])
        frozen = OUT / row["frozen_path"]
        key = (str(source), str(frozen))
        if key in seen:
            errors.append(f"duplicate provenance binding: {source}")
        seen.add(key)
        if not source.is_file() or not frozen.is_file():
            errors.append(f"missing source/frozen provenance file: {source}")
            continue
        if not any(source.resolve().is_relative_to(root) for root in allowed_roots):
            errors.append(f"provenance source escapes allowed read-only inputs: {source}")
        source_hash = common.sha256(source)
        if source_hash != row["sha256"] or common.sha256(frozen) != row["sha256"]:
            errors.append(f"working-tree/frozen provenance hash mismatch: {source}")
        if source.stat().st_size != row["bytes"]:
            errors.append(f"provenance byte count mismatch: {source}")
        if row.get("read_only_input") is not True:
            errors.append(f"provenance input not marked read-only: {source}")
    required_sources = {
        str(common.LATEST_MANIFEST.resolve()),
        str(common.CATALOG.resolve()),
        str(common.GENERATED_SPECS.resolve()),
        str(common.SHARED_VOCABULARY.resolve()),
        str(common.TARGETS_180.resolve()),
        str(common.PROOF_ORDER.resolve()),
    }
    if not required_sources <= {row["source_path"] for row in rows}:
        errors.append("provenance omits a central authority file")


def validate_evidence(errors: list[str]) -> None:
    versions = load_json(OUT / "evidence/tool_versions/manifest.json")
    if {row.get("tool") for row in versions} != {"argus", "z3", "verus"}:
        errors.append("tool-version manifest does not contain Argus, Z3, and Verus")
    expected_fragments = {
        "argus": "0.1.1",
        "z3": "4.12.5",
        "verus": "Version:",
    }
    for row in versions:
        output = (OUT / row["stdout"]).read_text() + (OUT / row["stderr"]).read_text()
        if row["exit_code"] != 0 or expected_fragments[row["tool"]] not in output:
            errors.append(f"{row['tool']}: version capture failed or unexpected")
        for key in ("command", "stdout", "stderr", "status"):
            if not (OUT / row[key]).is_file():
                errors.append(f"{row['tool']}: missing {key} evidence")

    witnesses = load_json(OUT / "evidence/equivalence/witness_manifest.json")
    if len(witnesses) != 4:
        errors.append("equivalence witness manifest does not contain four runs")
    pairs = Counter((row["family"], row["polarity"]) for row in witnesses)
    expected_pairs = Counter(
        {
            ("binary_search_duplicate", "positive"): 1,
            ("binary_search_duplicate", "negative"): 1,
            ("unstable_sort_equal_keys", "positive"): 1,
            ("unstable_sort_equal_keys", "negative"): 1,
        }
    )
    if pairs != expected_pairs:
        errors.append("equivalence witness family/polarity set is incomplete")
    for row in witnesses:
        if row["exit_code"] != 0 or row["solver_result"] != "sat":
            errors.append(
                f"{row['family']}.{row['polarity']}: witness did not replay SAT"
            )
        if not row.get("source_citations"):
            errors.append(f"{row['family']}: witness lacks source citations")
        for key in ("smt", "command", "stdout", "stderr", "status"):
            if not (OUT / row[key]).is_file():
                errors.append(f"{row['family']}: missing witness {key}")
    witness_by_pair = {
        (row["family"], row["polarity"]): row for row in witnesses
    }
    for polarity in ("positive", "negative"):
        row = witness_by_pair.get(("unstable_sort_equal_keys", polarity))
        if row is None:
            continue
        text = (OUT / row["smt"]).read_text()
        if (
            "(SameElementMultiset left right)" not in text
            or "ElementMultiplicity" not in text
        ):
            errors.append(
                f"unstable_sort_equal_keys.{polarity}: relation omits exact multiset"
            )
    negative = witness_by_pair.get(("unstable_sort_equal_keys", "negative"))
    if negative is not None:
        text = (OUT / negative["smt"]).read_text()
        if (
            "(store (store (store base 0 12) 1 10) 2 20)" not in text
            or "(ite (= identity 20) 2 1)" not in text
            or "(assert (not (EqualKeyEquivalent output1 output2)))" not in text
        ):
            errors.append(
                "unstable-sort negative witness does not reject a foreign "
                "same-key identity"
            )


def bounded_target_artifact_ids() -> frozenset[str]:
    return frozenset(
        [
            target_077.ARTIFACT_ID,
            target_078.ARTIFACT_ID,
            target_079.ARTIFACT_ID,
            target_013.ARTIFACT_ID,
            target_019.ARTIFACT_ID,
            target_020.ARTIFACT_ID,
            target_021.ARTIFACT_ID,
            target_022.ARTIFACT_ID,
            target_028.ARTIFACT_ID,
            target_029.ARTIFACT_ID,
            target_030.ARTIFACT_ID,
            target_051.ARTIFACT_ID,
            target_052.ARTIFACT_ID,
            target_065.ARTIFACT_ID,
            target_080.ARTIFACT_ID,
            target_081.ARTIFACT_ID,
            target_082.ARTIFACT_ID,
            target_106.ARTIFACT_ID,
            target_120.ARTIFACT_ID,
            *[
                config.artifact_id
                for config in chunk_contract_drift_cluster.ORDERED_TARGETS
            ],
            target_025.ARTIFACT_ID,
            target_026.ARTIFACT_ID,
            target_119.ARTIFACT_ID,
            *[
                config.artifact_id
                for config in mutable_iterator_constructors.TARGETS
            ],
            *[
                config.artifact_id
                for config in mutable_edge_extraction.TARGETS
            ],
            *[
                config.artifact_id
                for config in clone_effect_cluster.TARGETS
            ],
            *[
                config.artifact_id
                for config in exact_mutable_iterator_partitions.TARGETS
            ],
            *[
                config.artifact_id
                for config in mutable_fixed_chunk_edges.TARGETS
            ],
            *[
                config.artifact_id
                for config in split_at_mut_primitives.TARGETS
            ],
            *[
                config.artifact_id
                for config in split_off_pair.TARGETS
            ],
            *[config.artifact_id for config in raw_slice_pair.TARGETS],
            *[config.artifact_id for config in slice_index_trio.TARGETS],
            *[config.artifact_id for config in address_observer_pair.TARGETS],
            *[
                config.artifact_id
                for config in mutable_view_construction_cluster.TARGETS
            ],
            *[config.artifact_id for config in align_to_pair.TARGETS],
        ]
    )


def validate_bounded_target_evidence_directories(
    target_roots: Path,
    errors: list[str],
) -> None:
    actual = (
        {path.name for path in target_roots.iterdir()}
        if target_roots.is_dir()
        else set()
    )
    if actual != set(bounded_target_artifact_ids()):
        errors.append("target evidence exists outside the bounded target scope")


def validate_target_029_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_029.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 029 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    if (
        result.get("target") != target_029.TARGET
        or result.get("input_order") != target_029.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_029.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_029.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields")
        != sorted(expected_statuses)
    ):
        errors.append("target 029 result identity/classification is malformed")

    target_roots = OUT / "evidence/targets"
    validate_bounded_target_evidence_directories(target_roots, errors)

    def check_artifact(
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

    def check_capture(
        record: Any,
        expected_argv: list[str],
        expected_result: str,
        label: str,
        *,
        require_payload: bool = False,
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        stdout = paths["stdout"].read_text()
        stderr = paths["stderr"].read_text()
        first_line = stdout.splitlines()[0] if stdout.splitlines() else ""
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or stderr != ""
            or first_line != expected_result
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")
        if require_payload and len(stdout.splitlines()) < 2:
            errors.append(f"{label}: SAT model/value payload is missing")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 029 validation cannot locate z3")
        return
    obligation_specs = {
        target_029.PRIMARY: ("obligation", "sat"),
        target_029.SORTED_SANITY: ("sorted_domain_sanity", "unsat"),
        target_029.EXACT_OUTPUT: ("exact_output_obligation", "sat"),
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 029 obligation result set is incomplete")
        obligations = {}
    for purpose, (filename, expected_solver_result) in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 029 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_029.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 029 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 029 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 029 {purpose} metadata",
        )
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            expected_solver_result,
            f"target 029 {purpose}",
        )

    for key, purpose, filename, label in (
        (
            "counterexample_model",
            target_029.PRIMARY,
            "counterexample_model.smt2",
            "target 029 fixed-boundary counterexample",
        ),
        (
            "exact_output_witness",
            target_029.EXACT_OUTPUT,
            "exact_output_witness.smt2",
            "target 029 exact-output witness",
        ),
    ):
        path = root / filename
        evidence = result.get(key)
        if not isinstance(evidence, dict):
            errors.append(f"{label}: result entry is missing")
            continue
        check_artifact(evidence.get("smt"), path, f"{label} SMT")
        if path.is_file() and path.read_text() != target_029.fixed_model_text(
            purpose
        ):
            errors.append(f"{label}: fixed model differs from reviewed witness")
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            label,
            require_payload=True,
        )

    witness_path = root / "witness.json"
    check_artifact(result.get("witness"), witness_path, "target 029 witness")
    if witness_path.is_file():
        try:
            witness = load_json(witness_path)
            if witness != target_029.witness_payload():
                errors.append("target 029 witness differs from reviewed values")
            independent_result = replay_target_029.replay(witness_path)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 029 independent replay failed: {exc}")
            independent_result = None
    else:
        independent_result = None

    replay = result.get("witness_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_029.py"),
        "--witness",
        str(witness_path),
    ]
    if not isinstance(replay, dict):
        errors.append("target 029 witness replay capture is missing")
    else:
        for key in ("command", "stdout", "stderr", "status"):
            path_value = replay.get(key)
            if not isinstance(path_value, str) or not (OUT / path_value).is_file():
                errors.append(f"target 029 replay is missing {key}")
                break
        else:
            replay_stdout = (OUT / replay["stdout"]).read_text()
            replay_stderr = (OUT / replay["stderr"]).read_text()
            try:
                captured_result = json.loads(replay_stdout)
            except json.JSONDecodeError:
                captured_result = None
            if (
                replay.get("argv") != expected_replay_argv
                or (OUT / replay["command"]).read_text()
                != shlex.join(expected_replay_argv) + "\n"
                or replay.get("exit_code") != 0
                or (OUT / replay["status"]).read_text() != "0\n"
                or replay_stderr != ""
                or captured_result != independent_result
                or replay.get("result") != independent_result
            ):
                errors.append("target 029 independent replay capture is invalid")

    frozen_harness = (
        OUT
        / "provenance/frozen/implproof"
        / target_029.ARTIFACT_ID
        / "harness.rs"
    )
    verus_evidence = result.get("verus")
    expected_verus_argv = [
        str(common.VERUS),
        str(frozen_harness),
        "--crate-type=lib",
    ]
    if not isinstance(verus_evidence, dict):
        errors.append("target 029 Verus evidence is missing")
    else:
        check_artifact(
            verus_evidence.get("harness"),
            frozen_harness,
            "target 029 frozen Verus harness",
        )
        run = verus_evidence.get("run")
        if not isinstance(run, dict):
            errors.append("target 029 Verus command capture is missing")
        else:
            for key in ("command", "stdout", "stderr", "status"):
                value = run.get(key)
                if not isinstance(value, str) or not (OUT / value).is_file():
                    errors.append(f"target 029 Verus capture is missing {key}")
                    break
            else:
                stdout = (OUT / run["stdout"]).read_text()
                stderr = (OUT / run["stderr"]).read_text()
                if (
                    run.get("argv") != expected_verus_argv
                    or (OUT / run["command"]).read_text()
                    != shlex.join(expected_verus_argv) + "\n"
                    or run.get("exit_code") != 0
                    or (OUT / run["status"]).read_text() != "0\n"
                    or stderr != ""
                    or "verification results:: 9 verified, 0 errors"
                    not in stdout
                ):
                    errors.append("target 029 frozen Verus replay is invalid")


def validate_target_013_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_013.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 013 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    if (
        result.get("target") != target_013.TARGET
        or result.get("input_order") != target_013.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_013.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_013.ACTIVE_CONTRACT_TEXT
        or result.get("rejected_retained_contract_sha256")
        != target_013.RETAINED_CONTRACT_SHA256
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
    ):
        errors.append("target 013 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_capture(
        record: Any,
        expected_argv: list[str],
        expected_result: str,
        label: str,
        *,
        require_payload: bool = False,
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        stdout = paths["stdout"].read_text()
        stderr = paths["stderr"].read_text()
        lines = stdout.splitlines()
        first_line = lines[0] if lines else ""
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or stderr != ""
            or first_line != expected_result
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")
        if require_payload and len(lines) < 2:
            errors.append(f"{label}: SAT model/value payload is missing")

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    check_artifact(
        result.get("authority_bindings"),
        authority_path,
        "target 013 authority bindings",
    )
    check_artifact(
        result.get("boundary_manifest"),
        boundary_path,
        "target 013 boundary manifest",
    )
    if boundary_path.is_file():
        try:
            if load_json(boundary_path) != target_013.boundary_manifest():
                errors.append("target 013 boundary manifest differs from reviewed policy")
        except json.JSONDecodeError as exc:
            errors.append(f"target 013 boundary manifest is invalid JSON: {exc}")
    if authority_path.is_file():
        try:
            authority_bindings = load_json(authority_path)
            bindings = authority_bindings.get("bindings", {})
            if (
                authority_bindings.get("schema_version") != 1
                or bindings.get("target") != target_013.TARGET
                or bindings.get("input_order") != target_013.INPUT_ORDER
                or bindings.get("active_contract_sha256")
                != target_013.ACTIVE_CONTRACT_SHA256
                or bindings.get("retained_contract_sha256")
                != target_013.RETAINED_CONTRACT_SHA256
                or bindings.get("source_item_sha256")
                != "53fb689ca4c691d2e432cbea572e07fcc1c5cd487734c27f9d0b82841f5b7ae8"
                or set(bindings.get("all_trust_site_ids", "").split(";"))
                != set(target_013.boundary_manifest()["all_audited_trust_site_ids"])
            ):
                errors.append("target 013 authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"target 013 authority bindings are invalid JSON: {exc}")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 013 validation cannot locate z3")
        return
    obligation_specs = {
        target_013.PRIMARY: ("obligation", "sat"),
        target_013.EXACT_OUTPUT: ("exact_output_obligation", "unsat"),
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 013 obligation result set is incomplete")
        obligations = {}
    for purpose, (filename, expected_solver_result) in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 013 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_013.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 013 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 013 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 013 {purpose} metadata",
        )
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            expected_solver_result,
            f"target 013 {purpose}",
        )

    model_path = root / "counterexample_model.smt2"
    model = result.get("counterexample_model")
    if not isinstance(model, dict):
        errors.append("target 013 fixed-boundary model entry is missing")
    else:
        check_artifact(
            model.get("smt"),
            model_path,
            "target 013 fixed-boundary model SMT",
        )
        if model_path.is_file() and model_path.read_text() != target_013.fixed_model_text():
            errors.append("target 013 fixed model differs from reviewed witness")
        check_capture(
            model.get("solver"),
            [z3, "-smt2", str(model_path)],
            "sat",
            "target 013 fixed-boundary model",
            require_payload=True,
        )

    witness_path = root / "witness.json"
    check_artifact(result.get("witness"), witness_path, "target 013 witness")
    if witness_path.is_file():
        try:
            witness = load_json(witness_path)
            if witness != target_013.witness_payload():
                errors.append("target 013 witness differs from reviewed values")
            independent_result = replay_target_013.replay(witness_path)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 013 independent replay failed: {exc}")
            independent_result = None
    else:
        independent_result = None

    replay = result.get("witness_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_013.py"),
        "--witness",
        str(witness_path),
    ]
    if not isinstance(replay, dict):
        errors.append("target 013 witness replay capture is missing")
    else:
        for key in ("command", "stdout", "stderr", "status"):
            value = replay.get(key)
            if not isinstance(value, str) or not (OUT / value).is_file():
                errors.append(f"target 013 replay is missing {key}")
                break
        else:
            try:
                captured_result = json.loads((OUT / replay["stdout"]).read_text())
            except json.JSONDecodeError:
                captured_result = None
            if (
                replay.get("argv") != expected_replay_argv
                or (OUT / replay["command"]).read_text()
                != shlex.join(expected_replay_argv) + "\n"
                or replay.get("exit_code") != 0
                or (OUT / replay["status"]).read_text() != "0\n"
                or (OUT / replay["stderr"]).read_text() != ""
                or captured_result != independent_result
                or replay.get("result") != independent_result
            ):
                errors.append("target 013 independent replay capture is invalid")

    source_harness = OUT / "proofs/013_core_slice_as_chunks_mut.rs"
    harness_path = root / "verus/strengthened_harness.rs"
    verus_evidence = result.get("verus")
    if not isinstance(verus_evidence, dict):
        errors.append("target 013 Verus evidence is missing")
    else:
        check_artifact(
            verus_evidence.get("source_harness"),
            source_harness,
            "target 013 source Verus harness",
        )
        check_artifact(
            verus_evidence.get("harness"),
            harness_path,
            "target 013 captured Verus harness",
        )
        if (
            source_harness.is_file()
            and harness_path.is_file()
            and source_harness.read_bytes() != harness_path.read_bytes()
        ):
            errors.append("target 013 captured Verus harness differs from source")
        for key, extra, expected_summary in (
            ("typecheck", ["--no-verify"], ""),
            ("verification", [], "verification results:: 8 verified, 0 errors"),
        ):
            run = verus_evidence.get(key)
            expected_argv = [
                str(common.VERUS),
                str(harness_path),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 013 Verus {key} capture is missing")
                continue
            capture_paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            if (
                len(capture_paths) != 4
                or any(not path.is_file() for path in capture_paths.values())
                or run.get("argv") != expected_argv
                or capture_paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or capture_paths.get("status", Path()).read_text() != "0\n"
                or capture_paths.get("stderr", Path()).read_text() != ""
                or (
                    expected_summary
                    and expected_summary
                    not in capture_paths.get("stdout", Path()).read_text()
                )
            ):
                errors.append(f"target 013 Verus {key} capture is invalid")

    preservation = result.get("target_029_preservation")
    target_029_root = OUT / "evidence/targets" / target_029.ARTIFACT_ID
    current_digest = (
        run_target_013.tree_digest(target_029_root)
        if target_029_root.is_dir()
        else ""
    )
    if (
        not isinstance(preservation, dict)
        or preservation.get("before_sha256") != preservation.get("after_sha256")
        or preservation.get("after_sha256") != current_digest
    ):
        errors.append("target 013 evidence does not prove target 029 preservation")


def validate_target_106_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_106.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 106 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    }
    if (
        result.get("target") != target_106.TARGET
        or result.get("input_order") != target_106.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_106.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_106.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
    ):
        errors.append("target 106 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_solver_capture(
        record: Any,
        expected_argv: list[str],
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or paths["stdout"].read_text() != "unsat\n"
            or paths["stderr"].read_text() != ""
            or record.get("solver_result") != "unsat"
            or record.get("expected_solver_result") != "unsat"
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    check_artifact(
        result.get("authority_bindings"),
        authority_path,
        "target 106 authority bindings",
    )
    check_artifact(
        result.get("boundary_manifest"),
        boundary_path,
        "target 106 boundary manifest",
    )
    if boundary_path.is_file():
        try:
            if load_json(boundary_path) != target_106.boundary_manifest():
                errors.append("target 106 boundary manifest differs from reviewed policy")
        except json.JSONDecodeError as exc:
            errors.append(f"target 106 boundary manifest is invalid JSON: {exc}")
    if authority_path.is_file():
        try:
            authority_bindings = load_json(authority_path)
            bindings = authority_bindings.get("bindings", {})
            if (
                authority_bindings.get("schema_version") != 1
                or bindings.get("target") != target_106.TARGET
                or bindings.get("input_order") != target_106.INPUT_ORDER
                or bindings.get("active_contract_sha256")
                != target_106.ACTIVE_CONTRACT_SHA256
                or bindings.get("retained_contract_sha256")
                != target_106.ACTIVE_CONTRACT_SHA256
                or bindings.get("source_item_sha256")
                != "16885c97baf3a651ede1ef9e05515ebca484886eae5f110aee3481bd30b3a7ec"
                or set(bindings.get("all_trust_site_ids", "").split(";"))
                != set(target_106.boundary_manifest()["all_audited_trust_site_ids"])
            ):
                errors.append("target 106 authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"target 106 authority bindings are invalid JSON: {exc}")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 106 validation cannot locate z3")
        return
    obligation_specs = {
        target_106.PRIMARY: "obligation",
        target_106.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 106 obligation result set is incomplete")
        obligations = {}
    for purpose, filename in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 106 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_106.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 106 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 106 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 106 {purpose} metadata",
        )
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            f"target 106 {purpose}",
        )

    replay = result.get("solver_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_106.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent_result = replay_target_106.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"target 106 independent replay failed: {exc}")
        independent_result = None
    if not isinstance(replay, dict):
        errors.append("target 106 solver replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 106 independent solver replay capture is invalid")

    source_harness = OUT / "proofs/106_core_slice_splitn_mut.rs"
    harness_path = root / "verus/constructor_harness.rs"
    verus_evidence = result.get("verus")
    if not isinstance(verus_evidence, dict):
        errors.append("target 106 Verus evidence is missing")
    else:
        check_artifact(
            verus_evidence.get("source_harness"),
            source_harness,
            "target 106 source Verus harness",
        )
        check_artifact(
            verus_evidence.get("harness"),
            harness_path,
            "target 106 captured Verus harness",
        )
        if (
            source_harness.is_file()
            and harness_path.is_file()
            and source_harness.read_bytes() != harness_path.read_bytes()
        ):
            errors.append("target 106 captured Verus harness differs from source")
        for key, extra in (
            ("typecheck", ["--no-verify"]),
            ("verification", []),
        ):
            run = verus_evidence.get(key)
            expected_argv = [
                str(common.VERUS),
                str(harness_path),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 106 Verus {key} capture is missing")
                continue
            capture_paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                capture_paths.get("stdout", Path()).read_text()
                if len(capture_paths) == 4
                and all(path.is_file() for path in capture_paths.values())
                else ""
            )
            if (
                len(capture_paths) != 4
                or any(not path.is_file() for path in capture_paths.values())
                or run.get("argv") != expected_argv
                or capture_paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or capture_paths.get("status", Path()).read_text() != "0\n"
                or capture_paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and not re.search(
                        r"verification results:: [1-9][0-9]* verified, 0 errors",
                        stdout,
                    )
                )
            ):
                errors.append(f"target 106 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        target_013.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_029.ARTIFACT_ID
        ),
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 106 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_106.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 106 did not preserve accepted evidence {artifact_id}"
                )


def validate_target_081_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_081.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 081 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    if (
        result.get("target") != target_081.TARGET
        or result.get("input_order") != target_081.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_081.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_081.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_081.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target 081 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_solver_capture(
        record: Any,
        expected_argv: list[str],
        expected_result: str,
        label: str,
        *,
        require_payload: bool = False,
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        stdout = paths["stdout"].read_text()
        first_line = stdout.splitlines()[0] if stdout.splitlines() else ""
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or paths["stderr"].read_text() != ""
            or first_line != expected_result
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")
        if require_payload and len(stdout.splitlines()) < 2:
            errors.append(f"{label}: SAT value payload is missing")

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    check_artifact(
        result.get("authority_bindings"),
        authority_path,
        "target 081 authority bindings",
    )
    check_artifact(
        result.get("boundary_manifest"),
        boundary_path,
        "target 081 boundary manifest",
    )
    if boundary_path.is_file():
        try:
            if load_json(boundary_path) != target_081.boundary_manifest():
                errors.append("target 081 boundary manifest differs from reviewed policy")
        except json.JSONDecodeError as exc:
            errors.append(f"target 081 boundary manifest is invalid JSON: {exc}")

    crosswalk_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    crosswalk_matches = [
        row
        for row in crosswalk_rows
        if row["target"] == target_081.TARGET
        and row["input_order"] == target_081.INPUT_ORDER
    ]
    if len(crosswalk_matches) != 1:
        errors.append("target 081 crosswalk row is absent or duplicated")
    elif authority_path.is_file():
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
        try:
            authority = load_json(authority_path)
            expected_bindings = {
                field: crosswalk_matches[0][field] for field in authority_fields
            }
            if (
                authority.get("schema_version") != 1
                or authority.get("bindings") != expected_bindings
                or expected_bindings["active_contract_sha256"]
                != target_081.ACTIVE_CONTRACT_SHA256
                or expected_bindings["retained_contract_sha256"]
                != target_081.ACTIVE_CONTRACT_SHA256
                or expected_bindings["source_item_sha256"]
                != "92008bd2d8e9d1bb3d95e3585474f6c372dc276528c919693bdfcfd21f8863ed"
            ):
                errors.append("target 081 authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"target 081 authority bindings are invalid JSON: {exc}")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 081 validation cannot locate z3")
        return
    obligation_specs = {
        target_081.PRIMARY: ("obligation", "sat"),
        target_081.TOTAL_ORDER_SANITY: ("total_order_sanity", "unsat"),
        target_081.EXACT_FINAL_SLICE: (
            "exact_final_slice_obligation",
            "sat",
        ),
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 081 obligation result set is incomplete")
        obligations = {}
    for purpose, (filename, expected_solver_result) in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 081 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_081.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 081 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 081 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 081 {purpose} metadata",
        )
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            expected_solver_result,
            f"target 081 {purpose}",
        )

    for key, purpose, filename, label in (
        (
            "general_counterexample_model",
            target_081.PRIMARY,
            "counterexample_model.smt2",
            "target 081 non-total-comparator counterexample",
        ),
        (
            "exact_final_slice_witness",
            target_081.EXACT_FINAL_SLICE,
            "exact_final_slice_witness.smt2",
            "target 081 equal-key exact-final-slice witness",
        ),
    ):
        path = root / filename
        evidence = result.get(key)
        if not isinstance(evidence, dict):
            errors.append(f"{label}: result entry is missing")
            continue
        check_artifact(evidence.get("smt"), path, f"{label} SMT")
        if path.is_file() and path.read_text() != target_081.fixed_model_text(
            purpose
        ):
            errors.append(f"{label}: fixed model differs from reviewed witness")
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            label,
            require_payload=True,
        )

    witness_path = root / "witness.json"
    check_artifact(result.get("witness"), witness_path, "target 081 witness")
    if witness_path.is_file():
        try:
            witness = load_json(witness_path)
            if witness != target_081.witness_payload():
                errors.append("target 081 witness differs from reviewed values")
            independent_result = replay_target_081.replay(witness_path)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 081 independent replay failed: {exc}")
            independent_result = None
    else:
        independent_result = None

    replay = result.get("witness_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_081.py"),
        "--witness",
        str(witness_path),
    ]
    if not isinstance(replay, dict):
        errors.append("target 081 witness replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 081 independent replay capture is invalid")

    source_model = OUT / "proofs/081_core_slice_sort_unstable_by.rs"
    captured_model = root / "verus/contract_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append("target 081 Verus evidence is missing")
    else:
        check_artifact(
            verus.get("source_model"),
            source_model,
            "target 081 source Verus model",
        )
        check_artifact(
            verus.get("captured_model"),
            captured_model,
            "target 081 captured Verus model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append("target 081 captured Verus model differs from source")
        for key, extra in (
            ("typecheck", ["--no-verify"]),
            ("verification", []),
        ):
            run = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 081 Verus {key} capture is missing")
                continue
            capture_paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                capture_paths.get("stdout", Path()).read_text()
                if len(capture_paths) == 4
                and all(path.is_file() for path in capture_paths.values())
                else ""
            )
            if (
                len(capture_paths) != 4
                or any(not path.is_file() for path in capture_paths.values())
                or run.get("argv") != expected_argv
                or capture_paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or capture_paths.get("status", Path()).read_text() != "0\n"
                or capture_paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and "verification results:: 3 verified, 0 errors" not in stdout
                )
            ):
                errors.append(f"target 081 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        target_013.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_029.ARTIFACT_ID
        ),
        target_106.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_106.ARTIFACT_ID
        ),
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 081 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_081.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 081 did not preserve accepted evidence {artifact_id}"
                )


def validate_target_022_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_022.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 022 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    }
    if (
        result.get("target") != target_022.TARGET
        or result.get("input_order") != target_022.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_022.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_022.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_022.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target 022 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_solver_capture(
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or paths["stdout"].read_text() != f"{expected_result}\n"
            or paths["stderr"].read_text() != ""
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")

    crosswalk_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in crosswalk_rows
        if row["target"] == target_022.TARGET
        and row["input_order"] == target_022.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append("target 022 crosswalk row is absent or duplicated")
        return
    row = matches[0]

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    bound_inputs_path = root / "bound_inputs_manifest.json"
    check_artifact(
        result.get("authority_bindings"),
        authority_path,
        "target 022 authority bindings",
    )
    check_artifact(
        result.get("boundary_manifest"),
        boundary_path,
        "target 022 boundary manifest",
    )
    check_artifact(
        result.get("bound_inputs"),
        bound_inputs_path,
        "target 022 bound-input manifest",
    )

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
    if authority_path.is_file():
        try:
            authority = load_json(authority_path)
            expected_bindings = {field: row[field] for field in authority_fields}
            if (
                authority.get("schema_version") != 1
                or authority.get("bindings") != expected_bindings
                or expected_bindings["active_contract_sha256"]
                != target_022.ACTIVE_CONTRACT_SHA256
                or expected_bindings["retained_contract_sha256"]
                != target_022.ACTIVE_CONTRACT_SHA256
                or expected_bindings["source_item_sha256"]
                != "b42ea830188debee4c9145f4e52e8a270861f5c3845a4f1c4a50e006987ed5d7"
                or set(expected_bindings["all_trust_site_ids"].split(";"))
                != set(target_022.ALL_AUDITED_TRUST_SITES)
            ):
                errors.append("target 022 authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"target 022 authority bindings are invalid JSON: {exc}")

    if boundary_path.is_file():
        try:
            if load_json(boundary_path) != target_022.boundary_manifest():
                errors.append("target 022 boundary manifest differs from reviewed policy")
        except json.JSONDecodeError as exc:
            errors.append(f"target 022 boundary manifest is invalid JSON: {exc}")

    if bound_inputs_path.is_file():
        try:
            manifest = load_json(bound_inputs_path)
        except json.JSONDecodeError as exc:
            errors.append(f"target 022 bound-input manifest is invalid JSON: {exc}")
            manifest = {}
        expected_sources = {
            "slice_cast": target_022.CANONICAL_SLICE_CAST_REFERENCE,
            "ptr_add": target_022.CANONICAL_PTR_ADD_REFERENCE,
            "ptr_add_safety": target_022.CANONICAL_PTR_ADD_DOCS_REFERENCE,
            "const_ptr_source_sha256": target_022.CANONICAL_PTR_SOURCE_SHA256,
        }
        if (
            manifest.get("schema_version") != 1
            or manifest.get("canonical_sources") != expected_sources
        ):
            errors.append("target 022 canonical source bindings are malformed")
        expected_bound_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            "slice_as_ptr_range_item.rs": row["source_item_sha256"],
            "slice_as_ptr_range_docs.md": row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row[
                "transformation_manifest_sha256"
            ],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            "canonical_const_ptr_add.rs": (
                target_022.CANONICAL_PTR_ADD_ITEM_SHA256
            ),
            "canonical_ptr_add_safety.md": (
                target_022.CANONICAL_PTR_ADD_DOCS_SHA256
            ),
        }
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != set(
            expected_bound_hashes
        ):
            errors.append("target 022 bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_bound_hashes.items():
            path = root / "bound_inputs" / filename
            check_artifact(
                artifacts.get(filename),
                path,
                f"target 022 bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"target 022 bound input hash changed: {filename}")

    ptr_source = common.RUST_LIBRARY / "core/src/ptr/const_ptr.rs"
    ptr_docs = common.RUST_LIBRARY / "core/src/ptr/docs/add.md"
    if (
        not ptr_source.is_file()
        or common.sha256(ptr_source) != target_022.CANONICAL_PTR_SOURCE_SHA256
        or not ptr_docs.is_file()
        or common.sha256(ptr_docs) != target_022.CANONICAL_PTR_ADD_DOCS_SHA256
    ):
        errors.append("target 022 canonical ptr::add source or docs changed")
    elif (
        "".join(ptr_source.read_text().splitlines(keepends=True)[810:864])
        != (root / "bound_inputs/canonical_const_ptr_add.rs").read_text()
        or ptr_docs.read_bytes()
        != (root / "bound_inputs/canonical_ptr_add_safety.md").read_bytes()
    ):
        errors.append("target 022 target-local ptr::add copies are not canonical")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 022 validation cannot locate z3")
        return
    obligation_specs = {
        target_022.PRIMARY: "obligation",
        target_022.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 022 obligation result set is incomplete")
        obligations = {}
    for purpose, filename in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 022 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_022.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 022 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 022 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 022 {purpose} metadata",
        )
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "unsat",
            f"target 022 {purpose}",
        )

    probes = result.get("satisfiability_probes")
    if not isinstance(probes, dict) or set(probes) != set(
        target_022.PROBE_CASES
    ):
        errors.append("target 022 satisfiability probe set is incomplete")
        probes = {}
    for name, expected_case in target_022.PROBE_CASES.items():
        path = root / "probes" / f"{name}.smt2"
        evidence = probes.get(name)
        if not isinstance(evidence, dict):
            continue
        if evidence.get("case") != expected_case:
            errors.append(f"target 022 {name} probe values changed")
        check_artifact(evidence.get("smt"), path, f"target 022 {name} probe SMT")
        if path.is_file() and path.read_text() != target_022.probe_text(name):
            errors.append(f"target 022 {name} probe differs from reviewed text")
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            target_022.PROBE_EXPECTED_RESULTS[name],
            f"target 022 {name} probe",
        )

    replay = result.get("solver_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_022.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent_result = replay_target_022.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"target 022 independent replay failed: {exc}")
        independent_result = None
    if not isinstance(replay, dict):
        errors.append("target 022 solver replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 022 independent solver replay capture is invalid")

    source_model = OUT / "proofs/022_core_slice_as_ptr_range.rs"
    captured_model = root / "verus/source_transition_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append("target 022 Verus evidence is missing")
    else:
        check_artifact(
            verus.get("source_model"),
            source_model,
            "target 022 source Verus model",
        )
        check_artifact(
            verus.get("captured_model"),
            captured_model,
            "target 022 captured Verus model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append("target 022 captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append("target 022 Verus model contains external_body")
        for key, extra in (
            ("typecheck", ["--no-verify"]),
            ("verification", []),
        ):
            run = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 022 Verus {key} capture is missing")
                continue
            capture_paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                capture_paths.get("stdout", Path()).read_text()
                if len(capture_paths) == 4
                and all(path.is_file() for path in capture_paths.values())
                else ""
            )
            if (
                len(capture_paths) != 4
                or any(not path.is_file() for path in capture_paths.values())
                or run.get("argv") != expected_argv
                or capture_paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or capture_paths.get("status", Path()).read_text() != "0\n"
                or capture_paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and "verification results:: 2 verified, 0 errors" not in stdout
                )
            ):
                errors.append(f"target 022 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        target_013.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_013.ARTIFACT_ID
        ),
        target_029.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_029.ARTIFACT_ID
        ),
        target_081.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_081.ARTIFACT_ID
        ),
        target_106.ARTIFACT_ID: (
            OUT / "evidence/targets" / target_106.ARTIFACT_ID
        ),
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 022 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_022.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 022 did not preserve accepted evidence {artifact_id}"
                )


def validate_target_120_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_120.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 120 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-complete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-complete"
        ),
    }
    if (
        result.get("target") != target_120.TARGET
        or result.get("input_order") != target_120.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_120.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_120.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
        or result.get("remaining_not_run_rows") != 56
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_120.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target 120 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_solver_capture(
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or paths["stdout"].read_text() != f"{expected_result}\n"
            or paths["stderr"].read_text() != ""
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")

    crosswalk_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in crosswalk_rows
        if row["target"] == target_120.TARGET
        and row["input_order"] == target_120.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append("target 120 crosswalk row is absent or duplicated")
        return
    row = matches[0]

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    bound_inputs_path = root / "bound_inputs_manifest.json"
    check_artifact(
        result.get("authority_bindings"),
        authority_path,
        "target 120 authority bindings",
    )
    check_artifact(
        result.get("boundary_manifest"),
        boundary_path,
        "target 120 boundary manifest",
    )
    check_artifact(
        result.get("bound_inputs"),
        bound_inputs_path,
        "target 120 bound-input manifest",
    )

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
    if authority_path.is_file():
        try:
            authority = load_json(authority_path)
            expected_bindings = {field: row[field] for field in authority_fields}
            if (
                authority.get("schema_version") != 1
                or authority.get("bindings") != expected_bindings
                or expected_bindings["active_contract_sha256"]
                != target_120.ACTIVE_CONTRACT_SHA256
                or expected_bindings["retained_contract_sha256"]
                != target_120.ACTIVE_CONTRACT_SHA256
                or set(expected_bindings["all_trust_site_ids"].split(";"))
                != set(target_120.ALL_AUDITED_TRUST_SITES)
                or set(expected_bindings["inadmissible_trust_site_ids"].split(";"))
                != set(target_120.EXCLUDED_RETAINED_TRUST_SITES)
            ):
                errors.append("target 120 authority bindings are incomplete or stale")
        except json.JSONDecodeError as exc:
            errors.append(f"target 120 authority bindings are invalid JSON: {exc}")

    if boundary_path.is_file():
        try:
            if load_json(boundary_path) != target_120.boundary_manifest():
                errors.append("target 120 boundary manifest differs from reviewed policy")
        except json.JSONDecodeError as exc:
            errors.append(f"target 120 boundary manifest is invalid JSON: {exc}")

    if bound_inputs_path.is_file():
        try:
            manifest = load_json(bound_inputs_path)
        except json.JSONDecodeError as exc:
            errors.append(f"target 120 bound-input manifest is invalid JSON: {exc}")
            manifest = {}
        expected_sources = {
            name: {
                "source_path": binding["path"],
                "source_span": f"{binding['start']}-{binding['end']}",
                "source_file_sha256": binding["file_sha256"],
                "excerpt_sha256": binding["excerpt_sha256"],
            }
            for name, binding in target_120.CANONICAL_SOURCE_BINDINGS.items()
        }
        if (
            manifest.get("schema_version") != 1
            or manifest.get("canonical_sources") != expected_sources
        ):
            errors.append("target 120 canonical source bindings are malformed")
        expected_bound_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            "write_copy_of_slice_item.rs": row["source_item_sha256"],
            "write_copy_of_slice_docs.md": row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row[
                "transformation_manifest_sha256"
            ],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            **{
                f"canonical_{name}.rs": binding["excerpt_sha256"]
                for name, binding in target_120.CANONICAL_SOURCE_BINDINGS.items()
            },
        }
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != set(
            expected_bound_hashes
        ):
            errors.append("target 120 bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_bound_hashes.items():
            path = root / "bound_inputs" / filename
            check_artifact(
                artifacts.get(filename),
                path,
                f"target 120 bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"target 120 bound input hash changed: {filename}")
        for name, binding in target_120.CANONICAL_SOURCE_BINDINGS.items():
            source = common.RUST_LIBRARY / binding["path"]
            captured = root / "bound_inputs" / f"canonical_{name}.rs"
            if (
                not source.is_file()
                or common.sha256(source) != binding["file_sha256"]
                or not captured.is_file()
            ):
                errors.append(f"target 120 canonical {name} source changed")
                continue
            lines = source.read_text().splitlines(keepends=True)
            excerpt = "".join(lines[binding["start"] - 1 : binding["end"]])
            if captured.read_text() != excerpt:
                errors.append(f"target 120 canonical {name} copy is stale")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 120 validation cannot locate z3")
        return
    obligation_specs = {
        target_120.PRIMARY: "obligation",
        target_120.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 120 obligation result set is incomplete")
        obligations = {}
    for purpose, filename in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 120 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_120.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 120 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 120 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 120 {purpose} metadata",
        )
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "unsat",
            f"target 120 {purpose}",
        )

    probes = result.get("satisfiability_probes")
    if not isinstance(probes, dict) or set(probes) != set(
        target_120.PROBE_CASES
    ):
        errors.append("target 120 satisfiability probe set is incomplete")
        probes = {}
    for name, case in target_120.PROBE_CASES.items():
        path = root / "probes" / f"{name}.smt2"
        evidence = probes.get(name)
        if not isinstance(evidence, dict):
            continue
        if (
            evidence.get("kind") != case["kind"]
            or evidence.get("expected_solver_result")
            != target_120.PROBE_EXPECTED_RESULTS[name]
        ):
            errors.append(f"target 120 {name} probe metadata changed")
        check_artifact(evidence.get("smt"), path, f"target 120 {name} probe SMT")
        if path.is_file() and path.read_text() != target_120.probe_text(name):
            errors.append(f"target 120 {name} probe differs from reviewed text")
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            target_120.PROBE_EXPECTED_RESULTS[name],
            f"target 120 {name} probe",
        )

    replay = result.get("solver_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_120.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent_result = replay_target_120.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"target 120 independent replay failed: {exc}")
        independent_result = None
    if not isinstance(replay, dict):
        errors.append("target 120 solver replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 120 independent solver replay capture is invalid")

    source_model = OUT / "proofs/120_core_slice_write_copy_of_slice.rs"
    captured_model = root / "verus/per_slot_source_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append("target 120 Verus evidence is missing")
    else:
        check_artifact(
            verus.get("source_model"),
            source_model,
            "target 120 source Verus model",
        )
        check_artifact(
            verus.get("captured_model"),
            captured_model,
            "target 120 captured Verus model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append("target 120 captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append("target 120 Verus model contains external_body")
        for key, extra in (
            ("typecheck", ["--no-verify"]),
            ("verification", []),
        ):
            run = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 120 Verus {key} capture is missing")
                continue
            capture_paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                capture_paths.get("stdout", Path()).read_text()
                if len(capture_paths) == 4
                and all(path.is_file() for path in capture_paths.values())
                else ""
            )
            if (
                len(capture_paths) != 4
                or any(not path.is_file() for path in capture_paths.values())
                or run.get("argv") != expected_argv
                or capture_paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or capture_paths.get("status", Path()).read_text() != "0\n"
                or capture_paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and "verification results:: 3 verified, 0 errors" not in stdout
                )
            ):
                errors.append(f"target 120 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        artifact_id: OUT / "evidence/targets" / artifact_id
        for artifact_id in (
            target_013.ARTIFACT_ID,
            target_022.ARTIFACT_ID,
            target_029.ARTIFACT_ID,
            target_081.ARTIFACT_ID,
            target_106.ARTIFACT_ID,
        )
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 120 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_120.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 120 did not preserve accepted evidence {artifact_id}"
                )


def validate_target_051_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_051.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 051 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    if (
        result.get("target") != target_051.TARGET
        or result.get("input_order") != target_051.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_051.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_051.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
        or result.get("remaining_not_run_rows") != 55
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_051.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target 051 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_solver_capture(
        record: Any,
        expected_argv: list[str],
        expected_result: str,
        label: str,
        *,
        require_payload: bool = False,
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        stdout_lines = paths["stdout"].read_text().splitlines()
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or not stdout_lines
            or stdout_lines[0] != expected_result
            or paths["stderr"].read_text() != ""
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: solver capture is not an exact clean replay")
        if require_payload and len(stdout_lines) < 2:
            errors.append(f"{label}: SAT model/value payload is missing")

    crosswalk_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in crosswalk_rows
        if row["target"] == target_051.TARGET
        and row["input_order"] == target_051.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append("target 051 crosswalk row is absent or duplicated")
        return
    row = matches[0]

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    bound_inputs_path = root / "bound_inputs_manifest.json"
    witness_path = root / "witness.json"
    for descriptor, path, label in (
        (result.get("authority_bindings"), authority_path, "authority bindings"),
        (result.get("boundary_manifest"), boundary_path, "boundary manifest"),
        (result.get("bound_inputs"), bound_inputs_path, "bound-input manifest"),
        (result.get("witness"), witness_path, "witness"),
    ):
        check_artifact(descriptor, path, f"target 051 {label}")

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
    if authority_path.is_file():
        authority = load_json(authority_path)
        expected_bindings = {field: row[field] for field in authority_fields}
        if (
            authority.get("schema_version") != 1
            or authority.get("bindings") != expected_bindings
            or set(expected_bindings["all_trust_site_ids"].split(";"))
            != set(target_051.ALL_AUDITED_TRUST_SITES)
            or set(expected_bindings["inadmissible_trust_site_ids"].split(";"))
            != set(target_051.EXCLUDED_RETAINED_TRUST_SITES)
        ):
            errors.append("target 051 authority bindings are incomplete or stale")

    if boundary_path.is_file():
        manifest = load_json(boundary_path)
        if manifest != target_051.boundary_manifest():
            errors.append("target 051 boundary manifest differs from reviewed policy")
        shared = json.dumps(
            manifest.get("shared_boundary_observations", []),
            sort_keys=True,
        )
        for forbidden in (
            "validity bit",
            "error kind",
            "returned borrow",
            "alias map",
            "resulting state",
            "execution trace",
        ):
            if forbidden in shared:
                errors.append(
                    f"target 051 shared boundary contains forbidden {forbidden}"
                )

    if bound_inputs_path.is_file():
        manifest = load_json(bound_inputs_path)
        expected_sources = {
            name: {
                "source_path": binding["path"],
                "source_span": f"{binding['start']}-{binding['end']}",
                "source_file_sha256": binding["file_sha256"],
                "excerpt_sha256": binding["excerpt_sha256"],
            }
            for name, binding in target_051.CANONICAL_SOURCE_BINDINGS.items()
        }
        if (
            manifest.get("schema_version") != 1
            or manifest.get("canonical_sources") != expected_sources
        ):
            errors.append("target 051 canonical source bindings are malformed")
        expected_bound_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            "get_disjoint_mut_item.rs": row["source_item_sha256"],
            "get_disjoint_mut_docs.md": row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row[
                "transformation_manifest_sha256"
            ],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            **{
                f"canonical_{name}.rs": binding["excerpt_sha256"]
                for name, binding in target_051.CANONICAL_SOURCE_BINDINGS.items()
            },
        }
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != set(
            expected_bound_hashes
        ):
            errors.append("target 051 bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_bound_hashes.items():
            path = root / "bound_inputs" / filename
            check_artifact(
                artifacts.get(filename),
                path,
                f"target 051 bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"target 051 bound input hash changed: {filename}")
        for name, binding in target_051.CANONICAL_SOURCE_BINDINGS.items():
            source = common.RUST_LIBRARY / binding["path"]
            captured = root / "bound_inputs" / f"canonical_{name}.rs"
            if (
                not source.is_file()
                or common.sha256(source) != binding["file_sha256"]
                or not captured.is_file()
            ):
                errors.append(f"target 051 canonical {name} source changed")
                continue
            lines = source.read_text().splitlines(keepends=True)
            excerpt = "".join(lines[binding["start"] - 1 : binding["end"]])
            if captured.read_text() != excerpt:
                errors.append(f"target 051 canonical {name} copy is stale")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 051 validation cannot locate z3")
        return
    obligation_specs = {
        target_051.PRIMARY: "obligation",
        target_051.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 051 obligation result set is incomplete")
        obligations = {}
    for purpose, filename in obligation_specs.items():
        smt_path = root / f"{filename}.smt2"
        metadata_path = root / f"{filename}.metadata.json"
        if not smt_path.is_file() or not metadata_path.is_file():
            errors.append(f"target 051 {purpose}: obligation files are missing")
            continue
        try:
            metadata = load_json(metadata_path)
            target_051.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 051 {purpose}: checker rejected obligation: {exc}")
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 051 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 051 {purpose} metadata",
        )
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "sat",
            f"target 051 {purpose}",
        )

    fixed = result.get("fixed_witnesses")
    if not isinstance(fixed, dict) or set(fixed) != set(
        target_051.WITNESS_CASES
    ):
        errors.append("target 051 fixed witness set is incomplete")
        fixed = {}
    for name in target_051.WITNESS_CASES:
        path = root / "witnesses" / f"{name}.smt2"
        evidence = fixed.get(name)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), path, f"target 051 {name} SMT")
        if path.is_file() and path.read_text() != target_051.fixed_witness_text(
            name
        ):
            errors.append(f"target 051 {name} differs from reviewed witness")
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            f"target 051 {name}",
            require_payload=True,
        )

    probes = result.get("rejection_probes")
    if not isinstance(probes, dict) or set(probes) != set(
        target_051.PROBE_CASES
    ):
        errors.append("target 051 rejection probe set is incomplete")
        probes = {}
    for name, case in target_051.PROBE_CASES.items():
        path = root / "probes" / f"{name}.smt2"
        evidence = probes.get(name)
        if not isinstance(evidence, dict):
            continue
        expected = target_051.PROBE_EXPECTED_RESULTS[name]
        if (
            evidence.get("kind") != case["kind"]
            or evidence.get("expected_solver_result") != expected
        ):
            errors.append(f"target 051 {name} probe metadata changed")
        check_artifact(evidence.get("smt"), path, f"target 051 {name} probe SMT")
        if path.is_file() and path.read_text() != target_051.probe_text(name):
            errors.append(f"target 051 {name} probe differs from reviewed text")
        check_solver_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            expected,
            f"target 051 {name} probe",
        )

    if witness_path.is_file() and load_json(witness_path) != target_051.witness_payload():
        errors.append("target 051 witness payload differs from reviewed values")
    replay = result.get("solver_replay")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_051.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent_result = replay_target_051.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"target 051 independent replay failed: {exc}")
        independent_result = None
    if not isinstance(replay, dict):
        errors.append("target 051 solver replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 051 independent solver replay capture is invalid")

    source_model = OUT / "proofs/051_core_slice_get_disjoint_mut.rs"
    captured_model = root / "verus/source_and_contract_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append("target 051 Verus evidence is missing")
    else:
        check_artifact(
            verus.get("source_model"),
            source_model,
            "target 051 source Verus model",
        )
        check_artifact(
            verus.get("captured_model"),
            captured_model,
            "target 051 captured Verus model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append("target 051 captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append("target 051 Verus model contains external_body")
        for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
            run = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 051 Verus {key} capture is missing")
                continue
            paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                paths.get("stdout", Path()).read_text()
                if len(paths) == 4 and all(path.is_file() for path in paths.values())
                else ""
            )
            if (
                len(paths) != 4
                or any(not path.is_file() for path in paths.values())
                or run.get("argv") != expected_argv
                or paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or paths.get("status", Path()).read_text() != "0\n"
                or paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and "verification results:: 5 verified, 0 errors" not in stdout
                )
            ):
                errors.append(f"target 051 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        artifact_id: OUT / "evidence/targets" / artifact_id
        for artifact_id in (
            target_013.ARTIFACT_ID,
            target_022.ARTIFACT_ID,
            target_029.ARTIFACT_ID,
            target_081.ARTIFACT_ID,
            target_106.ARTIFACT_ID,
            target_120.ARTIFACT_ID,
        )
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 051 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_051.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 051 did not preserve accepted evidence {artifact_id}"
                )


def validate_target_052_evidence(errors: list[str]) -> None:
    root = OUT / "evidence/targets" / target_052.ARTIFACT_ID
    result_path = root / "result.json"
    if not result_path.is_file():
        errors.append("target 052 result evidence is missing")
        return
    result = load_json(result_path)
    expected_statuses = {
        "exact_output_determinism_status": "conditional-incomplete",
        "completeness_modulo_reviewed_equivalence_status": (
            "conditional-incomplete"
        ),
    }
    if (
        result.get("target") != target_052.TARGET
        or result.get("input_order") != target_052.INPUT_ORDER
        or result.get("active_contract_sha256")
        != target_052.ACTIVE_CONTRACT_SHA256
        or result.get("active_contract_text") != target_052.ACTIVE_CONTRACT_TEXT
        or result.get("classification") != expected_statuses
        or result.get("updated_crosswalk_fields") != sorted(expected_statuses)
        or result.get("remaining_not_run_rows") != 54
        or set(result.get("excluded_retained_trust_site_ids", []))
        != set(target_052.EXCLUDED_RETAINED_TRUST_SITES)
    ):
        errors.append("target 052 result identity/classification is malformed")

    def check_artifact(descriptor: Any, path: Path, label: str) -> None:
        if not isinstance(descriptor, dict) or not path.is_file():
            errors.append(f"{label}: missing artifact or descriptor")
            return
        if (
            descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256") != common.sha256(path)
            or descriptor.get("bytes") != path.stat().st_size
        ):
            errors.append(f"{label}: artifact path/hash/size mismatch")

    def check_capture(
        record: Any,
        expected_argv: list[str],
        expected_result: str,
        label: str,
        *,
        require_payload: bool = False,
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
            paths[key] = OUT / value
            if not paths[key].is_file():
                errors.append(f"{label}: missing {key} capture")
                return
        stdout_lines = paths["stdout"].read_text().splitlines()
        if (
            record.get("argv") != expected_argv
            or paths["command"].read_text() != shlex.join(expected_argv) + "\n"
            or record.get("exit_code") != 0
            or paths["status"].read_text() != "0\n"
            or not stdout_lines
            or stdout_lines[0] != expected_result
            or paths["stderr"].read_text() != ""
            or record.get("solver_result") != expected_result
            or record.get("expected_solver_result") != expected_result
        ):
            errors.append(f"{label}: command capture is not an exact clean replay")
        if require_payload and len(stdout_lines) < 2:
            errors.append(f"{label}: SAT witness payload is missing")

    crosswalk_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    matches = [
        row
        for row in crosswalk_rows
        if row["target"] == target_052.TARGET
        and row["input_order"] == target_052.INPUT_ORDER
    ]
    if len(matches) != 1:
        errors.append("target 052 crosswalk row is absent or duplicated")
        return
    row = matches[0]

    authority_path = root / "authority_bindings.json"
    boundary_path = root / "boundary_manifest.json"
    bound_inputs_path = root / "bound_inputs_manifest.json"
    witness_path = root / "witness.json"
    for descriptor, path, label in (
        (result.get("authority_bindings"), authority_path, "authority bindings"),
        (result.get("boundary_manifest"), boundary_path, "boundary manifest"),
        (result.get("bound_inputs"), bound_inputs_path, "bound-input manifest"),
        (result.get("witness"), witness_path, "witness"),
    ):
        check_artifact(descriptor, path, f"target 052 {label}")

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
    if authority_path.is_file():
        authority = load_json(authority_path)
        expected_bindings = {field: row[field] for field in authority_fields}
        if (
            authority.get("schema_version") != 1
            or authority.get("bindings") != expected_bindings
            or set(expected_bindings["all_trust_site_ids"].split(";"))
            != set(target_052.ALL_AUDITED_TRUST_SITES)
            or set(expected_bindings["inadmissible_trust_site_ids"].split(";"))
            != set(target_052.EXCLUDED_RETAINED_TRUST_SITES)
        ):
            errors.append("target 052 authority bindings are incomplete or stale")

    if boundary_path.is_file():
        manifest = load_json(boundary_path)
        if manifest != target_052.boundary_manifest():
            errors.append("target 052 boundary manifest differs from reviewed policy")
        shared = json.dumps(
            manifest.get("shared_boundary_observations", []),
            sort_keys=True,
        )
        for forbidden in (
            "returned borrow",
            "resulting state",
            "canonical answer",
            "initialization result",
            "execution trace",
        ):
            if forbidden in shared:
                errors.append(
                    f"target 052 shared boundary contains forbidden {forbidden}"
                )

    if bound_inputs_path.is_file():
        manifest = load_json(bound_inputs_path)
        expected_sources = {
            name: {
                "source_path": binding["path"],
                "source_span": f"{binding['start']}-{binding['end']}",
                "source_file_sha256": binding["file_sha256"],
                "excerpt_sha256": binding["excerpt_sha256"],
            }
            for name, binding in target_052.CANONICAL_SOURCE_BINDINGS.items()
        }
        if (
            manifest.get("schema_version") != 1
            or manifest.get("canonical_sources") != expected_sources
        ):
            errors.append("target 052 canonical source bindings are malformed")
        expected_hashes = {
            "active_contract.txt": row["active_contract_sha256"],
            "generated_declaration.rs": row["generated_declaration_sha256"],
            "get_disjoint_unchecked_mut_item.rs": row["source_item_sha256"],
            "get_disjoint_unchecked_mut_docs.md": row["public_docs_sha256"],
            "implproof_harness.rs": row["harness_sha256"],
            "transformation_manifest.json": row[
                "transformation_manifest_sha256"
            ],
            "dependency_assumption_manifest.json": row[
                "dependency_manifest_sha256"
            ],
            "source_body.json": row["source_body_manifest_sha256"],
            **{
                f"canonical_{name}.rs": binding["excerpt_sha256"]
                for name, binding in target_052.CANONICAL_SOURCE_BINDINGS.items()
            },
        }
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != set(
            expected_hashes
        ):
            errors.append("target 052 bound-input artifact set is incomplete")
            artifacts = {}
        for filename, expected_hash in expected_hashes.items():
            path = root / "bound_inputs" / filename
            check_artifact(
                artifacts.get(filename),
                path,
                f"target 052 bound input {filename}",
            )
            if path.is_file() and common.sha256(path) != expected_hash:
                errors.append(f"target 052 bound input hash changed: {filename}")
        for name, binding in target_052.CANONICAL_SOURCE_BINDINGS.items():
            source = common.RUST_LIBRARY / binding["path"]
            captured = root / "bound_inputs" / f"canonical_{name}.rs"
            if (
                not source.is_file()
                or common.sha256(source) != binding["file_sha256"]
                or not captured.is_file()
            ):
                errors.append(f"target 052 canonical {name} source changed")
                continue
            lines = source.read_text().splitlines(keepends=True)
            excerpt = "".join(lines[binding["start"] - 1 : binding["end"]])
            if captured.read_text() != excerpt:
                errors.append(f"target 052 canonical {name} copy is stale")

    z3 = shutil.which("z3")
    if not z3:
        errors.append("target 052 validation cannot locate z3")
        return
    obligation_specs = {
        target_052.PRIMARY: "obligation",
        target_052.EXACT_OUTPUT: "exact_output_obligation",
    }
    obligations = result.get("obligations")
    if not isinstance(obligations, dict) or set(obligations) != set(
        obligation_specs
    ):
        errors.append("target 052 obligation result set is incomplete")
        obligations = {}
    for purpose, stem in obligation_specs.items():
        smt_path = root / f"{stem}.smt2"
        metadata_path = root / f"{stem}.metadata.json"
        try:
            metadata = load_json(metadata_path)
            target_052.validate_target_obligation(smt_path.read_text(), metadata)
        except (GuardError, OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"target 052 {purpose}: checker rejected obligation: {exc}")
            continue
        evidence = obligations.get(purpose)
        if not isinstance(evidence, dict):
            errors.append(f"target 052 {purpose}: result descriptor is missing")
            continue
        check_artifact(evidence.get("smt"), smt_path, f"target 052 {purpose} SMT")
        check_artifact(
            evidence.get("metadata"),
            metadata_path,
            f"target 052 {purpose} metadata",
        )
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(smt_path)],
            "sat",
            f"target 052 {purpose}",
        )

    fixed = result.get("fixed_witnesses")
    if not isinstance(fixed, dict) or set(fixed) != set(
        target_052.WITNESS_CASES
    ):
        errors.append("target 052 fixed witness set is incomplete")
        fixed = {}
    for name in target_052.WITNESS_CASES:
        path = root / "witnesses" / f"{name}.smt2"
        evidence = fixed.get(name)
        if not isinstance(evidence, dict):
            continue
        check_artifact(evidence.get("smt"), path, f"target 052 {name} SMT")
        if path.is_file() and path.read_text() != target_052.fixed_witness_text(
            name
        ):
            errors.append(f"target 052 {name} differs from reviewed witness")
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            "sat",
            f"target 052 {name}",
            require_payload=True,
        )

    probes = result.get("rejection_probes")
    if not isinstance(probes, dict) or set(probes) != set(
        target_052.PROBE_CASES
    ):
        errors.append("target 052 rejection probe set is incomplete")
        probes = {}
    for name, case in target_052.PROBE_CASES.items():
        path = root / "probes" / f"{name}.smt2"
        evidence = probes.get(name)
        if not isinstance(evidence, dict):
            continue
        expected = target_052.PROBE_EXPECTED_RESULTS[name]
        if (
            evidence.get("kind") != case["kind"]
            or evidence.get("expected_solver_result") != expected
        ):
            errors.append(f"target 052 {name} probe metadata changed")
        check_artifact(evidence.get("smt"), path, f"target 052 {name} probe SMT")
        if path.is_file() and path.read_text() != target_052.probe_text(name):
            errors.append(f"target 052 {name} probe differs from reviewed text")
        check_capture(
            evidence.get("solver"),
            [z3, "-smt2", str(path)],
            expected,
            f"target 052 {name} probe",
        )

    if witness_path.is_file() and load_json(
        witness_path
    ) != target_052.witness_payload():
        errors.append("target 052 witness payload differs from reviewed values")
    expected_replay_argv = [
        sys.executable,
        str(OUT / "tools/replay_target_052.py"),
        "--evidence-root",
        str(root),
        "--z3",
        z3,
    ]
    try:
        independent_result = replay_target_052.replay(root, z3)
    except (GuardError, OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"target 052 independent replay failed: {exc}")
        independent_result = None
    replay = result.get("solver_replay")
    if not isinstance(replay, dict):
        errors.append("target 052 solver replay capture is missing")
    else:
        replay_paths = {
            key: OUT / replay.get(key, "")
            for key in ("command", "stdout", "stderr", "status")
            if isinstance(replay.get(key), str)
        }
        try:
            captured_result = json.loads(
                replay_paths.get("stdout", Path()).read_text()
            )
        except (OSError, json.JSONDecodeError):
            captured_result = None
        if (
            len(replay_paths) != 4
            or any(not path.is_file() for path in replay_paths.values())
            or replay.get("argv") != expected_replay_argv
            or replay_paths.get("command", Path()).read_text()
            != shlex.join(expected_replay_argv) + "\n"
            or replay.get("exit_code") != 0
            or replay_paths.get("status", Path()).read_text() != "0\n"
            or replay_paths.get("stderr", Path()).read_text() != ""
            or captured_result != independent_result
            or replay.get("result") != independent_result
        ):
            errors.append("target 052 independent solver replay capture is invalid")

    source_model = OUT / "proofs/052_core_slice_get_disjoint_unchecked_mut.rs"
    captured_model = root / "verus/source_and_contract_model.rs"
    verus = result.get("verus")
    if not isinstance(verus, dict):
        errors.append("target 052 Verus evidence is missing")
    else:
        check_artifact(
            verus.get("source_model"),
            source_model,
            "target 052 source Verus model",
        )
        check_artifact(
            verus.get("captured_model"),
            captured_model,
            "target 052 captured Verus model",
        )
        if (
            source_model.is_file()
            and captured_model.is_file()
            and source_model.read_bytes() != captured_model.read_bytes()
        ):
            errors.append("target 052 captured Verus model differs from source")
        if source_model.is_file() and "external_body" in source_model.read_text():
            errors.append("target 052 Verus model contains external_body")
        for key, extra in (("typecheck", ["--no-verify"]), ("verification", [])):
            run = verus.get(key)
            expected_argv = [
                str(common.VERUS),
                str(captured_model),
                "--crate-type=lib",
                *extra,
            ]
            if not isinstance(run, dict):
                errors.append(f"target 052 Verus {key} capture is missing")
                continue
            paths = {
                name: OUT / run.get(name, "")
                for name in ("command", "stdout", "stderr", "status")
                if isinstance(run.get(name), str)
            }
            stdout = (
                paths.get("stdout", Path()).read_text()
                if len(paths) == 4 and all(path.is_file() for path in paths.values())
                else ""
            )
            if (
                len(paths) != 4
                or any(not path.is_file() for path in paths.values())
                or run.get("argv") != expected_argv
                or paths.get("command", Path()).read_text()
                != shlex.join(expected_argv) + "\n"
                or run.get("exit_code") != 0
                or paths.get("status", Path()).read_text() != "0\n"
                or paths.get("stderr", Path()).read_text() != ""
                or (
                    key == "verification"
                    and "verification results:: 4 verified, 0 errors" not in stdout
                )
            ):
                errors.append(f"target 052 Verus {key} capture is invalid")

    preservation = result.get("preserved_target_evidence")
    expected_roots = {
        artifact_id: OUT / "evidence/targets" / artifact_id
        for artifact_id in (
            target_013.ARTIFACT_ID,
            target_022.ARTIFACT_ID,
            target_029.ARTIFACT_ID,
            target_051.ARTIFACT_ID,
            target_081.ARTIFACT_ID,
            target_106.ARTIFACT_ID,
            target_120.ARTIFACT_ID,
        )
    }
    if not isinstance(preservation, dict) or set(preservation) != set(
        expected_roots
    ):
        errors.append("target 052 preservation evidence is incomplete")
    else:
        for artifact_id, preserved_root in expected_roots.items():
            record = preservation.get(artifact_id)
            current_digest = (
                run_target_052.tree_digest(preserved_root)
                if preserved_root.is_dir()
                else ""
            )
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != record.get("after_sha256")
                or record.get("after_sha256") != current_digest
            ):
                errors.append(
                    f"target 052 did not preserve accepted evidence {artifact_id}"
                )


def validate_design_and_logs(errors: list[str]) -> None:
    smt_path = OUT / "crosswalk/conditional_theorem_template.smt2"
    metadata_path = OUT / "crosswalk/conditional_theorem_template.metadata.json"
    try:
        validate_obligation(smt_path.read_text(), load_json(metadata_path))
    except GuardError as exc:
        errors.append(f"conditional theorem template violates checker guards: {exc}")
    reference_smt, reference_metadata = example_obligation()
    if smt_path.read_text() != reference_smt or load_json(metadata_path) != reference_metadata:
        errors.append("emitted theorem template differs from tested reference")
    scalar_text = reference_smt.replace(
        "(check-sat)",
        "(declare-fun ComputeAnswer (Input Boundary) Int)\n(check-sat)",
    ).replace("(CallbackStep x b)", "(ComputeAnswer x b)")
    scalar_metadata = copy.deepcopy(reference_metadata)
    scalar_metadata["declared_functions"] = [
        {
            "symbol": "ComputeAnswer",
            "role": "source_transition",
            "source_citations": ["adversarial.rs:1"],
        }
    ]
    whole_relation_text = reference_smt.replace(
        "(check-sat)",
        "(declare-fun WholeResult (Input Output State) Bool)\n(check-sat)",
    ).replace(
        "(and (= (y_value y) (CallbackStep x b))\n"
        "       (= (s_value s) (x_value x)))",
        "(WholeResult x y s)",
    )
    whole_relation_metadata = copy.deepcopy(reference_metadata)
    whole_relation_metadata["declared_functions"] = [
        {
            "symbol": "WholeResult",
            "role": "source_transition",
            "source_citations": ["adversarial.rs:2"],
        }
    ]
    scalar_without_boundary_text = reference_smt.replace(
        "(check-sat)",
        "(declare-fun ComputeValue (Input) Int)\n(check-sat)",
    ).replace("(CallbackStep x b)", "(ComputeValue x)")
    scalar_without_boundary_metadata = copy.deepcopy(reference_metadata)
    scalar_without_boundary_metadata["declared_functions"] = [
        {
            "symbol": "ComputeValue",
            "role": "source_transition",
            "source_citations": ["adversarial.rs:3"],
        }
    ]
    primitive_answer_text = reference_smt.replace(
        "(check-sat)",
        "(declare-fun ComputeValue (Int) Int)\n(check-sat)",
    ).replace("(CallbackStep x b)", "(ComputeValue (x_value x))")
    primitive_answer_metadata = copy.deepcopy(reference_metadata)
    primitive_answer_metadata["declared_functions"] = [
        {
            "symbol": "ComputeValue",
            "role": "source_transition",
            "source_citations": ["adversarial.rs:4"],
        }
    ]
    primitive_relation_text = reference_smt.replace(
        "(check-sat)",
        "(declare-fun WholeResult (Int Int Int) Bool)\n(check-sat)",
    ).replace(
        "(and (= (y_value y) (CallbackStep x b))\n"
        "       (= (s_value s) (x_value x)))",
        "(WholeResult (x_value x) (y_value y) (s_value s))",
    )
    primitive_relation_metadata = copy.deepcopy(reference_metadata)
    primitive_relation_metadata["declared_functions"] = [
        {
            "symbol": "WholeResult",
            "role": "source_transition",
            "source_citations": ["adversarial.rs:5"],
        }
    ]
    unlisted_boundary_text = reference_smt.replace(
        "(b_callback_value Int)",
        "(b_callback_value Int) (b_unlisted Int)",
    )
    helper_text = reference_smt.replace(
        "(define-fun TargetDefinition_T",
        "(define-fun HiddenBoundary () Int\n"
        "  (b_callback_value b))\n"
        "(define-fun TargetDefinition_T",
    ).replace("(CallbackStep x b)", "HiddenBoundary")
    helper_metadata = copy.deepcopy(reference_metadata)
    helper_metadata["source_transition_definitions"].append("HiddenBoundary")
    dead_spec_text = reference_smt.replace(
        "(TargetDefinition_T x b y s))\n"
        "(define-fun Equivalent_T",
        "(or true (TargetDefinition_T x b y s)))\n"
        "(define-fun Equivalent_T",
    )
    extra_false_assertion_text = reference_smt.replace(
        "(check-sat)",
        "(assert false)\n(check-sat)",
    )
    extra_output_assertion_text = reference_smt.replace(
        "(check-sat)",
        "(assert (= (y_value y1) (y_value y2)))\n(check-sat)",
    )
    dead_exact_equality_text = reference_smt.replace(
        "(= (s_value s1) (s_value s2))",
        "(or true (= (s_value s1) (s_value s2)))",
    )
    aliased_execution_text = reference_smt.replace(
        "y2", "y1"
    ).replace("s2", "s1")
    aliased_execution_metadata = copy.deepcopy(reference_metadata)
    aliased_execution_metadata["theorem_variables"]["output2"] = "y1"
    aliased_execution_metadata["theorem_variables"]["state2"] = "s1"
    wrong_sort_text = reference_smt.replace(
        "(declare-const y2 Output)",
        "(declare-const y2 State)",
    )
    empty_observations_text = reference_smt.replace(
        "(and (= (y_value y1) (y_value y2))\n"
        "       (= (s_value s1) (s_value s2))))",
        "true)",
    )
    empty_observations_metadata = copy.deepcopy(reference_metadata)
    empty_observations_metadata["principal_observations"] = []
    partial_observations_text = reference_smt.replace(
        "(and (= (y_value y1) (y_value y2))\n"
        "       (= (s_value s1) (s_value s2))))",
        "(= (y_value y1) (y_value y2)))",
    )
    partial_observations_metadata = copy.deepcopy(reference_metadata)
    partial_observations_metadata["principal_observations"] = (
        partial_observations_metadata["principal_observations"][:1]
    )
    unreachable_transition_text = reference_smt.replace(
        "(and (= (y_value y) (CallbackStep x b))\n"
        "       (= (s_value s) (x_value x)))",
        "(and (= (y_value y) (x_value x))\n"
        "       (= (s_value s) (+ (x_value x) (b_callback_value b))))",
    )
    captured_conclusion_text = reference_smt.replace(
        "(define-fun Requires_T ((x Input)) Bool true)",
        "(define-fun Requires_T ((x Input)) Bool\n"
        "  (and (= (y_value y1) (y_value y2))\n"
        "       (= (s_value s1) (s_value s2))))",
    )
    cancelling_transition_text = reference_smt.replace(
        "(and (= (y_value y) (CallbackStep x b))\n"
        "       (= (s_value s) (x_value x)))",
        "(and (= (y_value y)\n"
        "          (+ (x_value x)\n"
        "             (- (CallbackStep x b) (CallbackStep x b))))\n"
        "       (= (s_value s) (+ (x_value x) (b_callback_value b))))",
    )

    def cancellation_laundering_text(
        expression: str, helper_definition: str = ""
    ) -> str:
        text = reference_smt
        if helper_definition:
            text = text.replace(
                "(define-fun TargetDefinition_T",
                f"{helper_definition}(define-fun TargetDefinition_T",
            )
        return text.replace(
            "(and (= (y_value y) (CallbackStep x b))\n"
            "       (= (s_value s) (x_value x)))",
            f"(and (= (y_value y) {expression})\n"
            "       (= (s_value s) (CallbackStep x b)))",
        )

    cancellation_laundering_probes = (
        (
            "direct subtraction-cancelled input",
            cancellation_laundering_text(
                "(+ (b_callback_value b) "
                "(- (x_value x) (x_value x)))"
            ),
        ),
        (
            "direct zero-multiplied input",
            cancellation_laundering_text(
                "(+ (b_callback_value b) (* 0 (x_value x)))"
            ),
        ),
        (
            "let-mediated subtraction-cancelled input",
            cancellation_laundering_text(
                "(let ((left (x_value x)) (right (x_value x))) "
                "(+ (b_callback_value b) (- left right)))"
            ),
        ),
        (
            "let-mediated zero-multiplied input",
            cancellation_laundering_text(
                "(let ((zero (- 2 2))) "
                "(+ (b_callback_value b) (* zero (x_value x))))"
            ),
        ),
        (
            "helper-mediated subtraction-cancelled input",
            cancellation_laundering_text(
                "(+ (b_callback_value b) (CancelInput (x_value x)))",
                "(define-fun CancelInput ((value Int)) Int "
                "(- value value))\n",
            ),
        ),
        (
            "helper-mediated zero-multiplied input",
            cancellation_laundering_text(
                "(+ (b_callback_value b) (ScaleInput 0 (x_value x)))",
                "(define-fun ScaleInput ((factor Int) (value Int)) Int "
                "(* factor value))\n",
            ),
        ),
    )
    for label, text in cancellation_laundering_probes:
        try:
            validate_obligation(text, reference_metadata)
        except GuardError:
            pass
        else:
            errors.append(f"checker guard accepts {label}")

    non_cancelling_affine_text = cancellation_laundering_text(
        "(+ (b_callback_value b) (* 2 (x_value x)))"
    )
    try:
        validate_obligation(non_cancelling_affine_text, reference_metadata)
    except GuardError as exc:
        errors.append(
            "checker guard rejects non-cancelling affine source transition: "
            f"{exc}"
        )

    check_sat_assuming_text = reference_smt.replace(
        "(check-sat)",
        "(check-sat-assuming (false))",
    )
    incompatible_logic_text = reference_smt.replace(
        "(set-logic ALL)",
        "(set-logic QF_LIA)",
    )
    global_answer_text = reference_smt.replace(
        "(declare-const b Boundary)",
        "(declare-const b Boundary)\n(declare-const forged_answer Int)",
    ).replace(
        "(and (= (y_value y) (CallbackStep x b))\n"
        "       (= (s_value s) (x_value x)))",
        "(and (= (y_value y) forged_answer)\n"
        "       (= (s_value s) (CallbackStep x b)))",
    )
    for label, text, metadata in (
        ("aggregate scalar whole-target UF", scalar_text, scalar_metadata),
        (
            "whole-target relation without Boundary",
            whole_relation_text,
            whole_relation_metadata,
        ),
        (
            "scalar whole-target UF without Boundary",
            scalar_without_boundary_text,
            scalar_without_boundary_metadata,
        ),
        (
            "primitive-signature answer UF",
            primitive_answer_text,
            primitive_answer_metadata,
        ),
        (
            "primitive-signature whole-target relation",
            primitive_relation_text,
            primitive_relation_metadata,
        ),
        (
            "Boundary datatype field without metadata",
            unlisted_boundary_text,
            reference_metadata,
        ),
        ("helper/global boundary-output laundering", helper_text, helper_metadata),
        ("semantically dead target call", dead_spec_text, reference_metadata),
        (
            "additional false assertion",
            extra_false_assertion_text,
            reference_metadata,
        ),
        (
            "additional principal-equality assertion",
            extra_output_assertion_text,
            reference_metadata,
        ),
        (
            "semantically dead exact equality",
            dead_exact_equality_text,
            reference_metadata,
        ),
        (
            "aliased execution variables",
            aliased_execution_text,
            aliased_execution_metadata,
        ),
        (
            "wrongly sorted theorem variable",
            wrong_sort_text,
            reference_metadata,
        ),
        (
            "empty principal-observation schema",
            empty_observations_text,
            empty_observations_metadata,
        ),
        (
            "partial principal-observation schema",
            partial_observations_text,
            partial_observations_metadata,
        ),
        (
            "unreachable source transition",
            unreachable_transition_text,
            reference_metadata,
        ),
        (
            "Requires_T conclusion capture",
            captured_conclusion_text,
            reference_metadata,
        ),
        (
            "algebraically cancelling source transition",
            cancelling_transition_text,
            reference_metadata,
        ),
        (
            "check-sat-assuming result injection",
            check_sat_assuming_text,
            reference_metadata,
        ),
        (
            "datatype-incompatible SMT logic",
            incompatible_logic_text,
            reference_metadata,
        ),
        (
            "fresh global answer constant",
            global_answer_text,
            reference_metadata,
        ),
    ):
        try:
            validate_obligation(text, metadata)
        except GuardError:
            pass
        else:
            errors.append(f"checker guard accepts {label}")

    design = (OUT / "research/CONDITIONAL_THEOREM_CHECKER_DESIGN.md").read_text()
    normalized_design = " ".join(design.split())
    ground_truth = (OUT / "research/GROUND_TRUTH.md").read_text()
    for required in (
        "Requires_T(x)",
        "Boundary_T(x, b)",
        "Spec_T(x, b, y1, s1)",
        "Spec_T(x, b, y2, s2)",
        "Equivalent_T(x, b, y1, s1, y2, s2)",
    ):
        if required not in design:
            errors.append(f"checker design omits literal theorem fragment {required}")
    for label in common.CLASSIFICATION_VOCABULARY:
        if f"`{label}`" not in design:
            errors.append(f"checker design omits classification label {label}")
    for required in (
        "active `r0_z3=unknown` generated rows selected: 62",
        "active `r0_z3=unsat` generated rows excluded: 58",
        "exact-vstd catalog rows excluded: 12",
        "dependency-manifest records expanded: 232",
        "harnesses containing `external_body`: 43",
        "trust-site records adjudicated: 409",
        "previously unlinked `external_body` sites resolved: 14",
        "exhaustively audited `external_body` sites: 86",
        "inadmissible complete/answer-equivalent `external_body` sites: 40",
        "intrinsically answer-equivalent dependency records: 3",
        "targets with admissible, narrower current boundaries: 28",
        "targets blocked by an answer-bearing boundary: 34",
        "`TS-019-D001` and",
        "`TS-021-D001` are intrinsically inadmissible",
    ):
        if required not in ground_truth:
            errors.append(f"ground truth omits measured fact: {required}")
    for required in (
        "exact element multiplicity",
        "foreign identity 12",
        "exact forwarding call",
        "independent of symbol name or signature",
        "exact match between every declared `Boundary` datatype field",
        "meaningful, non-tautological use",
        "helper-mediated",
        "exactly one top-level assertion",
        "six distinct theorem constants",
        "semantically guaranteed",
        "selector-and-sort-derived",
        "meaningfully reachable",
        "role-exact signatures",
        "closes over theorem constants",
        "directly and conjunctively determines",
        "argument-free `check-sat`",
        "datatype-compatible",
        "global constants outside",
        "affine arithmetic normalized",
        "zero multiplication",
        "exact `unsat`",
        "Target 120 source-backed MaybeUninit copy transition",
        "`TS-120-D004` and `TS-120-E005`",
        "`Uninitialized | Initialized(value)` cells",
        "array map of the `Initialized` constructor",
        "Target 052 source-backed unchecked disjoint-borrow transition",
        "`TS-052-D004` and `TS-052-E001`",
        "`SliceIndex<usize>::get_unchecked_mut`",
        "both slots must be initialized before `assume_init`",
        "well-formed disjoint arrays `[0, 2]` and `[1, 2]`",
        "Targets 019 and 021 source-backed slice casts",
        "`TS-019-D001` and `TS-021-D001`",
        "address-equals-length/null-provenance synthesis",
        "Target 020 source-backed mutable pointer range",
        "`TS-020-D003`, answer-bearing endpoint dependency `TS-020-D004`, and external body `TS-020-E001`",
        "mathematical `len * size_of::<T>()` arithmetic",
        "wrong start or end endpoints",
        "source-backed replacement identities",
        "excluded retained trust-site ID cannot back a boundary field",
        "`tools/run_pointer_cast_cluster.py`",
        "Targets 028, 030, and 065 source-backed search wrappers",
        "`TS-028-D002`, `TS-028-D003`, `TS-028-D004`, `TS-028-E001`, and",
        "`TS-030-D005`, `TS-030-D006`,",
        "`TS-065-D002` and",
        "predicate-to-Ordering",
        "`tools/run_search_family_cluster.py`",
        "Targets 012, 014, 015, 023, and 024 strengthened chunk contracts",
        "`TS-015-D006` and `TS-015-E002`",
        "`tools/run_chunk_contract_drift_cluster.py`",
        "Targets 025, 026, and 119 source-backed MaybeUninit lifecycle transitions",
        "`TS-025-D002` and `TS-025-E001`",
        "`TS-026-D002` and `TS-026-E001`",
        "`tools/run_maybeuninit_lifecycle_cluster.py`",
        "Targets 080 and 082 Ord-backed unstable-sort companions",
        "`TS-080-D002` and `TS-080-E001`",
        "`TS-082-D002`, `TS-082-D003`, and `TS-082-E001`",
        "arbitrary nonnegative slice length",
        "`tools/run_unstable_sort_companions.py`",
        "Target 077 source-backed selection method",
        "`TS-077-D002` and `TS-077-E001`",
        "only `TS-077-D003`",
        "zero-sized-type, minimum/maximum, swap, partition, recursive-loop/fallback",
        "side ordering and equal-class pivot identity",
        "`tools/run_target_077.py`",
        "Targets 078-079 bounded callback model and source-model gap",
        "`TS-078-D001`/`TS-079-D001`",
        "Only `TS-078-D004` and `TS-079-D004`",
        "`TS-078-D002`/`TS-079-D002`",
        "`TS-078-D003`/`TS-079-D003`",
        "`TS-078-E001`/`TS-079-E001`",
        "one `compare(a,b)` step followed by",
        "assumes no comparator totality",
        "`f(a)`, then `f(b)`, then",
        "without assuming a pure or stable key extractor",
        "callback-visible final state",
        "`missing-source-backed-model`, not `boundary-insufficient`",
        "`tools/run_selection_callback_cluster.py`",
        "Target 078 arbitrary-range `insert_tail`/`CopyOnDrop` refinement",
        "`ExactInsertTailLoop` and `ExactInsertTail`",
        "guards its induction hypothesis with `sift > begin`",
        "Ten source mutations cover operand order",
        "insertion at `begin`",
        "`path_policy_v2.json` registers the closed v3 evidence scope",
        "additive lane for the pending v3 review",
        "`review/REVIEW_ADDENDUM_TARGET_078_INSERT_TAIL_REFINEMENT_V3.md`",
        "`review/*TARGET_078_INSERT_TAIL_REFINEMENT_V3*.md` files",
        "`tools/run_acceptance.py` runs the v3 producer before policy consumers",
        "Targets 032, 036, 069, 074, 076, 093, and 098 mutable iterator constructors",
        "zero constructor-time callback calls",
        "raw address, allocation, provenance, and mutable-borrow identity",
        "`TS-076-C003`",
        "`core/src/slice/iter.rs:1289-1293`",
        "`tools/run_mutable_iterator_constructors.py`",
        "34 classified and 28",
        "Targets 091, 097, 101, and 103 mutable edge extraction",
        "`mem::replace(self, &mut [])`",
        "pre-result empty-slice literal",
        "Range disjointness is index-based",
        "`tools/run_mutable_edge_extraction.py`",
        "38 classified and 24",
        "Targets 037 and 043 clone-effect transitions",
        "relation-valued `cloned<T>`",
        "`CloneFromSpec`",
        "`is_val_statically_known`",
        "fill's original value into the final slot",
        "`tools/run_clone_effect_cluster.py`",
        "40 classified and 22",
        "Targets 035 and 068 exact mutable iterator partitions",
        "`len % chunk_size`",
        "forward split at `len - rem`",
        "reverse split at `rem`",
        "range-based ZST disjointness",
        "`tools/run_exact_mutable_iterator_partitions.py`",
        "42 classified and 20",
        "Targets 062, 090, and 096 mutable fixed-chunk edges",
        "`32a4497f959b05a42448f7ea2a070f4e3635c1b46d5c08628772d7601f9f9e57`",
        "`eb599a67a0f7b786e404c9b3f97181b56e9b01bb82f3cc21822b93d2d46ab950`",
        "`0c9131cd588a99217fc333ad32e54ac62deaf95cfc245fffb3523ba683296ce5`",
        "null-provenance/length-address pointer model",
        "array-only, array-first, and array-second",
        "Twenty-one SAT source instances",
        "Thirty UNSAT semantic probes",
        "`tools/run_mutable_fixed_chunk_edges.py`",
        "45 classified and 17",
        "Targets 085 and 086 source-backed mutable split primitives",
        "`f545d70fd2f00566e6847d457980a532ef48cdc82fe2e12eba1be9ccff4aebd6`",
        "`dfe96dd890e058e02f390e85bdfce250a48823c9e43c15ad599961b2f28f2da9`",
        "`TS-085-D002`, `TS-085-E002`, `TS-086-D005`, and `TS-086-E002`",
        "one-past-end",
        "nonempty ZST equal-address",
        "Eleven SAT source instances",
        "Twenty-three UNSAT semantic probes",
        "`tools/run_split_at_mut_primitives.py`",
        "47 classified and 15",
        "Targets 099 and 104 source-backed split-off pair",
        "`980c0fc48d42c16666be982fb8949777aea4c339d73a52ba80f62fded2ae7085`",
        "`74829510395c909f4449ed0dd06a0ac44332151e2a9d1feba392c5728e616e99`",
        "`TS-099-D001` through `TS-099-C001`",
        "`TS-104-D001` through `TS-104-C001`",
        "StartInclusive-to-Back",
        "EndInclusive checked addition",
        "active final-return partition clause",
        "Twenty-eight SAT source instances",
        "Twenty UNSAT semantic probes",
        "`tools/run_split_off_pair.py`",
        "49 classified and 13",
        "Targets 048 and 049 source-backed raw slice constructors",
        "`73ec9d9cba07629dcf152cde202578a52cea87134075f0568244d747a3183769`",
        "`47e90942a15f2cdb0e6584968eedeeb627353ed37da324f1af080c3917f0dc40`",
        "`TS-048-D001` and `TS-049-D001` remain context-only",
        "`TS-048-D002`/`TS-048-E001`",
        "`TS-049-D002`/`TS-049-E001`",
        "UB precondition, raw fat-pointer construction, and reference dereference",
        "allocated and dangling nonempty ZST slices",
        "fixed-input/fixed-boundary witness",
        "fourteen SAT source instances",
        "fifty-four UNSAT negative probes",
        "`tools/run_raw_slice_pair.py`",
        "51 classified and 11",
        "Targets 053 through 055 explicit SliceIndex transitions",
        "`87a9796fc553d16e3e75cfe5ea9196e6482c5088d278a2f10112c31107e74f9c`",
        "`71eedef5ee0aa574329fe132e65757563db0764095f5cc5dbdf2911acc0b4aad`",
        "`ec6f48bf7b072e49afdad4bacb69dc2288ec2047621c339df4614e01b612903f`",
        "`TS-053-D002`, `TS-054-D001`, and `TS-055-D001` remain context-only",
        "`TS-054-D002` and `TS-055-D002`",
        "`TS-054-E001` and `TS-055-E001`",
        "No SMT obligation declares an opaque function",
        "all 25 applicable sealed Rust 1.96",
        "canonical element-zero reference",
        "distinct well-formed element-one reference",
        "27 SAT source instances",
        "twelve UNSAT negative probes",
        "`tools/run_slice_index_trio.py`",
        "54 classified and 8",
        "Targets 039 and 111 source-backed address observers",
        "`6cb1971fc22b193456b858636b8e9d6ed1874cc9b7b9352f94eea2cf2a66960b`",
        "`efa221cefc2e3ffa897082292c658fd9163e1e151be34c08189360d0b01729bb`",
        "`TS-039-D006`",
        "`TS-111-D006`",
        "machine-usize wrapping subtraction",
        "documented ZST panic",
        "distinct-allocation empty subslice false positives",
        "22 SAT source instances",
        "46 UNSAT semantic/domain probes",
        "`tools/run_address_observer_pair.py`",
        "56 classified and 6",
        "Targets 017, 018, 046, and 047 source-backed mutable view construction",
        "`TS-017-D006`/`TS-017-E004`",
        "`TS-018-D004`/`TS-018-E002`",
        "`TS-046-D004`/`TS-046-E002`",
        "`TS-047-D001`/`TS-047-E001`",
        "checked multiplication overflow",
        "singleton array-to-slice unsizing",
        "borrow-lifetime final frames",
        "four clean UNSAT exact-output obligations",
        "four SAT full-state obligations",
        "one replayable fixed-input/fixed-boundary SAT witness per target",
        "full state is `conditional-incomplete`",
        "22 SAT source instances",
        "82 UNSAT semantic/domain probes",
        "`tools/run_mutable_view_construction_cluster.py`",
        "60 classified and 2",
        "Targets 008 and 009 source-backed `align_to` transitions",
        "`TS-008-D004`/`TS-008-E005`/`TS-008-E006`",
        "`TS-009-D004`/`TS-009-E003`/`TS-009-E004`",
        "initialized address-indexed input bytes",
        "`ptr::align_offset`",
        "`usize::MAX` no-solution",
        "gcd/ts/us `align_to_offsets` arithmetic",
        "single relational final byte frame",
        "Twenty SAT source instances",
        "Forty-three UNSAT probes",
        "`tools/run_align_to_pair.py`",
        "62 classified and zero `not-run`",
    ):
        if required not in normalized_design:
            errors.append(f"checker design omits strengthened policy: {required}")

    review = (OUT / "review/REVIEW_REQUEST.md").read_text()
    normalized_review = " ".join(review.split())
    if (
        "pending independent review" not in review
        or "stage-transition writer" not in review
        or "ACCEPT" not in review
        or "REJECT" not in review
        or "align_to" in review
    ):
        errors.append("independent Reviewer request is missing or malformed")
    for required in (
        "`core::slice::sort_unstable`",
        "`target-080-operational-v1-rust-1.96-complete`",
        "literal declaration and readable provenance",
        "without inspecting, quoting, or adjudicating opaque integrity identifiers",
        "`evidence/target_080_operational_v1/source_bindings.json`",
        "`tools/target_080_source_interpreter_v1.py`",
        "`evidence/target_080_operational_v1/boundary_manifest.json`",
        "`TS-080-D002` and `TS-080-E001`",
        "`TS-080-D003`",
        "state-independent contract total preorder",
        "realized callback schedule",
        "same input and the same boundary arrays",
        "28 retained witnesses",
        "all 26 source-force probes SAT",
        "all 15 source-semantic mutations SAT",
        "5 verified and 0 errors",
        "the 280 paths registered",
        "`preservation/path_policy_v4.json`",
        "`preservation/path_policy_v5.json`",
        "`target_080_operational_v1_review`",
        "`review-accepted`",
        "PYTHONDONTWRITEBYTECODE=1 python3 tools/run_acceptance.py",
        "exactly 54 command records",
        "at least 721",
    ):
        if required not in normalized_review:
            errors.append(f"independent Reviewer request omits: {required}")
    for stem in REQUIRED_LOGS:
        status = OUT / "logs" / f"{stem}.status.txt"
        if not status.is_file() or status.read_text().strip() != "0":
            errors.append(f"required fresh verification log is not successful: {stem}")
    ordered_replay_path = OUT / "logs/ordered_pointer_cast_cluster_replay.json"
    try:
        ordered_replay = load_json(ordered_replay_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"ordered pointer-cluster replay manifest is unreadable: {exc}")
        ordered_replay = {}
    expected_order = [
        target_019.ARTIFACT_ID,
        target_021.ARTIFACT_ID,
        target_020.ARTIFACT_ID,
    ]
    expected_cluster_results = {
        artifact_id: pointer_target_pipeline.COMPLETE
        for artifact_id in expected_order
    }
    if (
        ordered_replay.get("schema_version") != 1
        or ordered_replay.get("status") != "passed"
        or ordered_replay.get("ordered_artifact_ids") != expected_order
        or ordered_replay.get("initial_cluster_results")
        != expected_cluster_results
        or ordered_replay.get("final_cluster_results")
        != expected_cluster_results
    ):
        errors.append("ordered pointer-cluster replay manifest is malformed")
    crosswalk_artifacts = ordered_replay.get("crosswalk", {})
    pointer_stage_rows = common.read_csv(
        OUT / "crosswalk/target_to_proof_boundary.csv"
    )
    for row in pointer_stage_rows:
        if row["target"] in {
            target_028.TARGET,
            target_030.TARGET,
            target_065.TARGET,
            *{
                config.target
                for config in chunk_contract_drift_cluster.ORDERED_TARGETS
            },
                target_025.TARGET,
                target_026.TARGET,
                target_119.TARGET,
                target_080.TARGET,
                target_077.TARGET,
                target_078.TARGET,
                target_079.TARGET,
                target_082.TARGET,
                *{
                    config.target
                    for config in mutable_iterator_constructors.TARGETS
                },
                *{
                    config.target
                    for config in mutable_edge_extraction.TARGETS
                },
                *{
                    config.target
                    for config in clone_effect_cluster.TARGETS
                },
                *{
                    config.target
                    for config in exact_mutable_iterator_partitions.TARGETS
                },
                *{
                    config.target
                    for config in mutable_fixed_chunk_edges.TARGETS
                },
                *{
                    config.target
                    for config in split_at_mut_primitives.TARGETS
                },
                *{
                    config.target
                    for config in split_off_pair.TARGETS
                },
                *{
                    config.target
                    for config in raw_slice_pair.TARGETS
                },
                *{
                    config.target
                    for config in slice_index_trio.TARGETS
                },
                *{
                    config.target
                    for config in address_observer_pair.TARGETS
                },
                *{
                    config.target
                    for config in mutable_view_construction_cluster.TARGETS
                },
                *{
                    config.target
                    for config in align_to_pair.TARGETS
                },
        }:
            row["exact_output_determinism_status"] = "not-run"
            row["completeness_modulo_reviewed_equivalence_status"] = "not-run"
    csv_buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        csv_buffer,
        fieldnames=list(pointer_stage_rows[0]),
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(pointer_stage_rows)
    pointer_stage_bytes = {
        "csv": csv_buffer.getvalue().encode(),
        "json": (
            json.dumps(pointer_stage_rows, indent=2, sort_keys=True) + "\n"
        ).encode(),
    }
    for name, path in (
        ("csv", OUT / "crosswalk/target_to_proof_boundary.csv"),
        ("json", OUT / "crosswalk/target_to_proof_boundary.json"),
    ):
        descriptor = (
            crosswalk_artifacts.get(name)
            if isinstance(crosswalk_artifacts, dict)
            else None
        )
        expected_bytes = pointer_stage_bytes[name]
        if (
            not isinstance(descriptor, dict)
            or descriptor.get("path") != common.relpath(path)
            or descriptor.get("sha256")
            != common.sha256_bytes(expected_bytes)
            or descriptor.get("bytes") != len(expected_bytes)
        ):
            errors.append(f"ordered pointer-cluster replay has stale {name} binding")
    preservation = ordered_replay.get("preserved_baseline_evidence", {})
    if (
        not isinstance(preservation, dict)
        or set(preservation) != set(pointer_target_pipeline.BASELINE_ARTIFACT_IDS)
    ):
        errors.append("ordered pointer-cluster preservation record is incomplete")
    else:
        for artifact_id in pointer_target_pipeline.BASELINE_ARTIFACT_IDS:
            root = OUT / "evidence/targets" / artifact_id
            current = (
                pointer_target_pipeline.tree_digest(root)
                if root.is_dir()
                else ""
            )
            record = preservation.get(artifact_id)
            if (
                not isinstance(record, dict)
                or record.get("before_sha256") != current
                or record.get("after_sha256") != current
            ):
                errors.append(
                    f"ordered pointer-cluster replay did not preserve {artifact_id}"
                )
    solver_stdout = OUT / "logs/04_theorem_template_z3.stdout.txt"
    solver_stderr = OUT / "logs/04_theorem_template_z3.stderr.txt"
    if not solver_stdout.is_file() or solver_stdout.read_text() != "unsat\n":
        errors.append("theorem-template Z3 replay did not return exact `unsat`")
    if not solver_stderr.is_file() or solver_stderr.read_text() != "":
        errors.append("theorem-template Z3 replay emitted diagnostics")

    pipeline = load_json(OUT / "research/PIPELINE_STATE.json")
    delivery = pipeline.get("stages", {}).get("delivery", {})
    history = pipeline.get("stage_history", [])
    latest = history[-1] if history else {}
    if (
        set(pipeline)
        != {
            "current_stage",
            "stage_history",
            "stages",
            "vertical",
            "workflow_mode",
        }
        or pipeline.get("current_stage") != "delivery"
        or pipeline.get("vertical") != "software"
        or pipeline.get("workflow_mode") != "staged"
        or set(pipeline.get("stages", {})) != {"delivery"}
        or delivery.get("status") != "done"
        or delivery.get("completion_contract_version") != 1
        or not delivery.get("completion_contract_sha256")
        or latest.get("by") != "manager"
        or latest.get("direction") != "complete"
        or latest.get("from_stage") != "delivery"
        or latest.get("to_stage") != "delivery"
    ):
        errors.append("protected research/PIPELINE_STATE.json changed")


def main() -> None:
    errors: list[str] = []
    authority = independently_derive(errors)
    required_artifacts = (
        "crosswalk/target_to_proof_boundary.csv",
        "crosswalk/target_to_proof_boundary.json",
        "crosswalk/trust_site_inventory.csv",
        "crosswalk/trust_site_inventory.json",
        "crosswalk/contract_drift_reconciliation.csv",
        "crosswalk/contract_drift_reconciliation.json",
        "crosswalk/scope_summary.json",
        "provenance/input_provenance.json",
        "research/GROUND_TRUTH.md",
        "research/CONDITIONAL_THEOREM_CHECKER_DESIGN.md",
    )
    missing = [relative for relative in required_artifacts if not (OUT / relative).is_file()]
    if missing:
        print("validation=FAIL")
        for relative in missing:
            print(f"ERROR missing artifact: {relative}")
        raise SystemExit(1)

    crosswalk = validate_parallel_formats(
        errors,
        OUT / "crosswalk/target_to_proof_boundary.csv",
        OUT / "crosswalk/target_to_proof_boundary.json",
        "crosswalk",
    )
    trust = validate_parallel_formats(
        errors,
        OUT / "crosswalk/trust_site_inventory.csv",
        OUT / "crosswalk/trust_site_inventory.json",
        "trust inventory",
    )
    drifts = validate_parallel_formats(
        errors,
        OUT / "crosswalk/contract_drift_reconciliation.csv",
        OUT / "crosswalk/contract_drift_reconciliation.json",
        "drift reconciliation",
    )
    validate_crosswalk(errors, authority, crosswalk, trust)
    validate_trust_inventory(errors, authority, trust)
    validate_drifts(errors, drifts)
    validate_provenance(errors)
    validate_evidence(errors)
    validate_target_029_evidence(errors)
    validate_target_013_evidence(errors)
    validate_target_106_evidence(errors)
    validate_target_081_evidence(errors)
    validate_target_022_evidence(errors)
    validate_target_120_evidence(errors)
    validate_target_051_evidence(errors)
    validate_target_052_evidence(errors)
    pointer_target_validation.validate(
        errors,
        target_019,
        replay_target_019,
        run_target_019,
        source_model=OUT / "proofs/019_core_slice_as_mut_ptr.rs",
        expected_not_run=53,
    )
    pointer_target_validation.validate(
        errors,
        target_021,
        replay_target_021,
        run_target_021,
        source_model=OUT / "proofs/021_core_slice_as_ptr.rs",
        expected_not_run=52,
    )
    pointer_target_validation.validate(
        errors,
        target_020,
        replay_target_020,
        run_target_020,
        source_model=OUT / "proofs/020_core_slice_as_mut_ptr_range.rs",
        expected_not_run=51,
    )
    search_target_validation.validate(
        errors,
        target_028,
        replay_target_028,
        run_target_028,
        source_model=OUT / "proofs/028_core_slice_binary_search.rs",
        expected_not_run=50,
    )
    search_target_validation.validate(
        errors,
        target_030,
        replay_target_030,
        run_target_030,
        source_model=OUT / "proofs/030_core_slice_binary_search_by_key.rs",
        expected_not_run=49,
    )
    search_target_validation.validate(
        errors,
        target_065,
        replay_target_065,
        run_target_065,
        source_model=OUT / "proofs/065_core_slice_partition_point.rs",
        expected_not_run=48,
    )
    search_target_validation.validate_cluster(
        errors, run_search_family_cluster.ORDERED_TARGETS
    )
    chunk_target_validation.validate_cluster(errors)
    maybeuninit_lifecycle_validation.validate(errors)
    unstable_sort_companion_validation.validate(errors)
    selection_method_validation.validate(errors)
    selection_callback_validation.validate(errors)
    mutable_iterator_constructor_validation.validate(errors)
    mutable_edge_extraction_validation.validate(errors)
    clone_effect_cluster_validation.validate(errors)
    exact_mutable_iterator_partition_validation.validate(errors)
    mutable_fixed_chunk_edge_validation.validate(errors)
    split_at_mut_primitive_validation.validate(errors)
    split_off_pair_validation.validate(errors)
    raw_slice_pair_validation.validate(errors)
    slice_index_trio_validation.validate(errors)
    address_observer_pair_validation.validate(errors)
    mutable_view_construction_validation.validate(errors)
    align_to_pair_validation.validate(errors)
    validate_design_and_logs(errors)

    summary = load_json(OUT / "crosswalk/scope_summary.json")
    expected_semantic_dispositions = {
        "context-only-specification-vocabulary": 46,
        "context-only-source-closure": 91,
        "admissible-source-backed-support": 144,
        "admissible-source-backed-lower-boundary": 46,
        "inadmissible-complete-target-postcondition": 11,
        "inadmissible-complete-branch-postcondition": 14,
        "inadmissible-answer-equivalent-result": 9,
        "inadmissible-opaque-whole-algorithm": 6,
        "inadmissible-answer-bearing-support": 34,
        "mixed-support-includes-answer-bearing-site": 5,
        "inadmissible-answer-equivalent-dependency": 3,
    }
    if (
        summary.get("counts")
        != {
            "catalog_total": 132,
            "generated": 120,
            "exact_vstd": 12,
            "r0_unknown": 62,
            "r0_unsat": 58,
            "selected": 62,
        }
        or summary.get("reason_counts") != EXPECTED_REASON_COUNTS
        or summary.get("abcd_status_counts") != {"B": 62}
        or set(summary.get("contract_drift_targets", []))
        != common.EXPECTED_DRIFT_TARGETS
        or summary.get("trust_semantic_disposition_counts")
        != expected_semantic_dispositions
        or summary.get("unlinked_external_body_count") != 0
        or summary.get("inadmissible_external_body_count") != 40
        or summary.get("external_semantic_audit_category_counts")
        != EXPECTED_EXTERNAL_CATEGORY_COUNTS
        or summary.get("semantic_audit_version")
        != common.TRUST_SEMANTIC_AUDIT_VERSION
        or summary.get("semantic_audit_input_sha256")
        != {
            "dependency_records": EXPECTED_DEPENDENCY_AUDIT_SHA256,
            "external_body_contracts": EXPECTED_EXTERNAL_AUDIT_SHA256,
        }
        or summary.get("boundary_admissibility_counts")
        != {"admissible": 28, "inadmissible": 34}
    ):
        errors.append("scope summary does not match independently rederived authority")
    common_category_counts = Counter(
        common.EXTERNAL_SITE_SEMANTIC_AUDIT.values()
    )
    if (
        len(common.EXTERNAL_SITE_SEMANTIC_AUDIT) != 86
        or dict(common_category_counts) != EXPECTED_EXTERNAL_CATEGORY_COUNTS
        or set(common.EXTERNAL_SEMANTIC_CATEGORY_POLICY) != set(
            EXPECTED_EXTERNAL_POLICY
        )
    ):
        errors.append("external semantic policy is not the exhaustive reviewed set")

    if errors:
        print("validation=FAIL")
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    trust_counts = Counter(row["record_type"] for row in trust)
    external_harnesses = sum(
        int(row["external_body_count"]) > 0 for row in crosswalk
    )
    print("validation=PASS")
    print("scope=120_generated,62_UNKNOWN,58_UNSAT,12_exact_vstd_excluded")
    print("selected=62_unique_core_slice abcd_status=B")
    print(
        f"trust=232_dependency_records,"
        f"{trust_counts['harness-external-body']}_external_body_sites,"
        f"{external_harnesses}_external_body_harnesses"
    )
    print("semantic_boundaries=28_admissible,34_inadmissible,0_unlinked")
    print("drifts=6_active_authority_controls")
    print(target_results_summary(crosswalk))
    print(target_result_count_summary(crosswalk))
    print("review_gate=pending_independent_reviewer")


if __name__ == "__main__":
    main()
