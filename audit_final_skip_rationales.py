#!/usr/bin/env python3
"""Audit and repair final skip-rationale taxonomy for the canonical fresh run."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any


CANONICAL_FRESH_ROOT = Path(
    "/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06"
    "/specgen/all-2121-gpt56sol-fresh-20260806-0453"
)
DEFAULT_VSTD_CONTRACTS = Path(__file__).resolve().parent / "results" / "vstd_contracts.json"

AUDIT_CSV = "final_skip_rationale_audit.csv"
AUDIT_SUMMARY_JSON = "final_skip_rationale_audit_summary.json"
AUDIT_REPORT = "FINAL_SKIP_RATIONALE_AUDIT.md"
EXPECTED_FINAL_ROWS = 2121
EXPECTED_ADD_SPEC_ROWS = 127
EXPECTED_SKIP_ROWS = 1994

ISSUE_FIELDS = ("issues", "semantic_gate_issues", "semantic_review_issues")
DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG = "duplicate_vstd_assume_specification"
DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG = "determinism_unsupported_contract_form"
NON_ISSUE_CLASSIFICATION_TAGS = {"classification:suitable_now"}
RANGE_BOUNDS_BYTE_CHARACTER_ENDPOINT_MODEL_GAP_TAG = (
    "range_bounds_byte_character_endpoint_model_gap"
)
RECOGNIZED_CLASSIFICATION_TAGS = {
    "classification:associated_type_or_projection",
    "classification:complex_result_or_pattern_model",
    "classification:concurrency_or_hidden_state",
    "classification:determinism_checker_unsupported",
    "classification:formatting_effect",
    "classification:higher_order_contract",
    "classification:iterator_or_adapter_result",
    "classification:needs_new_vstd_abstraction",
    "classification:no_modeled_observable_output",
    "classification:ownership_or_uninitialized_model",
    "classification:representation_or_allocator",
    "classification:runtime_or_hidden_state",
    "classification:toolchain_unavailable",
    "classification:trait_contract_integration",
    "classification:unsafe_or_representation_sensitive",
}
RECOGNIZED_ISSUE_TAGS = {
    "associated_type_signature_requires_manual_integration",
    "atomic_state_not_exposed_by_ordinary_view",
    "borrowed_key_model_underdetermined",
    "call_site_intrinsic_hidden_state",
    "clone_behavior_domain_strengthening",
    "clone_semantics_unmodeled",
    "closure_call_ensures_or_prophetic_model_required",
    "compiler_intrinsic_discriminant_model_gap",
    "compiler_intrinsic_type_property_model_gap",
    "cow_to_mut_payload_reference_model_missing",
    "deref_mut_result_payload_model_missing",
    DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG,
    "direction_choice_not_modeled",
    DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
    "external_or_hidden_runtime_state",
    "formatting_state_not_modeled",
    "generic_pattern_prefix_trim_underdetermined",
    "generic_pattern_reverse_search_underdetermined",
    "generic_pattern_suffix_trim_underdetermined",
    "generic_slice_pattern_model_gap",
    "hashmap_get_disjoint_mut_reference_array_model_missing",
    "higher_order_closure_comparator_underdetermined",
    "higher_order_closure_key_extraction_underdetermined",
    "higher_order_closure_result_underdetermined",
    "implementation_dependent_split_point",
    "iterator_or_adapter_semantics_require_prophetic_model",
    "missing_nonnull_pointer_view",
    "multiple_rust_declarations_share_path",
    "must_compare_semantic_view_not_reference_identity",
    "mutable_reference_return_not_supported",
    "no_existing_contract_for_owner_or_module",
    "no_modeled_observable_output",
    "not_in_verus_rust_1_96",
    "one_sided_range_split_point_underdetermined",
    "panic_location_abstraction_missing",
    "partial_eq_semantics_unmodeled",
    "peekable_next_if_closure_observation_underdetermined",
    "peekable_next_if_map_mut_closure_observation_underdetermined",
    "permitted_partition_order_underdetermined",
    "pointer_address_or_provenance_model_gap",
    "public_api_allows_any_matching_index",
    RANGE_BOUNDS_BYTE_CHARACTER_ENDPOINT_MODEL_GAP_TAG,
    "raw_pointer_representation_contract",
    "raw_pointer_result",
    "representation_or_allocator_state_not_in_public_view",
    "requires_external_trait_specification_edit",
    "requires_linear_ownership_or_initialization_model",
    "result_type_or_pattern_semantics_need_additional_model",
    "unit_result_without_mutable_output_state",
    "unsafe_or_raw_pointer_signature",
    "value_unspecified_after_exhaustion",
}
EXISTING_VSTD_ASSUME_SPECIFICATION_RATIONALE_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"\bvstd\b.{0,160}\balready\b.{0,160}\bassume_specification\b",
        r"\balready\b.{0,160}\bassume_specification\b.{0,160}\bvstd\b",
        r"\b(existing|identical|equivalent|trusted)\b.{0,120}\bspecification\b"
        r".{0,160}\balready\b.{0,160}\bvstd\b",
        r"\bvstd\b.{0,160}\bspecification\b.{0,160}\balready\b.{0,80}"
        r"\b(covers|exists|provides|declares)\b",
        r"\bexisting vstd specification\b.{0,160}\balready\b.{0,80}"
        r"\b(covers|declares|provides)\b",
    )
]

REPAIR_ISSUE_TAGS = {
    "alloc::collections::LinkedList::contains": [
        "duplicate_vstd_assume_specification",
    ],
    "alloc::collections::LinkedList::front": [
        "duplicate_vstd_assume_specification",
    ],
    "core::alloc::Layout::new": [
        "duplicate_vstd_assume_specification",
    ],
    "core::alloc::Layout::repeat": [
        "duplicate_vstd_assume_specification",
    ],
    "core::array::repeat": [
        "clone_semantics_unmodeled",
    ],
    "core::mem::discriminant": [
        "compiler_intrinsic_discriminant_model_gap",
    ],
    "core::mem::needs_drop": [
        "compiler_intrinsic_type_property_model_gap",
    ],
    "core::net::IpAddr::is_ipv6": [
        "duplicate_vstd_assume_specification",
    ],
    "core::net::Ipv4Addr::is_private": [
        "duplicate_vstd_assume_specification",
    ],
    "core::net::Ipv6Addr::from_bits": [
        "duplicate_vstd_assume_specification",
    ],
    "core::panic::Location::caller": [
        "call_site_intrinsic_hidden_state",
    ],
    "core::slice::clone_from_slice": [
        "clone_semantics_unmodeled",
    ],
    "core::slice::fill": [
        "clone_semantics_unmodeled",
    ],
    "core::slice::strip_suffix": [
        "generic_slice_pattern_model_gap",
    ],
    "core::slice::subslice_range": [
        "pointer_address_or_provenance_model_gap",
    ],
    "core::time::Duration::div_duration_f32": [
        "duplicate_vstd_assume_specification",
    ],
}
DUPLICATE_VSTD_REPAIR_TARGETS = {
    target
    for target, tags in REPAIR_ISSUE_TAGS.items()
    if DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG in tags
}
_VSTD_API_PATHS_CACHE: dict[Path, set[str]] = {}

AUDIT_FIELDS = [
    "target",
    "category",
    "final_decision",
    "rationale_taxonomy",
    "taxonomy_source_fields",
    "taxonomy_source_backed",
    "adequacy_verdict",
    "adequacy_notes",
    "unjustified_skip",
    "issues_combined",
    "combined_issue_taxonomy_tags",
    "rationale",
    "requires",
    "requires_source_fidelity_classification",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def iter_tag_fragments(*values: Any) -> list[str]:
    fragments: list[str] = []
    for value in values:
        if isinstance(value, (list, tuple, set)):
            raw_items = value
        else:
            raw_items = (value,)
        for item in raw_items:
            for tag in str(item or "").split(";"):
                tag = tag.strip()
                if tag:
                    fragments.append(tag)
    return fragments


def split_tags(*values: Any) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for tag in iter_tag_fragments(*values):
        if tag in NON_ISSUE_CLASSIFICATION_TAGS:
            continue
        if tag not in seen:
            seen.add(tag)
            tags.append(tag)
    return tags


def classification_issue_tag(classification: str) -> str:
    tag = f"classification:{classification}" if classification else ""
    if tag in NON_ISSUE_CLASSIFICATION_TAGS:
        return ""
    return tag


def contains_non_issue_classification_tags(*values: Any) -> bool:
    return any(tag in NON_ISSUE_CLASSIFICATION_TAGS for tag in iter_tag_fragments(*values))


def recognized_issue_tags(tags: list[str]) -> list[str]:
    return [
        tag
        for tag in tags
        if tag in RECOGNIZED_CLASSIFICATION_TAGS or tag in RECOGNIZED_ISSUE_TAGS
    ]


def one_line(value: str, limit: int = 1200) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def bool_text(value: bool) -> str:
    return str(bool(value)).lower()


def int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def specgen_safe_name(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", path).strip("_")


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def manifest_paths_from_metadata(metadata: dict[str, Any]) -> list[Path]:
    manifest_paths: list[Path] = []

    def collect(item: dict[str, Any]) -> None:
        manifest = item.get("manifest")
        if manifest:
            manifest_paths.append(Path(str(manifest)))
        for batch in item.get("batches", []):
            if isinstance(batch, dict):
                collect(batch)

    collect(metadata)
    return sorted(set(manifest_paths), key=str)


def load_manifest_entries(root: Path, manifest: Path | None) -> dict[str, dict[str, Any]]:
    candidates: list[Path] = []
    if manifest is not None:
        candidates.append(manifest)
    else:
        batch_path = root / "batch_summary.json"
        if batch_path.exists():
            try:
                payload = json.loads(batch_path.read_text())
            except json.JSONDecodeError:
                payload = {}
            if isinstance(payload, dict):
                candidates.extend(
                    manifest_paths_from_metadata(payload.get("metadata", {}))
                )
        if not candidates:
            candidates.append(root.parent / "classified-manifest.json")

    entries: dict[str, dict[str, Any]] = {}
    entry_sources: dict[str, Path] = {}
    seen_candidates: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.expanduser().resolve(strict=False)
        if candidate in seen_candidates or not candidate.exists():
            continue
        seen_candidates.add(candidate)
        payload = json.loads(candidate.read_text())
        raw_entries = payload.get("targets", payload) if isinstance(payload, dict) else payload
        if not isinstance(raw_entries, list):
            raise ValueError(f"manifest is not a target list: {candidate}")
        for entry in raw_entries:
            if not isinstance(entry, dict):
                raise ValueError(f"manifest contains non-object targets: {candidate}")
            target = str(entry.get("target") or "")
            if not target:
                continue
            previous = entries.get(target)
            if previous is not None and previous != entry:
                raise ValueError(
                    f"conflicting manifest definitions for {target!r}: "
                    f"{entry_sources[target]} and {candidate}"
                )
            entries[target] = entry
            entry_sources[target] = candidate
    return entries


def load_vstd_api_paths(contracts: Path | None = None) -> set[str]:
    path = (contracts or DEFAULT_VSTD_CONTRACTS).expanduser().resolve()
    cached = _VSTD_API_PATHS_CACHE.get(path)
    if cached is not None:
        return cached

    payload = json.loads(path.read_text())
    if not isinstance(payload, list):
        raise ValueError(f"expected a list of vstd contracts in {path}")
    api_paths = {
        str(record.get("api_path") or "").strip()
        for record in payload
        if isinstance(record, dict) and str(record.get("api_path") or "").strip()
    }
    _VSTD_API_PATHS_CACHE[path] = api_paths
    return api_paths


def manifest_classification(
    manifest_entries: dict[str, dict[str, Any]],
    target: str,
) -> str:
    entry = manifest_entries.get(target) or {}
    return str(entry.get("classification") or "").strip()


def manifest_has_source_evidence(
    manifest_entries: dict[str, dict[str, Any]],
    target: str,
) -> bool:
    entry = manifest_entries.get(target) or {}
    declarations = entry.get("declarations") or []
    if not isinstance(declarations, list):
        return False
    return any(
        isinstance(declaration, dict)
        and bool(str(declaration.get("source_context") or "").strip())
        for declaration in declarations
    )


def repair_tags_for_target(
    target: str,
    manifest_entries: dict[str, dict[str, Any]],
) -> list[str]:
    tags = list(REPAIR_ISSUE_TAGS.get(target, []))
    classification_tag = classification_issue_tag(
        manifest_classification(manifest_entries, target)
    )
    if classification_tag:
        tags.insert(0, classification_tag)
    return split_tags(";".join(tags))


def merge_target_repair_tags(
    target: str,
    final_decision: str,
    tags: list[str],
    manifest_entries: dict[str, dict[str, Any]],
) -> list[str]:
    if final_decision != "skip" or target not in REPAIR_ISSUE_TAGS:
        return split_tags(";".join(tags))
    return split_tags(
        ";".join(tags),
        ";".join(repair_tags_for_target(target, manifest_entries)),
    )


def duplicate_vstd_rationale(rationale: str) -> bool:
    text = str(rationale or "").lower()
    return "vstd already" in text and "duplicate" in text


def existing_vstd_assume_specification_rationale(rationale: str) -> bool:
    text = " ".join(str(rationale or "").lower().split())
    if "vstd" not in text or "already" not in text:
        return False
    if not any(
        marker in text
        for marker in (
            "duplicate",
            "redundant",
            "rejected",
            "cannot typecheck",
            "fails typechecking",
            "already covers",
            "already covered",
        )
    ):
        return False
    return any(
        pattern.search(text)
        for pattern in EXISTING_VSTD_ASSUME_SPECIFICATION_RATIONALE_PATTERNS
    )


def is_duplicate_existing_vstd_skip(
    target: str,
    final_decision: str,
    rationale: str,
    tags: set[str],
    vstd_api_paths: set[str] | None = None,
) -> bool:
    exact_vstd_match = target in (
        vstd_api_paths if vstd_api_paths is not None else load_vstd_api_paths()
    )
    return final_decision == "skip" and (
        exact_vstd_match
        or DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG in tags
        or duplicate_vstd_rationale(rationale)
    )


def normalized_duplicate_vstd_issue_tags(
    target: str,
    final_decision: str,
    rationale: str,
    existing_tags: list[str],
    manifest_entries: dict[str, dict[str, Any]],
    vstd_api_paths: set[str] | None = None,
) -> list[str]:
    tags = split_tags(";".join(str(tag) for tag in existing_tags))
    classification = manifest_classification(manifest_entries, target)
    vstd_api_paths = (
        vstd_api_paths if vstd_api_paths is not None else load_vstd_api_paths()
    )
    exact_vstd_duplicate_skip = final_decision == "skip" and target in vstd_api_paths
    duplicate_existing_vstd_skip = is_duplicate_existing_vstd_skip(
        target,
        final_decision,
        rationale,
        set(tags),
        vstd_api_paths,
    ) or (
        final_decision == "skip"
        and classification == "suitable_now"
        and existing_vstd_assume_specification_rationale(rationale)
    )
    if not duplicate_existing_vstd_skip:
        if not tags and final_decision == "skip" and target not in REPAIR_ISSUE_TAGS:
            classification_tag = classification_issue_tag(classification)
            if classification_tag:
                return [classification_tag]
        cleaned = [
            tag for tag in tags if tag != DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG
        ]
        if not cleaned and DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG in tags:
            classification_tag = classification_issue_tag(classification)
            if classification_tag:
                cleaned = [classification_tag]
        return merge_target_repair_tags(
            target,
            final_decision,
            cleaned,
            manifest_entries,
        )

    normalized = (
        [tag for tag in tags if tag.startswith("classification:")]
        if exact_vstd_duplicate_skip
        else [
            tag
            for tag in tags
            if tag
            not in {
                DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
                DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG,
            }
        ]
    )
    classification_tags = [tag for tag in normalized if tag.startswith("classification:")]
    other_tags = [tag for tag in normalized if not tag.startswith("classification:")]
    if classification and classification != "suitable_now":
        classification_tags = split_tags(
            ";".join(classification_tags),
            f"classification:{classification}",
        )
    if exact_vstd_duplicate_skip:
        return split_tags(
            ";".join(classification_tags),
            DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
        )
    return merge_target_repair_tags(
        target,
        final_decision,
        split_tags(
            ";".join(classification_tags),
            DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
            ";".join(other_tags),
        ),
        manifest_entries,
    )


def record_issue_tags(record: dict[str, Any]) -> list[str]:
    return split_tags(
        record.get("anti_vacuity_issues") or [],
        record.get("issues") or [],
    )


def candidate_decision(record: dict[str, Any]) -> str:
    candidate = record.get("candidate") or {}
    return str(candidate.get("decision") or "").strip()


def candidate_rationale(record: dict[str, Any]) -> str:
    candidate = record.get("candidate") or {}
    return str(candidate.get("rationale") or "").strip()


def set_record_issue_tags(record: dict[str, Any], tags: list[str]) -> None:
    record["anti_vacuity_issues"] = list(tags)
    record["issues"] = list(tags)


def repair_result_issues(
    result: dict[str, Any],
    manifest_entries: dict[str, dict[str, Any]],
    vstd_api_paths: set[str] | None = None,
) -> bool:
    target = str(result.get("target") or "")
    final = result.get("final") or {}
    if candidate_decision(final) != "skip":
        return False

    old_tags = record_issue_tags(final)
    tags = normalized_duplicate_vstd_issue_tags(
        target,
        candidate_decision(final),
        candidate_rationale(final),
        old_tags,
        manifest_entries,
        vstd_api_paths,
    )
    if tags == old_tags and target in REPAIR_ISSUE_TAGS and not old_tags:
        tags = repair_tags_for_target(target, manifest_entries)
    final_has_inactive_tags = contains_non_issue_classification_tags(
        final.get("anti_vacuity_issues") or [],
        final.get("issues") or [],
    )
    if tags == old_tags and not final_has_inactive_tags:
        return False

    set_record_issue_tags(final, tags)
    final_rationale = candidate_rationale(final)
    for record in result.get("history") or []:
        if candidate_decision(record) != "skip" or candidate_rationale(record) != final_rationale:
            continue
        history_tags = record_issue_tags(record)
        normalized_history_tags = normalized_duplicate_vstd_issue_tags(
            target,
            candidate_decision(record),
            candidate_rationale(record),
            history_tags,
            manifest_entries,
            vstd_api_paths,
        )
        if (
            normalized_history_tags == history_tags
            and target in REPAIR_ISSUE_TAGS
            and not history_tags
        ):
            normalized_history_tags = tags
        history_has_inactive_tags = contains_non_issue_classification_tags(
            record.get("anti_vacuity_issues") or [],
            record.get("issues") or [],
        )
        if normalized_history_tags != history_tags or history_has_inactive_tags:
            set_record_issue_tags(record, normalized_history_tags)
    return True


def repair_batch_and_target_summaries(
    root: Path,
    manifest_entries: dict[str, dict[str, Any]],
    vstd_api_paths: set[str],
) -> list[str]:
    batch_path = root / "batch_summary.json"
    if not batch_path.exists():
        return []
    payload = json.loads(batch_path.read_text())
    repaired_targets: list[str] = []
    for result in payload.get("results", []):
        if repair_result_issues(result, manifest_entries, vstd_api_paths):
            repaired_targets.append(str(result["target"]))
    if not repaired_targets:
        return []

    batch_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    for target in repaired_targets:
        summary_path = root / "targets" / specgen_safe_name(target) / "summary.json"
        if not summary_path.exists():
            continue
        summary = json.loads(summary_path.read_text())
        if repair_result_issues(summary, manifest_entries, vstd_api_paths):
            summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return repaired_targets


def row_issue_tags(row: dict[str, str]) -> list[str]:
    return split_tags(*(row.get(field, "") for field in ISSUE_FIELDS))


def row_has_non_issue_classification_tags(row: dict[str, str]) -> bool:
    return contains_non_issue_classification_tags(
        *(row.get(field, "") for field in ISSUE_FIELDS)
    )


def repair_final_candidate_rows(
    root: Path,
    manifest_entries: dict[str, dict[str, Any]],
    vstd_api_paths: set[str],
) -> list[str]:
    csv_path = root / "final_candidates.csv"
    if not csv_path.exists():
        return []
    rows, fields = read_csv(csv_path)
    repaired_targets: list[str] = []
    for row in rows:
        target = row.get("target", "")
        if row.get("final_decision") != "skip":
            continue
        old_tags = row_issue_tags(row)
        tags = normalized_duplicate_vstd_issue_tags(
            target,
            row.get("final_decision", ""),
            row.get("rationale", ""),
            old_tags,
            manifest_entries,
            vstd_api_paths,
        )
        if tags == old_tags and target in REPAIR_ISSUE_TAGS and not old_tags:
            tags = repair_tags_for_target(target, manifest_entries)
        if tags == old_tags and not row_has_non_issue_classification_tags(row):
            continue
        row["issues"] = ";".join(tags)
        for field in ("semantic_gate_issues", "semantic_review_issues"):
            row[field] = ";".join(
                tag
                for tag in split_tags(row.get(field, ""))
                if tag
                not in {
                    DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
                    DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG,
                }
            )
        repaired_targets.append(target)
    if repaired_targets:
        write_csv(csv_path, rows, fields)
    return repaired_targets


def accepted_add_spec_fingerprint(rows: list[dict[str, str]]) -> str:
    parts = []
    for row in sorted(rows, key=lambda item: item.get("target", "")):
        if row.get("final_decision") != "add_spec":
            continue
        parts.append(
            "\0".join(
                [
                    row.get("target", ""),
                    row.get("contract_code", ""),
                    row.get("requires", ""),
                    row.get("ensures", ""),
                ]
            )
        )
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def classify_skip(
    row: dict[str, str],
    tags: set[str],
    vstd_api_paths: set[str] | None = None,
) -> tuple[str, str]:
    rationale = str(row.get("rationale") or "").lower()
    category = str(row.get("category") or "").lower()
    if is_duplicate_existing_vstd_skip(
        str(row.get("target") or ""),
        str(row.get("final_decision") or ""),
        rationale,
        tags,
        vstd_api_paths,
    ):
        return (
            "duplicate_existing_vstd_spec",
            "issue tags or rationale identify an existing vstd assume_specification",
        )
    if (
        "classification:higher_order_contract" in tags
        or any(tag.startswith("higher_order_closure_") for tag in tags)
        or "closure" in rationale
        or "predicate" in rationale
        or "callback" in rationale
    ):
        return (
            "higher_order_behavior_unmodeled",
            "closure, predicate, or comparator behavior is not fully observable in the public model",
        )
    if (
        "classification:unsafe_or_representation_sensitive" in tags
        or "raw_pointer_representation_contract" in tags
        or "pointer_address_or_provenance_model_gap" in tags
        or "pointer" in rationale
        or "provenance" in rationale
        or "alignment" in rationale
    ):
        return (
            "unsafe_or_representation_sensitive",
            "source behavior depends on unsafe representation, address, alignment, or provenance facts",
        )
    if (
        "classification:runtime_or_hidden_state" in tags
        or "classification:concurrency_or_hidden_state" in tags
        or "call_site_intrinsic_hidden_state" in tags
        or "os" in category
        or "runtime" in rationale
        or "hidden state" in rationale
        or "call-site" in rationale
        or "synchronization" in rationale
    ):
        return (
            "runtime_or_hidden_state",
            "source behavior depends on OS, runtime, synchronization, or compiler-maintained hidden state",
        )
    if (
        "classification:ownership_or_uninitialized_model" in tags
        or "maybeuninit" in rationale
        or "uninitialized" in rationale
    ):
        return (
            "ownership_or_uninitialized_model_gap",
            "available views do not model the ownership or uninitialized-state fact needed by the API",
        )
    if (
        "classification:representation_or_allocator" in tags
        or "allocator" in rationale
        or "capacity" in rationale
    ):
        return (
            "representation_or_allocator_model_gap",
            "source behavior depends on allocator or representation details outside the public model",
        )
    if "value_unspecified_after_exhaustion" in tags or "unspecified" in rationale:
        return (
            "source_unspecified_after_exhaustion",
            "Rust source or docs leave the value intentionally unspecified for this state",
        )
    if "classification:associated_type_or_projection" in tags:
        return (
            "associated_type_or_projection_gap",
            "generic associated-type or projection results lack a public specification relation",
        )
    if (
        "one_sided_range_split_point_underdetermined" in tags
        or "direction_choice_not_modeled" in tags
        or (
            "onesidedrange" in rationale
            and ("split_point_of" in rationale or "split-point" in rationale)
        )
    ):
        return (
            "one_sided_range_split_point_underdetermined",
            "OneSidedRange-to-Direction/split-index semantics are source-backed but not modeled in public vstd vocabulary",
        )
    if (
        RANGE_BOUNDS_BYTE_CHARACTER_ENDPOINT_MODEL_GAP_TAG in tags
        or (
            "rangebounds" in rationale
            and "byte range" in rationale
            and ("character indices" in rationale or "char boundary" in rationale)
        )
    ):
        return (
            "range_bounds_byte_character_endpoint_model_gap",
            "RangeBounds endpoint selection and byte/character boundary mapping are source-backed but not modeled in public vstd vocabulary",
        )
    if "classification:formatting_effect" in tags or "format" in rationale:
        return (
            "formatting_effect_unmodeled",
            "the API's observable behavior is a formatter side effect rather than a pure modeled value",
        )
    if (
        "clone_semantics_unmodeled" in tags
        or "clone_behavior_domain_strengthening" in tags
        or "clone" in rationale
        or "cloning" in rationale
    ):
        return (
            "clone_semantics_unmodeled",
            "Rust Clone does not guarantee equality or public-view preservation for arbitrary T",
        )
    if (
        "partial_eq_semantics_unmodeled" in tags
        or "classification:trait_contract_integration" in tags
        or "partialeq" in rationale
        or "partialord" in rationale
    ):
        return (
            "trait_contract_integration_gap",
            "trait method behavior needs a trait-level semantic law not available as public vstd vocabulary",
        )
    if (
        "classification:needs_new_vstd_abstraction" in tags
        or "needs new vstd" in rationale
        or "no predicate" in rationale
        or "no public" in rationale
    ):
        return (
            "needs_new_vstd_abstraction",
            "a source fact is documented but needs new shared vstd vocabulary before it can be expressed",
        )
    if (
        "classification:complex_result_or_pattern_model" in tags
        or "generic_slice_pattern_model_gap" in tags
        or "pattern" in rationale
    ):
        return (
            "complex_result_or_pattern_model_gap",
            "string, slice pattern, or complex result semantics lack a complete public model",
        )
    if "classification:iterator_or_adapter_result" in tags or "iterator" in rationale:
        return (
            "iterator_or_adapter_result_gap",
            "iterator or adapter state/result behavior is not captured by the available public model",
        )
    if (
        "classification:determinism_checker_unsupported" in tags
        or         DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG in tags
    ):
        return (
            "determinism_unsupported_contract_form",
            "determinism feedback could not certify the modeled contract form",
        )
    if (
        "classification:no_modeled_observable_output" in tags
        or "no_modeled_observable_output" in tags
    ):
        return (
            "no_modeled_observable_output",
            "the executable API has no modeled observable output beyond already-typed effects",
        )
    if (
        "classification:toolchain_unavailable" in tags
        or "not_in_verus_rust_1_96" in tags
    ):
        return (
            "toolchain_unavailable",
            "the API shape is not available in the pinned Verus Rust 1.96 toolchain",
        )
    if "public_api_allows_any_matching_index" in tags:
        return (
            "public_api_allows_multiple_results",
            "the public API permits more than one matching result and a singleton contract would be too strong",
        )
    if "borrowed-key" in rationale or "borrowed key" in rationale:
        return (
            "borrowed_key_model_underdetermined",
            "borrowed-key lookup semantics cannot select a unique stored key with existing predicates",
        )
    if "intrinsic" in rationale:
        return (
            "compiler_intrinsic_model_gap",
            "the result is determined by a compiler intrinsic without a public vstd semantic model",
        )
    return ("unclassified", "no normalized issue tag was available")


def audit_row(
    row: dict[str, str],
    vstd_api_paths: set[str],
    manifest_entries: dict[str, dict[str, Any]],
) -> dict[str, str]:
    classification_tag = classification_issue_tag(
        manifest_classification(
            manifest_entries,
            str(row.get("target") or ""),
        )
    )
    tags = split_tags(";".join(row_issue_tags(row)), classification_tag)
    normalized_tags = recognized_issue_tags(tags)
    tag_set = set(tags)
    taxonomy, taxonomy_reason = classify_skip(row, tag_set, vstd_api_paths)
    evidence_fields: list[str] = []
    if normalized_tags:
        evidence_fields.append("final_issue_tags")
    if str(row.get("rationale") or "").strip():
        evidence_fields.append("final_rationale")
    if str(row.get("requires_source_fidelity_classification") or "").strip():
        evidence_fields.append("requires_source_fidelity_classification")
    source_context_available = manifest_has_source_evidence(
        manifest_entries,
        str(row.get("target") or ""),
    )
    if source_context_available:
        evidence_fields.append("manifest_source_context")

    problems: list[str] = []
    if row.get("final_decision") != "skip":
        problems.append("final decision is not skip")
    if not str(row.get("rationale") or "").strip():
        problems.append("skip rationale is empty")
    if taxonomy == "unclassified":
        problems.append(taxonomy_reason)

    combined_tags = split_tags(";".join(tags), taxonomy)
    if not combined_tags:
        problems.append("combined issue/taxonomy tags are empty")

    source_backed = (
        bool(normalized_tags)
        and source_context_available
        and taxonomy != "unclassified"
    )
    if not source_backed:
        problems.append("taxonomy is not source-backed")

    return {
        "target": row.get("target", ""),
        "category": row.get("category", ""),
        "final_decision": row.get("final_decision", ""),
        "rationale_taxonomy": taxonomy,
        "taxonomy_source_fields": ";".join(evidence_fields),
        "taxonomy_source_backed": bool_text(source_backed),
        "adequacy_verdict": "adequate_source_backed_skip"
        if not problems
        else "unjustified_skip",
        "adequacy_notes": taxonomy_reason
        if not problems
        else "; ".join([taxonomy_reason, *problems]),
        "unjustified_skip": bool_text(bool(problems)),
        "issues_combined": ";".join(tags),
        "combined_issue_taxonomy_tags": ";".join(combined_tags),
        "rationale": one_line(row.get("rationale", "")),
        "requires": row.get("requires", ""),
        "requires_source_fidelity_classification": row.get(
            "requires_source_fidelity_classification",
            "",
        ),
    }


def build_summary(
    root: Path,
    audit_rows: list[dict[str, str]],
    final_rows: list[dict[str, str]],
    *,
    vstd_api_paths: set[str],
    batch_repairs: list[str],
    final_csv_repairs: list[str],
    accepted_fingerprint_before: str,
    accepted_fingerprint_after: str,
) -> dict[str, Any]:
    skip_rows = [row for row in final_rows if row.get("final_decision") == "skip"]
    add_spec_rows = [row for row in final_rows if row.get("final_decision") == "add_spec"]
    taxonomy_counts = Counter(row["rationale_taxonomy"] for row in audit_rows)
    issue_counts = Counter(
        tag for row in audit_rows for tag in split_tags(row["issues_combined"])
    )
    duplicate_taxonomy_rows = [
        row
        for row in audit_rows
        if row["rationale_taxonomy"] == "duplicate_existing_vstd_spec"
    ]
    duplicate_rows_with_duplicate_vstd_tag = [
        row
        for row in duplicate_taxonomy_rows
        if DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG
        in set(split_tags(row["issues_combined"]))
    ]
    duplicate_rows_with_generic_determinism_tag = [
        row
        for row in duplicate_taxonomy_rows
        if DETERMINISM_UNSUPPORTED_CONTRACT_FORM_TAG
        in set(split_tags(row["issues_combined"]))
    ]
    exact_vstd_skip_rows = [
        row for row in audit_rows if row["target"] in vstd_api_paths
    ]
    exact_vstd_skip_rows_not_duplicate_classified = [
        row
        for row in exact_vstd_skip_rows
        if row["rationale_taxonomy"] != "duplicate_existing_vstd_spec"
        or DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG
        not in set(split_tags(row["issues_combined"]))
    ]
    empty_issue_tag_rows = [
        row["target"] for row in audit_rows if not row["issues_combined"].strip()
    ]
    empty_combined_rows = [
        row["target"]
        for row in audit_rows
        if not row["combined_issue_taxonomy_tags"].strip()
    ]
    unclassified = [
        row["target"] for row in audit_rows if row["rationale_taxonomy"] == "unclassified"
    ]
    unjustified = [
        row["target"] for row in audit_rows if row["unjustified_skip"] == "true"
    ]
    checks = {
        f"final_rows_{EXPECTED_FINAL_ROWS}": len(final_rows) == EXPECTED_FINAL_ROWS,
        f"add_spec_rows_{EXPECTED_ADD_SPEC_ROWS}": (
            len(add_spec_rows) == EXPECTED_ADD_SPEC_ROWS
        ),
        f"skip_rows_{EXPECTED_SKIP_ROWS}": len(skip_rows) == EXPECTED_SKIP_ROWS,
        f"audited_skip_rows_{EXPECTED_SKIP_ROWS}": (
            len(audit_rows) == EXPECTED_SKIP_ROWS
        ),
        "empty_skip_rationale_rows_zero": all(
            str(row.get("rationale") or "").strip() for row in skip_rows
        ),
        "empty_skip_issue_tag_rows_zero": not empty_issue_tag_rows,
        "empty_combined_issue_taxonomy_rows_zero": not empty_combined_rows,
        "unclassified_skip_rows_zero": not unclassified,
        "unjustified_skip_rows_zero": not unjustified,
        "accepted_add_spec_contracts_unchanged": (
            accepted_fingerprint_before == accepted_fingerprint_after
        ),
        "duplicate_existing_vstd_spec_rows_match_issue_count": (
            len(duplicate_taxonomy_rows)
            == issue_counts.get(DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG, 0)
        ),
        "duplicate_existing_vstd_spec_rows_all_carry_duplicate_vstd_tag": (
            len(duplicate_rows_with_duplicate_vstd_tag) == len(duplicate_taxonomy_rows)
        ),
        "duplicate_existing_vstd_spec_rows_with_generic_determinism_zero": (
            not duplicate_rows_with_generic_determinism_tag
        ),
        "exact_vstd_skip_rows_not_duplicate_classified_zero": (
            not exact_vstd_skip_rows_not_duplicate_classified
        ),
    }
    return {
        "schema_version": 1,
        "generated_at_utc": utc_now(),
        "canonical_root": str(root.resolve()),
        "inputs": {
            "batch_summary_json": str((root / "batch_summary.json").resolve()),
            "final_candidates_csv": str((root / "final_candidates.csv").resolve()),
        },
        "counts": {
            "final_rows": len(final_rows),
            "add_spec_rows": len(add_spec_rows),
            "skip_rows": len(skip_rows),
            "audited_skip_rows": len(audit_rows),
            "empty_skip_rationale_rows": sum(
                not str(row.get("rationale") or "").strip() for row in skip_rows
            ),
            "empty_skip_issue_tag_rows": len(empty_issue_tag_rows),
            "empty_combined_issue_taxonomy_rows": len(empty_combined_rows),
            "unclassified_skip_rows": len(unclassified),
            "unjustified_skip_rows": len(unjustified),
            "batch_issue_tag_repairs_applied": len(batch_repairs),
            "final_csv_issue_tag_repairs_applied": len(final_csv_repairs),
            "tracked_issue_tag_repair_targets": len(REPAIR_ISSUE_TAGS),
            "tracked_issue_tag_repair_targets_with_tags": sum(
                1
                for target in REPAIR_ISSUE_TAGS
                for row in audit_rows
                if row["target"] == target and row["issues_combined"].strip()
            ),
            "duplicate_existing_vstd_spec_rows": len(duplicate_taxonomy_rows),
            "duplicate_vstd_assume_specification_issue_count": issue_counts.get(
                DUPLICATE_VSTD_ASSUME_SPECIFICATION_TAG,
                0,
            ),
            "duplicate_existing_vstd_spec_rows_with_duplicate_vstd_tag": len(
                duplicate_rows_with_duplicate_vstd_tag
            ),
            "duplicate_existing_vstd_spec_rows_with_generic_determinism_tag": len(
                duplicate_rows_with_generic_determinism_tag
            ),
            "exact_vstd_skip_rows": len(exact_vstd_skip_rows),
            "exact_vstd_skip_rows_not_duplicate_classified": len(
                exact_vstd_skip_rows_not_duplicate_classified
            ),
        },
        "taxonomy_counts": dict(sorted(taxonomy_counts.items())),
        "issue_counts": dict(issue_counts.most_common()),
        "empty_skip_issue_tag_targets": empty_issue_tag_rows,
        "empty_combined_issue_taxonomy_targets": empty_combined_rows,
        "unclassified_skip_targets": unclassified,
        "unjustified_skip_targets": unjustified,
        "duplicate_existing_vstd_spec_targets_missing_duplicate_vstd_tag": [
            row["target"]
            for row in duplicate_taxonomy_rows
            if row not in duplicate_rows_with_duplicate_vstd_tag
        ],
        "duplicate_existing_vstd_spec_targets_with_generic_determinism_tag": [
            row["target"] for row in duplicate_rows_with_generic_determinism_tag
        ],
        "exact_vstd_skip_targets_not_duplicate_classified": [
            row["target"] for row in exact_vstd_skip_rows_not_duplicate_classified
        ],
        "issue_tag_repair_targets": sorted(REPAIR_ISSUE_TAGS),
        "batch_issue_tag_repairs_applied": sorted(batch_repairs),
        "final_csv_issue_tag_repairs_applied": sorted(final_csv_repairs),
        "accepted_add_spec_contract_hash_before": accepted_fingerprint_before,
        "accepted_add_spec_contract_hash_after": accepted_fingerprint_after,
        "acceptance_checks": checks,
        "acceptance_passed": all(checks.values()),
    }


def write_report(path: Path, summary: dict[str, Any], artifacts: dict[str, str]) -> None:
    counts = summary["counts"]
    lines = [
        "# Final Skip Rationale Taxonomy Audit",
        "",
        f"Generated at UTC `{summary['generated_at_utc']}`.",
        "",
        "This audit covers every `final_candidates.csv` row whose final decision is "
        "`skip`, classifies the row by a source-backed rationale taxonomy, and "
        "tracks the targeted repair for skips that had a non-empty rationale but "
        "empty machine issue tags.",
        "",
        "## Counts",
        "",
        "| Measure | Value |",
        "| --- | ---: |",
        f"| final rows | {counts['final_rows']} |",
        f"| add_spec rows | {counts['add_spec_rows']} |",
        f"| skip rows | {counts['skip_rows']} |",
        f"| audited skip rows | {counts['audited_skip_rows']} |",
        f"| empty skip rationales | {counts['empty_skip_rationale_rows']} |",
        f"| empty skip issue tags | {counts['empty_skip_issue_tag_rows']} |",
        f"| empty combined issue/taxonomy tags | {counts['empty_combined_issue_taxonomy_rows']} |",
        f"| unclassified skips | {counts['unclassified_skip_rows']} |",
        f"| unjustified skips | {counts['unjustified_skip_rows']} |",
        f"| tracked issue-tag repair targets | {counts['tracked_issue_tag_repair_targets']} |",
        f"| tracked repair targets with tags | {counts['tracked_issue_tag_repair_targets_with_tags']} |",
        f"| batch issue-tag repairs applied | {counts['batch_issue_tag_repairs_applied']} |",
        f"| final CSV issue-tag repairs applied | {counts['final_csv_issue_tag_repairs_applied']} |",
        f"| duplicate existing vstd spec rows | {counts['duplicate_existing_vstd_spec_rows']} |",
        f"| duplicate vstd issue tags | {counts['duplicate_vstd_assume_specification_issue_count']} |",
        f"| duplicate rows with generic determinism tag | {counts['duplicate_existing_vstd_spec_rows_with_generic_determinism_tag']} |",
        f"| exact vstd skip rows | {counts['exact_vstd_skip_rows']} |",
        f"| exact vstd skips not duplicate-classified | {counts['exact_vstd_skip_rows_not_duplicate_classified']} |",
        "",
        "## Taxonomy Counts",
        "",
        "| Taxonomy | Rows |",
        "| --- | ---: |",
    ]
    for taxonomy, count in summary["taxonomy_counts"].items():
        lines.append(f"| `{taxonomy}` | {count} |")
    lines.extend(["", "## Acceptance Checks", "", "| Check | Passed |", "| --- | --- |"])
    for key, value in summary["acceptance_checks"].items():
        lines.append(f"| `{key}` | `{bool_text(bool(value))}` |")
    lines.extend(["", "## Artifacts", ""])
    for name, artifact_path in artifacts.items():
        lines.append(f"- `{name}`: `{artifact_path}`")
    path.write_text("\n".join(lines).rstrip() + "\n")


def verification_block(summary: dict[str, Any], artifacts: dict[str, str]) -> dict[str, Any]:
    counts = summary["counts"]
    return {
        "artifact_schema": 1,
        "source": (
            "final_candidates.csv rows where final_decision == 'skip', classified "
            "by audit_final_skip_rationales.py using final issue tags and "
            "source-backed rationales"
        ),
        "audited_skip_rows": counts["audited_skip_rows"],
        "skip_rows": counts["skip_rows"],
        "empty_skip_rationale_rows": counts["empty_skip_rationale_rows"],
        "empty_skip_issue_tag_rows": counts["empty_skip_issue_tag_rows"],
        "empty_combined_issue_taxonomy_rows": counts[
            "empty_combined_issue_taxonomy_rows"
        ],
        "unclassified_skip_rows": counts["unclassified_skip_rows"],
        "unjustified_skip_rows": counts["unjustified_skip_rows"],
        "tracked_issue_tag_repair_targets": counts["tracked_issue_tag_repair_targets"],
        "tracked_issue_tag_repair_targets_with_tags": counts[
            "tracked_issue_tag_repair_targets_with_tags"
        ],
        "duplicate_existing_vstd_spec_rows": counts["duplicate_existing_vstd_spec_rows"],
        "duplicate_vstd_assume_specification_issue_count": counts[
            "duplicate_vstd_assume_specification_issue_count"
        ],
        "duplicate_existing_vstd_spec_rows_with_duplicate_vstd_tag": counts[
            "duplicate_existing_vstd_spec_rows_with_duplicate_vstd_tag"
        ],
        "duplicate_existing_vstd_spec_rows_with_generic_determinism_tag": counts[
            "duplicate_existing_vstd_spec_rows_with_generic_determinism_tag"
        ],
        "duplicate_existing_vstd_spec_targets_missing_duplicate_vstd_tag": summary[
            "duplicate_existing_vstd_spec_targets_missing_duplicate_vstd_tag"
        ],
        "duplicate_existing_vstd_spec_targets_with_generic_determinism_tag": summary[
            "duplicate_existing_vstd_spec_targets_with_generic_determinism_tag"
        ],
        "exact_vstd_skip_rows": counts["exact_vstd_skip_rows"],
        "exact_vstd_skip_rows_not_duplicate_classified": counts[
            "exact_vstd_skip_rows_not_duplicate_classified"
        ],
        "exact_vstd_skip_targets_not_duplicate_classified": summary[
            "exact_vstd_skip_targets_not_duplicate_classified"
        ],
        "batch_issue_tag_repairs_applied": counts["batch_issue_tag_repairs_applied"],
        "final_csv_issue_tag_repairs_applied": counts[
            "final_csv_issue_tag_repairs_applied"
        ],
        "taxonomy_counts": summary["taxonomy_counts"],
        "issue_counts": summary["issue_counts"],
        "acceptance_checks": summary["acceptance_checks"],
        "acceptance_passed": summary["acceptance_passed"],
        "artifacts": artifacts,
    }


def update_final_verification(
    root: Path,
    summary: dict[str, Any],
    artifacts: dict[str, str],
) -> None:
    verification_path = root / "final_verification.json"
    if not verification_path.exists():
        return
    verification = json.loads(verification_path.read_text())
    verification["full_skip_rationale_taxonomy"] = verification_block(summary, artifacts)
    verification.setdefault("artifacts", {}).update(artifacts)
    verification_path.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")


def run_audit(
    root: Path = CANONICAL_FRESH_ROOT,
    *,
    manifest: Path | None = None,
    contracts: Path | None = None,
    repair_batch: bool = True,
    repair_final: bool = True,
    update_verification: bool = True,
    write_artifacts: bool = True,
) -> dict[str, Any]:
    root = root.expanduser().resolve()
    manifest = manifest.expanduser().resolve() if manifest is not None else None
    manifest_entries = load_manifest_entries(root, manifest)
    vstd_api_paths = load_vstd_api_paths(contracts)

    batch_repairs: list[str] = []
    if repair_batch:
        batch_repairs = repair_batch_and_target_summaries(
            root,
            manifest_entries,
            vstd_api_paths,
        )

    final_path = root / "final_candidates.csv"
    if not final_path.exists():
        raise FileNotFoundError(final_path)
    rows_before, fields = read_csv(final_path)
    accepted_before = accepted_add_spec_fingerprint(rows_before)

    final_csv_repairs: list[str] = []
    if repair_final:
        final_csv_repairs = repair_final_candidate_rows(
            root,
            manifest_entries,
            vstd_api_paths,
        )

    final_rows, fields = read_csv(final_path)
    accepted_after = accepted_add_spec_fingerprint(final_rows)
    audit_rows = [
        audit_row(row, vstd_api_paths, manifest_entries)
        for row in final_rows
        if row.get("final_decision") == "skip"
    ]
    summary = build_summary(
        root,
        audit_rows,
        final_rows,
        vstd_api_paths=vstd_api_paths,
        batch_repairs=batch_repairs,
        final_csv_repairs=final_csv_repairs,
        accepted_fingerprint_before=accepted_before,
        accepted_fingerprint_after=accepted_after,
    )

    artifacts = {
        AUDIT_CSV: str((root / AUDIT_CSV).resolve()),
        AUDIT_SUMMARY_JSON: str((root / AUDIT_SUMMARY_JSON).resolve()),
        AUDIT_REPORT: str((root / AUDIT_REPORT).resolve()),
    }
    summary["artifacts"] = artifacts

    if write_artifacts:
        write_csv(root / AUDIT_CSV, audit_rows, AUDIT_FIELDS)
        (root / AUDIT_SUMMARY_JSON).write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n"
        )
        write_report(root / AUDIT_REPORT, summary, artifacts)
    if update_verification:
        update_final_verification(root, summary, artifacts)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fresh-root",
        type=Path,
        default=CANONICAL_FRESH_ROOT,
        help="Canonical fresh specgen output root.",
    )
    parser.add_argument("--manifest", type=Path, help="Override classified manifest path.")
    parser.add_argument(
        "--contracts",
        type=Path,
        default=DEFAULT_VSTD_CONTRACTS,
        help="vstd_contracts.json file used for exact duplicate API-path normalization.",
    )
    parser.add_argument(
        "--no-repair-batch",
        action="store_true",
        help="Do not repair batch_summary.json or per-target summary.json issue tags.",
    )
    parser.add_argument(
        "--no-repair-final",
        action="store_true",
        help="Do not repair final_candidates.csv issue tags.",
    )
    parser.add_argument(
        "--no-update-final-verification",
        action="store_true",
        help="Do not add the audit block to final_verification.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_audit(
        args.fresh_root,
        manifest=args.manifest,
        contracts=args.contracts,
        repair_batch=not args.no_repair_batch,
        repair_final=not args.no_repair_final,
        update_verification=not args.no_update_final_verification,
    )
    counts = summary["counts"]
    print(
        "audited "
        f"{counts['audited_skip_rows']} skip rows; "
        f"empty_issue_tags={counts['empty_skip_issue_tag_rows']}; "
        f"empty_combined_issue_taxonomy={counts['empty_combined_issue_taxonomy_rows']}; "
        f"unclassified={counts['unclassified_skip_rows']}; "
        f"unjustified={counts['unjustified_skip_rows']}; "
        f"batch_repairs={counts['batch_issue_tag_repairs_applied']}; "
        f"final_csv_repairs={counts['final_csv_issue_tag_repairs_applied']}; "
        f"acceptance_passed={bool_text(summary['acceptance_passed'])}"
    )
    return 0 if summary["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
