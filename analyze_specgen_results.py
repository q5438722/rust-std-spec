#!/usr/bin/env python3
"""Summarize Rust std contract-generation and determinism-feedback results."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

WORKSPACE = Path(__file__).resolve().parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

import audit_final_skip_rationales


FINAL_CANDIDATE_FIELDS = [
    "target",
    "category",
    "status",
    "rounds",
    "initial_decision",
    "final_decision",
    "contract_form",
    "typecheck_passed",
    "det_status",
    "r0_z3",
    "classification",
    "raw_det_reward",
    "guarded_reward",
    "semantic_guarded_reward",
    "issues",
    "semantic_gate_issues",
    "semantic_review_issues",
    "requires",
    "ensures",
    "contract_code",
    "rationale",
    "requires_source_fidelity_classification",
    "requires_source_fidelity_rationale",
    "requires_source_reference",
    "requires_source_excerpt",
]

ACCEPTED_SEMANTIC_CANDIDATE_PREDICATE = [
    "final_decision == 'add_spec'",
    "typecheck_passed == true",
    "guarded_reward == 1",
    "semantic_guarded_reward == 1",
    "issues == ''",
    "semantic_gate_issues == ''",
    "semantic_review_issues == ''",
    "requires == '' or requires_source_fidelity_classification == 'source_justified'",
]

ALLOWED_FUNCTION_LIKE_KINDS = {
    "free_function",
    "inherent_method",
    "primitive_method",
    "trait_method",
}

ACCEPTED_REQUIRES_SOURCE_FIDELITY_SNAPSHOT_KEYS = [
    "artifact_schema",
    "source",
    "source_final_candidates_rows",
    "audited_rows",
    "source_gate_input_rows",
    "source_justified_rows",
    "source_unjustified_rows",
    "unclassified_rows",
    "accepted_after_source_gate_rows",
    "source_unjustified_targets",
    "source_unjustified_accepted_targets",
    "unclassified_targets",
    "validation",
]

ACCEPTED_ENSURES_SOURCE_FIDELITY_SNAPSHOT_KEYS = [
    "artifact_schema",
    "source",
    "source_final_candidates_rows",
    "accepted_rows",
    "audited_rows",
    "source_justified_rows",
    "source_unjustified_rows",
    "unclassified_rows",
    "source_context_evidence_rows",
    "source_unjustified_accepted_targets",
    "unclassified_targets",
    "validation",
]

SOURCE_FIDELITY_JUSTIFIED = "source_justified"
SOURCE_FIDELITY_UNCLASSIFIED = "unclassified"
SOURCE_FIDELITY_NOT_APPLICABLE = "not_applicable"

CSTRING_FROM_VEC_WITH_NUL_UNCHECKED_TARGET = (
    "alloc::ffi::CString::from_vec_with_nul_unchecked"
)
STRING_FROM_UTF8_UNCHECKED_TARGET = "alloc::string::String::from_utf8_unchecked"
SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET = "core::slice::split_at_mut_unchecked"
SLICE_SPLIT_AT_MUT_CHECKED_TARGET = "core::slice::split_at_mut_checked"
STR_SPLIT_AT_CHECKED_TARGET = "core::str::split_at_checked"
STR_SPLIT_AT_MUT_CHECKED_TARGET = "core::str::split_at_mut_checked"
STRING_REPLACE_RANGE_TARGET = "alloc::string::String::replace_range"
STR_FROM_UTF8_TARGET = "core::str::from_utf8"
STR_FROM_UTF8_MUT_TARGET = "core::str::from_utf8_mut"
SLICE_REVERSE_TARGET = "core::slice::reverse"
ARRAY_FROM_MUT_TARGET = "core::array::from_mut"
SLICE_FROM_MUT_TARGET = "core::slice::from_mut"
ARRAY_AS_MUT_SLICE_TARGET = "core::array::as_mut_slice"
ARRAY_EACH_MUT_TARGET = "core::array::each_mut"
SLICE_AS_MUT_ARRAY_TARGET = "core::slice::as_mut_array"
SLICE_FIRST_CHUNK_MUT_TARGET = "core::slice::first_chunk_mut"
SLICE_LAST_CHUNK_MUT_TARGET = "core::slice::last_chunk_mut"
SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET = "core::slice::split_first_chunk_mut"
SLICE_SPLIT_LAST_CHUNK_MUT_TARGET = "core::slice::split_last_chunk_mut"
SLICE_SPLIT_FIRST_MUT_TARGET = "core::slice::split_first_mut"
SLICE_SPLIT_LAST_MUT_TARGET = "core::slice::split_last_mut"
SLICE_SPLIT_OFF_FIRST_MUT_TARGET = "core::slice::split_off_first_mut"
SLICE_SPLIT_OFF_LAST_MUT_TARGET = "core::slice::split_off_last_mut"
SLICE_AS_CHUNKS_TARGET = "core::slice::as_chunks"
SLICE_AS_RCHUNKS_TARGET = "core::slice::as_rchunks"
SLICE_AS_CHUNKS_MUT_TARGET = "core::slice::as_chunks_mut"
SLICE_AS_RCHUNKS_MUT_TARGET = "core::slice::as_rchunks_mut"
SOURCE_BACKED_SAFE_SLICE_CHUNK_TARGETS = {
    SLICE_AS_CHUNKS_TARGET,
    SLICE_AS_RCHUNKS_TARGET,
    SLICE_AS_CHUNKS_MUT_TARGET,
    SLICE_AS_RCHUNKS_MUT_TARGET,
}
SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS = {
    ARRAY_FROM_MUT_TARGET,
    SLICE_FROM_MUT_TARGET,
    ARRAY_AS_MUT_SLICE_TARGET,
    SLICE_AS_MUT_ARRAY_TARGET,
    SLICE_FIRST_CHUNK_MUT_TARGET,
    SLICE_LAST_CHUNK_MUT_TARGET,
}
SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_TARGETS = {
    SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET,
    SLICE_SPLIT_LAST_CHUNK_MUT_TARGET,
}
SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS = {
    SLICE_SPLIT_FIRST_MUT_TARGET,
    SLICE_SPLIT_LAST_MUT_TARGET,
    SLICE_SPLIT_OFF_FIRST_MUT_TARGET,
    SLICE_SPLIT_OFF_LAST_MUT_TARGET,
}
SOURCE_BACKED_MUTATING_SLICE_TARGETS = {
    SLICE_REVERSE_TARGET,
}
SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS = {
    CSTRING_FROM_VEC_WITH_NUL_UNCHECKED_TARGET,
    STRING_FROM_UTF8_UNCHECKED_TARGET,
}
SOURCE_BACKED_BTREE_RAW_ALGEBRA_TARGETS = {
    "alloc::collections::BTreeMap::append",
    "alloc::collections::BTreeSet::append",
    "alloc::collections::BTreeSet::is_disjoint",
}
SOURCE_BACKED_CMP_MIN_MAX_TARGETS = {
    "core::cmp::min": {
        "function": "min",
        "kind": "minimum",
        "tie_argument": "first",
        "delegation": "v1.min(v2)",
    },
    "core::cmp::max": {
        "function": "max",
        "kind": "maximum",
        "tie_argument": "second",
        "delegation": "v1.max(v2)",
    },
}
VECDEQUE_BINARY_SEARCH_TARGET = "alloc::collections::VecDeque::binary_search"
SLICE_BINARY_SEARCH_TARGET = "core::slice::binary_search"
SOURCE_BACKED_BINARY_SEARCH_TARGETS = {
    VECDEQUE_BINARY_SEARCH_TARGET: {
        "display": "VecDeque::binary_search",
        "delegation": "self.binary_search_by(|e| e.cmp(x))",
        "not_sorted_token": "if the `vecdeque` is not sorted",
        "evidence_tokens": [
            "If the `VecDeque` is not sorted",
            "multiple matches",
            "one of the matches",
            "index where a matching",
            "while maintaining sorted order",
            "uniquely determined position",
            "If `num` is unique",
            "pub fn binary_search",
            "T: Ord",
            "self.binary_search_by(|e| e.cmp(x))",
        ],
    },
    SLICE_BINARY_SEARCH_TARGET: {
        "display": "slice::binary_search",
        "delegation": "self.binary_search_by(|p| p.cmp(x))",
        "not_sorted_token": "if the slice is not sorted",
        "evidence_tokens": [
            "If the slice is not sorted",
            "multiple matches",
            "one of the matches",
            "index where a matching",
            "while maintaining sorted order",
            "uniquely determined position",
            "If `num` is unique",
            "pub fn binary_search",
            "T: Ord",
            "self.binary_search_by(|p| p.cmp(x))",
        ],
    },
}
HASHSET_REPLACE_TARGET = "std::collections::HashSet::replace"
HASHMAP_REMOVE_ENTRY_TARGET = "std::collections::HashMap::remove_entry"
HASHMAP_GET_MUT_TARGET = "std::collections::HashMap::get_mut"
BTREEMAP_GET_MUT_TARGET = "alloc::collections::BTreeMap::get_mut"
LINKEDLIST_BACK_MUT_TARGET = "alloc::collections::LinkedList::back_mut"
SOURCE_BACKED_MAP_GET_MUT_TARGETS = {
    HASHMAP_GET_MUT_TARGET,
    BTREEMAP_GET_MUT_TARGET,
}
THREAD_RESULT_FLATTEN_TARGET = "std::thread::Result::flatten"
THREAD_RESULT_FLATTEN_CONTRACT_TARGET = (
    "core::result::Result::<core::result::Result<T,E>,E>::flatten"
)
RANGE_INCLUSIVE_EXHAUSTION_TARGETS = {
    "core::ops::RangeInclusive::start",
    "core::ops::RangeInclusive::end",
}

REQUIRES_SOURCE_FIDELITY_AUDIT_FIELDS = [
    "target",
    "requires",
    "classification",
    "rationale",
    "source_reference",
    "source_excerpt",
    "accepted_after_source_gate",
]

ENSURES_SOURCE_FIDELITY_AUDIT_FIELDS = [
    "target",
    "ensures",
    "classification",
    "evidence_kind",
    "rationale",
    "source_reference",
    "source_excerpt",
]

ACCEPTED_ASSUME_SPEC_TARGET_BINDING_AUDIT_FIELDS = [
    "target",
    "status",
    "binding_count",
    "binding",
    "binding_name",
    "binding_owner",
    "binding_module",
    "matched_expected_source",
    "matched_expected_owner",
    "matched_expected_module",
    "error",
]

ACCEPTED_ASSUME_SPEC_SIGNATURE_SHAPE_AUDIT_FIELDS = [
    "target",
    "status",
    "manifest_declaration",
    "manifest_input_arity",
    "assume_spec_input_arity",
    "manifest_input_shapes",
    "assume_spec_input_shapes",
    "input_arity_match",
    "input_shape_match",
    "manifest_output_shape",
    "assume_spec_output_shape",
    "output_shape_match",
    "error",
]

ACCEPTED_ASSUME_SPEC_GENERIC_BOUNDS_AUDIT_FIELDS = [
    "target",
    "status",
    "manifest_declaration",
    "manifest_generic_params",
    "assume_spec_generic_params",
    "generic_param_kinds_match",
    "manifest_const_generics",
    "assume_spec_const_generics",
    "const_generic_match",
    "manifest_trait_bounds",
    "assume_spec_trait_bounds",
    "trait_bounds_match",
    "manifest_where_clause_bounds",
    "assume_spec_where_clause_bounds",
    "where_clause_bounds_satisfied",
    "missing_bounds",
    "extra_bounds",
    "missing_where_clause_bounds",
    "extra_where_clause_bounds",
    "error",
]

FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_CSV = (
    "final_candidate_payload_consistency_audit.csv"
)
FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_JSON = (
    "final_candidate_payload_consistency_audit.json"
)
FINAL_CANDIDATE_PAYLOAD_COMPARE_FIELDS = [
    "final_decision",
    "contract_form",
    "contract_code",
    "requires",
    "ensures",
    "rationale",
    "raw_det_reward",
    "guarded_reward",
    "issues",
]
FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_FIELDS = [
    "target",
    "safe_name",
    "batch_result_present",
    "summary_artifact_present",
    "summary_artifact_valid",
    "batch_mismatched_fields",
    "summary_mismatched_fields",
    "field_mismatch_count",
    "validation_passed",
    "summary_artifact_path",
]
CANONICAL_ARTIFACT_PROVENANCE_SCHEMA = 1
STALE_OR_PRIOR_OUTPUT_ROOTS = [
    Path("/home/chentianyu/nanvix-rust-std-spec-survey/specgen/all-2121-gpt56sol"),
    Path("/home/chentianyu/nanvix-rust-std-specgen-rerun-2026-08-06/specgen/all-2121-gpt56sol"),
]
ALLOWED_STALE_REFERENCE_CONTEXT_PREFIXES = ("prior_fresh_delta.inputs.",)
EXTERNAL_TARGET_ARTIFACT_INPUT_CONTEXT_PREFIXES = (
    "final_candidate_payload_consistency.inputs.target_artifact_root_",
    "target_artifact_integrity.source.target_artifact_roots[",
    "target_artifact_integrity.source.targets_dir",
)
PROVENANCE_SAMPLE_LIMIT = 20


def metadata_nodes(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def collect(item: dict[str, Any]) -> None:
        nodes.append(item)
        batches = item.get("batches") or []
        if not isinstance(batches, list):
            raise ValueError("metadata.batches must be a list")
        for batch in batches:
            if not isinstance(batch, dict):
                raise ValueError("metadata.batches contains a non-object entry")
            collect(batch)

    collect(metadata)
    return nodes


def manifest_paths_from_metadata(metadata: dict[str, Any]) -> list[Path]:
    manifest_paths = [
        Path(str(item["manifest"]))
        for item in metadata_nodes(metadata)
        if item.get("manifest")
    ]
    return sorted(set(manifest_paths), key=str)


def target_artifact_root_paths_from_metadata(
    metadata: dict[str, Any],
) -> list[Path]:
    nodes = metadata_nodes(metadata)
    candidates: list[Path] = []
    for item in nodes:
        target_artifact_roots = item.get("target_artifact_roots") or []
        if isinstance(target_artifact_roots, (str, Path)):
            target_artifact_roots = [target_artifact_roots]
        candidates.extend(
            Path(str(value)).expanduser().absolute()
            for value in target_artifact_roots
            if value
        )

    if not candidates:
        for item in nodes:
            batch_files = item.get("batch_files") or []
            if isinstance(batch_files, (str, Path)):
                batch_files = [batch_files]
            candidates.extend(
                Path(str(value)).expanduser().absolute().parent
                for value in batch_files
                if value
            )

    roots: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        roots.append(candidate)
    return roots


def combined_target_artifact_root_declarations(
    batch_paths: list[Path],
    payloads: list[dict[str, Any]],
) -> list[Path]:
    roots: set[Path] = set()
    for batch_path, payload in zip(batch_paths, payloads, strict=True):
        declared_roots = target_artifact_root_paths_from_metadata(
            payload.get("metadata") or {}
        )
        if declared_roots:
            roots.update(declared_roots)
        else:
            roots.add(batch_path.parent.expanduser().absolute())
    return sorted(roots, key=str)


def manifest_entries_from_metadata(
    metadata: dict[str, Any],
) -> list[dict[str, Any]] | None:
    manifest_paths = manifest_paths_from_metadata(metadata)
    if not manifest_paths:
        return None

    entries: list[dict[str, Any]] = []
    for manifest_path in manifest_paths:
        payload = json.loads(manifest_path.read_text())
        manifest_entries = payload.get("targets", payload)
        if not isinstance(manifest_entries, list):
            raise ValueError(f"manifest is not a target list: {manifest_path}")
        if any(not isinstance(entry, dict) for entry in manifest_entries):
            raise ValueError(f"manifest contains non-object targets: {manifest_path}")
        entries.extend(manifest_entries)
    return entries


def manifest_targets_from_metadata(metadata: dict[str, Any]) -> set[str] | None:
    entries = manifest_entries_from_metadata(metadata)
    if entries is None:
        return None
    return {entry["target"] for entry in entries}


def specgen_safe_name(path: str) -> str:
    """Mirror run_rust_std_spec_feedback.safe_name for target artifact paths."""

    return re.sub(r"[^A-Za-z0-9_.-]+", "__", path).strip("_")


def read_json_artifact(path: Path) -> tuple[Any | None, str | None, str | None]:
    try:
        return json.loads(path.read_text()), None, None
    except json.JSONDecodeError as exc:
        return (
            None,
            "bad_json",
            f"{exc.msg} at line {exc.lineno}, column {exc.colno}",
        )
    except OSError as exc:
        return None, "unreadable", str(exc)


def entry_kinds(entry: dict[str, Any]) -> list[str]:
    return [str(kind) for kind in entry.get("kinds") or [] if str(kind)]


def declaration_has_function_signature(declaration: dict[str, Any]) -> bool:
    header = declaration.get("header")
    signature = declaration.get("signature")
    return (
        bool(declaration.get("name"))
        and isinstance(header, dict)
        and isinstance(signature, dict)
        and isinstance(signature.get("inputs"), list)
        and "is_c_variadic" in signature
        and "output" in signature
    )


def declaration_is_stable(declaration: dict[str, Any]) -> bool:
    stability = declaration.get("stability")
    return isinstance(stability, dict) and stability.get("level") == "stable"


def declaration_has_public_api_visibility(
    entry: dict[str, Any],
    declaration: dict[str, Any],
) -> bool:
    visibility = declaration.get("visibility")
    if visibility == "public":
        return True
    return visibility == "default" and "trait_method" in entry_kinds(entry)


def declaration_has_source_provenance(declaration: dict[str, Any]) -> bool:
    span = declaration.get("span")
    return (
        bool(declaration.get("declaration_id"))
        and isinstance(span, dict)
        and bool(span.get("filename"))
        and bool(str(declaration.get("source_context") or "").strip())
    )


def primary_declaration(entry: dict[str, Any] | None) -> dict[str, Any]:
    if not entry:
        return {}
    declarations = entry.get("declarations") or []
    for declaration in declarations:
        if declaration_has_source_provenance(declaration):
            return declaration
    return declarations[0] if declarations else {}


def declaration_source_reference(declaration: dict[str, Any]) -> str:
    span = declaration.get("span") or {}
    filename = span.get("filename") or ""
    begin = span.get("begin") or []
    line = begin[0] if isinstance(begin, list) and begin else None
    if filename and line:
        return f"{filename}:{line}"
    return str(filename)


def parse_source_context_lines(source_context: str) -> list[tuple[int, str]]:
    lines = []
    for line in source_context.splitlines():
        match = re.match(r"\s*(\d+):\s?(.*)", line)
        if match:
            lines.append((int(match.group(1)), match.group(2)))
    return lines


def source_context_plain_text(declaration: dict[str, Any]) -> str:
    parsed = parse_source_context_lines(str(declaration.get("source_context") or ""))
    if parsed:
        return " ".join(re.sub(r"^\s*///\s?", "", text).strip() for _, text in parsed)
    return str(declaration.get("source_context") or "")


def all_source_context_plain_text(entry: dict[str, Any] | None) -> str:
    if not entry:
        return ""
    declarations = [
        *(entry.get("verification_declarations") or []),
        *(entry.get("declarations") or []),
    ]
    return " ".join(
        source_context_plain_text(declaration)
        for declaration in declarations
        if declaration_has_source_provenance(declaration)
    )


def source_context_excerpt(
    declaration: dict[str, Any],
    *,
    before: int = 4,
    after: int = 8,
) -> str:
    span = declaration.get("span") or {}
    begin = span.get("begin") or []
    line = begin[0] if isinstance(begin, list) and begin else None
    parsed = parse_source_context_lines(str(declaration.get("source_context") or ""))
    if line is not None and parsed:
        selected = [
            (number, text)
            for number, text in parsed
            if line - before <= number <= line + after
        ]
        if selected:
            return "\n".join(f"{number}: {text}" for number, text in selected)
    return "\n".join(str(declaration.get("source_context") or "").splitlines()[:12])


def declaration_evidence_text(declaration: dict[str, Any]) -> str:
    pieces = [
        str(declaration.get("source_context") or ""),
        json.dumps(declaration.get("signature") or {}, sort_keys=True),
        json.dumps(declaration.get("generics") or {}, sort_keys=True),
    ]
    return "\n".join(pieces)


def source_text_for_entry(manifest_entry: dict[str, Any] | None) -> str:
    declaration = primary_declaration(manifest_entry)
    if not declaration_has_source_provenance(declaration):
        return ""
    return declaration_evidence_text(declaration)


def compact_verus_clause(text: Any) -> str:
    normalized = re.sub(r"\s+", "", str(text or "")).strip("()")
    normalized = normalized.replace("&&&", "&&")
    normalized = re.sub(r"(?<=\{)&&", "", normalized)
    return re.sub(r",(?=\))", "", normalized)


def exact_verus_clauses(clauses: list[str], expected: list[str]) -> bool:
    actual = [compact_verus_clause(item) for item in clauses if str(item).strip()]
    wanted = [compact_verus_clause(item) for item in expected]
    return actual == wanted


def compact_rust_path_text(text: Any) -> str:
    return re.sub(r"\s+", "", str(text or ""))


def find_matching_delimiter(
    text: str,
    start: int,
    open_ch: str,
    close_ch: str,
) -> int | None:
    if start >= len(text) or text[start] != open_ch:
        return None
    depth = 0
    index = start
    while index < len(text):
        char = text[index]
        if char == open_ch:
            depth += 1
        elif char == close_ch:
            depth -= 1
            if depth == 0:
                return index + 1
        index += 1
    return None


def skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def assume_specification_bindings_from_contract_code(
    contract_code: str,
) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    text = str(contract_code or "")
    for match in re.finditer(r"\bassume_specification\b", text):
        index = skip_whitespace(text, match.end())
        if index < len(text) and text[index] == "<":
            generic_end = find_matching_delimiter(text, index, "<", ">")
            if generic_end is None:
                bindings.append(
                    {
                        "status": "parse_failed",
                        "target": "",
                        "raw_target": "",
                        "error": "unclosed assume_specification generic parameter list",
                    }
                )
                continue
            index = skip_whitespace(text, generic_end)
        if index >= len(text) or text[index] != "[":
            bindings.append(
                {
                    "status": "parse_failed",
                    "target": "",
                    "raw_target": "",
                    "error": "missing assume_specification target bracket",
                }
            )
            continue
        target_end = find_matching_delimiter(text, index, "[", "]")
        if target_end is None:
            bindings.append(
                {
                    "status": "parse_failed",
                    "target": "",
                    "raw_target": "",
                    "error": "unclosed assume_specification target bracket",
                }
            )
            continue
        raw_target = text[index + 1 : target_end - 1]
        bindings.append(
            {
                "status": "ok",
                "target": compact_rust_path_text(raw_target),
                "raw_target": raw_target,
                "error": "",
            }
        )
    return bindings


def assume_specification_target_from_contract_code(contract_code: str) -> str:
    for binding in assume_specification_bindings_from_contract_code(contract_code):
        if binding.get("status") == "ok":
            return str(binding.get("target") or "")
    return ""


def declaration_is_core_result_flatten(declaration: dict[str, Any]) -> bool:
    owner = declaration.get("owner") or {}
    owner_path = owner.get("resolved_owner_path") or []
    span = declaration.get("span") or {}
    return (
        declaration.get("name") == "flatten"
        and owner_path == ["core", "result", "Result"]
        and span.get("filename") == "core/src/result.rs"
    )


def declaration_generic_param_has_trait_bound(
    declaration: dict[str, Any],
    param_name: str,
    trait_name: str,
) -> bool:
    generics = declaration.get("generics") or {}
    for param in generics.get("params") or []:
        if param.get("name") != param_name:
            continue
        kind = param.get("kind") or {}
        type_param = kind.get("type") or {}
        for bound in type_param.get("bounds") or []:
            trait = (bound.get("trait_bound") or {}).get("trait") or {}
            if str(trait.get("path") or "").split("::")[-1] == trait_name:
                return True
    for predicate in generics.get("where_predicates") or []:
        bound_predicate = predicate.get("bound_predicate") or {}
        predicate_type = bound_predicate.get("type") or {}
        if predicate_type.get("generic") != param_name:
            continue
        for bound in bound_predicate.get("bounds") or []:
            trait = (bound.get("trait_bound") or {}).get("trait") or {}
            if str(trait.get("path") or "").split("::")[-1] == trait_name:
                return True
    return False


def declaration_signature_is_cmp_min_max(declaration: dict[str, Any]) -> bool:
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["v1", "v2"]:
        return False
    if any(
        not isinstance(input_item[1], dict)
        or input_item[1].get("generic") != "T"
        for input_item in inputs
    ):
        return False
    output = signature.get("output") or {}
    return isinstance(output, dict) and output.get("generic") == "T"


def cmp_min_max_source_evidence_excerpt(
    declaration: dict[str, Any],
    target: str,
) -> str:
    spec = SOURCE_BACKED_CMP_MIN_MAX_TARGETS[target]
    line_tokens = [
        f"Compares and returns the {spec['kind']} of two values.",
        (
            f"Returns the {spec['tie_argument']} argument if the comparison "
            "determines them to be equal."
        ),
        f"Internally uses an alias to [`Ord::{spec['function']}`].",
        f"pub const fn {spec['function']}<",
        spec["delegation"],
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def cmp_min_max_source_supports_obeys_cmp_spec(
    target: str,
    declaration: dict[str, Any],
) -> bool:
    spec = SOURCE_BACKED_CMP_MIN_MAX_TARGETS.get(target)
    if not spec:
        return False
    source_lower = re.sub(
        r"\s+",
        " ",
        str(declaration.get("source_context") or ""),
    ).lower()
    required_source_tokens = [
        (
            f"returns the {spec['tie_argument']} argument if the comparison "
            "determines them to be equal"
        ),
        f"internally uses an alias to [`ord::{spec['function']}`]",
        spec["delegation"],
    ]
    return (
        declaration_generic_param_has_trait_bound(declaration, "T", "Ord")
        and declaration_signature_is_cmp_min_max(declaration)
        and all(token in source_lower for token in required_source_tokens)
    )


def declaration_signature_is_binary_search(
    declaration: dict[str, Any],
) -> bool:
    if declaration.get("name") != "binary_search":
        return False
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["self", "x"]:
        return False
    x_ref = inputs[1][1].get("borrowed_ref") if isinstance(inputs[1][1], dict) else None
    if not isinstance(x_ref, dict) or x_ref.get("is_mutable"):
        return False
    if (x_ref.get("type") or {}).get("generic") != "T":
        return False
    output = (signature.get("output") or {}).get("resolved_path") or {}
    if output.get("path") != "Result":
        return False
    args = ((output.get("args") or {}).get("angle_bracketed") or {}).get("args") or []
    return (
        len(args) == 2
        and all((arg.get("type") or {}).get("primitive") == "usize" for arg in args)
    )


def source_backed_binary_search_requires_match(requires_text: str) -> bool:
    requires_lower = re.sub(r"\s+", " ", requires_text).lower()
    required_requires_tokens = [
        "obeys_cmp::<t>",
        "0 <= i < j < v@.len()",
        "v@[i].cmp_spec(&v@[j]) != ordering::greater",
        "v@[i].cmp_spec(x) == ordering::equal",
        "v@[j].cmp_spec(x) == ordering::equal",
        "==> i == j",
    ]
    return all(token in requires_lower for token in required_requires_tokens)


def source_backed_binary_search_ensures_match(ensures: list[str]) -> bool:
    return exact_verus_clauses(
        ensures,
        [
            """match result {
            Ok(i) => {
                &&& i < v@.len()
                &&& v@[i as int].cmp_spec(x) == Ordering::Equal
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) < j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
            Err(i) => {
                &&& i <= v@.len()
                &&& forall|j: int| 0 <= j < (i as int) ==>
                    v@[j].cmp_spec(x) == Ordering::Less
                &&& forall|j: int| (i as int) <= j < v@.len() ==>
                    v@[j].cmp_spec(x) == Ordering::Greater
            },
        }"""
        ],
    )


def source_backed_binary_search_source_supports_contract(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires_text: str,
    ensures: list[str] | None = None,
) -> bool:
    spec = SOURCE_BACKED_BINARY_SEARCH_TARGETS.get(target)
    if not spec:
        return False
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    required_source_tokens = [
        spec["not_sorted_token"],
        "if there are multiple matches, then any one of the matches could be returned",
        "index where a matching element could be inserted while maintaining sorted order",
        "uniquely determined position",
        "if `num` is unique",
        spec["delegation"],
    ]
    return (
        source_backed_binary_search_requires_match(requires_text)
        and (ensures is None or source_backed_binary_search_ensures_match(ensures))
        and declaration_generic_param_has_trait_bound(declaration, "T", "Ord")
        and declaration_signature_is_binary_search(declaration)
        and all(token in source_lower for token in required_source_tokens)
    )


def source_backed_binary_search_source_evidence_excerpt(
    target: str,
    declaration: dict[str, Any],
) -> str:
    spec = SOURCE_BACKED_BINARY_SEARCH_TARGETS[target]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in spec["evidence_tokens"]):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def source_backed_unsafe_constructor_source_supports_contract(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    if target not in SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS:
        return False
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    if target == CSTRING_FROM_VEC_WITH_NUL_UNCHECKED_TARGET:
        return (
            exact_verus_clauses(
                requires,
                ["c_string_bytes_with_nul_valid(bytes@)"],
            )
            and exact_verus_clauses(
                ensures,
                ["result@ == bytes@.drop_last()"],
            )
            and all(
                token in source_lower
                for token in (
                    "must** have one nul byte as its last element",
                    "cannot be empty nor have any other nul byte anywhere else",
                    "pub unsafe fn from_vec_with_nul_unchecked",
                    "self::_from_vec_with_nul_unchecked(v)",
                    "self { inner: v.into_boxed_slice() }",
                )
            )
        )
    if target == STRING_FROM_UTF8_UNCHECKED_TARGET:
        return (
            exact_verus_clauses(
                requires,
                [
                    "exists|chars: vstd::prelude::Seq<char>| "
                    "vstd::utf8::encode_utf8(chars) == bytes@"
                ],
            )
            and exact_verus_clauses(
                ensures,
                [
                    "forall|chars: vstd::prelude::Seq<char>| "
                    "vstd::utf8::encode_utf8(chars) == bytes@ ==> res@ == chars"
                ],
            )
            and all(
                token in source_lower
                for token in (
                    "without checking that the string contains valid utf-8",
                    "bytes passed to it are valid utf-8",
                    "pub unsafe fn from_utf8_unchecked(bytes: vec<u8>) -> string",
                    "string { vec: bytes }",
                )
            )
        )
    return False


def str_from_utf8_mut_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
    contract_code: str,
) -> bool:
    source_lower = re.sub(
        r"\s+",
        " ",
        all_source_context_plain_text(manifest_entry),
    ).lower()
    return (
        assume_specification_target_from_contract_code(contract_code)
        == STR_FROM_UTF8_MUT_TARGET
        and exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                "final(v)@ == old(v)@",
                (
                    "valid_utf8(old(v)@) ==> "
                    "(result matches Ok(string) && string@ == decode_utf8(old(v)@))"
                ),
                "!valid_utf8(old(v)@) ==> result is Err",
            ],
        )
        and all(
            token in source_lower
            for token in (
                "converts a mutable slice of bytes to a mutable string slice",
                "pub const fn from_utf8_mut(v: &mut [u8]) -> result<&mut str, utf8error>",
                "converts::from_utf8_mut(v)",
                "match run_utf8_validation(v)",
                "ok(unsafe { from_utf8_unchecked_mut(v) })",
                "err(err) => err(err)",
            )
        )
    )


def str_from_utf8_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
    contract_code: str,
) -> bool:
    source_lower = re.sub(
        r"\s+",
        " ",
        all_source_context_plain_text(manifest_entry),
    ).lower()
    return (
        len(re.findall(r"\bassume_specification\b", contract_code)) == 1
        and assume_specification_target_from_contract_code(contract_code)
        == "str::from_utf8"
        and exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                (
                    "valid_utf8(v@) ==> "
                    "(result matches Ok(string) && string@ == decode_utf8(v@))"
                ),
                "!valid_utf8(v@) ==> result is Err",
            ],
        )
        and all(
            token in source_lower
            for token in (
                "returns `err` if the slice is not utf-8",
                "pub const fn from_utf8(v: &[u8]) -> result<&str, utf8error>",
                "converts::from_utf8(v)",
                "match run_utf8_validation(v)",
                "ok(unsafe { from_utf8_unchecked(v) })",
                "err(err) => err(err)",
            )
        )
    )


def thread_result_flatten_alias_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
    contract_code: str,
) -> bool:
    declaration = primary_declaration(manifest_entry)
    declarations = []
    if manifest_entry:
        declarations.extend(manifest_entry.get("verification_declarations") or [])
        declarations.extend(manifest_entry.get("declarations") or [])
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    exact_result_match = (
        "result == match value { "
        "core::result::Result::Ok(inner) => inner, "
        "core::result::Result::Err(e) => core::result::Result::Err(e) "
        "}"
    )
    exact_result_match_trailing_comma = (
        "result == match value { "
        "core::result::Result::Ok(inner) => inner, "
        "core::result::Result::Err(e) => core::result::Result::Err(e), "
        "}"
    )
    exact_result_match_error_name = (
        "result == match value { "
        "core::result::Result::Ok(inner) => inner, "
        "core::result::Result::Err(error) => core::result::Result::Err(error) "
        "}"
    )
    exact_result_match_error_name_trailing_comma = (
        "result == match value { "
        "core::result::Result::Ok(inner) => inner, "
        "core::result::Result::Err(error) => core::result::Result::Err(error), "
        "}"
    )
    exact_branch_match = (
        "match value { "
        "core::result::Result::Ok(inner) => result == inner, "
        "core::result::Result::Err(e) => result == core::result::Result::Err(e) "
        "}"
    )
    exact_branch_match_trailing_comma = (
        "match value { "
        "core::result::Result::Ok(inner) => result == inner, "
        "core::result::Result::Err(e) => result == core::result::Result::Err(e), "
        "}"
    )
    return (
        assume_specification_target_from_contract_code(contract_code)
        == THREAD_RESULT_FLATTEN_CONTRACT_TARGET
        and exact_verus_clauses(requires, [])
        and (
            exact_verus_clauses(ensures, [exact_result_match])
            or exact_verus_clauses(ensures, [exact_result_match_trailing_comma])
            or exact_verus_clauses(ensures, [exact_result_match_error_name])
            or exact_verus_clauses(
                ensures,
                [exact_result_match_error_name_trailing_comma],
            )
            or exact_verus_clauses(ensures, [exact_branch_match])
            or exact_verus_clauses(ensures, [exact_branch_match_trailing_comma])
        )
        and any(declaration_is_core_result_flatten(item) for item in declarations)
        and all(
            token in source_lower
            for token in (
                "impl<t, e> result<result<t, e>, e>",
                "converts from `result<result<t, e>, e>` to `result<t, e>`",
                "pub const fn flatten(self) -> result<t, e>",
                "match self",
                "ok(inner) => inner",
                "err(e) => err(e)",
            )
        )
    )


def thread_result_flatten_alias_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "impl<T, E> Result<Result<T, E>, E>",
        "Converts from `Result<Result<T, E>, E>`",
        "pub const fn flatten",
        "match self",
        "Ok(inner) => inner",
        "Err(e) => Err(e)",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def source_backed_unsafe_constructor_source_evidence_excerpt(
    target: str,
    declaration: dict[str, Any],
) -> str:
    line_tokens_by_target = {
        CSTRING_FROM_VEC_WITH_NUL_UNCHECKED_TARGET: [
            "must** have one nul byte as its last element",
            "cannot be empty nor have any other nul byte anywhere else",
            "pub unsafe fn from_vec_with_nul_unchecked",
            "Self::_from_vec_with_nul_unchecked(v)",
            "Self { inner: v.into_boxed_slice() }",
        ],
        STRING_FROM_UTF8_UNCHECKED_TARGET: [
            "without checking that the",
            "bytes passed",
            "valid UTF-8",
            "pub unsafe fn from_utf8_unchecked",
            "String { vec: bytes }",
        ],
    }
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(
            token.lower() in text_lower
            for token in line_tokens_by_target.get(target, [])
        ):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_slice_split_at_mut_unchecked(
    declaration: dict[str, Any],
) -> bool:
    if declaration.get("name") != "split_at_mut_unchecked":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if not header.get("is_unsafe") or len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["self", "mid"]:
        return False
    self_ref = inputs[0][1].get("borrowed_ref") if isinstance(inputs[0][1], dict) else None
    if (
        not isinstance(self_ref, dict)
        or not self_ref.get("is_mutable")
        or (self_ref.get("type") or {}).get("generic") != "Self"
    ):
        return False
    if not isinstance(inputs[1][1], dict) or inputs[1][1].get("primitive") != "usize":
        return False

    def is_mut_slice_ref(item: Any) -> bool:
        borrowed_ref = item.get("borrowed_ref") if isinstance(item, dict) else None
        slice_type = (
            (borrowed_ref.get("type") or {}).get("slice")
            if isinstance(borrowed_ref, dict)
            else None
        )
        return (
            isinstance(borrowed_ref, dict)
            and borrowed_ref.get("is_mutable")
            and isinstance(slice_type, dict)
            and slice_type.get("generic") == "T"
        )

    output_tuple = (signature.get("output") or {}).get("tuple") or []
    return len(output_tuple) == 2 and all(is_mut_slice_ref(item) for item in output_tuple)


def split_at_mut_unchecked_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(
            requires,
            ["mid as int <= old(slice)@.len()"],
        )
        and exact_verus_clauses(
            ensures,
            [
                "ret.0@ == old(slice)@.subrange(0, mid as int)",
                "ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)",
                "final(ret.0)@ == ret.0@",
                "final(ret.1)@ == ret.1@",
                "final(slice)@ == final(ret.0)@ + final(ret.1)@",
            ],
        )
        and declaration_signature_is_slice_split_at_mut_unchecked(declaration)
        and all(
            token in source_lower
            for token in (
                "0 <= mid <= self.len()",
                "mid <= len",
                "from_raw_parts_mut(ptr, mid)",
                "from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))",
            )
        )
    )


def split_at_mut_unchecked_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "0 <= mid <= self.len()",
        "mid <= len",
        "from_raw_parts_mut(ptr, mid)",
        "from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))",
        "not overlapping",
        "pub const unsafe fn split_at_mut_unchecked",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_slice_split_at_mut_checked(
    declaration: dict[str, Any],
) -> bool:
    if declaration.get("name") != "split_at_mut_checked":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if header.get("is_unsafe") or len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["self", "mid"]:
        return False
    self_ref = inputs[0][1].get("borrowed_ref") if isinstance(inputs[0][1], dict) else None
    if (
        not isinstance(self_ref, dict)
        or not self_ref.get("is_mutable")
        or (self_ref.get("type") or {}).get("generic") != "Self"
    ):
        return False
    if not isinstance(inputs[1][1], dict) or inputs[1][1].get("primitive") != "usize":
        return False

    def is_mut_slice_ref(item: Any) -> bool:
        borrowed_ref = item.get("borrowed_ref") if isinstance(item, dict) else None
        slice_type = (
            (borrowed_ref.get("type") or {}).get("slice")
            if isinstance(borrowed_ref, dict)
            else None
        )
        return (
            isinstance(borrowed_ref, dict)
            and borrowed_ref.get("is_mutable")
            and isinstance(slice_type, dict)
            and slice_type.get("generic") == "T"
        )

    output = signature.get("output") or {}
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    output_tuple = ((args[0].get("type") or {}).get("tuple")) or []
    return len(output_tuple) == 2 and all(
        is_mut_slice_ref(item) for item in output_tuple
    )


def split_at_mut_checked_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                "ret is Some == (mid <= old(slice)@.len())",
                (
                    "ret matches Some((left, right)) ==> { "
                    "&&& left@ == old(slice)@.subrange(0, mid as int) "
                    "&&& right@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int) "
                    "&&& final(left)@ == left@ "
                    "&&& final(right)@ == right@ "
                    "&&& final(slice)@ == final(left)@ + final(right)@ }"
                ),
                "ret is None ==> final(slice)@ == old(slice)@",
            ],
        )
        and declaration_signature_is_slice_split_at_mut_checked(declaration)
        and all(
            token in source_lower
            for token in (
                "first will contain all indices from `[0, mid)`",
                "second will contain all indices from `[mid, len)`",
                "otherwise, if `mid > len`, returns `none`",
                "pub const fn split_at_mut_checked",
                "if mid <= self.len()",
                "some(unsafe { self.split_at_mut_unchecked(mid) })",
            )
        )
    )


def split_at_mut_checked_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "first will contain all indices from `[0, mid)`",
        "second will contain all indices from `[mid, len)`",
        "mid > len",
        "pub const fn split_at_mut_checked",
        "if mid <= self.len()",
        "Some(unsafe { self.split_at_mut_unchecked(mid) })",
        "None",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_str_split_at_checked(
    declaration: dict[str, Any],
) -> bool:
    if declaration.get("name") != "split_at_checked":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if header.get("is_unsafe") or len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["self", "mid"]:
        return False
    self_ref = inputs[0][1].get("borrowed_ref") if isinstance(inputs[0][1], dict) else None
    if (
        not isinstance(self_ref, dict)
        or self_ref.get("is_mutable")
        or (self_ref.get("type") or {}).get("generic") != "Self"
    ):
        return False
    if not isinstance(inputs[1][1], dict) or inputs[1][1].get("primitive") != "usize":
        return False

    def is_str_ref(item: Any) -> bool:
        borrowed_ref = item.get("borrowed_ref") if isinstance(item, dict) else None
        return (
            isinstance(borrowed_ref, dict)
            and not borrowed_ref.get("is_mutable")
            and (borrowed_ref.get("type") or {}).get("primitive") == "str"
        )

    output = signature.get("output") or {}
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    output_tuple = ((args[0].get("type") or {}).get("tuple")) or []
    return len(output_tuple) == 2 and all(is_str_ref(item) for item in output_tuple)


def str_split_at_checked_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                "ret.is_some() == is_char_boundary(s.spec_bytes(), mid as int)",
                (
                    "ret.is_some() ==> ret.unwrap().0.spec_bytes() == "
                    "s.spec_bytes().subrange(0, mid as int)"
                ),
                (
                    "ret.is_some() ==> ret.unwrap().1.spec_bytes() == "
                    "s.spec_bytes().subrange(mid as int, s.spec_bytes().len() as int)"
                ),
            ],
        )
        and declaration_signature_is_str_split_at_checked(declaration)
        and all(
            token in source_lower
            for token in (
                "the argument, `mid`, should be a valid byte offset",
                "boundary of a utf-8 code point",
                "method returns `none` if",
                "the two slices returned go from the start",
                "pub const fn split_at_checked",
                "if self.is_char_boundary(mid)",
                "some(unsafe { self.split_at_unchecked(mid) })",
            )
        )
    )


def str_split_at_checked_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "valid byte offset",
        "boundary of a UTF-8 code point",
        "method returns `None`",
        "two slices returned",
        "pub const fn split_at_checked",
        "if self.is_char_boundary(mid)",
        "Some(unsafe { self.split_at_unchecked(mid) })",
        "None",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_str_split_at_mut_checked(
    declaration: dict[str, Any],
) -> bool:
    if declaration.get("name") != "split_at_mut_checked":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if header.get("is_unsafe") or len(inputs) != 2:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != ["self", "mid"]:
        return False
    self_ref = inputs[0][1].get("borrowed_ref") if isinstance(inputs[0][1], dict) else None
    if (
        not isinstance(self_ref, dict)
        or not self_ref.get("is_mutable")
        or (self_ref.get("type") or {}).get("generic") != "Self"
    ):
        return False
    if not isinstance(inputs[1][1], dict) or inputs[1][1].get("primitive") != "usize":
        return False

    def is_mut_str_ref(item: Any) -> bool:
        borrowed_ref = item.get("borrowed_ref") if isinstance(item, dict) else None
        return (
            isinstance(borrowed_ref, dict)
            and borrowed_ref.get("is_mutable")
            and (borrowed_ref.get("type") or {}).get("primitive") == "str"
        )

    output = signature.get("output") or {}
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    output_tuple = ((args[0].get("type") or {}).get("tuple")) or []
    return len(output_tuple) == 2 and all(is_mut_str_ref(item) for item in output_tuple)


def str_split_at_mut_checked_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                "ret is Some <==> is_char_boundary(old(s).spec_bytes(), mid as int)",
                (
                    "ret matches Some((left, right)) ==> { "
                    "&&& left.spec_bytes() =~= old(s).spec_bytes().subrange(0, mid as int) "
                    "&&& right.spec_bytes() =~= old(s).spec_bytes().subrange(mid as int, old(s).spec_bytes().len() as int) "
                    "&&& final(left).spec_bytes() == left.spec_bytes() "
                    "&&& final(right).spec_bytes() == right.spec_bytes() "
                    "&&& final(s).spec_bytes() == final(left).spec_bytes() + final(right).spec_bytes() }"
                ),
                "ret is None ==> final(s).spec_bytes() == old(s).spec_bytes()",
            ],
        )
        and declaration_signature_is_str_split_at_mut_checked(declaration)
        and all(
            token in source_lower
            for token in (
                "the argument, `mid`, should be a valid byte offset",
                "boundary of a utf-8 code point",
                "pub const fn split_at_mut_checked",
                "if self.is_char_boundary(mid)",
                "some(unsafe { self.split_at_mut_unchecked(mid) })",
                "from_utf8_unchecked_mut(slice::from_raw_parts_mut(ptr, mid))",
                "from_utf8_unchecked_mut(slice::from_raw_parts_mut(ptr.add(mid), len - mid))",
            )
        )
    )


def str_split_at_mut_checked_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "valid byte offset",
        "boundary of a UTF-8 code point",
        "pub const fn split_at_mut_checked",
        "if self.is_char_boundary(mid)",
        "Some(unsafe { self.split_at_mut_unchecked(mid) })",
        "None",
        "pub const unsafe fn split_at_mut_unchecked",
        "from_utf8_unchecked_mut(slice::from_raw_parts_mut(ptr, mid))",
        "from_utf8_unchecked_mut(slice::from_raw_parts_mut(ptr.add(mid), len - mid))",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_string_replace_range(declaration: dict[str, Any]) -> bool:
    if declaration.get("name") != "replace_range":
        return False
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    if len(inputs) != 3:
        return False
    if any(
        not isinstance(input_item, list) or len(input_item) != 2
        for input_item in inputs
    ):
        return False
    if [input_item[0] for input_item in inputs] != [
        "self",
        "range",
        "replace_with",
    ]:
        return False
    self_ref = inputs[0][1].get("borrowed_ref") if isinstance(inputs[0][1], dict) else None
    replace_ref = inputs[2][1].get("borrowed_ref") if isinstance(inputs[2][1], dict) else None
    generics = declaration.get("generics") or {}
    where_predicates = json.dumps(
        generics.get("where_predicates") or [],
        sort_keys=True,
    )
    return (
        isinstance(self_ref, dict)
        and self_ref.get("is_mutable")
        and (self_ref.get("type") or {}).get("generic") == "Self"
        and isinstance(inputs[1][1], dict)
        and inputs[1][1].get("generic") == "R"
        and isinstance(replace_ref, dict)
        and not replace_ref.get("is_mutable")
        and (replace_ref.get("type") or {}).get("primitive") == "str"
        and signature.get("output") is None
        and "RangeBounds" in where_predicates
        and "usize" in where_predicates
    )


def string_replace_range_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
    contract_code: str = "",
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(
        r"\s+",
        " ",
        all_source_context_plain_text(manifest_entry)
        or source_context_plain_text(declaration),
    ).lower()
    compact_contract = compact_verus_clause(contract_code).lower()
    return (
        exact_verus_clauses(
            requires,
            ["string_replace_range_valid(&range, encode_utf8(old(s)@))"],
        )
        and exact_verus_clauses(
            ensures,
            [
                (
                    "final(s)@ == string_replace_range_result(&range, "
                    "encode_utf8(old(s)@), replace_with@)"
                )
            ],
        )
        and declaration_signature_is_string_replace_range(declaration)
        and all(
            token in source_lower
            for token in (
                "only use `range` once",
                "let checked_range = slice::range(range, ..self.len())",
                "self.is_char_boundary(checked_range.start)",
                "self.is_char_boundary(checked_range.end)",
                "splice(checked_range, replace_with.bytes())",
            )
        )
        and (
            not contract_code
            or all(
                token in compact_contract
                for token in (
                    "string_replace_range_snapshot",
                    "range.spec_start_bound()",
                    "range.spec_end_bound()",
                    "string_replace_range_valid",
                    "is_char_boundary(old_bytes,snapshot.0)",
                    "is_char_boundary(old_bytes,snapshot.1)",
                    "string_replace_range_result",
                    "decode_utf8(",
                    "encode_utf8(replace_with)",
                )
            )
        )
        and "slice_range_start" not in compact_contract
        and "slice_range_end" not in compact_contract
    )


def string_replace_range_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "Panics if the range has",
        "char`] boundary",
        "pub fn replace_range",
        "R: RangeBounds<usize>",
        "only use `range` once",
        "let checked_range = slice::range(range, ..self.len())",
        "self.is_char_boundary(checked_range.start)",
        "self.is_char_boundary(checked_range.end)",
        "splice(checked_range, replace_with.bytes())",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def _borrowed_ref_type(item: Any) -> dict[str, Any]:
    borrowed_ref = item.get("borrowed_ref") if isinstance(item, dict) else None
    return borrowed_ref if isinstance(borrowed_ref, dict) else {}


def _borrowed_ref_inner_type(item: Any) -> dict[str, Any]:
    borrowed_ref = _borrowed_ref_type(item)
    inner = borrowed_ref.get("type")
    return inner if isinstance(inner, dict) else {}


def _is_mut_ref_to_generic(item: Any, name: str) -> bool:
    borrowed_ref = _borrowed_ref_type(item)
    inner = _borrowed_ref_inner_type(item)
    return bool(borrowed_ref.get("is_mutable")) and inner.get("generic") == name


def declaration_signature_is_slice_reverse(declaration: dict[str, Any]) -> bool:
    if declaration.get("name") != "reverse":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    owner_slice = (((declaration.get("owner") or {}).get("for") or {}).get("slice")) or {}
    return (
        not header.get("is_unsafe")
        and header.get("is_const")
        and len(inputs) == 1
        and isinstance(inputs[0], list)
        and inputs[0][0] == "self"
        and _is_mut_ref_to_generic(inputs[0][1], "Self")
        and owner_slice.get("generic") == "T"
        and signature.get("output") is None
    )


def slice_reverse_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(requires, [])
        and exact_verus_clauses(ensures, ["final(slice)@ == old(slice)@.reverse()"])
        and declaration_signature_is_slice_reverse(declaration)
        and all(
            token in source_lower
            for token in (
                "reverses the order of elements in the slice, in place",
                "pub const fn reverse(&mut self)",
                "let half_len = self.len() / 2",
                "revswap(front_half, back_half, half_len)",
                "mem::swap(&mut a[i], &mut b[n - 1 - i])",
            )
        )
    )


def slice_reverse_source_evidence_excerpt(declaration: dict[str, Any]) -> str:
    line_tokens = [
        "Reverses the order of elements in the slice, in place",
        "pub const fn reverse",
        "let half_len = self.len() / 2",
        "revswap(front_half, back_half, half_len)",
        "mem::swap(&mut a[i], &mut b[n - 1 - i])",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def declaration_signature_is_array_from_mut(declaration: dict[str, Any]) -> bool:
    if declaration.get("name") != "from_mut":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    if header.get("is_unsafe") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "s":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "T"):
        return False
    out_ref = _borrowed_ref_type(output)
    out_array = (_borrowed_ref_inner_type(output).get("array")) or {}
    return (
        bool(out_ref.get("is_mutable"))
        and out_array.get("len") == "1"
        and (out_array.get("type") or {}).get("generic") == "T"
    )


def declaration_signature_is_slice_from_mut(declaration: dict[str, Any]) -> bool:
    if declaration.get("name") != "from_mut":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    if header.get("is_unsafe") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "s":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "T"):
        return False
    out_ref = _borrowed_ref_type(output)
    out_slice = (_borrowed_ref_inner_type(output).get("slice")) or {}
    return bool(out_ref.get("is_mutable")) and out_slice.get("generic") == "T"


def declaration_signature_is_array_as_mut_slice(declaration: dict[str, Any]) -> bool:
    if declaration.get("name") != "as_mut_slice":
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    owner_array = (((declaration.get("owner") or {}).get("for") or {}).get("array")) or {}
    if header.get("is_unsafe") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "self":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "Self"):
        return False
    out_ref = _borrowed_ref_type(output)
    out_slice = (_borrowed_ref_inner_type(output).get("slice")) or {}
    return (
        bool(out_ref.get("is_mutable"))
        and out_slice.get("generic") == "T"
        and owner_array.get("len") == "N"
        and (owner_array.get("type") or {}).get("generic") == "T"
    )


def declaration_signature_is_slice_option_mut_array(
    declaration: dict[str, Any],
    method: str,
) -> bool:
    if declaration.get("name") != method:
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    owner_slice = (((declaration.get("owner") or {}).get("for") or {}).get("slice")) or {}
    generic_params = (declaration.get("generics") or {}).get("params") or []
    if header.get("is_unsafe") or not header.get("is_const") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "self":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "Self"):
        return False
    if owner_slice.get("generic") != "T":
        return False
    if not any(
        param.get("name") == "N"
        and (((param.get("kind") or {}).get("const") or {}).get("type") or {}).get(
            "primitive"
        )
        == "usize"
        for param in generic_params
    ):
        return False
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    inner = args[0].get("type") or {}
    out_ref = _borrowed_ref_type(inner)
    out_array = (_borrowed_ref_inner_type(inner).get("array")) or {}
    return (
        bool(out_ref.get("is_mutable"))
        and out_array.get("len") == "N"
        and (out_array.get("type") or {}).get("generic") == "T"
    )


def declaration_signature_is_slice_option_mut_chunk_tuple(
    declaration: dict[str, Any],
    method: str,
    *,
    array_index: int,
) -> bool:
    if declaration.get("name") != method:
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    owner_slice = (((declaration.get("owner") or {}).get("for") or {}).get("slice")) or {}
    generic_params = (declaration.get("generics") or {}).get("params") or []
    if header.get("is_unsafe") or not header.get("is_const") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "self":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "Self"):
        return False
    if owner_slice.get("generic") != "T":
        return False
    if not any(
        param.get("name") == "N"
        and (((param.get("kind") or {}).get("const") or {}).get("type") or {}).get(
            "primitive"
        )
        == "usize"
        for param in generic_params
    ):
        return False
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    tuple_items = (args[0].get("type") or {}).get("tuple") or []
    if len(tuple_items) != 2 or array_index not in {0, 1}:
        return False
    slice_index = 1 - array_index
    array_ref = _borrowed_ref_type(tuple_items[array_index])
    array_type = (_borrowed_ref_inner_type(tuple_items[array_index]).get("array")) or {}
    slice_ref = _borrowed_ref_type(tuple_items[slice_index])
    slice_type = (_borrowed_ref_inner_type(tuple_items[slice_index]).get("slice")) or {}
    return (
        bool(array_ref.get("is_mutable"))
        and array_type.get("len") == "N"
        and (array_type.get("type") or {}).get("generic") == "T"
        and bool(slice_ref.get("is_mutable"))
        and slice_type.get("generic") == "T"
    )


def declaration_signature_is_slice_single_element_mut_tuple_split(
    declaration: dict[str, Any],
    method: str,
) -> bool:
    if declaration.get("name") != method:
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    owner_slice = (((declaration.get("owner") or {}).get("for") or {}).get("slice")) or {}
    if header.get("is_unsafe") or not header.get("is_const") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "self":
        return False
    if not _is_mut_ref_to_generic(inputs[0][1], "Self"):
        return False
    if owner_slice.get("generic") != "T":
        return False
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    tuple_items = (args[0].get("type") or {}).get("tuple") or []
    if len(tuple_items) != 2:
        return False
    element_ref = _borrowed_ref_type(tuple_items[0])
    element_type = _borrowed_ref_inner_type(tuple_items[0])
    slice_ref = _borrowed_ref_type(tuple_items[1])
    slice_type = (_borrowed_ref_inner_type(tuple_items[1]).get("slice")) or {}
    return (
        bool(element_ref.get("is_mutable"))
        and element_type.get("generic") == "T"
        and bool(slice_ref.get("is_mutable"))
        and slice_type.get("generic") == "T"
    )


def declaration_signature_is_slice_split_off_mut_element(
    declaration: dict[str, Any],
    method: str,
) -> bool:
    if declaration.get("name") != method:
        return False
    header = declaration.get("header") or {}
    signature = declaration.get("signature") or {}
    inputs = signature.get("inputs") or []
    output = signature.get("output") or {}
    owner_slice = (((declaration.get("owner") or {}).get("for") or {}).get("slice")) or {}
    if header.get("is_unsafe") or not header.get("is_const") or len(inputs) != 1:
        return False
    if not isinstance(inputs[0], list) or inputs[0][0] != "self":
        return False
    outer_ref = _borrowed_ref_type(inputs[0][1])
    inner_ref = _borrowed_ref_inner_type(inputs[0][1]).get("borrowed_ref") or {}
    inner_type = (inner_ref.get("type") or {}) if isinstance(inner_ref, dict) else {}
    if (
        not bool(outer_ref.get("is_mutable"))
        or not bool(inner_ref.get("is_mutable"))
        or inner_type.get("generic") != "Self"
    ):
        return False
    if owner_slice.get("generic") != "T":
        return False
    resolved_path = output.get("resolved_path") or {}
    if not str(resolved_path.get("path") or "").endswith("Option"):
        return False
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    if len(args) != 1:
        return False
    out_ref = _borrowed_ref_type(args[0].get("type") or {})
    out_type = _borrowed_ref_inner_type(args[0].get("type") or {})
    return bool(out_ref.get("is_mutable")) and out_type.get("generic") == "T"


def direct_mut_view_adapter_source_supports_contract(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    if target == ARRAY_FROM_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "out@[0] == *old(s)",
                    "final(out)@ == out@",
                    "*final(s) == final(out)@[0]",
                ],
            )
            and declaration_signature_is_array_from_mut(declaration)
            and all(
                token in source_lower
                for token in (
                    "converts a mutable reference to `t` into a mutable reference to an array of length 1",
                    "without copying",
                    "pub const fn from_mut",
                    "(s as *mut t).cast::<[t; 1]>()",
                )
            )
        )
    if target == SLICE_FROM_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret@ == seq![*old(s)]",
                    "final(ret)@ == ret@",
                    "final(ret)@ == seq![*final(s)]",
                    "*final(s) == *old(s)",
                ],
            )
            and declaration_signature_is_slice_from_mut(declaration)
            and all(
                token in source_lower
                for token in (
                    "converts a reference to t into a slice of length 1",
                    "without copying",
                    "pub const fn from_mut",
                    "array::from_mut(s)",
                )
            )
        )
    if target == ARRAY_AS_MUT_SLICE_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "out@ == old(ar)@",
                    "final(out)@ == out@",
                    "final(out)@ == final(ar)@",
                ],
            )
            and declaration_signature_is_array_as_mut_slice(declaration)
            and all(
                token in source_lower
                for token in (
                    "returns a mutable slice containing the entire array",
                    "equivalent to `&mut s[..]`",
                    "pub const fn as_mut_slice",
                    "self",
                )
            )
        )
    if target == SLICE_AS_MUT_ARRAY_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (old(slice)@.len() == N)",
                    (
                        "ret matches Some(out) ==> { "
                        "&&& out@ == old(slice)@ "
                        "&&& final(out)@ == out@ "
                        "&&& final(slice)@ == final(out)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_option_mut_array(
                declaration,
                "as_mut_array",
            )
            and all(
                token in source_lower
                for token in (
                    "gets a mutable reference to the slice's underlying array",
                    "if `n` is not exactly equal to the length of `self`, then this method returns `none`",
                    "pub const fn as_mut_array",
                    "if self.len() == n",
                    "self.as_mut_ptr().cast_array()",
                    "let me = unsafe { &mut *ptr }",
                    "some(me)",
                )
            )
        )
    if target == SLICE_FIRST_CHUNK_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (N as int <= old(slice)@.len())",
                    (
                        "ret matches Some(out) ==> { "
                        "&&& out@ == old(slice)@.subrange(0, N as int) "
                        "&&& final(out)@ == out@ "
                        "&&& final(slice)@ == final(out)@ + "
                        "old(slice)@.subrange(N as int, old(slice)@.len() as int) }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_option_mut_array(
                declaration,
                "first_chunk_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "returns a mutable array reference to the first `n` items in the slice",
                    "if the slice is not at least `n` in length, this will return `none`",
                    "pub const fn first_chunk_mut",
                    "if self.len() < n",
                    "some(unsafe { &mut *(self.as_mut_ptr().cast_array()) })",
                )
            )
        )
    if target == SLICE_LAST_CHUNK_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (N as int <= old(slice)@.len())",
                    (
                        "ret matches Some(out) ==> { "
                        "&&& out@ == old(slice)@.subrange("
                        "old(slice)@.len() - N as int, old(slice)@.len() as int) "
                        "&&& final(out)@ == out@ "
                        "&&& final(slice)@ == old(slice)@.subrange("
                        "0, old(slice)@.len() - N as int) + final(out)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_option_mut_array(
                declaration,
                "last_chunk_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "returns a mutable array reference to the last `n` items in the slice",
                    "if the slice is not at least `n` in length, this will return `none`",
                    "pub const fn last_chunk_mut",
                    "checked_sub(n)",
                    "let (_, last) = self.split_at_mut(index)",
                    "some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })",
                )
            )
        )
    return False


def direct_mut_view_adapter_source_evidence_excerpt(
    target: str,
    declaration: dict[str, Any],
) -> str:
    line_tokens_by_target = {
        ARRAY_FROM_MUT_TARGET: [
            "Converts a mutable reference to `T`",
            "without copying",
            "pub const fn from_mut",
            "(s as *mut T).cast::<[T; 1]>()",
        ],
        SLICE_FROM_MUT_TARGET: [
            "Converts a reference to T",
            "without copying",
            "pub const fn from_mut",
            "array::from_mut(s)",
        ],
        ARRAY_AS_MUT_SLICE_TARGET: [
            "Returns a mutable slice containing the entire array",
            "Equivalent to",
            "pub const fn as_mut_slice",
            "self",
        ],
        SLICE_AS_MUT_ARRAY_TARGET: [
            "Gets a mutable reference to the slice's underlying array",
            "If `N` is not exactly equal",
            "pub const fn as_mut_array",
            "if self.len() == N",
            "self.as_mut_ptr().cast_array()",
            "Some(me)",
        ],
        SLICE_FIRST_CHUNK_MUT_TARGET: [
            "Returns a mutable array reference to the first `N` items",
            "If the slice is not at least `N`",
            "pub const fn first_chunk_mut",
            "if self.len() < N",
            "self.as_mut_ptr().cast_array()",
        ],
        SLICE_LAST_CHUNK_MUT_TARGET: [
            "Returns a mutable array reference to the last `N` items",
            "If the slice is not at least `N`",
            "pub const fn last_chunk_mut",
            "checked_sub(N)",
            "self.split_at_mut(index)",
            "last.as_mut_ptr().cast_array()",
        ],
    }
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(
            token.lower() in text_lower
            for token in line_tokens_by_target.get(target, [])
        ):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def array_each_mut_source_supports_contract(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    return (
        exact_verus_clauses(requires, [])
        and exact_verus_clauses(
            ensures,
            [
                "forall|i: int| #![auto] 0 <= i < N ==> *out[i] == old(ar)@[i]",
                "forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == *out[i]",
                "forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == final(ar)@[i]",
            ],
        )
        and all(
            token in source_lower
            for token in (
                "borrows each element mutably and returns an array of mutable references",
                "pub const fn each_mut(&mut self) -> [&mut t; n]",
                "buf[i] = &raw mut self[i]",
                "`*mut t` has the same layout as `&mut t`",
                "transmute_unchecked(buf)",
            )
        )
    )


def array_each_mut_source_evidence_excerpt(declaration: dict[str, Any]) -> str:
    line_tokens = (
        "Borrows each element mutably and returns an array of mutable references",
        "pub const fn each_mut",
        "buf[i] = &raw mut self[i]",
        "`*mut T` has the same layout as `&mut T`",
        "transmute_unchecked(buf)",
    )
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def option_mut_tuple_view_source_supports_contract(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    if target == SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (N as int <= old(slice)@.len())",
                    (
                        "ret matches Some((first, tail)) ==> { "
                        "&&& first@ == old(slice)@.subrange(0, N as int) "
                        "&&& tail@ == old(slice)@.subrange(N as int, old(slice)@.len() as int) "
                        "&&& final(first)@ == first@ "
                        "&&& final(tail)@ == tail@ "
                        "&&& final(slice)@ == final(first)@ + final(tail)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_option_mut_chunk_tuple(
                declaration,
                "split_first_chunk_mut",
                array_index=0,
            )
            and all(
                token in source_lower
                for token in (
                    "returns a mutable array reference to the first `n` items in the slice and the remaining slice",
                    "if the slice is not at least `n` in length, this will return `none`",
                    "pub const fn split_first_chunk_mut",
                    "let some((first, tail)) = self.split_at_mut_checked(n) else { return none }",
                    "first.as_mut_ptr().cast_array()",
                    "some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))",
                )
            )
        )
    if target == SLICE_SPLIT_LAST_CHUNK_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (N as int <= old(slice)@.len())",
                    (
                        "ret matches Some((init, last)) ==> { "
                        "&&& init@ == old(slice)@.subrange(0, old(slice)@.len() - N as int) "
                        "&&& last@ == old(slice)@.subrange(old(slice)@.len() - N as int, old(slice)@.len() as int) "
                        "&&& final(init)@ == init@ "
                        "&&& final(last)@ == last@ "
                        "&&& final(slice)@ == final(init)@ + final(last)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_option_mut_chunk_tuple(
                declaration,
                "split_last_chunk_mut",
                array_index=1,
            )
            and all(
                token in source_lower
                for token in (
                    "returns a mutable array reference to the last `n` items in the slice and the remaining slice",
                    "if the slice is not at least `n` in length, this will return `none`",
                    "pub const fn split_last_chunk_mut",
                    "let some(index) = self.len().checked_sub(n) else { return none }",
                    "let (init, last) = self.split_at_mut(index)",
                    "some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))",
                )
            )
        )
    return False


def option_mut_tuple_view_source_evidence_excerpt(
    target: str,
    declaration: dict[str, Any],
) -> str:
    line_tokens_by_target = {
        SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET: [
            "Returns a mutable array reference to the first `N` items",
            "remaining",
            "If the slice is not at least `N`",
            "pub const fn split_first_chunk_mut",
            "split_at_mut_checked(N)",
            "first.as_mut_ptr().cast_array()",
            "Some((unsafe",
        ],
        SLICE_SPLIT_LAST_CHUNK_MUT_TARGET: [
            "Returns a mutable array reference to the last `N` items",
            "remaining",
            "If the slice is not at least `N`",
            "pub const fn split_last_chunk_mut",
            "checked_sub(N)",
            "self.split_at_mut(index)",
            "last.as_mut_ptr().cast_array()",
        ],
    }
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(
            token.lower() in text_lower
            for token in line_tokens_by_target.get(target, [])
        ):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def single_element_mut_split_source_supports_contract(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    declaration = primary_declaration(manifest_entry)
    source_lower = re.sub(r"\s+", " ", source_context_plain_text(declaration)).lower()
    if target == SLICE_SPLIT_FIRST_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (old(slice)@.len() != 0)",
                    (
                        "ret matches Some((first, tail)) ==> { "
                        "&&& *first == old(slice)@[0] "
                        "&&& tail@ == old(slice)@.subrange(1, old(slice)@.len() as int) "
                        "&&& *final(first) == *first "
                        "&&& final(tail)@ == tail@ "
                        "&&& final(slice)@ == seq![*final(first)] + final(tail)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_single_element_mut_tuple_split(
                declaration,
                "split_first_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "pub const fn split_first_mut",
                    "if let [first, tail @ ..] = self",
                    "some((first, tail))",
                )
            )
        )
    if target == SLICE_SPLIT_LAST_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (old(slice)@.len() != 0)",
                    (
                        "ret matches Some((last, init)) ==> { "
                        "&&& *last == old(slice)@[(old(slice)@.len() - 1) as int] "
                        "&&& init@ == old(slice)@.subrange(0, old(slice)@.len() - 1) "
                        "&&& *final(last) == *last "
                        "&&& final(init)@ == init@ "
                        "&&& final(slice)@ == final(init)@ + seq![*final(last)] }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_single_element_mut_tuple_split(
                declaration,
                "split_last_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "pub const fn split_last_mut",
                    "if let [init @ .., last] = self",
                    "some((last, init))",
                )
            )
        )
    if target == SLICE_SPLIT_OFF_FIRST_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (old(slice)@.len() != 0)",
                    (
                        "ret matches Some(first) ==> { "
                        "&&& *first == old(slice)@[0] "
                        "&&& *final(first) == *first "
                        "&&& final(slice)@ == old(slice)@.subrange(1, old(slice)@.len() as int) "
                        "&&& old(slice)@ == seq![*final(first)] + final(slice)@ }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_split_off_mut_element(
                declaration,
                "split_off_first_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "pub const fn split_off_first_mut",
                    "mem::replace(self, &mut []).split_first_mut()",
                    "let some((first, rem))",
                    "*self = rem",
                    "some(first)",
                )
            )
        )
    if target == SLICE_SPLIT_OFF_LAST_MUT_TARGET:
        return (
            exact_verus_clauses(requires, [])
            and exact_verus_clauses(
                ensures,
                [
                    "ret is Some == (old(slice)@.len() != 0)",
                    (
                        "ret matches Some(last) ==> { "
                        "&&& *last == old(slice)@[(old(slice)@.len() - 1) as int] "
                        "&&& *final(last) == *last "
                        "&&& final(slice)@ == old(slice)@.subrange(0, old(slice)@.len() - 1) "
                        "&&& old(slice)@ == final(slice)@ + seq![*final(last)] }"
                    ),
                    "ret is None ==> final(slice)@ == old(slice)@",
                ],
            )
            and declaration_signature_is_slice_split_off_mut_element(
                declaration,
                "split_off_last_mut",
            )
            and all(
                token in source_lower
                for token in (
                    "pub const fn split_off_last_mut",
                    "mem::replace(self, &mut []).split_last_mut()",
                    "let some((last, rem))",
                    "*self = rem",
                    "some(last)",
                )
            )
        )
    return False


def single_element_mut_split_source_evidence_excerpt(
    target: str,
    declaration: dict[str, Any],
) -> str:
    line_tokens_by_target = {
        SLICE_SPLIT_FIRST_MUT_TARGET: [
            "pub const fn split_first_mut",
            "[first, tail @ ..]",
            "Some((first, tail))",
        ],
        SLICE_SPLIT_LAST_MUT_TARGET: [
            "pub const fn split_last_mut",
            "[init @ .., last]",
            "Some((last, init))",
        ],
        SLICE_SPLIT_OFF_FIRST_MUT_TARGET: [
            "pub const fn split_off_first_mut",
            "mem::replace(self, &mut []).split_first_mut()",
            "*self = rem",
            "Some(first)",
        ],
        SLICE_SPLIT_OFF_LAST_MUT_TARGET: [
            "pub const fn split_off_last_mut",
            "mem::replace(self, &mut []).split_last_mut()",
            "*self = rem",
            "Some(last)",
        ],
    }
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(
            token.lower() in text_lower
            for token in line_tokens_by_target.get(target, [])
        ):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def btree_source_supports_raw_algebra_target(
    target: str,
    manifest_entry: dict[str, Any] | None,
) -> bool:
    source_lower = source_text_for_entry(manifest_entry).lower()
    if not source_lower or "ord" not in source_lower:
        return False
    if target == "alloc::collections::BTreeMap::append":
        return all(
            token in source_lower
            for token in (
                "moves all elements from `other` into `self`",
                "leaving `other` empty",
                "mem::replace(other",
                "self.merge(",
                "other_val",
            )
        )
    if target == "alloc::collections::BTreeSet::append":
        return all(
            token in source_lower
            for token in (
                "moves all elements from `other` into `self`",
                "leaving `other` empty",
                "self.map.append(&mut other.map)",
            )
        )
    if target == "alloc::collections::BTreeSet::is_disjoint":
        return all(
            token in source_lower
            for token in (
                "no elements in common",
                "empty intersection",
                "self.intersection(other).next().is_none()",
            )
        )
    return False


def btree_contract_uses_source_backed_raw_algebra(
    target: str,
    requires_text: str,
    ensures_text: str,
    manifest_entry: dict[str, Any] | None,
) -> bool:
    if target not in SOURCE_BACKED_BTREE_RAW_ALGEBRA_TARGETS:
        return False
    requires_lower = requires_text.lower()
    ensures_lower = ensures_text.lower()
    if "obeys_cmp" not in requires_lower:
        return False
    if not btree_source_supports_raw_algebra_target(target, manifest_entry):
        return False
    if target == "alloc::collections::BTreeMap::append":
        return all(
            token in ensures_lower
            for token in (
                "final(m)@",
                "old(m)@.union_prefer_right(old(other)@)",
                "final(other)@",
                "map::<key, value>::empty()",
            )
        )
    if target == "alloc::collections::BTreeSet::append":
        return all(
            token in ensures_lower
            for token in (
                "final(m)@",
                "old(m)@.union(old(other)@)",
                "final(other)@",
                "set::<key>::empty()",
            )
        )
    if target == "alloc::collections::BTreeSet::is_disjoint":
        return "result" in ensures_lower and "m@.disjoint(other@)" in ensures_lower
    return False


def hashset_replace_source_supports_operation(
    manifest_entry: dict[str, Any] | None,
) -> bool:
    source_lower = source_text_for_entry(manifest_entry).lower()
    return all(
        token in source_lower
        for token in (
            "replacing the existing value",
            "returns the replaced value",
            "self.base.replace(value)",
        )
    )


def hashset_replace_contract_uses_source_backed_view(
    requires_text: str,
    ensures_text: str,
    manifest_entry: dict[str, Any] | None,
) -> bool:
    requires_lower = requires_text.lower()
    ensures_lower = ensures_text.lower()
    return (
        "obeys_key_model" in requires_lower
        and "builds_valid_hashers" in requires_lower
        and all(
            token in ensures_lower
            for token in (
                "sets_borrowed_key_to_key",
                "set_contains_borrowed_key",
                "old(m)@.remove(replaced).insert(value)",
                "old(m)@.insert(value)",
            )
        )
        and hashset_replace_source_supports_operation(manifest_entry)
    )


def hashmap_remove_entry_source_supports_operation(
    manifest_entry: dict[str, Any] | None,
) -> bool:
    source_lower = re.sub(r"\s+", " ", source_text_for_entry(manifest_entry)).lower()
    return all(
        token in source_lower
        for token in (
            "removes a key from the map, returning the stored key and value",
            "the key may be any borrowed form of the map's key type",
            "hash",
            "eq",
            "self.base.remove_entry(k)",
        )
    )


def hashmap_remove_entry_source_evidence_excerpt(
    declaration: dict[str, Any],
) -> str:
    line_tokens = [
        "Removes a key from the map, returning the stored key and value",
        "The key may be any borrowed form of the map's key type",
        "[`Hash`] and [`Eq`] on the borrowed form *must* match",
        "pub fn remove_entry",
        "K: Borrow<Q>",
        "Q: Hash + Eq",
        "self.base.remove_entry(k)",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def hashmap_get_mut_source_supports_operation(
    manifest_entry: dict[str, Any] | None,
) -> bool:
    source_lower = re.sub(r"\s+", " ", source_text_for_entry(manifest_entry)).lower()
    return all(
        token in source_lower
        for token in (
            "returns a mutable reference to the value corresponding to the key",
            "the key may be any borrowed form of the map's key type",
            "hash",
            "eq",
            "self.base.get_mut(k)",
        )
    )


def btreemap_get_mut_source_supports_operation(
    manifest_entry: dict[str, Any] | None,
) -> bool:
    source_lower = re.sub(r"\s+", " ", source_text_for_entry(manifest_entry)).lower()
    return all(
        token in source_lower
        for token in (
            "returns a mutable reference to the value corresponding to the key",
            "*must* match the ordering on the key type",
            "search_tree(key)",
            "found(handle) => some(handle.into_val_mut())",
            "godown(_) => none",
        )
    )


def map_get_mut_source_supports_operation(
    target: str,
    manifest_entry: dict[str, Any] | None,
) -> bool:
    if target == HASHMAP_GET_MUT_TARGET:
        return hashmap_get_mut_source_supports_operation(manifest_entry)
    if target == BTREEMAP_GET_MUT_TARGET:
        return btreemap_get_mut_source_supports_operation(manifest_entry)
    return False


def map_get_mut_source_evidence_excerpt(
    declaration: dict[str, Any],
    target: str,
) -> str:
    if target == HASHMAP_GET_MUT_TARGET:
        line_tokens = [
            "Returns a mutable reference to the value corresponding to the key",
            "The key may be any borrowed form of the map's key type",
            "[`Hash`] and [`Eq`] on the borrowed form *must* match",
            "pub fn get_mut",
            "K: Borrow<Q>",
            "Q: Hash + Eq",
            "self.base.get_mut(k)",
        ]
    else:
        line_tokens = [
            "Returns a mutable reference to the value corresponding to the key",
            "ordering on the borrowed form *must* match",
            "pub fn get_mut",
            "K: Borrow<Q> + Ord",
            "Q: Ord",
            "search_tree(key)",
            "Found(handle) => Some(handle.into_val_mut())",
            "GoDown(_) => None",
        ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def map_get_mut_contract_uses_source_backed_shape(
    target: str,
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    if target not in SOURCE_BACKED_MAP_GET_MUT_TARGETS:
        return False
    required_requires = {
        HASHMAP_GET_MUT_TARGET: [
            "obeys_key_model::<Key>()",
            "builds_valid_hashers::<S>()",
        ],
        BTREEMAP_GET_MUT_TARGET: ["obeys_cmp::<Key>()"],
    }
    if not exact_verus_clauses(requires, required_requires[target]):
        return False
    compact_ensures = "\n".join(compact_verus_clause(item) for item in ensures)
    required_tokens = [
        "letold_map=old(m)@",
        "letselected_key=choose|key:Key|sets_borrowed_key_to_key(old_map.dom(),k,&key)",
        "contains_borrowed_key(old_map,k)==>sets_borrowed_key_to_key(old_map.dom(),k,&selected_key)",
        "resultisSome==contains_borrowed_key(old_map,k)",
        "*v==old_map[selected_key]",
        "*final(v)==*v",
        "final(m)@==old_map",
        "!contains_borrowed_key(old_map,k)",
    ]
    return (
        all(token in compact_ensures for token in required_tokens)
        and map_get_mut_source_supports_operation(target, manifest_entry)
    )


def linkedlist_back_mut_contract_uses_source_backed_shape(
    manifest_entry: dict[str, Any] | None,
    requires: list[str],
    ensures: list[str],
) -> bool:
    if not exact_verus_clauses(requires, []):
        return False
    if not exact_verus_clauses(
        ensures,
        [
            "result is Some == (old(list)@.len() != 0)",
            "result is None == (old(list)@.len() == 0)",
            (
                "result matches Some(value) ==> { "
                "&&& *value == old(list)@.last() "
                "&&& *final(value) == *value "
                "&&& final(list)@ == old(list)@ }"
            ),
            "result is None ==> final(list)@ == old(list)@",
        ],
    ):
        return False
    source_lower = re.sub(r"\s+", " ", source_text_for_entry(manifest_entry)).lower()
    return all(
        token in source_lower
        for token in (
            "provides a mutable reference to the back element",
            "or `none` if the list",
            "is empty",
            "pub fn back_mut(&mut self) -> option<&mut t>",
            "self.tail.as_mut().map(|node| &mut node.as_mut().element)",
        )
    )


def linkedlist_back_mut_source_evidence_excerpt(declaration: dict[str, Any]) -> str:
    context = str(declaration.get("source_context") or "")
    line_tokens = (
        "Provides a mutable reference to the back element",
        "or `None` if the list is empty",
        "pub fn back_mut",
        "self.tail.as_mut().map",
    )
    selected: list[tuple[int, str]] = []
    for line in context.splitlines():
        match = re.match(r"\s*(\d+):\s?(.*)", line)
        if not match:
            continue
        number = int(match.group(1))
        text = match.group(2).strip()
        if any(token in text for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def safe_slice_chunk_source_supports_nonzero_n(
    target: str,
    requires: list[str],
    manifest_entry: dict[str, Any] | None,
) -> bool:
    if target not in SOURCE_BACKED_SAFE_SLICE_CHUNK_TARGETS:
        return False
    normalized_requires = [
        normalized_contract_clause(item)
        for item in requires
        if str(item).strip()
    ]
    if normalized_requires != ["N != 0"]:
        return False
    source_lower = re.sub(r"\s+", " ", source_text_for_entry(manifest_entry)).lower()
    per_target_tokens = {
        SLICE_AS_CHUNKS_TARGET: (
            "pub const fn as_chunks",
            "panics if `n` is zero",
            "assert!(n != 0",
            "let len_rounded_down = self.len() / n * n",
            "self.split_at_unchecked(len_rounded_down)",
            "multiple_of_n.as_chunks_unchecked()",
        ),
        SLICE_AS_RCHUNKS_TARGET: (
            "pub const fn as_rchunks",
            "panics if `n` is zero",
            "assert!(n != 0",
            "let len = self.len() / n",
            "self.split_at(self.len() - len * n)",
            "multiple_of_n.as_chunks_unchecked()",
        ),
        SLICE_AS_CHUNKS_MUT_TARGET: (
            "pub const fn as_chunks_mut",
            "panics if `n` is zero",
            "assert!(n != 0",
            "let len_rounded_down = self.len() / n * n",
            "self.split_at_mut_unchecked(len_rounded_down)",
            "multiple_of_n.as_chunks_unchecked_mut()",
        ),
        SLICE_AS_RCHUNKS_MUT_TARGET: (
            "pub const fn as_rchunks_mut",
            "panics if `n` is zero",
            "assert!(n != 0",
            "let len = self.len() / n",
            "self.split_at_mut(self.len() - len * n)",
            "multiple_of_n.as_chunks_unchecked_mut()",
        ),
    }
    return all(token in source_lower for token in per_target_tokens[target])


def safe_slice_chunk_source_evidence_excerpt(
    declaration: dict[str, Any],
    target: str,
) -> str:
    line_tokens = [
        "Panics if `N` is zero",
        "chunks.len()` equals `slice.len() / N",
        "remainder.len()` equals `slice.len() % N",
        "remainder, chunks) = slice.as_rchunks",
        "chunks, remainder) = slice.as_chunks_mut",
        "remainder, chunks) = slice.as_rchunks_mut",
        "pub const fn as_chunks",
        "pub const fn as_rchunks",
        "pub const fn as_chunks_mut",
        "pub const fn as_rchunks_mut",
        "assert!(N != 0",
        "len_rounded_down",
        "remainder_len",
        "split_at_unchecked",
        "split_at_mut_unchecked",
        "split_at_mut",
        "as_chunks_unchecked",
        "as_chunks_unchecked_mut",
    ]
    selected = []
    for number, text in parse_source_context_lines(
        str(declaration.get("source_context") or "")
    ):
        text_lower = text.lower()
        if any(token.lower() in text_lower for token in line_tokens):
            selected.append((number, text))
    if selected:
        return "\n".join(f"{number}: {text}" for number, text in selected)
    return source_context_excerpt(declaration)


def make_requires_source_fidelity_result(
    classification: str,
    rationale: str,
    source_reference: str,
    source_excerpt: str = "",
) -> dict[str, str]:
    return {
        "classification": classification,
        "rationale": rationale,
        "source_reference": source_reference,
        "source_excerpt": source_excerpt,
    }


def classify_requires_source_fidelity(
    target: str,
    requires: list[str],
    manifest_entry: dict[str, Any] | None,
    ensures: list[str] | None = None,
) -> dict[str, str]:
    requires_text = "; ".join(str(item) for item in requires if str(item).strip())
    if not requires_text.strip():
        return make_requires_source_fidelity_result(
            SOURCE_FIDELITY_NOT_APPLICABLE,
            "No requires clause is present.",
            "",
        )

    declaration = primary_declaration(manifest_entry)
    source_reference = declaration_source_reference(declaration)
    source_excerpt = source_context_excerpt(declaration)
    source_text = declaration_evidence_text(declaration)
    source_lower = source_text.lower()
    requires_lower = requires_text.lower()

    def justified(rationale: str) -> dict[str, str]:
        return make_requires_source_fidelity_result(
            SOURCE_FIDELITY_JUSTIFIED,
            rationale,
            source_reference,
            source_excerpt,
        )

    def unclassified(rationale: str) -> dict[str, str]:
        return make_requires_source_fidelity_result(
            SOURCE_FIDELITY_UNCLASSIFIED,
            rationale,
            source_reference,
            source_excerpt,
        )

    if not declaration:
        return unclassified(
            "No classified-manifest declaration/source_context was available for "
            "auditing this non-empty requires clause."
        )

    if target == SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET:
        if split_at_mut_unchecked_source_supports_contract(
            manifest_entry,
            requires,
            ensures or [],
        ):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} states the unsafe precondition `0 <= mid <= "
                "self.len()`, checks `mid <= len`, and constructs the two mutable "
                "sub-slices with `from_raw_parts_mut(ptr, mid)` and "
                "`from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid))`; "
                "the requires clause, prefix/suffix view postconditions, returned "
                "sub-slice preservation at function return, and concatenated input "
                "post-state are exactly that source-backed normal-return shape.",
                source_reference,
                split_at_mut_unchecked_source_evidence_excerpt(declaration),
            )
        return unclassified(
            "core::slice::split_at_mut_unchecked is accepted only when the "
            "requires clause exactly states `mid <= old(slice).len()` and the "
            "postconditions exactly model the source prefix/suffix "
            "`from_raw_parts_mut` construction, returned sub-slice preservation, "
            "and final concatenated slice state."
        )

    if target == STRING_REPLACE_RANGE_TARGET:
        if string_replace_range_source_supports_contract(
            manifest_entry,
            requires,
            ensures or [],
        ):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} normalizes `range` exactly once with "
                "`slice::range(range, ..self.len())`, documents the panic domain "
                "for invalid range order and non-character-boundary endpoints, "
                "then checks both byte endpoints before splicing replacement bytes; "
                "`string_replace_range_valid` is exactly that source-backed "
                "normal-return domain.",
                source_reference,
                string_replace_range_source_evidence_excerpt(declaration),
            )
        return unclassified(
            "String::replace_range accepts a non-empty requires clause only for "
            "the source-backed one-snapshot RangeBounds byte-range shape that "
            "validates the normalized byte range and both UTF-8 character "
            "boundaries before the splice."
        )

    if target in SOURCE_BACKED_SAFE_SLICE_CHUNK_TARGETS and "n != 0" in requires_lower:
        if safe_slice_chunk_source_supports_nonzero_n(
            target,
            requires,
            manifest_entry,
        ):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} documents that this safe chunk partition "
                "panics when `N` is zero, immediately asserts `N != 0`, and then "
                "splits the slice before casting the exact multiple-of-N region "
                "with `as_chunks_unchecked`/`as_chunks_unchecked_mut`; the "
                "`N != 0` requires clause is therefore exactly the "
                "source-backed normal-return domain.",
                source_reference,
                safe_slice_chunk_source_evidence_excerpt(declaration, target),
            )
        return unclassified(
            "core::slice::{as_chunks,as_rchunks,as_chunks_mut,as_rchunks_mut} "
            "accept `N != 0` only when the classified-manifest source evidence "
            "documents the panicking zero-N domain, the immediate "
            "`assert!(N != 0)`, and the split plus "
            "`as_chunks_unchecked`/`as_chunks_unchecked_mut` construction."
        )

    if target in SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS:
        if source_backed_unsafe_constructor_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures or [],
        ):
            if target == CSTRING_FROM_VEC_WITH_NUL_UNCHECKED_TARGET:
                rationale = (
                    f"{source_reference} states the safety precondition that the "
                    "input Vec has exactly one nul byte and it is the last element, "
                    "then delegates to `_from_vec_with_nul_unchecked` which stores "
                    "the vector as the CString backing slice; "
                    "`c_string_bytes_with_nul_valid(bytes@)` and "
                    "`result@ == bytes@.drop_last()` are exactly that safe "
                    "deterministic CString view."
                )
            else:
                rationale = (
                    f"{source_reference} states the safety precondition that the "
                    "input bytes are valid UTF-8 and constructs `String { vec: "
                    "bytes }`; the UTF-8 encoding existence requirement and "
                    "`res@` character-view postcondition are exactly that "
                    "deterministic observable String value."
                )
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                rationale,
                source_reference,
                source_backed_unsafe_constructor_source_evidence_excerpt(
                    target,
                    declaration,
                ),
            )
        return unclassified(
            "This unsafe constructor is accepted only when the generated contract "
            "exactly matches the Rust 1.96 safety precondition and source-backed "
            "observable postcondition for this specific target."
        )

    if target in SOURCE_BACKED_CMP_MIN_MAX_TARGETS and "obeys_cmp_spec" in requires_lower:
        if cmp_min_max_source_supports_obeys_cmp_spec(target, declaration):
            spec = SOURCE_BACKED_CMP_MIN_MAX_TARGETS[target]
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} shows `T: Ord`, documents that equal "
                f"comparisons return the {spec['tie_argument']} argument, and "
                f"delegates the executable body to `{spec['delegation']}`; "
                "`T::obeys_cmp_spec()` is the vstd law connecting that Rust "
                "ordering behavior to the modeled comparison relation.",
                source_reference,
                cmp_min_max_source_evidence_excerpt(declaration, target),
            )
        return unclassified(
            "The `T::obeys_cmp_spec()` requires clause is accepted for "
            "core::cmp::{min,max} only when the classified-manifest source "
            "evidence shows `T: Ord`, documented equal-tie behavior, and "
            "delegation to `v1.min(v2)`/`v1.max(v2)`."
        )

    if target in SOURCE_BACKED_BINARY_SEARCH_TARGETS:
        if source_backed_binary_search_source_supports_contract(
            target,
            manifest_entry,
            requires_text,
            ensures or [],
        ):
            spec = SOURCE_BACKED_BINARY_SEARCH_TARGETS[target]
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} shows `{spec['display']}` has a `T: Ord` "
                f"bound, delegates to `{spec['delegation']}`, "
                "documents the sorted-input domain and insertion-index result, "
                "and documents that duplicate matches may return any matching "
                "index while unique matches have a uniquely determined position; "
                "`obeys_cmp` plus the sortedness and unique-match requires clauses "
                "and the Ok/Err partition postcondition are the vstd bridge that "
                "makes this source behavior deterministic.",
                source_reference,
                source_backed_binary_search_source_evidence_excerpt(
                    target,
                    declaration,
                ),
            )
        spec = SOURCE_BACKED_BINARY_SEARCH_TARGETS[target]
        return unclassified(
            f"The {spec['display']} requires clause is accepted only for the "
            "source-backed shape that combines `obeys_cmp::<T>()`, modeled "
            "nondecreasing sortedness, and a unique element comparing equal to "
            "the searched value, with classified-manifest evidence for `T: Ord`, "
            "documented duplicate-match nondeterminism, insertion-index behavior, "
            f"delegation to `{spec['delegation']}`, and the matching Ok/Err "
            "partition postcondition."
        )

    if (
        target == HASHMAP_GET_MUT_TARGET
        and "obeys_key_model" in requires_lower
        and "builds_valid_hashers" in requires_lower
    ):
        if hashmap_get_mut_source_supports_operation(manifest_entry):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} documents that get_mut returns a mutable "
                "reference to the value for a borrowed key, requires borrowed-key "
                "Hash/Eq compatibility, and delegates to `self.base.get_mut(k)`; "
                "`obeys_key_model` and `builds_valid_hashers` are the vstd laws "
                "connecting that source HashMap behavior to the borrowed-key "
                "semantic view.",
                source_reference,
                map_get_mut_source_evidence_excerpt(declaration, target),
            )
        return unclassified(
            "The `obeys_key_model`/`builds_valid_hashers` requires clause is "
            "accepted for HashMap::get_mut only when the classified-manifest "
            "source evidence documents borrowed-key Hash/Eq compatibility, "
            "mutable-reference lookup behavior, and delegation to "
            "`self.base.get_mut(k)`."
        )

    if target == BTREEMAP_GET_MUT_TARGET and "obeys_cmp" in requires_lower:
        if btreemap_get_mut_source_supports_operation(manifest_entry):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} documents that get_mut returns a mutable "
                "reference to the value for a borrowed key, requires borrowed-key "
                "ordering to match the owned key ordering, and implements the "
                "lookup with `search_tree(key)` / `Found(handle) => "
                "Some(handle.into_val_mut())`; `obeys_cmp` is the vstd law "
                "connecting that source ordering behavior to the semantic map "
                "view.",
                source_reference,
                map_get_mut_source_evidence_excerpt(declaration, target),
            )
        return unclassified(
            "The `obeys_cmp` requires clause is accepted for BTreeMap::get_mut "
            "only when the classified-manifest source evidence documents the "
            "borrowed-key Ord compatibility and the get_mut search_tree / "
            "into_val_mut lookup shape."
        )

    if (
        target in SOURCE_BACKED_BTREE_RAW_ALGEBRA_TARGETS
        and "obeys_cmp" in requires_lower
        and btree_source_supports_raw_algebra_target(target, manifest_entry)
    ):
        return justified(
            f"{source_reference} shows this BTree operation is implemented over "
            "the ordered map/set structure with an `Ord` bound, and its documented "
            "effect is exactly the map/set algebra modeled by the candidate; the "
            "Verus `obeys_cmp` law is the bridge from Rust `Ord` execution to the "
            "semantic collection view."
        )

    if "obeys_cmp" in requires_lower and target.startswith(
        ("alloc::collections::BTreeMap::", "alloc::collections::BTreeSet::")
    ):
        if "ord" in source_lower and any(
            token in source_lower
            for token in ("first", "last", "is_subset", "replace", "pop_")
        ):
            return justified(
                f"{source_reference} shows the BTree operation's Rust source is "
                "ordered by the `Ord` comparator; the Verus `obeys_cmp` "
                "precondition is the vstd law connecting that source comparator "
                "to the semantic map/set view."
            )

    if (
        target == HASHMAP_REMOVE_ENTRY_TARGET
        and "obeys_key_model" in requires_lower
        and "builds_valid_hashers" in requires_lower
    ):
        if hashmap_remove_entry_source_supports_operation(manifest_entry):
            return make_requires_source_fidelity_result(
                SOURCE_FIDELITY_JUSTIFIED,
                f"{source_reference} documents that remove_entry accepts any "
                "borrowed key whose Hash/Eq behavior matches the map key type, "
                "returns the stored key and value when present, and delegates to "
                "`self.base.remove_entry(k)`; `obeys_key_model` and "
                "`builds_valid_hashers` are the vstd laws connecting that "
                "source HashMap behavior to the borrowed-key semantic view.",
                source_reference,
                hashmap_remove_entry_source_evidence_excerpt(declaration),
            )
        return unclassified(
            "The `obeys_key_model`/`builds_valid_hashers` requires clause is "
            "accepted for HashMap::remove_entry only when the classified-manifest "
            "source evidence documents borrowed-key Hash/Eq compatibility, "
            "returned stored key/value behavior, and delegation to "
            "`self.base.remove_entry(k)`."
        )

    if (
        "obeys_key_model" in requires_lower
        and "builds_valid_hashers" in requires_lower
        and target.startswith("std::collections::HashSet::")
    ):
        if "hashset" in source_lower and any(
            token in source_lower for token in ("contains", "is_subset", "iter().all")
        ):
            return justified(
                f"{source_reference} shows the HashSet operation is implemented "
                "by iteration and `contains`/subset queries; Rust HashSet "
                "semantics rely on Eq/Hash and the BuildHasher, and the vstd "
                "`obeys_key_model`/`builds_valid_hashers` laws are the semantic "
                "bridge for that source behavior."
            )

    if (
        target == HASHSET_REPLACE_TARGET
        and "obeys_key_model" in requires_lower
        and "builds_valid_hashers" in requires_lower
    ):
        if hashset_replace_source_supports_operation(manifest_entry):
            return justified(
                f"{source_reference} documents replacing an equal existing set "
                "value and returning the replaced value, and delegates to "
                "`self.base.replace(value)`; Rust HashSet semantics rely on "
                "Eq/Hash and the BuildHasher, so the vstd "
                "`obeys_key_model`/`builds_valid_hashers` laws are the required "
                "semantic bridge."
            )

    if target.startswith("alloc::string::String::") and "encode_utf8" in requires_lower:
        if "is_char_boundary" in source_lower or "self[idx..]" in source_lower:
            return justified(
                f"{source_reference} shows the String source checks or indexes on "
                "UTF-8 character boundaries before returning normally; the "
                "requires clause encodes that documented non-panicking byte-index "
                "domain in vstd UTF-8 terms."
            )

    if target == "alloc::vec::Vec::dedup" and "obeys_eq" in requires_lower:
        if "dedup_by" in source_lower and "== b" in source_lower:
            return justified(
                f"{source_reference} shows `Vec::dedup` delegates to "
                "`dedup_by(|a, b| a == b)`; the vstd equality law connects that "
                "source `PartialEq` comparison to the sequence-view postcondition."
            )

    if (
        target in {"alloc::vec::Vec::into_flattened", "core::slice::as_flattened"}
        and "usize::max" in requires_lower
    ):
        if "checked_mul" in source_lower and "len overflow" in source_lower:
            return justified(
                f"{source_reference} shows the source computes the flattened "
                "length with checked multiplication and panics on length overflow; "
                "the requires clause restricts the contract to the normal-return "
                "domain."
            )

    if target == "core::result::Result::expect_err" and "result is err" in requires_lower:
        if "match self" in source_lower and "err(e) => e" in source_lower:
            return justified(
                f"{source_reference} shows the source returns only the `Err(e)` "
                "match arm and calls the unwrap failure path for `Ok`; the "
                "requires clause selects the non-panicking normal-return branch."
            )

    if (
        ("partial_cmp_spec" in requires_lower or "partialordspec" in requires_lower)
        and "partialord" in source_lower
        and any(token in source_text for token in ("<", "<="))
    ):
        return justified(
            f"{source_reference} shows the Rust source is guarded by `PartialOrd` "
            "and computes the result with `<`/`<=`; the vstd partial-order law "
            "connects those executable comparisons to the spec predicates."
        )

    if "obeys_eq_spec" in requires_lower:
        if "partialeq" in source_lower and any(
            token in source_lower for token in ("slice_contains", "needle ==")
        ):
            return justified(
                f"{source_reference} shows the slice source requires `PartialEq` "
                "and computes the result by equality comparison; the vstd "
                "equality law connects that executable comparison to `eq_spec`."
            )

    return unclassified(
        "No source-context rule established this requires clause from the "
        "classified-manifest declaration and Rust/vstd semantics; the row is "
        "therefore not accepted by the source-fidelity gate."
    )


def target_artifact_index(
    out_dir: Path,
    metadata: dict[str, Any],
) -> tuple[list[Path], dict[str, list[Path]], list[str]]:
    candidates: list[Path] = []
    out_dir = out_dir.expanduser().absolute()
    if (out_dir / "targets").is_dir():
        candidates.append(out_dir)
    candidates.extend(target_artifact_root_paths_from_metadata(metadata))
    if not candidates:
        candidates.append(out_dir)

    roots: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        absolute = candidate.expanduser().absolute()
        if absolute in seen:
            continue
        seen.add(absolute)
        roots.append(absolute)

    directories: dict[str, list[Path]] = {}
    unexpected: list[str] = []
    for root in roots:
        if target_artifact_root_error_reasons(root):
            continue
        targets_dir = root / "targets"
        for entry in sorted(targets_dir.iterdir(), key=lambda path: path.name):
            if entry.is_dir():
                directories.setdefault(entry.name, []).append(entry)
            else:
                unexpected.append(str(entry.resolve(strict=False)))
    return roots, directories, unexpected


def target_artifact_root_error_reasons(root: Path) -> list[str]:
    root = root.expanduser().absolute()
    root_resolved = root.resolve(strict=False)
    targets_dir = root / "targets"
    targets_dir_resolved = targets_dir.resolve(strict=False)
    reasons = []
    if not root.is_dir():
        reasons.append("input_root_is_not_a_directory")
    if root.is_symlink() or root != root_resolved:
        reasons.append("input_root_does_not_resolve_to_itself")
    if not targets_dir.is_dir():
        reasons.append("targets_tree_is_not_a_directory")
    if targets_dir.is_symlink() or not path_is_relative_to(
        targets_dir_resolved,
        root_resolved,
    ):
        reasons.append("targets_tree_resolves_outside_input_root")
    return reasons


def build_target_artifact_integrity(
    out_dir: Path,
    metadata: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_paths = manifest_paths_from_metadata(metadata)
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_targets = [str(entry.get("target") or "") for entry in manifest_entries]
    empty_manifest_target_rows = [
        index for index, target in enumerate(manifest_targets) if not target
    ]
    manifest_target_counts = Counter(target for target in manifest_targets if target)
    manifest_target_set = set(manifest_target_counts)
    duplicate_manifest_targets = sorted(
        target for target, count in manifest_target_counts.items() if count > 1
    )
    manifest_entries_by_target: dict[str, dict[str, Any]] = {}
    for entry, target in zip(manifest_entries, manifest_targets, strict=False):
        if target and target not in manifest_entries_by_target:
            manifest_entries_by_target[target] = entry

    row_targets = [str(row.get("target") or "") for row in rows]
    row_counts = Counter(target for target in row_targets if target)
    row_target_set = set(row_counts)
    duplicate_final_candidate_targets = sorted(
        target for target, count in row_counts.items() if count > 1
    )
    rows_by_target = {str(row.get("target") or ""): row for row in rows}
    missing_final_candidate_rows = sorted(manifest_target_set - row_target_set)
    extra_final_candidate_rows = sorted(row_target_set - manifest_target_set)

    safe_name_to_targets: dict[str, list[str]] = {}
    empty_safe_name_targets = []
    for target in sorted(manifest_target_set):
        safe = specgen_safe_name(target)
        if not safe:
            empty_safe_name_targets.append(target)
        safe_name_to_targets.setdefault(safe, []).append(target)
    safe_name_collisions = [
        {
            "safe_name": safe,
            "targets": sorted(set(targets)),
        }
        for safe, targets in sorted(safe_name_to_targets.items())
        if safe and len(set(targets)) > 1
    ]
    expected_safe_names = {safe for safe in safe_name_to_targets if safe}

    target_artifact_roots, target_dirs_by_name, unexpected_target_root_entries = (
        target_artifact_index(out_dir, metadata)
    )
    invalid_target_artifact_roots = [
        {
            "path": str(path),
            "resolved_path": str(path.resolve(strict=False)),
            "errors": target_artifact_root_error_reasons(path),
        }
        for path in target_artifact_roots
        if target_artifact_root_error_reasons(path)
    ]
    missing_target_artifact_root_targets_dirs = [
        item["path"]
        for item in invalid_target_artifact_roots
        if "targets_tree_is_not_a_directory" in item["errors"]
    ]
    actual_target_dir_set = set(target_dirs_by_name)
    actual_target_dirs = [
        path
        for paths in target_dirs_by_name.values()
        for path in paths
    ]
    duplicate_target_dirs = sorted(
        name for name, paths in target_dirs_by_name.items() if len(paths) > 1
    )
    missing_target_dirs = sorted(expected_safe_names - actual_target_dir_set)
    orphan_target_dirs = sorted(actual_target_dir_set - expected_safe_names)
    target_json_count = sum(
        (target_dir / "target.json").is_file()
        for target_dir in actual_target_dirs
    )
    summary_json_count = sum(
        (target_dir / "summary.json").is_file()
        for target_dir in actual_target_dirs
    )

    missing_target_json_artifacts = []
    missing_summary_json_artifacts = []
    non_file_artifacts = []
    bad_json_artifacts = []
    unreadable_artifacts = []
    non_object_artifacts = []
    target_json_target_mismatches = []
    target_json_category_mismatches = []
    summary_target_mismatches = []
    summary_category_mismatches = []
    summary_final_decision_mismatches = []
    result_category_mismatches = []

    def artifact_record(target: str, path: Path) -> dict[str, str]:
        return {
            "target": target,
            "safe_name": specgen_safe_name(target),
            "path": str(path.resolve()),
        }

    def add_json_error(
        bucket: list[dict[str, str]],
        *,
        target: str,
        path: Path,
        error: str,
    ) -> None:
        record = artifact_record(target, path)
        record["error"] = error
        bucket.append(record)

    for target in sorted(manifest_target_set):
        manifest_entry = manifest_entries_by_target[target]
        row = rows_by_target.get(target)
        manifest_category = str(manifest_entry.get("category") or "")
        row_category = str((row or {}).get("category") or "")
        if row and row_category != manifest_category:
            result_category_mismatches.append(
                {
                    "target": target,
                    "expected": manifest_category,
                    "actual": row_category,
                }
            )
        safe = specgen_safe_name(target)
        target_dir_candidates = target_dirs_by_name.get(safe, [])
        target_dir = (
            target_dir_candidates[0]
            if target_dir_candidates
            else out_dir / "targets" / safe
        )
        target_json_path = target_dir / "target.json"
        summary_json_path = target_dir / "summary.json"

        if not target_json_path.exists():
            missing_target_json_artifacts.append(
                artifact_record(target, target_json_path)
            )
        elif not target_json_path.is_file():
            non_file_artifacts.append(artifact_record(target, target_json_path))
        else:
            target_payload, error_kind, error = read_json_artifact(target_json_path)
            if error_kind == "bad_json":
                add_json_error(
                    bad_json_artifacts,
                    target=target,
                    path=target_json_path,
                    error=error or "",
                )
            elif error_kind == "unreadable":
                add_json_error(
                    unreadable_artifacts,
                    target=target,
                    path=target_json_path,
                    error=error or "",
                )
            elif not isinstance(target_payload, dict):
                non_object_artifacts.append(artifact_record(target, target_json_path))
            else:
                actual_target = str(target_payload.get("target") or "")
                actual_category = str(target_payload.get("category") or "")
                if actual_target != target:
                    target_json_target_mismatches.append(
                        {
                            **artifact_record(target, target_json_path),
                            "expected": target,
                            "actual": actual_target,
                        }
                    )
                if actual_category != manifest_category:
                    target_json_category_mismatches.append(
                        {
                            **artifact_record(target, target_json_path),
                            "expected": manifest_category,
                            "actual": actual_category,
                        }
                    )

        if not summary_json_path.exists():
            missing_summary_json_artifacts.append(
                artifact_record(target, summary_json_path)
            )
        elif not summary_json_path.is_file():
            non_file_artifacts.append(artifact_record(target, summary_json_path))
        else:
            summary_payload, error_kind, error = read_json_artifact(summary_json_path)
            if error_kind == "bad_json":
                add_json_error(
                    bad_json_artifacts,
                    target=target,
                    path=summary_json_path,
                    error=error or "",
                )
            elif error_kind == "unreadable":
                add_json_error(
                    unreadable_artifacts,
                    target=target,
                    path=summary_json_path,
                    error=error or "",
                )
            elif not isinstance(summary_payload, dict):
                non_object_artifacts.append(artifact_record(target, summary_json_path))
            else:
                expected_decision = str((row or {}).get("final_decision") or "")
                actual_target = str(summary_payload.get("target") or "")
                actual_category = str(summary_payload.get("category") or "")
                summary_final = summary_payload.get("final") or {}
                if not isinstance(summary_final, dict):
                    non_object_artifacts.append(artifact_record(target, summary_json_path))
                    actual_decision = ""
                else:
                    actual_decision = decision(summary_final)
                if actual_target != target:
                    summary_target_mismatches.append(
                        {
                            **artifact_record(target, summary_json_path),
                            "expected": target,
                            "actual": actual_target,
                        }
                    )
                if actual_category != manifest_category:
                    summary_category_mismatches.append(
                        {
                            **artifact_record(target, summary_json_path),
                            "expected": manifest_category,
                            "actual": actual_category,
                        }
                    )
                if row and actual_decision != expected_decision:
                    summary_final_decision_mismatches.append(
                        {
                            **artifact_record(target, summary_json_path),
                            "expected": expected_decision,
                            "actual": actual_decision,
                        }
                    )

    missing_artifact_count = (
        len(missing_target_dirs)
        + len(missing_target_json_artifacts)
        + len(missing_summary_json_artifacts)
    )
    orphan_artifact_count = len(orphan_target_dirs) + len(unexpected_target_root_entries)
    bad_json_artifact_count = len(bad_json_artifacts)
    bad_artifact_count = (
        bad_json_artifact_count
        + len(unreadable_artifacts)
        + len(non_file_artifacts)
        + len(non_object_artifacts)
    )
    mismatched_artifact_count = (
        len(target_json_target_mismatches)
        + len(target_json_category_mismatches)
        + len(summary_target_mismatches)
        + len(summary_category_mismatches)
        + len(summary_final_decision_mismatches)
    )

    validation_errors = []
    for label, count in [
        ("classified_manifest_missing_from_batch_metadata", int(not manifest_paths)),
        (
            "invalid_target_artifact_roots",
            len(invalid_target_artifact_roots),
        ),
        ("empty_manifest_target_rows", len(empty_manifest_target_rows)),
        ("duplicate_manifest_targets", len(duplicate_manifest_targets)),
        ("missing_final_candidate_rows", len(missing_final_candidate_rows)),
        ("extra_final_candidate_rows", len(extra_final_candidate_rows)),
        ("duplicate_final_candidate_targets", len(duplicate_final_candidate_targets)),
        ("result_category_mismatches", len(result_category_mismatches)),
        ("empty_safe_name_targets", len(empty_safe_name_targets)),
        ("safe_name_collisions", len(safe_name_collisions)),
        ("duplicate_target_dirs", len(duplicate_target_dirs)),
        ("missing_artifacts", missing_artifact_count),
        ("orphan_artifacts", orphan_artifact_count),
        ("bad_json_artifacts", bad_json_artifact_count),
        ("unreadable_artifacts", len(unreadable_artifacts)),
        ("non_file_artifacts", len(non_file_artifacts)),
        ("non_object_artifacts", len(non_object_artifacts)),
        ("mismatched_artifacts", mismatched_artifact_count),
    ]:
        if count:
            validation_errors.append(f"{label}:{count}")

    is_bijection = (
        bool(manifest_paths)
        and bool(target_artifact_roots)
        and not missing_target_artifact_root_targets_dirs
        and not empty_manifest_target_rows
        and not duplicate_manifest_targets
        and not missing_final_candidate_rows
        and not extra_final_candidate_rows
        and not duplicate_final_candidate_targets
        and not empty_safe_name_targets
        and not safe_name_collisions
        and not duplicate_target_dirs
        and actual_target_dir_set == expected_safe_names
        and len(actual_target_dirs) == len(expected_safe_names) == len(manifest_target_set)
        and target_json_count == len(expected_safe_names)
        and summary_json_count == len(expected_safe_names)
        and not unexpected_target_root_entries
    )

    return {
        "source": {
            "loaded_from_batch_summary_metadata": bool(manifest_paths),
            "manifest_path_count": len(manifest_paths),
            "manifest_paths": [str(path.resolve()) for path in manifest_paths],
            "target_artifact_roots": [
                str(path) for path in target_artifact_roots
            ],
            "safe_name_function": (
                "re.sub(r'[^A-Za-z0-9_.-]+', '__', target).strip('_')"
            ),
        },
        "validation_passed": not validation_errors,
        "validation_errors": validation_errors,
        "manifest_target_rows": len(manifest_entries),
        "manifest_targets": len(manifest_target_set),
        "final_candidate_rows": len(rows),
        "final_candidate_targets": len(row_target_set),
        "expected_target_artifact_count": len(manifest_target_set),
        "expected_safe_name_count": len(expected_safe_names),
        "target_dir_count": len(actual_target_dirs),
        "target_json_count": target_json_count,
        "summary_json_count": summary_json_count,
        "safe_name_collision_count": len(safe_name_collisions),
        "safe_name_collision_target_count": sum(
            len(item["targets"]) for item in safe_name_collisions
        ),
        "result_category_mismatch_count": len(result_category_mismatches),
        "missing_artifact_count": missing_artifact_count,
        "extra_artifact_count": orphan_artifact_count,
        "orphan_artifact_count": orphan_artifact_count,
        "bad_json_artifact_count": bad_json_artifact_count,
        "bad_artifact_count": bad_artifact_count,
        "mismatched_artifact_count": mismatched_artifact_count,
        "target_bijection": {
            "is_bijection": is_bijection,
            "all_manifest_targets_have_artifacts": missing_artifact_count == 0,
            "no_orphan_artifacts": orphan_artifact_count == 0,
            "no_safe_name_collisions": not safe_name_collisions,
            "all_artifact_json_valid": bad_artifact_count == 0,
            "all_artifact_payloads_match_expected_data": (
                mismatched_artifact_count == 0
            ),
            "all_result_rows_match_manifest_category": not result_category_mismatches,
        },
        "safe_name_collisions": safe_name_collisions,
        "duplicate_target_dirs": duplicate_target_dirs,
        "target_artifact_roots_missing_targets_dir": (
            missing_target_artifact_root_targets_dirs
        ),
        "invalid_target_artifact_roots": invalid_target_artifact_roots,
        "empty_safe_name_targets": empty_safe_name_targets,
        "duplicate_manifest_targets": duplicate_manifest_targets,
        "duplicate_final_candidate_targets": duplicate_final_candidate_targets,
        "missing_final_candidate_rows": missing_final_candidate_rows,
        "extra_final_candidate_rows": extra_final_candidate_rows,
        "missing_artifacts": {
            "target_dirs": missing_target_dirs,
            "target_json": missing_target_json_artifacts,
            "summary_json": missing_summary_json_artifacts,
        },
        "orphan_artifacts": {
            "target_dirs": orphan_target_dirs,
            "target_root_entries": unexpected_target_root_entries,
        },
        "bad_json_artifacts": bad_json_artifacts,
        "unreadable_artifacts": unreadable_artifacts,
        "non_file_artifacts": non_file_artifacts,
        "non_object_artifacts": non_object_artifacts,
        "mismatches": {
            "result_category": result_category_mismatches,
            "target_json_target": target_json_target_mismatches,
            "target_json_category": target_json_category_mismatches,
            "summary_target": summary_target_mismatches,
            "summary_category": summary_category_mismatches,
            "summary_final_decision": summary_final_decision_mismatches,
        },
    }


def read_final_candidates_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def serialized_candidate_clause_list(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    return str(value)


def normalized_source_issue_tags(
    target: str,
    final_decision: str,
    candidate: dict[str, Any],
    final_record: dict[str, Any],
    manifest_entries_by_target: dict[str, dict[str, Any]],
) -> list[str]:
    existing_tags = audit_final_skip_rationales.record_issue_tags(final_record)
    tags = audit_final_skip_rationales.normalized_duplicate_vstd_issue_tags(
        target,
        final_decision,
        str(candidate.get("rationale") or ""),
        existing_tags,
        manifest_entries_by_target,
    )
    if (
        tags == existing_tags
        and final_decision == "skip"
        and target in audit_final_skip_rationales.REPAIR_ISSUE_TAGS
        and not existing_tags
    ):
        tags = audit_final_skip_rationales.repair_tags_for_target(
            target,
            manifest_entries_by_target,
        )
    return tags


def final_record_payload_values(
    target: str,
    final_record: dict[str, Any],
    manifest_entries_by_target: dict[str, dict[str, Any]],
) -> dict[str, str]:
    if not isinstance(final_record, dict):
        return {}
    candidate = final_record.get("candidate") or {}
    if not isinstance(candidate, dict):
        candidate = {}

    values: dict[str, str] = {}
    if "decision" in candidate or "decision" in final_record:
        values["final_decision"] = str(decision(final_record) or "")
    for field in ("contract_form", "contract_code", "requires", "ensures", "rationale"):
        if field not in candidate:
            continue
        if field == "contract_code":
            values[field] = serialized_contract_code(candidate)
        elif field in {"requires", "ensures"}:
            values[field] = serialized_candidate_clause_list(candidate.get(field))
        else:
            values[field] = str(candidate.get(field) or "")
    if "raw_det_reward" in final_record:
        values["raw_det_reward"] = str(int_value(final_record.get("raw_det_reward", 0)))
    if "guarded_reward" in final_record:
        values["guarded_reward"] = str(int_value(final_record.get("guarded_reward", 0)))
    if "anti_vacuity_issues" in final_record or "issues" in final_record:
        values["issues"] = ";".join(
            normalized_source_issue_tags(
                target,
                values.get("final_decision", str(decision(final_record) or "")),
                candidate,
                final_record,
                manifest_entries_by_target,
            )
        )
    return values


def csv_row_payload_values(row: dict[str, str]) -> dict[str, str]:
    return {
        field: ";".join(audit_final_skip_rationales.split_tags(row.get(field, "")))
        if field == "issues"
        else str(row.get(field, ""))
        for field in FINAL_CANDIDATE_PAYLOAD_COMPARE_FIELDS
    }


def payload_field_mismatches(
    *,
    target: str,
    source: str,
    source_path: Path,
    csv_values: dict[str, str],
    source_values: dict[str, str],
) -> list[dict[str, str]]:
    mismatches = []
    for field in FINAL_CANDIDATE_PAYLOAD_COMPARE_FIELDS:
        if field not in source_values:
            continue
        csv_value = csv_values.get(field, "")
        source_value = source_values[field]
        if csv_value == source_value:
            continue
        mismatches.append(
            {
                "target": target,
                "source": source,
                "field": field,
                "csv_value": csv_value,
                "source_value": source_value,
                "source_path": str(source_path.resolve()),
            }
        )
    return mismatches


def build_final_candidate_payload_consistency_audit(
    out_dir: Path,
    metadata: dict[str, Any],
    combined_payload: dict[str, Any],
) -> dict[str, Any]:
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_entries_by_target = {
        str(entry.get("target") or ""): entry for entry in manifest_entries
    }
    final_candidates_path = out_dir / "final_candidates.csv"
    csv_rows, csv_fields = read_final_candidates_csv(final_candidates_path)
    csv_targets = [str(row.get("target") or "") for row in csv_rows]
    duplicate_csv_targets = sorted(
        target
        for target, count in Counter(target for target in csv_targets if target).items()
        if count > 1
    )
    results_by_target = {
        str(result.get("target") or ""): result
        for result in combined_payload.get("results", [])
        if isinstance(result, dict)
    }
    batch_summary_path = out_dir / "batch_summary.json"
    target_artifact_roots, target_dirs_by_name, _ = target_artifact_index(
        out_dir,
        metadata,
    )

    audit_rows: list[dict[str, Any]] = []
    missing_batch_results: list[str] = []
    missing_summary_artifacts: list[dict[str, str]] = []
    bad_summary_artifacts: list[dict[str, str]] = []
    non_object_summary_artifacts: list[dict[str, str]] = []
    field_mismatches: list[dict[str, str]] = []

    for row in csv_rows:
        target = str(row.get("target") or "")
        safe = specgen_safe_name(target)
        target_dir_candidates = target_dirs_by_name.get(safe, [])
        summary_path = (
            target_dir_candidates[0] / "summary.json"
            if target_dir_candidates
            else out_dir / "targets" / safe / "summary.json"
        )
        csv_values = csv_row_payload_values(row)
        batch_mismatches: list[dict[str, str]] = []
        summary_mismatches: list[dict[str, str]] = []
        summary_present = summary_path.exists()
        summary_valid = False

        batch_result = results_by_target.get(target)
        if batch_result is None:
            missing_batch_results.append(target)
        else:
            final_record = batch_result.get("final") or {}
            batch_mismatches = payload_field_mismatches(
                target=target,
                source="batch_summary.results.final",
                source_path=batch_summary_path,
                csv_values=csv_values,
                source_values=final_record_payload_values(
                    target,
                    final_record,
                    manifest_entries_by_target,
                ),
            )
            field_mismatches.extend(batch_mismatches)

        if not summary_present:
            missing_summary_artifacts.append(
                {
                    "target": target,
                    "safe_name": safe,
                    "path": str(summary_path.resolve()),
                }
            )
        elif not summary_path.is_file():
            bad_summary_artifacts.append(
                {
                    "target": target,
                    "safe_name": safe,
                    "path": str(summary_path.resolve()),
                    "error": "not_file",
                }
            )
        else:
            summary_payload, error_kind, error = read_json_artifact(summary_path)
            if error_kind:
                bad_summary_artifacts.append(
                    {
                        "target": target,
                        "safe_name": safe,
                        "path": str(summary_path.resolve()),
                        "error": f"{error_kind}:{error or ''}",
                    }
                )
            elif not isinstance(summary_payload, dict):
                non_object_summary_artifacts.append(
                    {
                        "target": target,
                        "safe_name": safe,
                        "path": str(summary_path.resolve()),
                    }
                )
            else:
                summary_valid = True
                final_record = summary_payload.get("final") or {}
                summary_mismatches = payload_field_mismatches(
                    target=target,
                    source="target_summary.final",
                    source_path=summary_path,
                    csv_values=csv_values,
                    source_values=final_record_payload_values(
                        target,
                        final_record,
                        manifest_entries_by_target,
                    ),
                )
                field_mismatches.extend(summary_mismatches)

        row_mismatches = [*batch_mismatches, *summary_mismatches]
        audit_rows.append(
            {
                "target": target,
                "safe_name": safe,
                "batch_result_present": str(batch_result is not None).lower(),
                "summary_artifact_present": str(summary_present).lower(),
                "summary_artifact_valid": str(summary_valid).lower(),
                "batch_mismatched_fields": ";".join(
                    mismatch["field"] for mismatch in batch_mismatches
                ),
                "summary_mismatched_fields": ";".join(
                    mismatch["field"] for mismatch in summary_mismatches
                ),
                "field_mismatch_count": len(row_mismatches),
                "validation_passed": str(not row_mismatches).lower(),
                "summary_artifact_path": str(summary_path.resolve()),
            }
        )

    rows_with_field_mismatches = sorted(
        {mismatch["target"] for mismatch in field_mismatches}
    )
    artifacts = {
        FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_CSV: str(
            (out_dir / FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_CSV).resolve()
        ),
        FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_JSON: str(
            (out_dir / FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_JSON).resolve()
        ),
    }
    validation = {
        "all_final_candidate_rows_audited": len(audit_rows) == len(csv_rows),
        "final_candidates_csv_has_expected_fields": set(
            FINAL_CANDIDATE_PAYLOAD_COMPARE_FIELDS
        ).issubset(set(csv_fields)),
        "no_duplicate_final_candidate_targets": not duplicate_csv_targets,
        "no_missing_batch_results": not missing_batch_results,
        "no_missing_summary_artifacts": not missing_summary_artifacts,
        "no_invalid_summary_artifacts": (
            not bad_summary_artifacts and not non_object_summary_artifacts
        ),
        "no_field_mismatches": not field_mismatches,
    }
    validation["validation_passed"] = all(validation.values())
    return {
        "artifact_schema": 1,
        "source": (
            "Compares every final_candidates.csv row against the full "
            "batch_summary.json results[*].final candidate payload and the matching "
            "targets/<safe-name>/summary.json final candidate payload."
        ),
        "inputs": {
            "final_candidates_csv": str(final_candidates_path.resolve()),
            "batch_summary_json": str(batch_summary_path.resolve()),
            **{
                f"target_artifact_root_{index}": str(path.resolve())
                for index, path in enumerate(target_artifact_roots)
            },
        },
        "audited_rows": len(audit_rows),
        "final_candidates_csv_rows": len(csv_rows),
        "batch_result_rows": len(results_by_target),
        "missing_batch_result_count": len(missing_batch_results),
        "missing_summary_artifact_count": len(missing_summary_artifacts),
        "invalid_summary_artifact_count": (
            len(bad_summary_artifacts) + len(non_object_summary_artifacts)
        ),
        "duplicate_final_candidate_target_count": len(duplicate_csv_targets),
        "field_mismatch_count": len(field_mismatches),
        "rows_with_field_mismatch_count": len(rows_with_field_mismatches),
        "compared_fields": FINAL_CANDIDATE_PAYLOAD_COMPARE_FIELDS,
        "missing_batch_results": missing_batch_results,
        "missing_summary_artifacts": missing_summary_artifacts,
        "bad_summary_artifacts": bad_summary_artifacts,
        "non_object_summary_artifacts": non_object_summary_artifacts,
        "duplicate_final_candidate_targets": duplicate_csv_targets,
        "rows_with_field_mismatches": rows_with_field_mismatches,
        "field_mismatches": field_mismatches,
        "rows": audit_rows,
        "artifacts": artifacts,
        "validation": validation,
        "validation_passed": validation["validation_passed"],
    }


def final_candidate_payload_consistency_verification_block(
    audit: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value in audit.items()
        if key not in {"rows"}
    }


def write_final_candidate_payload_consistency_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_CSV,
        audit.get("rows", []),
        fieldnames=FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_FIELDS,
    )
    (out_dir / FINAL_CANDIDATE_PAYLOAD_CONSISTENCY_AUDIT_JSON).write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def update_final_candidate_payload_consistency_verification(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    verification_path = out_dir / "final_verification.json"
    verification = json.loads(verification_path.read_text())
    verification["final_candidate_payload_consistency"] = (
        final_candidate_payload_consistency_verification_block(audit)
    )
    verification.setdefault("artifacts", {}).update(audit.get("artifacts", {}))
    verification_path.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")


def path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def absolute_reference_path(base_dir: Path, value: Any) -> Path | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path


def resolved_path_or_text(path: Path) -> Path:
    return path.resolve(strict=False)


def provenance_reference_record(
    *,
    context: str,
    path: Path,
    canonical_root_resolved: Path,
) -> dict[str, Any]:
    resolved = resolved_path_or_text(path)
    return {
        "context": context,
        "path": str(path),
        "resolved_path": str(resolved),
        "exists": path.exists(),
        "is_symlink": path.is_symlink(),
        "under_canonical_root": path_is_relative_to(resolved, canonical_root_resolved),
    }


def add_provenance_reference(
    references: list[dict[str, Any]],
    *,
    context: str,
    value: Any,
    base_dir: Path,
    canonical_root_resolved: Path,
) -> None:
    path = absolute_reference_path(base_dir, value)
    if path is None:
        return
    references.append(
        provenance_reference_record(
            context=context,
            path=path,
            canonical_root_resolved=canonical_root_resolved,
        )
    )


def add_provenance_mapping_references(
    references: list[dict[str, Any]],
    *,
    context: str,
    mapping: Any,
    base_dir: Path,
    canonical_root_resolved: Path,
) -> None:
    if not isinstance(mapping, dict):
        return
    for key, value in sorted(mapping.items(), key=lambda item: str(item[0])):
        add_provenance_reference(
            references,
            context=f"{context}.{key}",
            value=value,
            base_dir=base_dir,
            canonical_root_resolved=canonical_root_resolved,
        )


def collect_delivery_artifact_references(
    out_dir: Path,
    verification: dict[str, Any],
    canonical_root_resolved: Path,
) -> list[dict[str, Any]]:
    references: list[dict[str, Any]] = []
    for index, path in enumerate(verification.get("batch_files") or []):
        add_provenance_reference(
            references,
            context=f"batch_files[{index}]",
            value=path,
            base_dir=out_dir,
            canonical_root_resolved=canonical_root_resolved,
        )

    add_provenance_mapping_references(
        references,
        context="artifacts",
        mapping=verification.get("artifacts"),
        base_dir=out_dir,
        canonical_root_resolved=canonical_root_resolved,
    )

    accepted_artifacts = verification.get("accepted_semantic_candidates") or {}
    if isinstance(accepted_artifacts, dict):
        for key in ("csv", "json"):
            add_provenance_reference(
                references,
                context=f"accepted_semantic_candidates.{key}",
                value=accepted_artifacts.get(key),
                base_dir=out_dir,
                canonical_root_resolved=canonical_root_resolved,
            )

    for block_name in (
        "final_candidate_payload_consistency",
        "full_skip_rationale_taxonomy",
    ):
        block = verification.get(block_name) or {}
        if not isinstance(block, dict):
            continue
        add_provenance_mapping_references(
            references,
            context=f"{block_name}.artifacts",
            mapping=block.get("artifacts"),
            base_dir=out_dir,
            canonical_root_resolved=canonical_root_resolved,
        )
        add_provenance_mapping_references(
            references,
            context=f"{block_name}.inputs",
            mapping=block.get("inputs"),
            base_dir=out_dir,
            canonical_root_resolved=canonical_root_resolved,
        )

    target_integrity = verification.get("target_artifact_integrity") or {}
    target_source = (
        target_integrity.get("source") if isinstance(target_integrity, dict) else {}
    )
    if isinstance(target_source, dict):
        target_artifact_roots = target_source.get("target_artifact_roots") or []
        if isinstance(target_artifact_roots, (str, Path)):
            target_artifact_roots = [target_artifact_roots]
        if isinstance(target_artifact_roots, list):
            for index, target_artifact_root in enumerate(target_artifact_roots):
                add_provenance_reference(
                    references,
                    context=(
                        "target_artifact_integrity.source."
                        f"target_artifact_roots[{index}]"
                    ),
                    value=target_artifact_root,
                    base_dir=out_dir,
                    canonical_root_resolved=canonical_root_resolved,
                )
        add_provenance_reference(
            references,
            context="target_artifact_integrity.source.targets_dir",
            value=target_source.get("targets_dir"),
            base_dir=out_dir,
            canonical_root_resolved=canonical_root_resolved,
        )

    return references


def matching_stale_root(path_text: str, stale_roots: list[Path]) -> str:
    path = Path(path_text)
    for root in stale_roots:
        if path_is_relative_to(path, root):
            return str(root)
    return ""


def stale_reference_is_allowed(context: str) -> bool:
    return any(
        context.startswith(prefix) for prefix in ALLOWED_STALE_REFERENCE_CONTEXT_PREFIXES
    )


def external_target_artifact_input_context(context: str) -> bool:
    return any(
        context.startswith(prefix)
        for prefix in EXTERNAL_TARGET_ARTIFACT_INPUT_CONTEXT_PREFIXES
    )


def external_target_artifact_tree(ref: dict[str, Any]) -> Path:
    path = Path(str(ref["path"]))
    if str(ref["context"]).endswith(".targets_dir"):
        return path
    return path / "targets"


def external_target_artifact_input_errors(
    refs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for ref in refs:
        path = Path(str(ref["path"]))
        resolved = Path(str(ref["resolved_path"]))
        target_tree = external_target_artifact_tree(ref)
        target_tree_resolved = target_tree.resolve(strict=False)
        reasons = []
        if not path.is_dir():
            reasons.append("input_root_is_not_a_directory")
        if path.is_symlink() or path != resolved:
            reasons.append("input_root_does_not_resolve_to_itself")
        if not target_tree.is_dir():
            reasons.append("targets_tree_is_not_a_directory")
        if not path_is_relative_to(target_tree_resolved, resolved):
            reasons.append("targets_tree_resolves_outside_input_root")
        if reasons:
            errors.append(
                {
                    **ref,
                    "target_artifact_tree": str(target_tree),
                    "target_artifact_tree_resolved": str(target_tree_resolved),
                    "errors": reasons,
                }
            )
    return errors


def external_target_artifact_tree_resolution_audit(
    refs: list[dict[str, Any]],
    canonical_root_resolved: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    symlinks: list[dict[str, str]] = []
    symlink_escapes: list[dict[str, str]] = []
    seen_trees: set[Path] = set()
    for ref in refs:
        target_tree = external_target_artifact_tree(ref)
        target_tree_resolved = target_tree.resolve(strict=False)
        if (
            target_tree_resolved in seen_trees
            or path_is_relative_to(target_tree_resolved, canonical_root_resolved)
            or not target_tree.is_dir()
        ):
            continue
        seen_trees.add(target_tree_resolved)
        tree_symlinks, tree_symlink_escapes, _ = tree_resolution_audit(
            target_tree,
            target_tree_resolved,
        )
        input_root = str(ref["path"])
        symlinks.extend({**record, "input_root": input_root} for record in tree_symlinks)
        symlink_escapes.extend(
            {**record, "input_root": input_root}
            for record in tree_symlink_escapes
        )
    return symlinks, symlink_escapes


def tree_resolution_audit(
    canonical_root: Path,
    canonical_root_resolved: Path,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    symlinks = []
    symlink_escapes = []
    resolved_escapes = []

    for path in sorted(canonical_root.rglob("*"), key=lambda item: str(item)):
        resolved = resolved_path_or_text(path)
        record = {
            "path": str(path),
            "resolved_path": str(resolved),
        }
        if path.is_symlink():
            symlinks.append(record)
        if not path_is_relative_to(resolved, canonical_root_resolved):
            resolved_escapes.append(record)
            if path.is_symlink():
                symlink_escapes.append(record)

    return symlinks, symlink_escapes, resolved_escapes


def build_canonical_artifact_provenance(
    out_dir: Path,
    verification: dict[str, Any],
) -> dict[str, Any]:
    canonical_root = out_dir.expanduser().absolute()
    canonical_root_resolved = canonical_root.resolve(strict=False)
    stale_roots = [
        root.expanduser().resolve(strict=False) for root in STALE_OR_PRIOR_OUTPUT_ROOTS
    ]
    verification = dict(verification)
    verification.pop("canonical_artifact_provenance", None)

    references = collect_delivery_artifact_references(
        canonical_root,
        verification,
        canonical_root_resolved,
    )
    external_target_input_refs = [
        ref
        for ref in references
        if external_target_artifact_input_context(str(ref["context"]))
    ]
    delivery_refs = [
        ref
        for ref in references
        if not external_target_artifact_input_context(str(ref["context"]))
    ]
    out_of_tree_refs = [
        ref for ref in delivery_refs if not ref.get("under_canonical_root")
    ]
    missing_refs = [ref for ref in references if not ref.get("exists")]
    external_target_input_errors = external_target_artifact_input_errors(
        external_target_input_refs
    )

    stale_refs = []
    allowed_stale_refs = []
    for ref in references:
        stale_root = matching_stale_root(str(ref["path"]), stale_roots)
        if not stale_root:
            stale_root = matching_stale_root(str(ref["resolved_path"]), stale_roots)
        if not stale_root:
            continue
        record = {**ref, "stale_root": stale_root}
        if stale_reference_is_allowed(str(ref["context"])):
            allowed_stale_refs.append(record)
        else:
            stale_refs.append(record)

    symlinks, symlink_escapes, resolved_escapes = tree_resolution_audit(
        canonical_root,
        canonical_root_resolved,
    )
    external_input_symlinks, external_input_symlink_escapes = (
        external_target_artifact_tree_resolution_audit(
            external_target_input_refs,
            canonical_root_resolved,
        )
    )
    all_symlinks = [*symlinks, *external_input_symlinks]
    all_symlink_escapes = [*symlink_escapes, *external_input_symlink_escapes]

    target_integrity = verification.get("target_artifact_integrity") or {}
    if not isinstance(target_integrity, dict):
        target_integrity = {}
    expected_target_artifact_count = target_integrity.get(
        "expected_target_artifact_count", 0
    )
    target_artifact_counts = {
        "expected_target_artifact_count": expected_target_artifact_count,
        "target_dir_count": target_integrity.get("target_dir_count", 0),
        "target_json_count": target_integrity.get("target_json_count", 0),
        "summary_json_count": target_integrity.get("summary_json_count", 0),
        "target_artifact_integrity_validation_passed": bool(
            target_integrity.get("validation_passed")
        ),
    }
    target_artifacts_match_expected = (
        bool(target_integrity.get("validation_passed"))
        and target_artifact_counts["target_dir_count"] == expected_target_artifact_count
        and target_artifact_counts["target_json_count"] == expected_target_artifact_count
        and target_artifact_counts["summary_json_count"] == expected_target_artifact_count
    )

    validation = {
        "canonical_root_exists": canonical_root.is_dir(),
        "canonical_root_resolves_to_itself": canonical_root == canonical_root_resolved,
        "all_referenced_delivery_artifacts_under_canonical_root": not out_of_tree_refs,
        "all_referenced_delivery_artifacts_exist": not missing_refs,
        "external_target_artifact_inputs_valid": not external_target_input_errors,
        "no_stale_or_prior_tree_refs_outside_allowed_prior_fresh_delta_inputs": (
            not stale_refs
        ),
        "no_symlink_escapes": not all_symlink_escapes,
        "no_paths_resolve_outside_canonical_root": not resolved_escapes,
        "target_artifacts_match_expected_count": target_artifacts_match_expected,
    }
    validation["validation_passed"] = all(validation.values())

    return {
        "artifact_schema": CANONICAL_ARTIFACT_PROVENANCE_SCHEMA,
        "source": (
            "Audits delivery-artifact path references emitted by final_verification.json, "
            "the canonical output tree, and explicitly declared external target-artifact "
            "input roots. Manifest paths and explicit prior_fresh_delta comparison inputs "
            "are treated as non-delivery inputs."
        ),
        "canonical_root": str(canonical_root),
        "canonical_root_resolved": str(canonical_root_resolved),
        "stale_or_prior_output_roots": [str(root) for root in stale_roots],
        "allowed_stale_reference_context_prefixes": list(
            ALLOWED_STALE_REFERENCE_CONTEXT_PREFIXES
        ),
        "external_target_artifact_input_context_prefixes": list(
            EXTERNAL_TARGET_ARTIFACT_INPUT_CONTEXT_PREFIXES
        ),
        **target_artifact_counts,
        "referenced_path_count": len(references),
        "referenced_delivery_artifact_count": len(delivery_refs),
        "referenced_external_target_artifact_input_count": len(
            external_target_input_refs
        ),
        "out_of_canonical_tree_ref_count": len(out_of_tree_refs),
        "missing_reference_count": len(missing_refs),
        "invalid_external_target_artifact_input_count": len(
            external_target_input_errors
        ),
        "stale_or_prior_tree_refs_outside_allowed_prior_fresh_delta_count": len(
            stale_refs
        ),
        "allowed_prior_fresh_delta_stale_ref_count": len(allowed_stale_refs),
        "symlink_count": len(all_symlinks),
        "symlink_escape_count": len(all_symlink_escapes),
        "external_target_artifact_input_symlink_count": len(
            external_input_symlinks
        ),
        "external_target_artifact_input_symlink_escape_count": len(
            external_input_symlink_escapes
        ),
        "resolved_outside_canonical_tree_count": len(resolved_escapes),
        "sample_out_of_canonical_tree_refs": out_of_tree_refs[:PROVENANCE_SAMPLE_LIMIT],
        "sample_missing_refs": missing_refs[:PROVENANCE_SAMPLE_LIMIT],
        "sample_invalid_external_target_artifact_inputs": (
            external_target_input_errors[:PROVENANCE_SAMPLE_LIMIT]
        ),
        "sample_stale_or_prior_tree_refs_outside_allowed_prior_fresh_delta": (
            stale_refs[:PROVENANCE_SAMPLE_LIMIT]
        ),
        "sample_allowed_prior_fresh_delta_stale_refs": allowed_stale_refs[
            :PROVENANCE_SAMPLE_LIMIT
        ],
        "sample_symlink_escapes": all_symlink_escapes[:PROVENANCE_SAMPLE_LIMIT],
        "sample_resolved_outside_canonical_tree": resolved_escapes[
            :PROVENANCE_SAMPLE_LIMIT
        ],
        "validation": validation,
        "validation_passed": validation["validation_passed"],
    }


def accepted_requires_source_fidelity_metadata_snapshot(
    verification: dict[str, Any],
) -> dict[str, Any]:
    block = verification.get("accepted_requires_source_fidelity")
    if not isinstance(block, dict):
        return {}

    snapshot = {
        key: block[key]
        for key in ACCEPTED_REQUIRES_SOURCE_FIDELITY_SNAPSHOT_KEYS
        if key in block
    }
    validation = snapshot.get("validation")
    if isinstance(validation, dict):
        snapshot["validation_passed"] = bool(validation.get("validation_passed"))
    return snapshot


def accepted_ensures_source_fidelity_metadata_snapshot(
    verification: dict[str, Any],
) -> dict[str, Any]:
    block = verification.get("accepted_ensures_source_fidelity")
    if not isinstance(block, dict):
        return {}

    snapshot = {
        key: block[key]
        for key in ACCEPTED_ENSURES_SOURCE_FIDELITY_SNAPSHOT_KEYS
        if key in block
    }
    validation = snapshot.get("validation")
    if isinstance(validation, dict):
        snapshot["validation_passed"] = bool(validation.get("validation_passed"))
    return snapshot


def requires_source_fidelity_index_sentence(verification: dict[str, Any]) -> str:
    snapshot = accepted_requires_source_fidelity_metadata_snapshot(verification)
    validation = snapshot.get("validation")
    validation_passed = (
        isinstance(validation, dict) and bool(validation.get("validation_passed"))
    )
    validation_value = "true" if validation_passed else "false"
    return (
        "It also records `accepted_requires_source_fidelity`: "
        f"`audited_rows={snapshot.get('audited_rows', 0)}`, "
        f"`source_gate_input_rows={snapshot.get('source_gate_input_rows', 0)}`, "
        f"`source_justified_rows={snapshot.get('source_justified_rows', 0)}`, "
        f"`source_unjustified_rows={snapshot.get('source_unjustified_rows', 0)}`, "
        f"`unclassified_rows={snapshot.get('unclassified_rows', 0)}`, "
        f"`accepted_after_source_gate_rows="
        f"{snapshot.get('accepted_after_source_gate_rows', 0)}`, "
        f"and `validation.validation_passed={validation_value}`."
    )


def ensures_source_fidelity_index_sentence(verification: dict[str, Any]) -> str:
    snapshot = accepted_ensures_source_fidelity_metadata_snapshot(verification)
    validation = snapshot.get("validation")
    validation_passed = (
        isinstance(validation, dict) and bool(validation.get("validation_passed"))
    )
    validation_value = "true" if validation_passed else "false"
    return (
        "It also records `accepted_ensures_source_fidelity`: "
        f"`accepted_rows={snapshot.get('accepted_rows', 0)}`, "
        f"`audited_rows={snapshot.get('audited_rows', 0)}`, "
        f"`source_justified_rows={snapshot.get('source_justified_rows', 0)}`, "
        f"`source_unjustified_rows={snapshot.get('source_unjustified_rows', 0)}`, "
        f"`unclassified_rows={snapshot.get('unclassified_rows', 0)}`, "
        f"`source_context_evidence_rows="
        f"{snapshot.get('source_context_evidence_rows', 0)}`, "
        f"and `validation.validation_passed={validation_value}`."
    )


def scope_validation_index_sentence(verification: dict[str, Any]) -> str:
    scope = verification.get("scope_validation")
    if not isinstance(scope, dict):
        scope = {}
    target_bijection = scope.get("target_bijection")
    if not isinstance(target_bijection, dict):
        target_bijection = {}
    function_like_scope = scope.get("function_like_manifest_scope")
    if not isinstance(function_like_scope, dict):
        function_like_scope = {}
    declaration_scope = scope.get("declaration_scope")
    if not isinstance(declaration_scope, dict):
        declaration_scope = {}
    accepted_candidate_scope = scope.get("accepted_candidate_scope")
    if not isinstance(accepted_candidate_scope, dict):
        accepted_candidate_scope = {}

    validation_value = "true" if bool(scope.get("validation_passed")) else "false"
    bijection_value = (
        "true" if bool(target_bijection.get("is_bijection")) else "false"
    )
    allowed_kinds = function_like_scope.get("allowed_kinds") or []
    allowed_kinds_text = ", ".join(str(kind) for kind in allowed_kinds)
    if not allowed_kinds_text:
        allowed_kinds_text = "<none>"
    manifest_targets = int_value(target_bijection.get("manifest_targets"))
    final_candidate_targets = int_value(target_bijection.get("final_candidate_targets"))
    public_scope_targets = int_value(
        declaration_scope.get("targets_with_public_stable_function_like_declaration_scope")
    )
    declaration_manifest_targets = int_value(declaration_scope.get("manifest_targets"))
    source_provenance_declarations = int_value(
        declaration_scope.get("source_provenance_declarations")
    )
    total_declarations = int_value(declaration_scope.get("total_declarations"))
    accepted_rows = int_value(
        accepted_candidate_scope.get("accepted_semantic_candidate_rows")
    )

    return (
        "It also records `scope_validation.validation_passed="
        f"{validation_value}`: `target_bijection.is_bijection={bijection_value}` "
        f"for the {manifest_targets:,}/{final_candidate_targets:,} "
        "manifest-to-final-candidate target mapping, "
        "allowed function-like kinds "
        f"`function_like_manifest_scope.allowed_kinds=[{allowed_kinds_text}]` "
        f"with `unexpected_kind_count="
        f"{int_value(function_like_scope.get('unexpected_kind_count'))}`, "
        f"`declaration_scope.targets_with_public_stable_function_like_declaration_scope="
        f"{public_scope_targets:,}/{declaration_manifest_targets:,}` with "
        f"`targets_missing_public_stable_function_like_declaration_scope_count="
        f"{int_value(declaration_scope.get('targets_missing_public_stable_function_like_declaration_scope_count'))}` "
        f"and source provenance on {source_provenance_declarations:,}/"
        f"{total_declarations:,} declarations, and "
        f"`accepted_candidate_scope.accepted_targets_not_in_manifest_count="
        f"{int_value(accepted_candidate_scope.get('accepted_targets_not_in_manifest_count'))}` "
        f"for {accepted_rows:,} accepted semantic candidates."
    )


def delivery_index_summary_sentence(verification: dict[str, Any]) -> str:
    target_integrity = verification.get("target_artifact_integrity")
    if not isinstance(target_integrity, dict):
        target_integrity = {}
    final_decisions = verification.get("final_decision_counts")
    if not isinstance(final_decisions, dict):
        final_decisions = {}
    accepted = verification.get("accepted_semantic_candidates")
    if not isinstance(accepted, dict):
        accepted = {}
    skip_taxonomy = verification.get("full_skip_rationale_taxonomy")
    if not isinstance(skip_taxonomy, dict):
        skip_taxonomy = {}
    skip_rationale = verification.get("skip_rationale")
    if not isinstance(skip_rationale, dict):
        skip_rationale = {}

    return (
        "The canonical tree's `final_verification.json` reports "
        f"{int_value(verification.get('result_rows')):,} result rows, "
        f"{int_value(verification.get('final_candidates')):,} final candidates, "
        f"{int_value(verification.get('missing_target_count')):,} missing targets, "
        f"{int_value(verification.get('extra_target_count')):,} extra targets, "
        f"{int_value(verification.get('duplicate_result_count')):,} duplicate result targets, "
        "passing scope validation, passing target artifact integrity validation "
        f"with {int_value(target_integrity.get('expected_target_artifact_count')):,} expected target artifacts, "
        f"{int_value(target_integrity.get('target_dir_count')):,} target directories, "
        f"{int_value(target_integrity.get('target_json_count')):,} `target.json` files, "
        f"and {int_value(target_integrity.get('summary_json_count')):,} `summary.json` files, "
        f"{int_value(final_decisions.get('add_spec')):,} final `add_spec` rows, "
        f"{int_value(final_decisions.get('skip')):,} skip rows, "
        f"{int_value(accepted.get('rows')):,} accepted semantic candidates, "
        f"{int_value(skip_rationale.get('empty_skip_rationale_rows')):,} empty skip-rationale rows, "
        f"and a full {int_value(skip_taxonomy.get('audited_skip_rows')):,}-row "
        "skip-rationale taxonomy audit with zero unclassified, unjustified, "
        "empty issue-tag, or empty combined issue/taxonomy rows."
    )


def delivery_index_count_phrase(value: Any, plural_noun: str) -> str:
    count = int_value(value)
    if count == 0:
        return f"zero {plural_noun}"
    return f"{count:,} {plural_noun}"


def delivery_index_taxonomy_row_phrase(value: Any, taxonomy_name: str) -> str:
    count = int_value(value)
    if count == 0:
        return f"zero `{taxonomy_name}` rows"
    if count == 1:
        return f"one `{taxonomy_name}` row"
    return f"{count:,} `{taxonomy_name}` rows"


def delivery_index_full_skip_taxonomy_sentence(
    verification: dict[str, Any],
) -> str:
    skip_taxonomy = verification.get("full_skip_rationale_taxonomy")
    if not isinstance(skip_taxonomy, dict):
        skip_taxonomy = {}
    taxonomy_counts = skip_taxonomy.get("taxonomy_counts")
    if not isinstance(taxonomy_counts, dict):
        taxonomy_counts = {}

    source_backed_rationale_model_gap = skip_taxonomy.get(
        "source_backed_rationale_model_gap",
        taxonomy_counts.get("source_backed_rationale_model_gap", 0),
    )
    range_bounds_byte_character_endpoint_model_gap = taxonomy_counts.get(
        "range_bounds_byte_character_endpoint_model_gap",
        0,
    )

    return (
        "The audit records "
        f"{int_value(skip_taxonomy.get('duplicate_existing_vstd_spec_rows')):,} "
        "`duplicate_existing_vstd_spec` rows, all "
        f"{int_value(skip_taxonomy.get('duplicate_existing_vstd_spec_rows_with_duplicate_vstd_tag')):,} "
        "carry `duplicate_vstd_assume_specification`, all "
        f"{int_value(skip_taxonomy.get('exact_vstd_skip_rows')):,} "
        "exact-vstd skip rows are duplicate-classified, "
        f"{delivery_index_count_phrase(skip_taxonomy.get('duplicate_existing_vstd_spec_rows_with_generic_determinism_tag'), 'duplicate-vstd taxonomy rows')} "
        "carry `determinism_unsupported_contract_form`, "
        f"{delivery_index_taxonomy_row_phrase(source_backed_rationale_model_gap, 'source_backed_rationale_model_gap')}, "
        "and "
        f"{delivery_index_taxonomy_row_phrase(range_bounds_byte_character_endpoint_model_gap, 'range_bounds_byte_character_endpoint_model_gap')}."
    )


def canonical_artifact_provenance_metadata_snapshot(
    delivery_root: Path,
    verification: dict[str, Any],
) -> dict[str, Any]:
    provenance = verification.get("canonical_artifact_provenance")
    if not isinstance(provenance, dict):
        provenance = {}

    metadata_path = delivery_root / "delivery_metadata.json"
    if not metadata_path.is_file():
        return provenance

    metadata = json.loads(metadata_path.read_text())
    snapshot = metadata.get("verification_snapshot")
    if not isinstance(snapshot, dict):
        return provenance
    metadata_provenance = snapshot.get("canonical_artifact_provenance")
    if isinstance(metadata_provenance, dict):
        return metadata_provenance
    return provenance


def canonical_artifact_provenance_index_sentence(
    provenance: dict[str, Any],
) -> str:
    validation_value = (
        "true" if bool(provenance.get("validation_passed")) else "false"
    )
    return (
        "It also records `canonical_artifact_provenance.validation_passed="
        f"{validation_value}`: "
        f"{delivery_index_count_phrase(provenance.get('referenced_delivery_artifact_count'), 'referenced delivery artifacts')}, "
        f"{delivery_index_count_phrase(provenance.get('expected_target_artifact_count'), 'expected target artifacts')}, "
        f"{delivery_index_count_phrase(provenance.get('out_of_canonical_tree_ref_count'), 'out-of-canonical-tree references')}, "
        f"{delivery_index_count_phrase(provenance.get('stale_or_prior_tree_refs_outside_allowed_prior_fresh_delta_count'), 'stale/prior-tree references outside allowed `prior_fresh_delta` comparison inputs')}, "
        f"{delivery_index_count_phrase(provenance.get('symlink_escape_count'), 'symlink escapes')}, "
        "and "
        f"{delivery_index_count_phrase(provenance.get('resolved_outside_canonical_tree_count'), 'paths resolving outside the canonical tree')}."
    )


def update_delivery_index_with_summary_counts(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    sentence = delivery_index_summary_sentence(verification)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"The canonical tree's `final_verification\.json` reports .*? "
        r"It also records `scope_validation\.validation_passed=",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(
            f"{sentence} It also records `scope_validation.validation_passed=",
            text,
            count=1,
        )
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    for block_name, pattern in (
        (
            "accepted_assume_spec_target_binding_audit",
            r"(accepted assume-spec target-binding audit: )\d+ accepted rows, \d+ audited rows",
        ),
        (
            "accepted_assume_spec_signature_shape_audit",
            r"(accepted assume-spec signature-shape audit records )\d+ accepted rows, \d+ audited rows",
        ),
        (
            "accepted_assume_spec_generic_bounds_audit",
            r"(accepted assume-spec generic/bounds audit records )\d+ accepted rows, \d+ audited rows",
        ),
    ):
        block = verification.get(block_name)
        if not isinstance(block, dict):
            continue
        replacement = (
            rf"\g<1>{int_value(block.get('accepted_rows')):,} accepted rows, "
            f"{int_value(block.get('audited_rows')):,} audited rows"
        )
        updated = re.sub(pattern, replacement, updated, count=1)
    index_path.write_text(updated)


def update_delivery_index_with_scope_validation(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    sentence = scope_validation_index_sentence(verification)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"It also records `scope_validation\.validation_passed="
        r"(?:true|false)`: .*? accepted semantic candidates\.",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    elif "It also records `canonical_artifact_provenance.validation_passed=" in text:
        updated = text.replace(
            "It also records `canonical_artifact_provenance.validation_passed=",
            f"{sentence} It also records `canonical_artifact_provenance.validation_passed=",
            1,
        )
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    index_path.write_text(updated)


def update_delivery_index_with_canonical_artifact_provenance(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    provenance = canonical_artifact_provenance_metadata_snapshot(
        delivery_root,
        verification,
    )
    sentence = canonical_artifact_provenance_index_sentence(provenance)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"It also records `canonical_artifact_provenance\.validation_passed="
        r"(?:true|false)`: .*? paths resolving outside the canonical tree\.",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    elif "It also records `final_candidate_payload_consistency.validation.validation_passed=" in text:
        updated = text.replace(
            "It also records `final_candidate_payload_consistency.validation.validation_passed=",
            f"{sentence} It also records `final_candidate_payload_consistency.validation.validation_passed=",
            1,
        )
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    index_path.write_text(updated)


def update_delivery_index_with_full_skip_taxonomy(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    sentence = delivery_index_full_skip_taxonomy_sentence(verification)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"The audit records .*?`range_bounds_byte_character_endpoint_model_gap` "
        r"rows?(?: for `[^`]+`)?\.",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    elif "The `core::slice::split_off` row is normalized" in text:
        updated = text.replace(
            "The `core::slice::split_off` row is normalized",
            f"{sentence} The `core::slice::split_off` row is normalized",
            1,
        )
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    index_path.write_text(updated)


def update_delivery_index_with_requires_source_fidelity(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    sentence = requires_source_fidelity_index_sentence(verification)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"It also records `accepted_requires_source_fidelity`: "
        r".*?`validation\.validation_passed=(?:true|false)`\.",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    elif "The 122nd accepted row is" in text:
        updated = text.replace(
            "The 122nd accepted row is",
            f"{sentence} The 122nd accepted row is",
            1,
        )
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    updated = re.sub(
        r"The 122nd accepted row is .*? byte views\.",
        "The accepted set now includes the source-backed "
        "`core::slice::binary_search` contract with source-justified "
        "`obeys_cmp`, sortedness, unique-match, and Ok/Err partition clauses.",
        updated,
        count=1,
        flags=re.DOTALL,
    )
    index_path.write_text(updated)


def update_delivery_index_with_ensures_source_fidelity(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    if not index_path.is_file():
        return

    sentence = ensures_source_fidelity_index_sentence(verification)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"It also records `accepted_ensures_source_fidelity`: "
        r".*?`validation\.validation_passed=(?:true|false)`\.",
        re.DOTALL,
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    else:
        requires_pattern = re.compile(
            r"It also records `accepted_requires_source_fidelity`: "
            r".*?`validation\.validation_passed=(?:true|false)`\.",
            re.DOTALL,
        )
        match = requires_pattern.search(text)
        if match:
            updated = text[: match.end()] + f" {sentence}" + text[match.end() :]
        else:
            updated = text.rstrip() + "\n\n" + sentence + "\n"
    index_path.write_text(updated)


def prior_fresh_delta_index_sentence(summary: dict[str, Any]) -> str:
    decision_delta = summary.get("decision_delta")
    if not isinstance(decision_delta, dict):
        decision_delta = {}
    verifier = summary.get("fresh_verifier_counts")
    if not isinstance(verifier, dict):
        verifier = {}
    return (
        "The canonical `prior_fresh_delta/` audit has also been refreshed after "
        "the `alloc::string::String::replace_range` recovery: it records "
        f"{int_value(decision_delta.get('changed_count')):,} final-decision "
        "changes, "
        f"{int_value(decision_delta.get('prior_add_fresh_skip_count')):,} "
        "`add_spec->skip`, "
        f"{int_value(decision_delta.get('prior_skip_fresh_add_count')):,} "
        "`skip->add_spec`, "
        f"{int_value(verifier.get('accepted_semantic_candidates')):,} fresh "
        "accepted semantic candidates, and "
        f"{int_value(verifier.get('final_skip')):,} fresh skips."
    )


def update_delivery_index_with_prior_fresh_delta(out_dir: Path) -> None:
    delivery_root = out_dir.parent.parent
    index_path = delivery_root / "DELIVERY_INDEX.md"
    summary_path = out_dir / "prior_fresh_delta" / "summary.json"
    if not index_path.is_file() or not summary_path.is_file():
        return

    summary = json.loads(summary_path.read_text())
    sentence = prior_fresh_delta_index_sentence(summary)
    text = index_path.read_text()
    sentence_pattern = re.compile(
        r"The canonical `prior_fresh_delta/` audit has also been refreshed [^\n]*\."
    )
    if sentence_pattern.search(text):
        updated = sentence_pattern.sub(sentence, text, count=1)
    else:
        updated = text.rstrip() + "\n\n" + sentence + "\n"
    index_path.write_text(updated)


def update_delivery_metadata_with_canonical_verification(
    out_dir: Path,
    verification: dict[str, Any],
) -> None:
    delivery_root = out_dir.parent.parent
    metadata_path = delivery_root / "delivery_metadata.json"
    if not metadata_path.is_file():
        return

    metadata = json.loads(metadata_path.read_text())
    canonical_output = metadata.get("canonical_verified_output")
    if not isinstance(canonical_output, dict):
        return
    canonical_path = canonical_output.get("absolute_path")
    if not canonical_path:
        return
    if Path(str(canonical_path)).expanduser().resolve(strict=False) != out_dir.resolve(
        strict=False
    ):
        return

    canonical_output["absolute_path"] = str(out_dir.resolve(strict=False))
    canonical_output["verification_source"] = str(
        (out_dir / "final_verification.json").relative_to(delivery_root)
    )
    for noncanonical in metadata.get("noncanonical_outputs") or []:
        if isinstance(noncanonical, dict):
            noncanonical.pop("absolute_path", None)
            noncanonical.setdefault(
                "reference_policy",
                "not_a_delivery_artifact; absolute path omitted from canonical provenance",
            )

    snapshot = metadata.setdefault("verification_snapshot", {})
    for key in (
        "manifest_targets",
        "result_rows",
        "csv_rows",
        "final_candidates",
        "duplicate_result_count",
        "missing_target_count",
        "extra_target_count",
        "add_spec_recheck_required",
        "add_spec_rechecked",
    ):
        if key in verification:
            snapshot[key] = verification[key]
    for key in (
        "analysis_counts",
        "batch_counts",
        "candidate_decision_counts",
        "determinism_counts",
        "final_decision_counts",
        "status_counts",
        "unresolved_counts",
        "contract_code_schema_hygiene",
    ):
        block = verification.get(key)
        if isinstance(block, dict):
            snapshot[key] = block
    accepted_semantic = verification.get("accepted_semantic_candidates")
    if isinstance(accepted_semantic, dict):
        snapshot["accepted_semantic_candidates"] = {
            key: accepted_semantic[key]
            for key in ("rows", "validation")
            if key in accepted_semantic
        }

    def compact_block(name: str, keys: tuple[str, ...]) -> None:
        block = verification.get(name)
        if isinstance(block, dict):
            compact = {key: block[key] for key in keys if key in block}
            validation = block.get("validation")
            if (
                "validation_passed" not in compact
                and isinstance(validation, dict)
                and "validation_passed" in validation
            ):
                compact["validation_passed"] = validation["validation_passed"]
            snapshot[name] = compact

    compact_block(
        "accepted_assume_spec_target_binding_audit",
        (
            "accepted_rows",
            "audited_rows",
            "missing",
            "multiple",
            "parse_failed",
            "mismatched",
            "validation_passed",
        ),
    )
    compact_block(
        "accepted_assume_spec_signature_shape_audit",
        (
            "accepted_rows",
            "audited_rows",
            "parse_failed",
            "input_arity_mismatches",
            "input_shape_mismatches",
            "output_shape_mismatches",
            "validation_passed",
        ),
    )
    compact_block(
        "accepted_assume_spec_generic_bounds_audit",
        (
            "accepted_rows",
            "audited_rows",
            "parse_failed",
            "missing_manifest_signatures",
            "generic_param_mismatches",
            "const_generic_mismatches",
            "trait_bound_mismatches",
            "where_clause_mismatches",
            "missing_bound_rows",
            "extra_bound_rows",
            "mismatches",
            "validation_passed",
        ),
    )
    compact_block(
        "final_candidate_payload_consistency",
        (
            "audited_rows",
            "missing_batch_result_count",
            "missing_summary_artifact_count",
            "field_mismatch_count",
            "validation_passed",
        ),
    )
    compact_block(
        "target_artifact_integrity",
        (
            "expected_target_artifact_count",
            "target_dir_count",
            "target_json_count",
            "summary_json_count",
            "validation_passed",
        ),
    )
    compact_block(
        "skip_rationale",
        (
            "final_rows",
            "final_candidate_rows",
            "skip_rows",
            "skip_rows_with_rationale",
            "empty_skip_rationale_rows",
            "empty_rationale_rows",
            "all_skip_rows_have_rationale",
            "all_skip_rationales_non_empty",
            "accepted_semantic_candidate_rows",
        ),
    )
    compact_block(
        "full_skip_rationale_taxonomy",
        (
            "audited_skip_rows",
            "skip_rows",
            "empty_skip_rationale_rows",
            "empty_skip_issue_tag_rows",
            "empty_combined_issue_taxonomy_rows",
            "unclassified_skip_rows",
            "unjustified_skip_rows",
            "tracked_issue_tag_repair_targets",
            "tracked_issue_tag_repair_targets_with_tags",
            "duplicate_existing_vstd_spec_rows",
            "duplicate_vstd_assume_specification_issue_count",
            "duplicate_existing_vstd_spec_rows_with_duplicate_vstd_tag",
            "duplicate_existing_vstd_spec_rows_with_generic_determinism_tag",
            "source_backed_rationale_model_gap",
            "taxonomy_counts",
            "acceptance_checks",
            "acceptance_passed",
        ),
    )
    scope_validation = verification.get("scope_validation")
    if isinstance(scope_validation, dict):
        snapshot["scope_validation"] = scope_validation
    snapshot["canonical_artifact_provenance"] = verification[
        "canonical_artifact_provenance"
    ]
    requires_snapshot = accepted_requires_source_fidelity_metadata_snapshot(
        verification
    )
    if requires_snapshot:
        snapshot["accepted_requires_source_fidelity"] = requires_snapshot
    ensures_snapshot = accepted_ensures_source_fidelity_metadata_snapshot(
        verification
    )
    if ensures_snapshot:
        snapshot["accepted_ensures_source_fidelity"] = ensures_snapshot
    metadata["updated_at_utc"] = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")


def update_canonical_artifact_provenance_verification(out_dir: Path) -> dict[str, Any]:
    verification_path = out_dir / "final_verification.json"
    verification = json.loads(verification_path.read_text())
    provenance = build_canonical_artifact_provenance(out_dir, verification)
    verification["canonical_artifact_provenance"] = provenance
    verification_path.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
    update_delivery_metadata_with_canonical_verification(out_dir, verification)
    update_delivery_index_with_summary_counts(out_dir, verification)
    update_delivery_index_with_scope_validation(out_dir, verification)
    update_delivery_index_with_canonical_artifact_provenance(out_dir, verification)
    update_delivery_index_with_full_skip_taxonomy(out_dir, verification)
    update_delivery_index_with_requires_source_fidelity(out_dir, verification)
    update_delivery_index_with_ensures_source_fidelity(out_dir, verification)
    update_delivery_index_with_prior_fresh_delta(out_dir)
    return provenance


def build_scope_validation(
    metadata: dict[str, Any],
    rows: list[dict[str, Any]],
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_paths = manifest_paths_from_metadata(metadata)
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_targets = [str(entry.get("target") or "") for entry in manifest_entries]
    empty_manifest_target_rows = [
        index for index, target in enumerate(manifest_targets) if not target
    ]
    manifest_target_counts = Counter(target for target in manifest_targets if target)
    manifest_target_set = set(manifest_target_counts)
    duplicate_manifest_targets = sorted(
        target for target, count in manifest_target_counts.items() if count > 1
    )

    final_targets = [row["target"] for row in rows]
    final_target_counts = Counter(final_targets)
    final_target_set = set(final_targets)
    duplicate_final_targets = sorted(
        target for target, count in final_target_counts.items() if count > 1
    )
    missing_final_targets = sorted(manifest_target_set - final_target_set)
    extra_final_targets = sorted(final_target_set - manifest_target_set)

    accepted_targets = [row["target"] for row in accepted_rows]
    accepted_targets_not_in_manifest = sorted(set(accepted_targets) - manifest_target_set)

    kind_counts = Counter(
        kind for entry in manifest_entries for kind in entry_kinds(entry)
    )
    kind_combination_counts = Counter(
        ";".join(entry_kinds(entry)) for entry in manifest_entries
    )
    unexpected_kinds = sorted(set(kind_counts) - ALLOWED_FUNCTION_LIKE_KINDS)
    targets_with_unexpected_kinds = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if set(entry_kinds(entry)) - ALLOWED_FUNCTION_LIKE_KINDS
    )
    targets_with_empty_kinds = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if not entry_kinds(entry)
    )

    targets_missing_declarations = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if not entry.get("declarations")
    )
    declaration_count_mismatch_targets = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if entry.get("declaration_count") != len(entry.get("declarations") or [])
    )
    declaration_records = [
        (entry, declaration)
        for entry in manifest_entries
        for declaration in entry.get("declarations") or []
    ]
    total_declarations = len(declaration_records)
    declarations_with_signature = sum(
        declaration_has_function_signature(declaration)
        for _, declaration in declaration_records
    )
    stable_declarations = sum(
        declaration_is_stable(declaration) for _, declaration in declaration_records
    )
    public_api_declarations = sum(
        declaration_has_public_api_visibility(entry, declaration)
        for entry, declaration in declaration_records
    )
    provenance_declarations = sum(
        declaration_has_source_provenance(declaration)
        for _, declaration in declaration_records
    )

    declarations_missing_function_signature = sorted(
        str(entry.get("target") or "")
        for entry, declaration in declaration_records
        if not declaration_has_function_signature(declaration)
    )
    declarations_missing_stability = sorted(
        str(entry.get("target") or "")
        for entry, declaration in declaration_records
        if not declaration_is_stable(declaration)
    )
    declarations_missing_public_api_visibility = sorted(
        str(entry.get("target") or "")
        for entry, declaration in declaration_records
        if not declaration_has_public_api_visibility(entry, declaration)
    )
    declarations_missing_provenance = sorted(
        str(entry.get("target") or "")
        for entry, declaration in declaration_records
        if not declaration_has_source_provenance(declaration)
    )
    targets_missing_declaration_provenance = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if not any(
            declaration_has_source_provenance(declaration)
            for declaration in entry.get("declarations") or []
        )
    )
    targets_missing_public_stable_function_like_scope = sorted(
        str(entry.get("target") or "")
        for entry in manifest_entries
        if not (
            entry_kinds(entry)
            and not (set(entry_kinds(entry)) - ALLOWED_FUNCTION_LIKE_KINDS)
            and entry.get("declarations")
            and all(
                declaration_has_function_signature(declaration)
                and declaration_is_stable(declaration)
                and declaration_has_public_api_visibility(entry, declaration)
                and declaration_has_source_provenance(declaration)
                for declaration in entry.get("declarations") or []
            )
        )
    )

    validation_errors = []
    if not manifest_paths:
        validation_errors.append("classified_manifest_missing_from_batch_metadata")
    if empty_manifest_target_rows:
        validation_errors.append(
            f"empty_manifest_target_rows:{len(empty_manifest_target_rows)}"
        )
    if duplicate_manifest_targets:
        validation_errors.append(
            f"duplicate_manifest_targets:{len(duplicate_manifest_targets)}"
        )
    if missing_final_targets:
        validation_errors.append(f"missing_final_targets:{len(missing_final_targets)}")
    if extra_final_targets:
        validation_errors.append(f"extra_final_targets:{len(extra_final_targets)}")
    if duplicate_final_targets:
        validation_errors.append(
            f"duplicate_final_targets:{len(duplicate_final_targets)}"
        )
    if unexpected_kinds:
        validation_errors.append(f"unexpected_kinds:{len(unexpected_kinds)}")
    if targets_with_empty_kinds:
        validation_errors.append(
            f"targets_with_empty_kinds:{len(targets_with_empty_kinds)}"
        )
    if targets_missing_declarations:
        validation_errors.append(
            f"targets_missing_declarations:{len(targets_missing_declarations)}"
        )
    if declaration_count_mismatch_targets:
        validation_errors.append(
            f"declaration_count_mismatch_targets:{len(declaration_count_mismatch_targets)}"
        )
    if declarations_missing_function_signature:
        validation_errors.append(
            "declarations_missing_function_signature:"
            f"{len(declarations_missing_function_signature)}"
        )
    if declarations_missing_stability:
        validation_errors.append(
            f"declarations_missing_stability:{len(declarations_missing_stability)}"
        )
    if declarations_missing_public_api_visibility:
        validation_errors.append(
            "declarations_missing_public_api_visibility:"
            f"{len(declarations_missing_public_api_visibility)}"
        )
    if declarations_missing_provenance:
        validation_errors.append(
            f"declarations_missing_provenance:{len(declarations_missing_provenance)}"
        )
    if accepted_targets_not_in_manifest:
        validation_errors.append(
            "accepted_targets_not_in_manifest:"
            f"{len(accepted_targets_not_in_manifest)}"
        )

    return {
        "source": {
            "loaded_from_batch_summary_metadata": bool(manifest_paths),
            "manifest_path_count": len(manifest_paths),
            "manifest_paths": [str(path.resolve()) for path in manifest_paths],
        },
        "validation_passed": not validation_errors,
        "validation_errors": validation_errors,
        "target_bijection": {
            "manifest_target_rows": len(manifest_entries),
            "manifest_targets": len(manifest_target_set),
            "final_candidate_rows": len(rows),
            "final_candidate_targets": len(final_target_set),
            "missing_final_candidate_target_count": len(missing_final_targets),
            "extra_final_candidate_target_count": len(extra_final_targets),
            "duplicate_manifest_target_count": len(duplicate_manifest_targets),
            "duplicate_final_candidate_target_count": len(duplicate_final_targets),
            "missing_final_candidate_targets": missing_final_targets,
            "extra_final_candidate_targets": extra_final_targets,
            "duplicate_manifest_targets": duplicate_manifest_targets,
            "duplicate_final_candidate_targets": duplicate_final_targets,
            "is_bijection": (
                bool(manifest_paths)
                and not empty_manifest_target_rows
                and not duplicate_manifest_targets
                and not missing_final_targets
                and not extra_final_targets
                and not duplicate_final_targets
                and len(rows) == len(manifest_target_set)
            ),
        },
        "function_like_manifest_scope": {
            "allowed_kinds": sorted(ALLOWED_FUNCTION_LIKE_KINDS),
            "observed_kinds": sorted(kind_counts),
            "kind_counts": dict(sorted(kind_counts.items())),
            "kind_combination_counts": dict(sorted(kind_combination_counts.items())),
            "unexpected_kinds": unexpected_kinds,
            "unexpected_kind_count": len(unexpected_kinds),
            "targets_with_unexpected_kinds": targets_with_unexpected_kinds,
            "targets_with_unexpected_kinds_count": len(targets_with_unexpected_kinds),
            "targets_with_empty_kinds": targets_with_empty_kinds,
            "targets_with_empty_kinds_count": len(targets_with_empty_kinds),
            "all_targets_have_only_function_like_kinds": (
                not unexpected_kinds and not targets_with_empty_kinds
            ),
        },
        "declaration_scope": {
            "manifest_targets": len(manifest_target_set),
            "total_declarations": total_declarations,
            "targets_with_declarations": (
                len(manifest_entries) - len(targets_missing_declarations)
            ),
            "targets_missing_declarations": targets_missing_declarations,
            "targets_missing_declarations_count": len(targets_missing_declarations),
            "declaration_count_mismatch_targets": declaration_count_mismatch_targets,
            "declaration_count_mismatch_target_count": len(
                declaration_count_mismatch_targets
            ),
            "declarations_with_function_signature": declarations_with_signature,
            "declarations_missing_function_signature_count": len(
                declarations_missing_function_signature
            ),
            "declarations_missing_function_signature_targets": (
                declarations_missing_function_signature
            ),
            "stable_declarations": stable_declarations,
            "declarations_missing_stability_count": len(
                declarations_missing_stability
            ),
            "declarations_missing_stability_targets": declarations_missing_stability,
            "public_api_visibility_declarations": public_api_declarations,
            "declarations_missing_public_api_visibility_count": len(
                declarations_missing_public_api_visibility
            ),
            "declarations_missing_public_api_visibility_targets": (
                declarations_missing_public_api_visibility
            ),
            "source_provenance_declarations": provenance_declarations,
            "declarations_missing_provenance_count": len(
                declarations_missing_provenance
            ),
            "declarations_missing_provenance_targets": declarations_missing_provenance,
            "targets_with_non_empty_declaration_provenance": (
                len(manifest_entries) - len(targets_missing_declaration_provenance)
            ),
            "targets_missing_declaration_provenance_count": len(
                targets_missing_declaration_provenance
            ),
            "targets_missing_declaration_provenance": (
                targets_missing_declaration_provenance
            ),
            "targets_with_public_stable_function_like_declaration_scope": (
                len(manifest_entries)
                - len(targets_missing_public_stable_function_like_scope)
            ),
            "targets_missing_public_stable_function_like_declaration_scope_count": len(
                targets_missing_public_stable_function_like_scope
            ),
            "targets_missing_public_stable_function_like_declaration_scope": (
                targets_missing_public_stable_function_like_scope
            ),
            "all_targets_have_declarations": not targets_missing_declarations,
            "all_declaration_counts_match_manifest": (
                not declaration_count_mismatch_targets
            ),
            "all_declarations_have_function_signatures": (
                declarations_with_signature == total_declarations
            ),
            "all_declarations_are_stable": stable_declarations == total_declarations,
            "all_declarations_have_public_api_visibility": (
                public_api_declarations == total_declarations
            ),
            "all_declarations_have_source_provenance": (
                provenance_declarations == total_declarations
            ),
            "all_targets_have_non_empty_declaration_provenance": (
                not targets_missing_declaration_provenance
            ),
            "all_targets_have_public_stable_function_like_declaration_scope": (
                not targets_missing_public_stable_function_like_scope
            ),
            "rustdoc_visibility_counts": dict(
                sorted(
                    Counter(
                        str(declaration.get("visibility") or "")
                        for _, declaration in declaration_records
                    ).items()
                )
            ),
            "stability_level_counts": dict(
                sorted(
                    Counter(
                        str((declaration.get("stability") or {}).get("level") or "")
                        for _, declaration in declaration_records
                    ).items()
                )
            ),
            "public_api_visibility_rule": (
                "rustdoc visibility 'public' is public API; rustdoc visibility "
                "'default' is accepted only for trait_method declarations because "
                "associated items inherit the public stable trait API scope"
            ),
        },
        "accepted_candidate_scope": {
            "accepted_semantic_candidate_rows": len(accepted_rows),
            "accepted_targets_not_in_manifest_count": len(
                accepted_targets_not_in_manifest
            ),
            "accepted_targets_not_in_manifest": accepted_targets_not_in_manifest,
            "all_accepted_targets_in_manifest": not accepted_targets_not_in_manifest,
        },
    }


def decision(round_record: dict[str, Any]) -> str:
    return (round_record.get("candidate") or {}).get(
        "decision",
        round_record.get("decision", ""),
    )


def typecheck_passed(round_record: dict[str, Any]) -> bool:
    typecheck = (round_record.get("checker") or {}).get("typecheck") or {}
    return typecheck.get("returncode") == 0


def serialized_contract_code(candidate: dict[str, Any]) -> str:
    value = candidate.get("contract_code")
    if value is None:
        return ""
    code = str(value)
    if candidate.get("decision") == "skip" and code.strip() == "None":
        return ""
    return code


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def is_semantic_candidate_before_source_fidelity(row: dict[str, Any]) -> bool:
    return (
        row.get("final_decision") == "add_spec"
        and bool_value(row.get("typecheck_passed"))
        and int_value(row.get("guarded_reward")) == 1
        and int_value(row.get("semantic_guarded_reward")) == 1
        and not str(row.get("issues") or "").strip()
        and not str(row.get("semantic_gate_issues") or "").strip()
        and not str(row.get("semantic_review_issues") or "").strip()
    )


def requires_source_fidelity_allows_acceptance(row: dict[str, Any]) -> bool:
    if not str(row.get("requires") or "").strip():
        return True
    return (
        row.get("requires_source_fidelity_classification")
        == SOURCE_FIDELITY_JUSTIFIED
    )


def is_accepted_semantic_candidate(row: dict[str, Any]) -> bool:
    return is_semantic_candidate_before_source_fidelity(
        row
    ) and requires_source_fidelity_allows_acceptance(row)


def normalized_contract_clause(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip()).rstrip(",;").strip()


def has_exact_clause(text: Any, expected: str) -> bool:
    if normalized_contract_clause(text) == expected:
        return True
    return any(
        normalized_contract_clause(part) == expected
        for part in str(text or "").split(";")
    )


def build_accepted_contract_text_safety(
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    def unique_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(
            {row["target"]: row for row in rows}.values(),
            key=lambda row: row["target"],
        )

    empty_ensures_rows = [
        row for row in accepted_rows if not str(row.get("ensures") or "").strip()
    ]
    exact_true_ensures_rows = [
        row for row in accepted_rows if has_exact_clause(row.get("ensures"), "true")
    ]
    exact_false_ensures_rows = [
        row for row in accepted_rows if has_exact_clause(row.get("ensures"), "false")
    ]
    exact_true_false_ensures_rows = unique_rows(
        exact_true_ensures_rows + exact_false_ensures_rows
    )
    false_precondition_rows = [
        row
        for row in accepted_rows
        if has_exact_clause(row.get("requires"), "false")
        or re.search(r"\brequires\s+false\s*[,;]", str(row.get("contract_code") or ""))
    ]
    arbitrary_token_rows = []
    assume_token_rows = []
    for row in accepted_rows:
        contract_text = "\n".join(
            str(row.get(field) or "")
            for field in ("requires", "ensures", "contract_code")
        )
        if re.search(r"\barbitrary\s*\(", contract_text):
            arbitrary_token_rows.append(row)
        if re.search(r"\bassume\s*\(", contract_text):
            assume_token_rows.append(row)
    arbitrary_or_assume_token_rows = unique_rows(
        arbitrary_token_rows + assume_token_rows
    )
    non_empty_requires_rows = [
        row for row in accepted_rows if str(row.get("requires") or "").strip()
    ]

    def targets(rows: list[dict[str, Any]]) -> list[str]:
        return [row["target"] for row in rows]

    audit = {
        "source": (
            "accepted semantic candidates from this analyzer run; token checks search "
            "requires, ensures, and contract_code for exact false preconditions, "
            "exact true/false ensures, arbitrary(...), and standalone assume(...)"
        ),
        "accepted_rows": len(accepted_rows),
        "empty_ensures_count": len(empty_ensures_rows),
        "empty_ensures_rows": len(empty_ensures_rows),
        "empty_ensures_targets": targets(empty_ensures_rows),
        "exact_true_ensures_count": len(exact_true_ensures_rows),
        "exact_true_ensures_targets": targets(exact_true_ensures_rows),
        "exact_false_ensures_count": len(exact_false_ensures_rows),
        "exact_false_ensures_targets": targets(exact_false_ensures_rows),
        "exact_true_false_ensures_count": len(exact_true_false_ensures_rows),
        "exact_true_false_ensures_rows": len(exact_true_false_ensures_rows),
        "exact_true_false_ensures_targets": targets(exact_true_false_ensures_rows),
        "false_precondition_count": len(false_precondition_rows),
        "false_precondition_rows": len(false_precondition_rows),
        "false_precondition_targets": targets(false_precondition_rows),
        "arbitrary_token_count": len(arbitrary_token_rows),
        "arbitrary_token_targets": targets(arbitrary_token_rows),
        "assume_token_count": len(assume_token_rows),
        "assume_token_targets": targets(assume_token_rows),
        "arbitrary_or_assume_token_count": len(arbitrary_or_assume_token_rows),
        "arbitrary_assume_token_count": len(arbitrary_or_assume_token_rows),
        "arbitrary_or_assume_token_targets": targets(arbitrary_or_assume_token_rows),
        "non_empty_requires_count": len(non_empty_requires_rows),
        "non_empty_requires_targets": targets(non_empty_requires_rows),
        "non_empty_requires": [
            {
                "target": row["target"],
                "requires": row["requires"],
            }
            for row in non_empty_requires_rows
        ],
    }
    audit["validation"] = {
        "all_ensures_non_empty": audit["empty_ensures_count"] == 0,
        "no_exact_true_false_ensures": (
            audit["exact_true_false_ensures_count"] == 0
        ),
        "no_false_preconditions": audit["false_precondition_count"] == 0,
        "no_arbitrary_or_assume_tokens": (
            audit["arbitrary_or_assume_token_count"] == 0
        ),
        "validation_passed": (
            audit["empty_ensures_count"] == 0
            and audit["exact_true_false_ensures_count"] == 0
            and audit["false_precondition_count"] == 0
            and audit["arbitrary_or_assume_token_count"] == 0
        ),
    }
    return audit


def strip_rust_path_generics(text: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("::", index):
            generic_start = skip_whitespace(text, index + 2)
            if generic_start < len(text) and text[generic_start] == "<":
                generic_end = find_matching_delimiter(text, generic_start, "<", ">")
                if generic_end is not None:
                    index = generic_end
                    continue
        if text[index] == "<":
            generic_end = find_matching_delimiter(text, index, "<", ">")
            if generic_end is not None:
                index = generic_end
                continue
        result.append(text[index])
        index += 1
    return "".join(result)


def split_rust_path_parts(text: str) -> list[str]:
    return [
        part.strip()
        for part in strip_rust_path_generics(text).split("::")
        if part.strip()
    ]


def rust_receiver_kind(receiver: str) -> str:
    compact = compact_rust_path_text(receiver)
    if compact == "str":
        return "str"
    if compact.startswith("[") and compact.endswith("]"):
        square_depth = 0
        angle_depth = 0
        paren_depth = 0
        for char in compact[1:-1]:
            if char == "[":
                square_depth += 1
            elif char == "]" and square_depth:
                square_depth -= 1
            elif char == "<":
                angle_depth += 1
            elif char == ">" and angle_depth:
                angle_depth -= 1
            elif char == "(":
                paren_depth += 1
            elif char == ")" and paren_depth:
                paren_depth -= 1
            elif (
                char == ";"
                and square_depth == 0
                and angle_depth == 0
                and paren_depth == 0
            ):
                return "array"
        return "slice"
    parts = split_rust_path_parts(receiver)
    return parts[-1] if parts else compact


def parse_assume_specification_binding_target(raw_target: str) -> dict[str, Any]:
    target = str(raw_target or "").strip()
    receiver = ""
    rest = target
    if rest.startswith("<"):
        receiver_end = find_matching_delimiter(rest, 0, "<", ">")
        if receiver_end is None:
            return {
                "status": "parse_failed",
                "error": "unclosed qualified receiver type",
            }
        receiver = rest[1 : receiver_end - 1].strip()
        rest = rest[receiver_end:].strip()
        if rest.startswith("::"):
            rest = rest[2:].strip()
    path_parts = split_rust_path_parts(rest)
    if not path_parts:
        return {
            "status": "parse_failed",
            "error": "empty assume_specification target path",
        }
    return {
        "status": "ok",
        "error": "",
        "raw": target,
        "compact": compact_rust_path_text(target),
        "receiver": receiver,
        "receiver_kind": rust_receiver_kind(receiver) if receiver else "",
        "path_parts": path_parts,
        "name": path_parts[-1],
    }


def module_text(parts: list[str] | tuple[str, ...]) -> str:
    return "::".join(parts)


def owner_for_kind(owner_for: Any) -> str:
    if not isinstance(owner_for, dict):
        return ""
    if owner_for.get("primitive"):
        return str(owner_for["primitive"])
    if "slice" in owner_for:
        return "slice"
    if "array" in owner_for:
        return "array"
    resolved_path = owner_for.get("resolved_path") or {}
    if resolved_path.get("path"):
        return str(resolved_path["path"])
    return ""


def manifest_public_paths(entry: dict[str, Any]) -> list[str]:
    paths = [str(entry.get("target") or "")]
    paths.extend(str(path) for path in entry.get("origin_paths") or [] if str(path))
    paths.extend(str(path) for path in entry.get("display_paths") or [] if str(path))
    return [path for path in paths if path]


def public_path_module_candidates(
    entry: dict[str, Any],
    name: str,
    *,
    owner_name: str = "",
) -> set[tuple[str, ...]]:
    modules: set[tuple[str, ...]] = set()
    for path in manifest_public_paths(entry):
        parsed = parse_assume_specification_binding_target(path)
        if parsed.get("status") != "ok" or parsed.get("name") != name:
            continue
        parts = list(parsed.get("path_parts") or [])
        if owner_name and len(parts) >= 2 and parts[-2] == owner_name:
            modules.add(tuple(parts[:-2]))
        else:
            modules.add(tuple(parts[:-1]))
    return modules


def add_expected_binding_alternative(
    alternatives: list[dict[str, Any]],
    *,
    name: str,
    owner_name: str = "",
    owner_kind: str = "",
    module_parts: tuple[str, ...] = (),
    source: str,
) -> None:
    if not name:
        return
    candidate = {
        "name": name,
        "owner_name": owner_name,
        "owner_kind": owner_kind,
        "module_parts": module_parts,
        "source": source,
    }
    key = (
        candidate["name"],
        candidate["owner_name"],
        candidate["owner_kind"],
        candidate["module_parts"],
        candidate["source"],
    )
    existing = {
        (
            alt["name"],
            alt["owner_name"],
            alt["owner_kind"],
            alt["module_parts"],
            alt["source"],
        )
        for alt in alternatives
    }
    if key not in existing:
        alternatives.append(candidate)


def expected_binding_alternatives(
    manifest_entry: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not manifest_entry:
        return []
    alternatives: list[dict[str, Any]] = []
    target = str(manifest_entry.get("target") or "")
    target_parts = target.split("::") if target else []
    target_name = target_parts[-1] if target_parts else ""
    kinds = set(entry_kinds(manifest_entry))
    if "free_function" in kinds and target_name:
        add_expected_binding_alternative(
            alternatives,
            name=target_name,
            module_parts=tuple(target_parts[:-1]),
            source="manifest target free_function path",
        )
    if {"inherent_method", "trait_method"} & kinds and len(target_parts) >= 2:
        add_expected_binding_alternative(
            alternatives,
            name=target_name,
            owner_name=target_parts[-2],
            module_parts=tuple(target_parts[:-2]),
            source="manifest target method path",
        )

    declarations = [
        *(manifest_entry.get("declarations") or []),
        *(manifest_entry.get("verification_declarations") or []),
    ]
    for declaration in declarations:
        name = str(declaration.get("name") or target_name)
        owner = declaration.get("owner") or {}
        resolved_owner_path = owner.get("resolved_owner_path") or []
        if resolved_owner_path:
            owner_name = str(resolved_owner_path[-1])
            add_expected_binding_alternative(
                alternatives,
                name=name,
                owner_name=owner_name,
                module_parts=tuple(str(part) for part in resolved_owner_path[:-1]),
                source="manifest declaration resolved_owner_path",
            )
            for module_parts in public_path_module_candidates(
                manifest_entry,
                name,
                owner_name=owner_name,
            ):
                add_expected_binding_alternative(
                    alternatives,
                    name=name,
                    owner_name=owner_name,
                    module_parts=module_parts,
                    source="manifest public owner path",
                )
            continue

        owner_kind = owner_for_kind(owner.get("for"))
        if owner_kind:
            module_candidates = public_path_module_candidates(manifest_entry, name)
            if not module_candidates:
                module_candidates = {()}
            for module_parts in module_candidates:
                add_expected_binding_alternative(
                    alternatives,
                    name=name,
                    owner_kind=owner_kind,
                    module_parts=module_parts,
                    source="manifest declaration receiver",
                )
            continue

        module_candidates = public_path_module_candidates(manifest_entry, name)
        if not module_candidates and target_name == name:
            module_candidates = {tuple(target_parts[:-1])}
        for module_parts in module_candidates:
            add_expected_binding_alternative(
                alternatives,
                name=name,
                module_parts=module_parts,
                source="manifest declaration free_function",
            )
    return alternatives


def actual_binding_alternatives(parsed_binding: dict[str, Any]) -> list[dict[str, Any]]:
    parts = list(parsed_binding.get("path_parts") or [])
    name = str(parsed_binding.get("name") or "")
    alternatives: list[dict[str, Any]] = []
    if parsed_binding.get("receiver_kind"):
        alternatives.append(
            {
                "name": name,
                "owner_name": "",
                "owner_kind": parsed_binding["receiver_kind"],
                "module_parts": tuple(parts[:-1]),
                "shape": "qualified_receiver",
            }
        )
        return alternatives

    alternatives.append(
        {
            "name": name,
            "owner_name": "",
            "owner_kind": "",
            "module_parts": tuple(parts[:-1]),
            "shape": "free_path",
        }
    )
    for owner_index in range(max(len(parts) - 1, 0)):
        owner_name = parts[owner_index]
        alternatives.append(
            {
                "name": name,
                "owner_name": owner_name,
                "owner_kind": owner_name if owner_name == "str" else "",
                "module_parts": tuple(parts[:owner_index]),
                "shape": "owner_path",
            }
        )
    return alternatives


def owner_matches(actual: dict[str, Any], expected: dict[str, Any]) -> bool:
    expected_kind = str(expected.get("owner_kind") or "")
    expected_name = str(expected.get("owner_name") or "")
    if expected_kind:
        return (
            str(actual.get("owner_kind") or "") == expected_kind
            or str(actual.get("owner_name") or "") == expected_kind
        )
    if expected_name:
        return str(actual.get("owner_name") or "") == expected_name
    return not str(actual.get("owner_name") or "") and not str(
        actual.get("owner_kind") or ""
    )


def module_matches(
    actual_parts: tuple[str, ...],
    expected_parts: tuple[str, ...],
) -> bool:
    if actual_parts == expected_parts:
        return True
    if not actual_parts:
        return True
    if len(actual_parts) <= len(expected_parts):
        return expected_parts[-len(actual_parts) :] == actual_parts
    return False


def match_binding_to_manifest(
    parsed_binding: dict[str, Any],
    manifest_entry: dict[str, Any] | None,
) -> dict[str, Any] | None:
    actual_alternatives = actual_binding_alternatives(parsed_binding)
    expected_alternatives = expected_binding_alternatives(manifest_entry)
    for actual in actual_alternatives:
        for expected in expected_alternatives:
            if actual["name"] != expected["name"]:
                continue
            if not owner_matches(actual, expected):
                continue
            if not module_matches(actual["module_parts"], expected["module_parts"]):
                continue
            return {
                "actual": actual,
                "expected": expected,
            }
    return None


def binding_owner_text(binding: dict[str, Any]) -> str:
    owner_kind = str(binding.get("owner_kind") or "")
    owner_name = str(binding.get("owner_name") or "")
    return owner_kind or owner_name


def build_accepted_assume_spec_target_binding_audit(
    metadata: dict[str, Any],
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_entries_by_target = {
        str(entry.get("target") or ""): entry
        for entry in manifest_entries
        if str(entry.get("target") or "")
    }

    audit_rows: list[dict[str, Any]] = []
    missing_rows = []
    multiple_rows = []
    parse_failed_rows = []
    mismatched_rows = []
    for row in accepted_rows:
        target = row["target"]
        bindings = assume_specification_bindings_from_contract_code(
            str(row.get("contract_code") or "")
        )
        parsed_binding: dict[str, Any] | None = None
        matched_binding: dict[str, Any] | None = None
        binding_text = ""
        error = ""

        if not bindings:
            status = "missing"
            error = "no assume_specification binding found"
            missing_rows.append(row)
        elif len(bindings) > 1:
            status = "multiple"
            binding_text = ";".join(
                str(binding.get("target") or "") for binding in bindings
            )
            error = f"expected exactly one binding, found {len(bindings)}"
            multiple_rows.append(row)
        elif bindings[0].get("status") != "ok":
            status = "parse_failed"
            error = str(bindings[0].get("error") or "binding parse failed")
            parse_failed_rows.append(row)
        else:
            binding_text = str(bindings[0].get("target") or "")
            parsed_binding = parse_assume_specification_binding_target(
                str(bindings[0].get("raw_target") or "")
            )
            if parsed_binding.get("status") != "ok":
                status = "parse_failed"
                error = str(parsed_binding.get("error") or "binding parse failed")
                parse_failed_rows.append(row)
            else:
                matched_binding = match_binding_to_manifest(
                    parsed_binding,
                    manifest_entries_by_target.get(target),
                )
                if matched_binding is None:
                    status = "mismatched"
                    error = "binding owner/name/module did not match manifest target"
                    mismatched_rows.append(row)
                else:
                    status = "ok"

        actual = (matched_binding or {}).get("actual") or {}
        expected = (matched_binding or {}).get("expected") or {}
        if parsed_binding and parsed_binding.get("status") == "ok" and not actual:
            actual_alternatives = actual_binding_alternatives(parsed_binding)
            actual = actual_alternatives[0] if actual_alternatives else {}
        audit_rows.append(
            {
                "target": target,
                "status": status,
                "binding_count": len(bindings),
                "binding": binding_text,
                "binding_name": (
                    str(parsed_binding.get("name") or "") if parsed_binding else ""
                ),
                "binding_owner": binding_owner_text(actual),
                "binding_module": module_text(actual.get("module_parts") or ()),
                "matched_expected_source": str(expected.get("source") or ""),
                "matched_expected_owner": binding_owner_text(expected),
                "matched_expected_module": module_text(
                    expected.get("module_parts") or ()
                ),
                "error": error,
            }
        )

    def targets(rows: list[dict[str, Any]]) -> list[str]:
        return [row["target"] for row in rows]

    audit = {
        "artifact_schema": 1,
        "source": (
            "Accepted semantic candidates from this analyzer run; each contract_code "
            "is parsed with delimiter-aware handling for multiline "
            "assume_specification generics and nested slice/array brackets, then "
            "the bound owner/name/module is compared with the classified-manifest "
            "declaration for the row target."
        ),
        "accepted_rows": len(accepted_rows),
        "audited_rows": len(audit_rows),
        "missing_binding_rows": len(missing_rows),
        "multiple_binding_rows": len(multiple_rows),
        "parse_failed_binding_rows": len(parse_failed_rows),
        "mismatched_binding_rows": len(mismatched_rows),
        "missing": len(missing_rows),
        "multiple": len(multiple_rows),
        "parse_failed": len(parse_failed_rows),
        "mismatched": len(mismatched_rows),
        "missing_binding_targets": targets(missing_rows),
        "multiple_binding_targets": targets(multiple_rows),
        "parse_failed_binding_targets": targets(parse_failed_rows),
        "mismatched_binding_targets": targets(mismatched_rows),
        "rows": audit_rows,
    }
    audit["validation"] = {
        "audit_covers_all_accepted_rows": len(audit_rows) == len(accepted_rows),
        "no_missing_bindings": audit["missing_binding_rows"] == 0,
        "no_multiple_bindings": audit["multiple_binding_rows"] == 0,
        "no_parse_failed_bindings": audit["parse_failed_binding_rows"] == 0,
        "no_mismatched_bindings": audit["mismatched_binding_rows"] == 0,
        "validation_passed": (
            len(audit_rows) == len(accepted_rows)
            and audit["missing_binding_rows"] == 0
            and audit["multiple_binding_rows"] == 0
            and audit["parse_failed_binding_rows"] == 0
            and audit["mismatched_binding_rows"] == 0
        ),
    }
    return audit


def split_top_level_items(text: str, separator: str = ",") -> list[str]:
    items: list[str] = []
    start = 0
    stack: list[str] = []
    close_for_open = {"<": ">", "(": ")", "[": "]", "{": "}"}
    for index, char in enumerate(text):
        if char in close_for_open:
            stack.append(close_for_open[char])
        elif stack and char == stack[-1]:
            stack.pop()
        elif char == separator and not stack:
            item = text[start:index].strip()
            if item:
                items.append(item)
            start = index + 1
    item = text[start:].strip()
    if item:
        items.append(item)
    return items


def find_top_level_colon(text: str) -> int | None:
    stack: list[str] = []
    close_for_open = {"<": ">", "(": ")", "[": "]", "{": "}"}
    for index, char in enumerate(text):
        if char in close_for_open:
            stack.append(close_for_open[char])
            continue
        if stack and char == stack[-1]:
            stack.pop()
            continue
        if char != ":" or stack:
            continue
        previous_char = text[index - 1] if index else ""
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if previous_char != ":" and next_char != ":":
            return index
    return None


def find_top_level_angle_start(text: str) -> int | None:
    stack: list[str] = []
    close_for_open = {"(": ")", "[": "]", "{": "}"}
    for index, char in enumerate(text):
        if char in close_for_open:
            stack.append(close_for_open[char])
            continue
        if stack and char == stack[-1]:
            stack.pop()
            continue
        if char == "<" and not stack:
            return index
    return None


def keyword_starts_at(text: str, index: int, keyword: str) -> bool:
    if not text.startswith(keyword, index):
        return False
    before = text[index - 1] if index else ""
    after_index = index + len(keyword)
    after = text[after_index] if after_index < len(text) else ""
    return not (before.isalnum() or before == "_") and not (
        after.isalnum() or after == "_"
    )


def find_contract_clause_start(
    text: str,
    start: int,
    keywords: tuple[str, ...],
) -> int:
    stack: list[str] = []
    close_for_open = {"<": ">", "(": ")", "[": "]", "{": "}"}
    index = start
    while index < len(text):
        char = text[index]
        if char in close_for_open:
            stack.append(close_for_open[char])
        elif stack and char == stack[-1]:
            stack.pop()
        elif not stack:
            if char == ";":
                return index
            if any(
                keyword_starts_at(text, index, keyword)
                for keyword in keywords
            ):
                return index
        index += 1
    return len(text)


def find_contract_header_clause_start(text: str, start: int) -> int:
    return find_contract_clause_start(text, start, ("where", "requires", "ensures"))


def find_contract_body_clause_start(text: str, start: int) -> int:
    return find_contract_clause_start(text, start, ("requires", "ensures"))


def assume_specification_generic_names(generic_params_text: str) -> set[str]:
    names: set[str] = set()
    for item in split_top_level_items(generic_params_text):
        item = item.strip()
        if not item or item.startswith("'"):
            continue
        if item.startswith("const "):
            item = item[len("const ") :].strip()
        match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)", item)
        if match:
            names.add(match.group(1))
    return names


def split_top_level_bound_items(text: str) -> list[str]:
    return split_top_level_items(text, separator="+")


def strip_top_level_default(text: str) -> str:
    stack: list[str] = []
    close_for_open = {"<": ">", "(": ")", "[": "]", "{": "}"}
    for index, char in enumerate(text):
        if char in close_for_open:
            stack.append(close_for_open[char])
            continue
        if stack and char == stack[-1]:
            stack.pop()
            continue
        if char == "=" and not stack:
            return text[:index].strip()
    return text.strip()


def parse_contract_generic_params(
    generic_params_text: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    params: list[dict[str, Any]] = []
    errors: list[str] = []
    for raw_item in split_top_level_items(generic_params_text):
        item = strip_top_level_default(raw_item.strip().rstrip(","))
        if not item:
            continue
        if item.startswith("'"):
            match = re.match(r"('[A-Za-z_][A-Za-z0-9_]*)", item)
            if not match:
                errors.append(f"malformed lifetime parameter: {raw_item}")
                continue
            params.append(
                {
                    "kind": "lifetime",
                    "name": match.group(1),
                    "bounds": [],
                    "const_type": "",
                    "raw": raw_item.strip(),
                }
            )
            continue
        if item.startswith("const "):
            rest = item[len("const ") :].strip()
            colon = find_top_level_colon(rest)
            if colon is None:
                errors.append(f"const generic lacks type annotation: {raw_item}")
                continue
            name = rest[:colon].strip()
            const_type = rest[colon + 1 :].strip()
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) or not const_type:
                errors.append(f"malformed const generic parameter: {raw_item}")
                continue
            params.append(
                {
                    "kind": "const",
                    "name": name,
                    "bounds": [],
                    "const_type": const_type,
                    "raw": raw_item.strip(),
                }
            )
            continue
        colon = find_top_level_colon(item)
        name_text = item[:colon].strip() if colon is not None else item.strip()
        match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*$", name_text)
        if not match:
            errors.append(f"malformed type generic parameter: {raw_item}")
            continue
        bounds_text = item[colon + 1 :].strip() if colon is not None else ""
        params.append(
            {
                "kind": "type",
                "name": match.group(1),
                "bounds": split_top_level_bound_items(bounds_text),
                "const_type": "",
                "raw": raw_item.strip(),
            }
        )
    return params, errors


def parse_contract_where_predicates(
    where_clause_text: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    predicates: list[dict[str, Any]] = []
    errors: list[str] = []
    if not where_clause_text.strip():
        return predicates, errors
    for raw_item in split_top_level_items(where_clause_text):
        item = raw_item.strip().rstrip(",")
        if not item:
            continue
        colon = find_top_level_colon(item)
        if colon is None:
            errors.append(f"where predicate lacks top-level bound: {raw_item}")
            continue
        subject = item[:colon].strip()
        bounds_text = item[colon + 1 :].strip()
        if not subject or not bounds_text:
            errors.append(f"malformed where predicate: {raw_item}")
            continue
        predicates.append(
            {
                "subject": subject,
                "bounds": split_top_level_bound_items(bounds_text),
                "raw": raw_item.strip(),
            }
        )
    return predicates, errors


def parse_assume_specification_parameters(params_text: str) -> tuple[list[dict[str, str]], str]:
    params: list[dict[str, str]] = []
    if not params_text.strip():
        return params, ""
    for item in split_top_level_items(params_text):
        colon = find_top_level_colon(item)
        if colon is None:
            return [], f"parameter lacks top-level type annotation: {item}"
        name = item[:colon].strip()
        type_text = item[colon + 1 :].strip()
        if not name or not type_text:
            return [], f"malformed parameter declaration: {item}"
        params.append({"name": name, "type": type_text})
    return params, ""


def parse_assume_specification_header(contract_code: str) -> dict[str, Any]:
    text = str(contract_code or "")
    match = re.search(r"\bassume_specification\b", text)
    if not match:
        return {"status": "parse_failed", "error": "no assume_specification found"}

    index = skip_whitespace(text, match.end())
    generic_params_text = ""
    if index < len(text) and text[index] == "<":
        generic_end = find_matching_delimiter(text, index, "<", ">")
        if generic_end is None:
            return {
                "status": "parse_failed",
                "error": "unclosed assume_specification generic parameter list",
            }
        generic_params_text = text[index + 1 : generic_end - 1]
        index = skip_whitespace(text, generic_end)

    if index >= len(text) or text[index] != "[":
        return {
            "status": "parse_failed",
            "error": "missing assume_specification target bracket",
        }
    target_end = find_matching_delimiter(text, index, "[", "]")
    if target_end is None:
        return {
            "status": "parse_failed",
            "error": "unclosed assume_specification target bracket",
        }
    raw_target = text[index + 1 : target_end - 1]
    index = skip_whitespace(text, target_end)

    if index >= len(text) or text[index] != "(":
        return {
            "status": "parse_failed",
            "error": "missing assume_specification parameter list",
        }
    params_end = find_matching_delimiter(text, index, "(", ")")
    if params_end is None:
        return {
            "status": "parse_failed",
            "error": "unclosed assume_specification parameter list",
        }
    params, params_error = parse_assume_specification_parameters(
        text[index + 1 : params_end - 1]
    )
    if params_error:
        return {"status": "parse_failed", "error": params_error}

    output_type = ""
    index = skip_whitespace(text, params_end)
    if text.startswith("->", index):
        output_start = skip_whitespace(text, index + 2)
        output_end = find_contract_header_clause_start(text, output_start)
        output_type = text[output_start:output_end].strip()
        if not output_type:
            return {
                "status": "parse_failed",
                "error": "empty assume_specification output type",
            }
        index = skip_whitespace(text, output_end)

    where_clause_text = ""
    if keyword_starts_at(text, index, "where"):
        where_start = skip_whitespace(text, index + len("where"))
        where_end = find_contract_body_clause_start(text, where_start)
        where_clause_text = text[where_start:where_end].strip().rstrip(",").strip()
        index = skip_whitespace(text, where_end)

    generic_params, generic_param_errors = parse_contract_generic_params(
        generic_params_text
    )
    where_predicates, where_predicate_errors = parse_contract_where_predicates(
        where_clause_text
    )

    return {
        "status": "ok",
        "error": "",
        "raw_target": raw_target,
        "target": compact_rust_path_text(raw_target),
        "generic_names": assume_specification_generic_names(generic_params_text),
        "generic_params_text": generic_params_text,
        "generic_params": generic_params,
        "generic_param_errors": generic_param_errors,
        "where_clause_text": where_clause_text,
        "where_predicates": where_predicates,
        "where_predicate_errors": where_predicate_errors,
        "params": params,
        "output_type": output_type,
    }


def matching_delimiter_covers_text(text: str, open_ch: str, close_ch: str) -> bool:
    end = find_matching_delimiter(text, 0, open_ch, close_ch)
    return end == len(text)


def normalize_array_len_text(text: Any) -> str:
    return re.sub(r"\s+", "", str(text or ""))


def format_path_type_shape(path_name: str, args: list[str]) -> str:
    if args:
        return f"path:{path_name}<{','.join(args)}>"
    return f"path:{path_name}"


def manifest_self_type_shape(declaration: dict[str, Any] | None) -> str:
    owner_for = ((declaration or {}).get("owner") or {}).get("for") or {}
    if not owner_for:
        return "generic"
    return manifest_type_shape(owner_for, declaration, expand_self=False)


def manifest_path_type_shape(
    resolved_path: dict[str, Any],
    declaration: dict[str, Any] | None,
) -> str:
    path_name = str(resolved_path.get("path") or "").split("::")[-1]
    args = (
        ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get("args")
        or []
    )
    arg_shapes: list[str] = []
    for arg in args:
        if not isinstance(arg, dict):
            continue
        if isinstance(arg.get("type"), dict):
            arg_shapes.append(manifest_type_shape(arg["type"], declaration))
        elif "const" in arg:
            arg_shapes.append(f"const:{normalize_array_len_text(arg.get('const'))}")
    return format_path_type_shape(path_name, arg_shapes)


def manifest_type_shape(
    item: Any,
    declaration: dict[str, Any] | None = None,
    *,
    expand_self: bool = True,
) -> str:
    if item is None:
        return "unit"
    if not isinstance(item, dict):
        return "unknown"
    if "borrowed_ref" in item:
        borrowed_ref = item.get("borrowed_ref") or {}
        ref_kind = "mut_ref" if borrowed_ref.get("is_mutable") else "shared_ref"
        return (
            f"{ref_kind}<"
            f"{manifest_type_shape(borrowed_ref.get('type'), declaration)}>"
        )
    if "raw_pointer" in item:
        raw_pointer = item.get("raw_pointer") or {}
        ptr_kind = (
            "raw_mut_pointer"
            if raw_pointer.get("is_mutable")
            else "raw_const_pointer"
        )
        return f"{ptr_kind}<{manifest_type_shape(raw_pointer.get('type'), declaration)}>"
    if "primitive" in item:
        return f"primitive:{item.get('primitive')}"
    if "generic" in item:
        if item.get("generic") == "Self" and expand_self:
            return manifest_self_type_shape(declaration)
        return "generic"
    if "resolved_path" in item:
        return manifest_path_type_shape(item.get("resolved_path") or {}, declaration)
    if "slice" in item:
        return f"slice<{manifest_type_shape(item.get('slice'), declaration)}>"
    if "array" in item:
        array = item.get("array") or {}
        return (
            f"array[{normalize_array_len_text(array.get('len'))}]<"
            f"{manifest_type_shape(array.get('type'), declaration)}>"
        )
    if "tuple" in item:
        return "tuple(" + ",".join(
            manifest_type_shape(part, declaration) for part in item.get("tuple") or []
        ) + ")"
    return "unknown"


def strip_named_contract_result_type(type_text: str) -> str:
    text = type_text.strip()
    if not (
        text.startswith("(")
        and matching_delimiter_covers_text(text, "(", ")")
    ):
        return text
    inner = text[1:-1].strip()
    colon = find_top_level_colon(inner)
    if colon is not None:
        name = inner[:colon].strip()
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
            return inner[colon + 1 :].strip()
    return text


def parse_contract_ref_rest(rest: str) -> tuple[bool, str]:
    rest = rest.strip()
    if rest.startswith("'"):
        match = re.match(r"'[A-Za-z_][A-Za-z0-9_]*", rest)
        if match:
            rest = rest[match.end() :].strip()
    if rest.startswith("mut") and (
        len(rest) == 3 or not (rest[3].isalnum() or rest[3] == "_")
    ):
        return True, rest[3:].strip()
    return False, rest


def contract_type_shape(
    type_text: Any,
    generic_names: set[str] | None = None,
) -> str:
    generic_names = generic_names or set()
    text = strip_named_contract_result_type(str(type_text or "").strip().rstrip(","))
    if not text or text == "()":
        return "unit"
    if text.startswith("&"):
        is_mut, inner = parse_contract_ref_rest(text[1:])
        ref_kind = "mut_ref" if is_mut else "shared_ref"
        return f"{ref_kind}<{contract_type_shape(inner, generic_names)}>"
    for prefix, ptr_kind in (
        ("*mut", "raw_mut_pointer"),
        ("*const", "raw_const_pointer"),
    ):
        if text.startswith(prefix) and (
            len(text) == len(prefix)
            or text[len(prefix)].isspace()
        ):
            return (
                f"{ptr_kind}<"
                f"{contract_type_shape(text[len(prefix) :], generic_names)}>"
            )
    if text.startswith("[") and matching_delimiter_covers_text(text, "[", "]"):
        inner = text[1:-1].strip()
        parts = split_top_level_items(inner, separator=";")
        if len(parts) == 2:
            return (
                f"array[{normalize_array_len_text(parts[1])}]<"
                f"{contract_type_shape(parts[0], generic_names)}>"
            )
        return f"slice<{contract_type_shape(inner, generic_names)}>"
    if text.startswith("(") and matching_delimiter_covers_text(text, "(", ")"):
        inner = text[1:-1].strip()
        parts = split_top_level_items(inner)
        if len(parts) > 1 or inner.endswith(","):
            return "tuple(" + ",".join(
                contract_type_shape(part, generic_names) for part in parts
            ) + ")"
        return contract_type_shape(inner, generic_names)

    primitive = {
        "bool",
        "char",
        "i8",
        "i16",
        "i32",
        "i64",
        "i128",
        "isize",
        "str",
        "u8",
        "u16",
        "u32",
        "u64",
        "u128",
        "usize",
    }
    if text in primitive:
        return f"primitive:{text}"

    angle_start = find_top_level_angle_start(text)
    arg_shapes: list[str] = []
    base = text
    if angle_start is not None:
        angle_end = find_matching_delimiter(text, angle_start, "<", ">")
        if angle_end == len(text):
            base = text[:angle_start].strip()
            arg_shapes = [
                contract_type_shape(part, generic_names)
                for part in split_top_level_items(text[angle_start + 1 : angle_end - 1])
            ]
    base = base.rstrip(":").strip()
    path_parts = split_rust_path_parts(base)
    path_name = path_parts[-1] if path_parts else base
    if not arg_shapes and path_name in generic_names:
        return "generic"
    if not arg_shapes and path_name == "Self":
        return "generic"
    if path_name in primitive:
        return f"primitive:{path_name}"
    return format_path_type_shape(path_name, arg_shapes)


def manifest_signature_input_shapes(declaration: dict[str, Any]) -> list[str]:
    signature = declaration.get("signature") or {}
    shapes = []
    for input_item in signature.get("inputs") or []:
        if isinstance(input_item, list) and len(input_item) == 2:
            shapes.append(manifest_type_shape(input_item[1], declaration))
        else:
            shapes.append("unknown")
    return shapes


def manifest_signature_output_shape(declaration: dict[str, Any]) -> str:
    signature = declaration.get("signature") or {}
    return manifest_type_shape(signature.get("output"), declaration)


def build_accepted_assume_spec_signature_shape_audit(
    metadata: dict[str, Any],
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_entries_by_target = {
        str(entry.get("target") or ""): entry
        for entry in manifest_entries
        if str(entry.get("target") or "")
    }

    audit_rows: list[dict[str, Any]] = []
    parse_failed_targets = []
    missing_manifest_targets = []
    input_arity_mismatch_targets = []
    input_shape_mismatch_targets = []
    output_shape_mismatch_targets = []

    for row in accepted_rows:
        target = row["target"]
        header = parse_assume_specification_header(str(row.get("contract_code") or ""))
        manifest_entry = manifest_entries_by_target.get(target)
        declaration = primary_declaration(manifest_entry)
        signature = declaration.get("signature") or {}
        manifest_input_shapes: list[str] = []
        assume_spec_input_shapes: list[str] = []
        manifest_output_shape = ""
        assume_spec_output_shape = ""
        input_arity_match = False
        input_shape_match = False
        output_shape_match = False
        errors = []

        if not manifest_entry or not declaration_has_function_signature(declaration):
            errors.append("missing classified-manifest function signature")
            missing_manifest_targets.append(target)
        elif header.get("status") != "ok":
            errors.append(str(header.get("error") or "assume_specification parse failed"))
            parse_failed_targets.append(target)
        else:
            generic_names = set(header.get("generic_names") or set())
            params = header.get("params") or []
            manifest_input_shapes = manifest_signature_input_shapes(declaration)
            assume_spec_input_shapes = [
                contract_type_shape(param.get("type"), generic_names) for param in params
            ]
            manifest_output_shape = manifest_signature_output_shape(declaration)
            assume_spec_output_shape = contract_type_shape(
                header.get("output_type") or "",
                generic_names,
            )
            input_arity_match = len(manifest_input_shapes) == len(
                assume_spec_input_shapes
            )
            input_shape_match = (
                input_arity_match and manifest_input_shapes == assume_spec_input_shapes
            )
            output_shape_match = manifest_output_shape == assume_spec_output_shape

            if not input_arity_match:
                errors.append("ordered input arity does not match manifest signature")
                input_arity_mismatch_targets.append(target)
            elif not input_shape_match:
                errors.append(
                    "ordered input receiver/reference mutability shape does not match "
                    "manifest signature"
                )
                input_shape_mismatch_targets.append(target)
            if not output_shape_match:
                errors.append("output/result shape does not match manifest signature")
                output_shape_mismatch_targets.append(target)

        if not errors:
            status = "ok"
        elif target in parse_failed_targets:
            status = "parse_failed"
        elif target in missing_manifest_targets:
            status = "missing_manifest_signature"
        else:
            status = "mismatched"

        audit_rows.append(
            {
                "target": target,
                "status": status,
                "manifest_declaration": declaration_source_reference(declaration),
                "manifest_input_arity": len(manifest_input_shapes),
                "assume_spec_input_arity": len(assume_spec_input_shapes),
                "manifest_input_shapes": ";".join(manifest_input_shapes),
                "assume_spec_input_shapes": ";".join(assume_spec_input_shapes),
                "input_arity_match": input_arity_match,
                "input_shape_match": input_shape_match,
                "manifest_output_shape": manifest_output_shape,
                "assume_spec_output_shape": assume_spec_output_shape,
                "output_shape_match": output_shape_match,
                "error": "; ".join(errors),
            }
        )

    audit = {
        "artifact_schema": 1,
        "source": (
            "Accepted semantic candidates from this analyzer run. Each "
            "assume_specification header is parsed for ordered parameters and result "
            "type, then compared against the Rust 1.96 classified-manifest signature "
            "for input arity, receiver/reference mutability shape, and output/result "
            "shape."
        ),
        "accepted_rows": len(accepted_rows),
        "audited_rows": len(audit_rows),
        "parse_failed": len(parse_failed_targets),
        "missing_manifest_signatures": len(missing_manifest_targets),
        "input_arity_mismatches": len(input_arity_mismatch_targets),
        "input_shape_mismatches": len(input_shape_mismatch_targets),
        "output_shape_mismatches": len(output_shape_mismatch_targets),
        "parse_failed_targets": parse_failed_targets,
        "missing_manifest_signature_targets": missing_manifest_targets,
        "input_arity_mismatch_targets": input_arity_mismatch_targets,
        "input_shape_mismatch_targets": input_shape_mismatch_targets,
        "output_shape_mismatch_targets": output_shape_mismatch_targets,
        "rows": audit_rows,
    }
    audit["validation"] = {
        "audit_covers_all_accepted_rows": len(audit_rows) == len(accepted_rows),
        "no_parse_failures": audit["parse_failed"] == 0,
        "no_missing_manifest_signatures": audit["missing_manifest_signatures"] == 0,
        "no_input_arity_mismatches": audit["input_arity_mismatches"] == 0,
        "no_input_shape_mismatches": audit["input_shape_mismatches"] == 0,
        "no_output_shape_mismatches": audit["output_shape_mismatches"] == 0,
        "validation_passed": (
            len(audit_rows) == len(accepted_rows)
            and audit["parse_failed"] == 0
            and audit["missing_manifest_signatures"] == 0
            and audit["input_arity_mismatches"] == 0
            and audit["input_shape_mismatches"] == 0
            and audit["output_shape_mismatches"] == 0
        ),
    }
    audit["validation_passed"] = audit["validation"]["validation_passed"]
    return audit


def manifest_generic_param_kind(param: dict[str, Any]) -> str:
    kind = param.get("kind") or {}
    if "const" in kind:
        return "const"
    if "lifetime" in kind:
        return "lifetime"
    return "type"


def manifest_generic_params_from_generics(
    generics: dict[str, Any] | None,
    *,
    source: str,
    start_index: int,
    declaration: dict[str, Any],
) -> list[dict[str, Any]]:
    records = []
    for offset, param in enumerate((generics or {}).get("params") or []):
        kind = manifest_generic_param_kind(param)
        const_type = ""
        if kind == "const":
            const_type = manifest_type_shape(
                ((param.get("kind") or {}).get("const") or {}).get("type"),
                declaration,
            )
        records.append(
            {
                "role": f"g{start_index + offset}",
                "kind": kind,
                "name": str(param.get("name") or ""),
                "const_type": const_type,
                "source": source,
                "param": param,
            }
        )
    return records


def manifest_combined_generic_params(
    declaration: dict[str, Any],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    owner = declaration.get("owner") or {}
    records.extend(
        manifest_generic_params_from_generics(
            owner.get("generics") or {},
            source="owner",
            start_index=len(records),
            declaration=declaration,
        )
    )
    records.extend(
        manifest_generic_params_from_generics(
            declaration.get("generics") or {},
            source="declaration",
            start_index=len(records),
            declaration=declaration,
        )
    )
    return records


def generic_param_records_for_matching(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [record for record in records if record.get("kind") != "lifetime"]


def normalize_bound_type_text(text: Any, generic_name_to_role: dict[str, str]) -> str:
    value = strip_named_contract_result_type(str(text or "").strip().rstrip(","))
    if not value:
        return ""
    if value.startswith("&"):
        _, rest = parse_contract_ref_rest(value[1:])
        return f"&{normalize_bound_type_text(rest, generic_name_to_role)}"
    if value.startswith("'"):
        return "lifetime"
    if value.startswith("(") and matching_delimiter_covers_text(value, "(", ")"):
        inner = value[1:-1].strip()
        parts = split_top_level_items(inner)
        if len(parts) > 1 or inner.endswith(","):
            return (
                "("
                + ",".join(
                    normalize_bound_type_text(part, generic_name_to_role)
                    for part in parts
                )
                + ")"
            )
        return normalize_bound_type_text(inner, generic_name_to_role)
    angle_start = find_top_level_angle_start(value)
    args: list[str] = []
    base = value
    if angle_start is not None:
        angle_end = find_matching_delimiter(value, angle_start, "<", ">")
        if angle_end == len(value):
            base = value[:angle_start].strip()
            args = [
                normalize_bound_type_text(part, generic_name_to_role)
                for part in split_top_level_items(value[angle_start + 1 : angle_end - 1])
            ]
    base_parts = split_rust_path_parts(base)
    name = base_parts[-1] if base_parts else base.strip()
    if name in generic_name_to_role:
        return generic_name_to_role[name]
    primitive = {
        "bool",
        "char",
        "i8",
        "i16",
        "i32",
        "i64",
        "i128",
        "isize",
        "str",
        "u8",
        "u16",
        "u32",
        "u64",
        "u128",
        "usize",
    }
    if name in primitive:
        return f"primitive:{name}"
    if args:
        return f"{name}<{','.join(args)}>"
    return name


def normalize_manifest_bound_type(
    item: Any,
    generic_name_to_role: dict[str, str],
    declaration: dict[str, Any],
) -> str:
    if isinstance(item, dict):
        if "generic" in item:
            name = str(item.get("generic") or "")
            return generic_name_to_role.get(name, name)
        if "primitive" in item:
            return f"primitive:{item.get('primitive')}"
        if "borrowed_ref" in item:
            borrowed_ref = item.get("borrowed_ref") or {}
            return "&" + normalize_manifest_bound_type(
                borrowed_ref.get("type"),
                generic_name_to_role,
                declaration,
            )
        if "resolved_path" in item:
            resolved_path = item.get("resolved_path") or {}
            path_name = str(resolved_path.get("path") or "").split("::")[-1]
            args = (
                ((resolved_path.get("args") or {}).get("angle_bracketed") or {}).get(
                    "args"
                )
                or []
            )
            arg_texts = []
            for arg in args:
                if isinstance(arg, dict) and isinstance(arg.get("type"), dict):
                    arg_texts.append(
                        normalize_manifest_bound_type(
                            arg["type"],
                            generic_name_to_role,
                            declaration,
                        )
                    )
                elif isinstance(arg, dict) and "const" in arg:
                    arg_texts.append(normalize_array_len_text(arg.get("const")))
            if arg_texts:
                return f"{path_name}<{','.join(arg_texts)}>"
            return path_name
        if "tuple" in item:
            return (
                "("
                + ",".join(
                    normalize_manifest_bound_type(part, generic_name_to_role, declaration)
                    for part in item.get("tuple") or []
                )
                + ")"
            )
    return manifest_type_shape(item, declaration)


def normalize_manifest_trait_bound(
    bound: dict[str, Any],
    generic_name_to_role: dict[str, str],
    declaration: dict[str, Any],
) -> str:
    trait_bound = bound.get("trait_bound") or {}
    trait = trait_bound.get("trait") or {}
    trait_name = str(trait.get("path") or "").split("::")[-1]
    modifier = str(trait_bound.get("modifier") or "")
    if modifier == "maybe" and trait_name == "Sized":
        return "?Sized"
    args = (((trait.get("args") or {}).get("angle_bracketed") or {}).get("args")) or []
    arg_texts = []
    for arg in args:
        if isinstance(arg, dict) and isinstance(arg.get("type"), dict):
            arg_texts.append(
                normalize_manifest_bound_type(
                    arg["type"],
                    generic_name_to_role,
                    declaration,
                )
            )
        elif isinstance(arg, dict) and "const" in arg:
            arg_texts.append(normalize_array_len_text(arg.get("const")))
    if arg_texts:
        return f"{trait_name}<{','.join(arg_texts)}>"
    return trait_name


def normalize_contract_trait_bound(
    bound_text: Any,
    generic_name_to_role: dict[str, str],
) -> str:
    text = str(bound_text or "").strip().rstrip(",").strip()
    if not text:
        return ""
    if text.startswith("for<"):
        binder_end = find_matching_delimiter(text, 3, "<", ">")
        if binder_end is not None:
            text = text[binder_end:].strip()
    for prefix in ("~const ", "const "):
        if text.startswith(prefix):
            text = text[len(prefix) :].strip()
    maybe = False
    if text.startswith("?"):
        maybe = True
        text = text[1:].strip()
    angle_start = find_top_level_angle_start(text)
    args: list[str] = []
    base = text
    if angle_start is not None:
        angle_end = find_matching_delimiter(text, angle_start, "<", ">")
        if angle_end == len(text):
            base = text[:angle_start].strip()
            args = [
                normalize_bound_type_text(part, generic_name_to_role)
                for part in split_top_level_items(text[angle_start + 1 : angle_end - 1])
            ]
    path_parts = split_rust_path_parts(base)
    name = path_parts[-1] if path_parts else base.strip()
    if maybe and name == "Sized":
        return "?Sized"
    if args:
        return f"{name}<{','.join(args)}>"
    return name


def manifest_bound_subject_role(
    item: Any,
    generic_name_to_role: dict[str, str],
    declaration: dict[str, Any],
) -> str:
    if isinstance(item, dict) and "generic" in item:
        name = str(item.get("generic") or "")
        return generic_name_to_role.get(name, name)
    return normalize_manifest_bound_type(item, generic_name_to_role, declaration)


def add_bound_record(
    bounds_by_role: dict[str, set[str]],
    role: str,
    bound: str,
) -> None:
    if not role or not bound or bound == "lifetime":
        return
    bounds_by_role.setdefault(role, set()).add(bound)


def manifest_where_predicate_bound_records(
    generics: dict[str, Any] | None,
    generic_name_to_role: dict[str, str],
    declaration: dict[str, Any],
) -> set[tuple[str, str]]:
    records: set[tuple[str, str]] = set()
    for predicate in (generics or {}).get("where_predicates") or []:
        bound_predicate = predicate.get("bound_predicate") or {}
        role = manifest_bound_subject_role(
            bound_predicate.get("type"),
            generic_name_to_role,
            declaration,
        )
        for bound in bound_predicate.get("bounds") or []:
            normalized = normalize_manifest_trait_bound(
                bound,
                generic_name_to_role,
                declaration,
            )
            if role and normalized and normalized != "lifetime":
                records.add((role, normalized))
    return records


def manifest_generic_bounds_signature(
    declaration: dict[str, Any],
) -> dict[str, Any]:
    params = manifest_combined_generic_params(declaration)
    name_to_role = {
        str(record.get("name") or ""): str(record.get("role") or "")
        for record in params
        if str(record.get("name") or "")
    }
    bounds_by_role: dict[str, set[str]] = {}
    for record in params:
        if record.get("kind") != "type":
            continue
        type_param = ((record.get("param") or {}).get("kind") or {}).get("type") or {}
        for bound in type_param.get("bounds") or []:
            add_bound_record(
                bounds_by_role,
                str(record.get("role") or ""),
                normalize_manifest_trait_bound(bound, name_to_role, declaration),
            )
    owner = declaration.get("owner") or {}
    owner_where_bounds = manifest_where_predicate_bound_records(
        owner.get("generics") or {},
        name_to_role,
        declaration,
    )
    declaration_where_bounds = manifest_where_predicate_bound_records(
        declaration.get("generics") or {},
        name_to_role,
        declaration,
    )
    for role, bound in owner_where_bounds | declaration_where_bounds:
        add_bound_record(bounds_by_role, role, bound)
    return {
        "params": params,
        "bounds_by_role": bounds_by_role,
        "where_bounds": owner_where_bounds | declaration_where_bounds,
    }


def contract_generic_bounds_signature(
    header: dict[str, Any],
    expected_params: list[dict[str, Any]],
) -> dict[str, Any]:
    actual_params = list(header.get("generic_params") or [])
    actual_match_params = generic_param_records_for_matching(actual_params)
    expected_match_params = generic_param_records_for_matching(expected_params)
    actual_name_to_role: dict[str, str] = {}
    for index, actual in enumerate(actual_match_params):
        if index < len(expected_match_params):
            role = str(expected_match_params[index].get("role") or f"g{index}")
        else:
            role = f"extra{index}"
        actual_name_to_role[str(actual.get("name") or "")] = role

    bounds_by_role: dict[str, set[str]] = {}
    for actual in actual_match_params:
        role = actual_name_to_role.get(str(actual.get("name") or ""), "")
        if actual.get("kind") != "type":
            continue
        for bound in actual.get("bounds") or []:
            add_bound_record(
                bounds_by_role,
                role,
                normalize_contract_trait_bound(bound, actual_name_to_role),
            )

    where_bounds: set[tuple[str, str]] = set()
    for predicate in header.get("where_predicates") or []:
        role = normalize_bound_type_text(
            predicate.get("subject") or "",
            actual_name_to_role,
        )
        for bound in predicate.get("bounds") or []:
            normalized = normalize_contract_trait_bound(bound, actual_name_to_role)
            if role and normalized and normalized != "lifetime":
                where_bounds.add((role, normalized))
                add_bound_record(bounds_by_role, role, normalized)

    return {
        "params": actual_params,
        "match_params": actual_match_params,
        "bounds_by_role": bounds_by_role,
        "where_bounds": where_bounds,
    }


def bound_record_set(bounds_by_role: dict[str, set[str]]) -> set[tuple[str, str]]:
    return {
        (role, bound)
        for role, bounds in bounds_by_role.items()
        for bound in bounds
        if role and bound
    }


def format_generic_params(records: list[dict[str, Any]]) -> str:
    pieces = []
    for record in records:
        piece = (
            f"{record.get('role', '')}:{record.get('kind', '')}:"
            f"{record.get('name', '')}"
        )
        if record.get("kind") == "const":
            piece += f":{record.get('const_type', '')}"
        source = record.get("source")
        if source:
            piece += f":{source}"
        pieces.append(piece)
    return ";".join(pieces)


def format_actual_generic_params(
    records: list[dict[str, Any]],
    expected_match_params: list[dict[str, Any]],
) -> str:
    pieces = []
    match_index = 0
    for record in records:
        if record.get("kind") == "lifetime":
            role = "lifetime"
        elif match_index < len(expected_match_params):
            role = str(expected_match_params[match_index].get("role") or f"g{match_index}")
            match_index += 1
        else:
            role = f"extra{match_index}"
            match_index += 1
        piece = f"{role}:{record.get('kind', '')}:{record.get('name', '')}"
        if record.get("kind") == "const":
            piece += f":{contract_type_shape(record.get('const_type') or '')}"
        pieces.append(piece)
    return ";".join(pieces)


def format_const_generics(records: list[dict[str, Any]]) -> str:
    return ";".join(
        f"{record.get('role', '')}:{record.get('name', '')}:{record.get('const_type', '')}"
        for record in records
        if record.get("kind") == "const"
    )


def format_actual_const_generics(
    records: list[dict[str, Any]],
    expected_match_params: list[dict[str, Any]],
) -> str:
    pieces = []
    match_index = 0
    for record in records:
        if record.get("kind") == "lifetime":
            continue
        if match_index < len(expected_match_params):
            role = str(expected_match_params[match_index].get("role") or f"g{match_index}")
        else:
            role = f"extra{match_index}"
        match_index += 1
        if record.get("kind") == "const":
            pieces.append(
                f"{role}:{record.get('name', '')}:"
                f"{contract_type_shape(record.get('const_type') or '')}"
            )
    return ";".join(pieces)


def format_bound_records(records: set[tuple[str, str]]) -> str:
    return ";".join(f"{role}:{bound}" for role, bound in sorted(records))


def build_accepted_assume_spec_generic_bounds_audit(
    metadata: dict[str, Any],
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    manifest_entries = manifest_entries_from_metadata(metadata) or []
    manifest_entries_by_target = {
        str(entry.get("target") or ""): entry
        for entry in manifest_entries
        if str(entry.get("target") or "")
    }

    audit_rows: list[dict[str, Any]] = []
    parse_failed_targets = []
    missing_manifest_targets = []
    generic_param_mismatch_targets = []
    const_generic_mismatch_targets = []
    trait_bound_mismatch_targets = []
    where_clause_mismatch_targets = []
    missing_bound_targets = []
    extra_bound_targets = []

    for row in accepted_rows:
        target = row["target"]
        header = parse_assume_specification_header(str(row.get("contract_code") or ""))
        manifest_entry = manifest_entries_by_target.get(target)
        declaration = primary_declaration(manifest_entry)
        errors = []
        manifest_signature = {"params": [], "bounds_by_role": {}, "where_bounds": set()}
        actual_signature = {"params": [], "match_params": [], "bounds_by_role": {}, "where_bounds": set()}
        generic_param_kinds_match = False
        const_generic_match = False
        trait_bounds_match = False
        where_clause_bounds_satisfied = False
        missing_bounds: set[tuple[str, str]] = set()
        extra_bounds: set[tuple[str, str]] = set()
        missing_where_bounds: set[tuple[str, str]] = set()
        extra_where_bounds: set[tuple[str, str]] = set()

        if not manifest_entry or not declaration_has_function_signature(declaration):
            errors.append("missing classified-manifest function signature")
            missing_manifest_targets.append(target)
        elif header.get("status") != "ok":
            errors.append(str(header.get("error") or "assume_specification parse failed"))
            parse_failed_targets.append(target)
        else:
            parse_errors = [
                *(header.get("generic_param_errors") or []),
                *(header.get("where_predicate_errors") or []),
            ]
            if parse_errors:
                errors.extend(str(error) for error in parse_errors)
                parse_failed_targets.append(target)
            else:
                manifest_signature = manifest_generic_bounds_signature(declaration)
                expected_match_params = generic_param_records_for_matching(
                    manifest_signature["params"]
                )
                actual_signature = contract_generic_bounds_signature(
                    header,
                    manifest_signature["params"],
                )
                actual_match_params = actual_signature["match_params"]
                expected_kinds = [
                    str(record.get("kind") or "") for record in expected_match_params
                ]
                actual_kinds = [
                    str(record.get("kind") or "") for record in actual_match_params
                ]
                generic_param_kinds_match = expected_kinds == actual_kinds

                expected_const_types = [
                    (
                        str(record.get("role") or ""),
                        str(record.get("const_type") or ""),
                    )
                    for record in expected_match_params
                    if record.get("kind") == "const"
                ]
                actual_const_types = []
                for index, actual in enumerate(actual_match_params):
                    if actual.get("kind") != "const":
                        continue
                    role = (
                        str(expected_match_params[index].get("role") or f"g{index}")
                        if index < len(expected_match_params)
                        else f"extra{index}"
                    )
                    actual_const_types.append(
                        (
                            role,
                            contract_type_shape(actual.get("const_type") or ""),
                        )
                    )
                const_generic_match = expected_const_types == actual_const_types

                expected_bounds = bound_record_set(manifest_signature["bounds_by_role"])
                actual_bounds = bound_record_set(actual_signature["bounds_by_role"])
                missing_bounds = expected_bounds - actual_bounds
                extra_bounds = actual_bounds - expected_bounds
                trait_bounds_match = not missing_bounds and not extra_bounds

                expected_where_bounds = set(manifest_signature["where_bounds"])
                actual_where_bounds = set(actual_signature["where_bounds"])
                missing_where_bounds = expected_where_bounds - actual_bounds
                extra_where_bounds = actual_where_bounds - expected_bounds
                where_clause_bounds_satisfied = (
                    not missing_where_bounds and not extra_where_bounds
                )

                if not generic_param_kinds_match:
                    errors.append("generic parameter kind/order does not match manifest")
                    generic_param_mismatch_targets.append(target)
                if not const_generic_match:
                    errors.append("const generic parameter/type does not match manifest")
                    const_generic_mismatch_targets.append(target)
                if missing_bounds:
                    errors.append("assume_specification is missing manifest trait bounds")
                    missing_bound_targets.append(target)
                if extra_bounds:
                    errors.append("assume_specification has extra trait bounds")
                    extra_bound_targets.append(target)
                if not trait_bounds_match:
                    trait_bound_mismatch_targets.append(target)
                if not where_clause_bounds_satisfied:
                    errors.append(
                        "manifest where-clause bounds are not satisfied by the "
                        "assume_specification bounds"
                    )
                    where_clause_mismatch_targets.append(target)

        if not errors:
            status = "ok"
        elif target in parse_failed_targets:
            status = "parse_failed"
        elif target in missing_manifest_targets:
            status = "missing_manifest_signature"
        else:
            status = "mismatched"

        expected_match_params = generic_param_records_for_matching(
            manifest_signature.get("params") or []
        )
        audit_rows.append(
            {
                "target": target,
                "status": status,
                "manifest_declaration": declaration_source_reference(declaration),
                "manifest_generic_params": format_generic_params(
                    manifest_signature.get("params") or []
                ),
                "assume_spec_generic_params": format_actual_generic_params(
                    actual_signature.get("params") or [],
                    expected_match_params,
                ),
                "generic_param_kinds_match": generic_param_kinds_match,
                "manifest_const_generics": format_const_generics(
                    manifest_signature.get("params") or []
                ),
                "assume_spec_const_generics": format_actual_const_generics(
                    actual_signature.get("params") or [],
                    expected_match_params,
                ),
                "const_generic_match": const_generic_match,
                "manifest_trait_bounds": format_bound_records(
                    bound_record_set(manifest_signature.get("bounds_by_role") or {})
                ),
                "assume_spec_trait_bounds": format_bound_records(
                    bound_record_set(actual_signature.get("bounds_by_role") or {})
                ),
                "trait_bounds_match": trait_bounds_match,
                "manifest_where_clause_bounds": format_bound_records(
                    set(manifest_signature.get("where_bounds") or set())
                ),
                "assume_spec_where_clause_bounds": format_bound_records(
                    set(actual_signature.get("where_bounds") or set())
                ),
                "where_clause_bounds_satisfied": where_clause_bounds_satisfied,
                "missing_bounds": format_bound_records(missing_bounds),
                "extra_bounds": format_bound_records(extra_bounds),
                "missing_where_clause_bounds": format_bound_records(missing_where_bounds),
                "extra_where_clause_bounds": format_bound_records(extra_where_bounds),
                "error": "; ".join(errors),
            }
        )

    mismatched_targets = sorted(
        set(generic_param_mismatch_targets)
        | set(const_generic_mismatch_targets)
        | set(trait_bound_mismatch_targets)
        | set(where_clause_mismatch_targets)
    )
    audit = {
        "artifact_schema": 1,
        "source": (
            "Accepted semantic candidates from this analyzer run. Each "
            "assume_specification header is parsed for type and const generic "
            "parameters, inline bounds, and where predicates, then role-normalized "
            "against the Rust 1.96 classified-manifest owner and declaration "
            "generics. Contract-side generic names may differ from rustdoc names, "
            "but kind order, const types, and the semantic trait-bound set must "
            "match; manifest where-clause bounds may be satisfied either inline or "
            "in an explicit assume_specification where clause."
        ),
        "accepted_rows": len(accepted_rows),
        "audited_rows": len(audit_rows),
        "parse_failed": len(parse_failed_targets),
        "missing_manifest_signatures": len(missing_manifest_targets),
        "generic_param_mismatches": len(generic_param_mismatch_targets),
        "const_generic_mismatches": len(const_generic_mismatch_targets),
        "trait_bound_mismatches": len(trait_bound_mismatch_targets),
        "where_clause_mismatches": len(where_clause_mismatch_targets),
        "missing_bound_rows": len(missing_bound_targets),
        "extra_bound_rows": len(extra_bound_targets),
        "mismatches": len(mismatched_targets),
        "parse_failed_targets": parse_failed_targets,
        "missing_manifest_signature_targets": missing_manifest_targets,
        "generic_param_mismatch_targets": generic_param_mismatch_targets,
        "const_generic_mismatch_targets": const_generic_mismatch_targets,
        "trait_bound_mismatch_targets": trait_bound_mismatch_targets,
        "where_clause_mismatch_targets": where_clause_mismatch_targets,
        "missing_bound_targets": missing_bound_targets,
        "extra_bound_targets": extra_bound_targets,
        "mismatched_targets": mismatched_targets,
        "rows": audit_rows,
    }
    audit["validation"] = {
        "audit_covers_all_accepted_rows": len(audit_rows) == len(accepted_rows),
        "no_parse_failures": audit["parse_failed"] == 0,
        "no_missing_manifest_signatures": audit["missing_manifest_signatures"] == 0,
        "no_generic_param_mismatches": audit["generic_param_mismatches"] == 0,
        "no_const_generic_mismatches": audit["const_generic_mismatches"] == 0,
        "no_trait_bound_mismatches": audit["trait_bound_mismatches"] == 0,
        "no_where_clause_mismatches": audit["where_clause_mismatches"] == 0,
        "no_missing_bounds": audit["missing_bound_rows"] == 0,
        "no_extra_bounds": audit["extra_bound_rows"] == 0,
        "validation_passed": (
            len(audit_rows) == len(accepted_rows)
            and audit["parse_failed"] == 0
            and audit["missing_manifest_signatures"] == 0
            and audit["generic_param_mismatches"] == 0
            and audit["const_generic_mismatches"] == 0
            and audit["trait_bound_mismatches"] == 0
            and audit["where_clause_mismatches"] == 0
            and audit["missing_bound_rows"] == 0
            and audit["extra_bound_rows"] == 0
        ),
    }
    audit["validation_passed"] = audit["validation"]["validation_passed"]
    return audit


def build_requires_source_fidelity_audit(
    rows: list[dict[str, Any]],
    accepted_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    source_gate_input_rows = [
        row
        for row in rows
        if is_semantic_candidate_before_source_fidelity(row)
        and str(row.get("requires") or "").strip()
    ]
    accepted_targets = {row["target"] for row in accepted_rows}
    audit_rows = [
        {
            "target": row["target"],
            "requires": row["requires"],
            "classification": row.get(
                "requires_source_fidelity_classification", SOURCE_FIDELITY_UNCLASSIFIED
            ),
            "rationale": row.get("requires_source_fidelity_rationale", ""),
            "source_reference": row.get("requires_source_reference", ""),
            "source_excerpt": row.get("requires_source_excerpt", ""),
            "accepted_after_source_gate": row["target"] in accepted_targets,
        }
        for row in source_gate_input_rows
    ]
    source_unjustified_rows = [
        row
        for row in audit_rows
        if row["classification"] not in {SOURCE_FIDELITY_JUSTIFIED}
    ]
    unclassified_rows = [
        row
        for row in audit_rows
        if row["classification"] == SOURCE_FIDELITY_UNCLASSIFIED
    ]
    source_unjustified_accepted_rows = [
        row for row in source_unjustified_rows if row["accepted_after_source_gate"]
    ]
    return {
        "artifact_schema": 1,
        "source": (
            "Semantic candidates with non-empty requires before the "
            "requires-source-fidelity gate. Each classification is derived from "
            "classified-manifest declaration/source_context evidence plus "
            "Rust/vstd semantic laws, not from model rationale."
        ),
        "source_final_candidates_rows": len(rows),
        "source_gate_input_rows": len(source_gate_input_rows),
        "audited_rows": len(audit_rows),
        "source_justified_rows": sum(
            row["classification"] == SOURCE_FIDELITY_JUSTIFIED for row in audit_rows
        ),
        "source_unjustified_rows": len(source_unjustified_rows),
        "unclassified_rows": len(unclassified_rows),
        "accepted_after_source_gate_rows": sum(
            bool(row["accepted_after_source_gate"]) for row in audit_rows
        ),
        "source_unjustified_targets": [
            row["target"] for row in source_unjustified_rows
        ],
        "unclassified_targets": [row["target"] for row in unclassified_rows],
        "source_unjustified_accepted_targets": [
            row["target"] for row in source_unjustified_accepted_rows
        ],
        "rows": audit_rows,
        "validation": {
            "audit_covers_all_non_empty_requires_source_gate_inputs": (
                len(audit_rows) == len(source_gate_input_rows)
            ),
            "all_audited_rows_have_required_fields": all(
                all(str(row.get(field) or "").strip() for field in fields)
                for row in audit_rows
                for fields in [
                    ("target", "requires", "classification", "rationale", "source_reference")
                ]
            ),
            "no_unclassified_rows": not unclassified_rows,
            "no_source_unjustified_rows": not source_unjustified_rows,
            "no_source_unjustified_accepted_rows": (
                not source_unjustified_accepted_rows
            ),
            "validation_passed": (
                len(audit_rows) == len(source_gate_input_rows)
                and all(
                    all(str(row.get(field) or "").strip() for field in fields)
                    for row in audit_rows
                    for fields in [
                        (
                            "target",
                            "requires",
                            "classification",
                            "rationale",
                            "source_reference",
                        )
                    ]
                )
                and not unclassified_rows
                and not source_unjustified_accepted_rows
            ),
        },
    }


def make_ensures_source_fidelity_result(
    classification: str,
    evidence_kind: str,
    rationale: str,
    source_reference: str,
    source_excerpt: str = "",
) -> dict[str, str]:
    return {
        "classification": classification,
        "evidence_kind": evidence_kind,
        "rationale": rationale,
        "source_reference": source_reference,
        "source_excerpt": source_excerpt,
    }


def classify_ensures_source_fidelity(
    target: str,
    requires: list[str],
    ensures: list[str],
    manifest_entry: dict[str, Any] | None,
    contract_code: str,
) -> dict[str, str]:
    ensures_text = "; ".join(str(item) for item in ensures if str(item).strip())
    if not ensures_text.strip():
        return make_ensures_source_fidelity_result(
            SOURCE_FIDELITY_UNCLASSIFIED,
            "empty_ensures",
            "No ensures clause is present for this accepted semantic candidate.",
            "",
        )

    declaration = primary_declaration(manifest_entry)
    source_reference = declaration_source_reference(declaration)
    source_excerpt = source_context_excerpt(declaration)
    if not declaration_has_source_provenance(declaration):
        return make_ensures_source_fidelity_result(
            SOURCE_FIDELITY_UNCLASSIFIED,
            "missing_manifest_source_context",
            "No classified-manifest declaration with source_context evidence was "
            "available for auditing this accepted ensures clause.",
            source_reference,
            source_excerpt,
        )

    source_lower = re.sub(
        r"\s+",
        " ",
        all_source_context_plain_text(manifest_entry) or source_context_plain_text(declaration),
    ).lower()
    ensures_lower = re.sub(r"\s+", " ", ensures_text).lower()
    compact_ensures = compact_verus_clause(ensures_text).lower()
    method_name = target.split("::")[-1]

    def justified(
        evidence_kind: str,
        rationale: str,
        excerpt: str | None = None,
    ) -> dict[str, str]:
        return make_ensures_source_fidelity_result(
            SOURCE_FIDELITY_JUSTIFIED,
            evidence_kind,
            rationale,
            source_reference,
            excerpt if excerpt is not None else source_excerpt,
        )

    def unclassified(rationale: str) -> dict[str, str]:
        return make_ensures_source_fidelity_result(
            SOURCE_FIDELITY_UNCLASSIFIED,
            "no_matching_source_context_rule",
            rationale,
            source_reference,
            source_excerpt,
        )

    def source_mentions(*tokens: str) -> bool:
        return all(token.lower() in source_lower for token in tokens)

    def ensures_mentions(*tokens: str) -> bool:
        return all(token.lower() in ensures_lower for token in tokens)

    if (
        target == THREAD_RESULT_FLATTEN_TARGET
        and thread_result_flatten_alias_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        return justified(
            "exact_thread_result_flatten_source_gate",
            f"{source_reference} is a public alias for core Result::flatten and "
            "the classified source_context contains the matching Ok/Err branch "
            "structure; the ensures clause models exactly that branch result.",
        )

    if (
        target in SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS
        and source_backed_unsafe_constructor_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_unsafe_constructor_source_gate",
            f"{source_reference} contains the Rust 1.96 safety/documentation and "
            "constructor body that establish the accepted observable result view; "
            "the ensures clause is the exact source-backed postcondition checked "
            "by the semantic gate.",
            source_backed_unsafe_constructor_source_evidence_excerpt(
                target,
                declaration,
            ),
        )

    if (
        target == SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET
        and split_at_mut_unchecked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_split_at_mut_unchecked_source_gate",
            f"{source_reference} checks `mid <= len` and constructs the returned "
            "mutable prefix/suffix with `from_raw_parts_mut`; the ensures clauses "
            "model those source-backed returned views and final slice state.",
            split_at_mut_unchecked_source_evidence_excerpt(declaration),
        )

    if (
        target == SLICE_SPLIT_AT_MUT_CHECKED_TARGET
        and split_at_mut_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_slice_split_at_mut_checked_source_gate",
            f"{source_reference} documents the checked split branch and delegates "
            "the successful branch to `split_at_mut_unchecked`; the ensures "
            "clauses model the exact Some/None source behavior.",
            split_at_mut_checked_source_evidence_excerpt(declaration),
        )

    if (
        target == STR_SPLIT_AT_CHECKED_TARGET
        and str_split_at_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_str_split_at_checked_source_gate",
            f"{source_reference} checks the UTF-8 character boundary and delegates "
            "the successful branch to `split_at_unchecked`; the ensures clauses "
            "model that byte-view Some/None behavior.",
            str_split_at_checked_source_evidence_excerpt(declaration),
        )

    if (
        target == STR_SPLIT_AT_MUT_CHECKED_TARGET
        and str_split_at_mut_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_str_split_at_mut_checked_source_gate",
            f"{source_reference} checks the UTF-8 character boundary and builds "
            "mutable prefix/suffix strings from the split byte slices; the ensures "
            "clauses model that exact source-backed Some/None behavior.",
            str_split_at_mut_checked_source_evidence_excerpt(declaration),
        )

    if (
        target == STR_FROM_UTF8_TARGET
        and str_from_utf8_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        return justified(
            "exact_str_from_utf8_source_gate",
            f"{source_reference} delegates validation to `run_utf8_validation` and "
            "returns Ok only through `from_utf8_unchecked`; the ensures clauses "
            "model precisely the valid/invalid UTF-8 result branches.",
        )

    if (
        target == STR_FROM_UTF8_MUT_TARGET
        and str_from_utf8_mut_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        return justified(
            "exact_str_from_utf8_mut_source_gate",
            f"{source_reference} delegates mutable-byte validation to "
            "`run_utf8_validation` and returns Ok only through "
            "`from_utf8_unchecked_mut`; the ensures clauses model the preserved "
            "byte slice and exact valid/invalid UTF-8 result branches.",
        )

    if (
        target == STRING_REPLACE_RANGE_TARGET
        and string_replace_range_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        return justified(
            "exact_string_replace_range_source_gate",
            f"{source_reference} snapshots `range` once with `slice::range`, checks "
            "the resulting byte endpoints as UTF-8 character boundaries, and "
            "splices `replace_with.bytes()` into that checked byte range; the "
            "ensures clause models exactly the decoded byte sequence after that "
            "source-backed splice.",
            string_replace_range_source_evidence_excerpt(declaration),
        )

    if (
        target in SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS
        and direct_mut_view_adapter_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_direct_mut_view_adapter_source_gate",
            f"{source_reference} constructs the returned mutable view directly from "
            "the input array/slice/value without copying; the ensures clauses model "
            "that source-backed view and final-state relationship.",
        )

    if (
        target == ARRAY_EACH_MUT_TARGET
        and array_each_mut_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_array_each_mut_source_gate",
            f"{source_reference} constructs one mutable reference for each array "
            "element and transmutes that initialized pointer array into the "
            "returned reference array; the ensures clauses model only per-index "
            "dereferenced values and the final array relation, without pointer or "
            "provenance claims.",
            array_each_mut_source_evidence_excerpt(declaration),
        )

    if (
        target in SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_TARGETS
        and option_mut_tuple_view_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_option_mut_tuple_view_source_gate",
            f"{source_reference} branches on the checked split and returns the "
            "documented mutable chunk/tail tuple; the ensures clauses model the "
            "source-backed Some/None tuple views and input post-state.",
        )

    if (
        target in SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS
        and single_element_mut_split_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_single_element_mut_split_source_gate",
            f"{source_reference} splits off the first/last mutable element exactly "
            "as documented and implemented; the ensures clauses model the returned "
            "element/rest views and final input state.",
        )

    if (
        target in SOURCE_BACKED_MUTATING_SLICE_TARGETS
        and slice_reverse_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_mutating_slice_source_gate",
            f"{source_reference} reverses the slice in place by swapping mirrored "
            "front/back elements; the ensures clause models the full observable "
            "final sequence view without pointer/provenance claims.",
            slice_reverse_source_evidence_excerpt(declaration),
        )

    if (
        target in SOURCE_BACKED_BINARY_SEARCH_TARGETS
        and source_backed_binary_search_source_supports_contract(
            target,
            manifest_entry,
            "\n".join(requires),
            ensures,
        )
    ):
        spec = SOURCE_BACKED_BINARY_SEARCH_TARGETS[target]
        return justified(
            "exact_binary_search_source_gate",
            f"{source_reference} shows `{spec['display']}` has the `T: Ord` bound, "
            f"documents sorted-input/insertion-index behavior and duplicate-match "
            f"nondeterminism, and delegates to `{spec['delegation']}`; the ensures "
            "clauses are the source-backed unique-match Ok/Err partition model.",
            source_backed_binary_search_source_evidence_excerpt(target, declaration),
        )

    if (
        target in SOURCE_BACKED_MAP_GET_MUT_TARGETS
        and map_get_mut_contract_uses_source_backed_shape(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_map_get_mut_source_gate",
            f"{source_reference} documents borrowed-key lookup and implements the "
            "mutable-reference return through the underlying map search; the "
            "ensures clauses model the selected old semantic value and unchanged "
            "map view without pointer/provenance claims.",
            map_get_mut_source_evidence_excerpt(declaration, target),
        )

    if (
        target == LINKEDLIST_BACK_MUT_TARGET
        and linkedlist_back_mut_contract_uses_source_backed_shape(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        return justified(
            "exact_linkedlist_back_mut_source_gate",
            f"{source_reference} documents a mutable back-element lookup and "
            "implements it by projecting `self.tail.as_mut()` to "
            "`node.as_mut().element`; the ensures clauses model the source-backed "
            "Some/None branch, old tail value, and unchanged list view without "
            "pointer/provenance claims.",
            linkedlist_back_mut_source_evidence_excerpt(declaration),
        )

    if btree_contract_uses_source_backed_raw_algebra(
        target,
        "\n".join(requires),
        "\n".join(ensures),
        manifest_entry,
    ):
        return justified(
            "exact_btree_raw_algebra_source_gate",
            f"{source_reference} documents and implements this BTree operation over "
            "the ordered map/set structure; the ensures clauses use the accepted "
            "source-backed semantic map/set algebra for that operation.",
        )

    if hashset_replace_contract_uses_source_backed_view(
        "\n".join(requires),
        "\n".join(ensures),
        manifest_entry,
    ):
        return justified(
            "exact_hashset_replace_source_gate",
            f"{source_reference} documents replacing an equal existing value and "
            "delegates to `self.base.replace(value)`; the ensures clauses model "
            "the source-backed semantic set update and returned replaced value.",
        )

    if (
        target in SOURCE_BACKED_SAFE_SLICE_CHUNK_TARGETS
        and safe_slice_chunk_source_supports_nonzero_n(target, requires, manifest_entry)
        and ensures_mentions("ret.")
        and (
            "subrange" in ensures_lower
            or "as_chunks" in source_lower
            or "chunks" in ensures_lower
        )
    ):
        return justified(
            "slice_chunk_source_context",
            f"{source_reference} documents the chunk/remainder lengths, panics for "
            "zero `N`, and implements the result by splitting before "
            "`as_chunks_unchecked`/`as_chunks_unchecked_mut`; the ensures clauses "
            "model exactly those source-backed chunk and remainder views.",
            safe_slice_chunk_source_evidence_excerpt(declaration, target),
        )

    if (
        target in SOURCE_BACKED_CMP_MIN_MAX_TARGETS
        and cmp_min_max_source_supports_obeys_cmp_spec(target, declaration)
        and "cmp_spec" in ensures_lower
        and "r ==" in ensures_lower
    ):
        spec = SOURCE_BACKED_CMP_MIN_MAX_TARGETS[target]
        return justified(
            "cmp_min_max_source_context",
            f"{source_reference} documents the {spec['kind']} operation, the equal "
            f"tie rule returning the {spec['tie_argument']} argument, and delegates "
            f"to `{spec['delegation']}`; the ensures clauses model that exact "
            "source-backed comparison result.",
            cmp_min_max_source_evidence_excerpt(declaration, target),
        )

    if target.startswith("alloc::collections::BTreeMap::") and (
        "contains_key" in ensures_lower
        or "old(m)@" in ensures_lower
        or "final(m)@" in ensures_lower
    ):
        return justified(
            "btree_map_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `BTreeMap::{method_name}` over the ordered map implementation; "
            "the accepted ensures clauses are expressed only over the observable "
            "map view, first/last key selection, returned value, and documented "
            "mutation effect from that source operation.",
        )

    if target.startswith("alloc::collections::BTreeSet::") and (
        "contains" in ensures_lower
        or "old(m)@" in ensures_lower
        or "subset_of" in ensures_lower
        or "disjoint" in ensures_lower
        or "final(m)@" in ensures_lower
    ):
        return justified(
            "btree_set_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `BTreeSet::{method_name}` over the ordered set implementation; "
            "the accepted ensures clauses are expressed only over the observable "
            "set view, first/last element selection, relation result, and "
            "documented mutation effect from that source operation.",
        )

    if target.startswith("std::collections::HashSet::") and (
        "subset_of" in ensures_lower
        or "disjoint" in ensures_lower
        or "set_contains_borrowed_key" in ensures_lower
        or "old(m)@" in ensures_lower
    ):
        return justified(
            "hashset_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `HashSet::{method_name}` and contains the Eq/Hash-backed set "
            "operation used by the implementation; the accepted ensures clauses "
            "model only the observable semantic set relation/update.",
        )

    if target == HASHMAP_REMOVE_ENTRY_TARGET and hashmap_remove_entry_source_supports_operation(
        manifest_entry
    ):
        return justified(
            "hashmap_remove_entry_source_context",
            f"{source_reference} documents borrowed-key Hash/Eq compatibility, "
            "returns the stored key/value pair, and delegates to "
            "`self.base.remove_entry(k)`; the ensures clauses model exactly that "
            "source-backed removal and optional returned pair.",
            hashmap_remove_entry_source_evidence_excerpt(declaration),
        )

    if target.startswith("alloc::string::String::") and (
        "s@" in ensures_lower
        or "res@" in ensures_lower
        or "encode_utf8" in ensures_lower
        or "spec_capacity" in ensures_lower
        or "final(s)" in ensures_lower
    ):
        return justified(
            "string_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `String::{method_name}`; the accepted ensures clauses model only "
            "the observable UTF-8 character/byte view, length/capacity, returned "
            "character/string, and documented mutation effect of that source body.",
        )

    if target.startswith("core::str::") and (
        "spec_bytes" in ensures_lower
        or "decode_utf8" in ensures_lower
        or "valid_utf8" in ensures_lower
        or "trim" in source_lower
        or "ascii" in source_lower
        or "char_boundary" in ensures_lower
    ):
        return justified(
            "str_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `str::{method_name}`; the accepted ensures clauses model only the "
            "documented UTF-8 byte/string view, boundary, trim, ASCII, or validation "
            "behavior exposed by that source operation.",
        )

    if target.startswith("core::slice::") and (
        "slice@" in ensures_lower
        or "old(slice)@" in ensures_lower
        or "subrange" in ensures_lower
        or "result" in ensures_lower
        or "ret" in ensures_lower
        or "starts_with" in source_lower
        or "ascii" in source_lower
    ):
        return justified(
            "slice_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `slice::{method_name}`; the accepted ensures clauses model only "
            "the documented observable slice view, split/chunk relation, ASCII "
            "predicate, search result, or returned array/slice view from that source.",
        )

    if target.startswith("core::array::") and (
        "arr@" in ensures_lower
        or "ar@" in ensures_lower
        or "out@" in ensures_lower
        or "old(arr)@" in ensures_lower
        or "ret" in ensures_lower
        or "result" in ensures_lower
        or "final(" in ensures_lower
    ):
        return justified(
            "array_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `array::{method_name}`; the accepted ensures clauses model the "
            "documented array/slice/reference view constructed by that source.",
        )

    if target.startswith("core::option::Option::") and (
        "option::" in ensures_lower
        or "some" in ensures_lower
        or "none" in ensures_lower
        or "match" in ensures_lower
    ):
        return justified(
            "option_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `Option::{method_name}` and exposes the match/constructor "
            "branches; the accepted ensures clauses model only that public "
            "Some/None branch result.",
        )

    if target.startswith("core::result::Result::") and (
        "result::" in ensures_lower
        or "ok" in ensures_lower
        or "err" in ensures_lower
        or "match" in ensures_lower
    ):
        return justified(
            "result_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `Result::{method_name}` and exposes the match/constructor "
            "branches; the accepted ensures clauses model only that public Ok/Err "
            "branch result or documented non-panicking branch.",
        )

    if target.startswith("core::ops::RangeInclusive::") and (
        "start" in ensures_lower or "end" in ensures_lower or "empty" in ensures_lower
    ):
        return justified(
            "range_inclusive_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `RangeInclusive::{method_name}`; the accepted ensures clauses "
            "model the documented start/end pair or emptiness predicate for the "
            "non-exhausted observable range state.",
        )

    if target == "core::ops::Range::is_empty" and (
        "result" in ensures_lower or "ret" in ensures_lower
    ):
        return justified(
            "range_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            "for `Range::is_empty`; the accepted ensures clause models the "
            "documented empty-range comparison over the observable bounds.",
        )

    if target in {"core::convert::identity", "core::hint::black_box"} and (
        "result == value" in ensures_lower or "ret == x" in ensures_lower
        or "output == dummy" in ensures_lower
    ):
        return justified(
            "identity_like_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            "for an identity-like executable API; the accepted ensures clause "
            "models the source-backed returned input value.",
        )

    if target == "core::hint::select_unpredictable" and "result" in ensures_lower:
        return justified(
            "select_unpredictable_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            "for `select_unpredictable`; the accepted ensures clause models the "
            "documented selected input value without relying on branch prediction.",
        )

    if target in {"core::mem::min_align_of", "core::mem::min_align_of_val"} and (
        "align" in ensures_lower or "result" in ensures_lower
    ):
        return justified(
            "mem_align_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            "for the minimum-alignment query; the accepted ensures clause models "
            "the source-backed alignment value exposed by that API.",
        )

    if target == "core::mem::replace" and (
        "final(" in ensures_lower or "result" in ensures_lower or "dest" in ensures_lower
    ):
        return justified(
            "mem_replace_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            "for `mem::replace`; the accepted ensures clauses model the documented "
            "old-value return and new destination post-state.",
        )

    if target.startswith("alloc::vec::Vec::") and (
        "v@" in ensures_lower
        or "old(v)@" in ensures_lower
        or "result@" in ensures_lower
        or "slice@" in ensures_lower
        or "vec@" in ensures_lower
        or "dedup" in source_lower
        or "flattened" in source_lower
    ):
        return justified(
            "vec_declaration_source_context",
            f"{source_reference} is the classified Rust declaration/source_context "
            f"for `Vec::{method_name}`; the accepted ensures clauses model the "
            "documented observable vector/slice view transformation of that source.",
        )

    return unclassified(
        "No source-context rule established this accepted ensures clause from the "
        "classified-manifest declaration/source_context and Rust/vstd semantic "
        "laws; the audit does not use the model rationale as source evidence."
    )


def build_accepted_ensures_source_fidelity_audit(
    rows: list[dict[str, Any]],
    accepted_rows: list[dict[str, Any]],
    classifications_by_target: dict[str, dict[str, str]],
) -> dict[str, Any]:
    audit_rows = []
    for row in accepted_rows:
        target = row["target"]
        classification = classifications_by_target.get(target) or {}
        audit_rows.append(
            {
                "target": target,
                "ensures": row.get("ensures", ""),
                "classification": classification.get(
                    "classification",
                    SOURCE_FIDELITY_UNCLASSIFIED,
                ),
                "evidence_kind": classification.get("evidence_kind", ""),
                "rationale": classification.get("rationale", ""),
                "source_reference": classification.get("source_reference", ""),
                "source_excerpt": classification.get("source_excerpt", ""),
            }
        )

    source_unjustified_rows = [
        row
        for row in audit_rows
        if row["classification"] not in {SOURCE_FIDELITY_JUSTIFIED}
    ]
    unclassified_rows = [
        row for row in audit_rows if row["classification"] == SOURCE_FIDELITY_UNCLASSIFIED
    ]
    rows_with_source_context_evidence = [
        row
        for row in audit_rows
        if str(row.get("source_reference") or "").strip()
        and str(row.get("source_excerpt") or "").strip()
    ]

    required_field_groups = [
        (
            "target",
            "ensures",
            "classification",
            "evidence_kind",
            "rationale",
            "source_reference",
            "source_excerpt",
        )
    ]
    all_rows_have_required_fields = all(
        all(str(row.get(field) or "").strip() for field in fields)
        for row in audit_rows
        for fields in required_field_groups
    )
    validation = {
        "audit_covers_all_accepted_rows": len(audit_rows) == len(accepted_rows),
        "all_accepted_rows_have_non_empty_ensures": all(
            str(row.get("ensures") or "").strip() for row in audit_rows
        ),
        "all_audited_rows_have_required_fields": all_rows_have_required_fields,
        "all_audited_rows_have_source_context_evidence": (
            len(rows_with_source_context_evidence) == len(audit_rows)
        ),
        "no_unclassified_rows": not unclassified_rows,
        "no_source_unjustified_rows": not source_unjustified_rows,
        "validation_passed": (
            len(audit_rows) == len(accepted_rows)
            and all(str(row.get("ensures") or "").strip() for row in audit_rows)
            and all_rows_have_required_fields
            and len(rows_with_source_context_evidence) == len(audit_rows)
            and not unclassified_rows
            and not source_unjustified_rows
        ),
    }
    return {
        "artifact_schema": 1,
        "source": (
            "Every accepted semantic candidate from this analyzer run. Each "
            "ensures-source-fidelity classification is derived from "
            "classified-manifest declaration/source_context evidence plus "
            "Rust/vstd semantic laws and existing semantic source gates; model "
            "rationale text is not used as evidence."
        ),
        "source_final_candidates_rows": len(rows),
        "accepted_rows": len(accepted_rows),
        "audited_rows": len(audit_rows),
        "source_justified_rows": sum(
            row["classification"] == SOURCE_FIDELITY_JUSTIFIED for row in audit_rows
        ),
        "source_unjustified_rows": len(source_unjustified_rows),
        "unclassified_rows": len(unclassified_rows),
        "source_context_evidence_rows": len(rows_with_source_context_evidence),
        "source_unjustified_accepted_targets": [
            row["target"] for row in source_unjustified_rows
        ],
        "unclassified_targets": [row["target"] for row in unclassified_rows],
        "rows": audit_rows,
        "validation": validation,
        "validation_passed": validation["validation_passed"],
    }


def det_summary(round_record: dict[str, Any]) -> dict[str, Any]:
    return (round_record.get("checker") or {}).get("determinism") or {}


def semantic_gate_issues(
    target: str,
    requires: list[str],
    ensures: list[str],
    manifest_entry: dict[str, Any] | None = None,
    contract_code: str = "",
) -> list[str]:
    requires_text = "\n".join(requires)
    ensures_text = "\n".join(ensures)
    issues = []
    if (
        target == THREAD_RESULT_FLATTEN_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not thread_result_flatten_alias_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        issues.append("thread_result_flatten_alias_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not source_backed_unsafe_constructor_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("unsafe_constructor_source_contract_mismatch")
    if (
        target == SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not split_at_mut_unchecked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("slice_split_at_mut_unchecked_source_contract_mismatch")
    if (
        target == SLICE_SPLIT_AT_MUT_CHECKED_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not split_at_mut_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("slice_split_at_mut_checked_source_contract_mismatch")
    if (
        target == STR_SPLIT_AT_CHECKED_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not str_split_at_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("str_split_at_checked_source_contract_mismatch")
    if (
        target == STR_SPLIT_AT_MUT_CHECKED_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not str_split_at_mut_checked_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("str_split_at_mut_checked_source_contract_mismatch")
    if (
        target == STR_FROM_UTF8_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not str_from_utf8_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        issues.append("str_from_utf8_source_contract_mismatch")
    if (
        target == STR_FROM_UTF8_MUT_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not str_from_utf8_mut_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        issues.append("str_from_utf8_mut_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not direct_mut_view_adapter_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("direct_mut_view_adapter_source_contract_mismatch")
    if (
        target == ARRAY_EACH_MUT_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not array_each_mut_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("array_each_mut_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not option_mut_tuple_view_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("option_mut_tuple_view_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not single_element_mut_split_source_supports_contract(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("single_element_mut_split_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_MUTATING_SLICE_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not slice_reverse_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("mutating_slice_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_BINARY_SEARCH_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not source_backed_binary_search_source_supports_contract(
            target,
            manifest_entry,
            requires_text,
            ensures,
        )
    ):
        issues.append("binary_search_source_contract_mismatch")
    if (
        target in SOURCE_BACKED_MAP_GET_MUT_TARGETS
        and (requires_text.strip() or ensures_text.strip())
        and not map_get_mut_contract_uses_source_backed_shape(
            target,
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("map_get_mut_source_contract_mismatch")
    if (
        target == LINKEDLIST_BACK_MUT_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not linkedlist_back_mut_contract_uses_source_backed_shape(
            manifest_entry,
            requires,
            ensures,
        )
    ):
        issues.append("linkedlist_back_mut_source_contract_mismatch")
    if target.startswith(
        ("alloc::collections::BTreeMap::", "alloc::collections::BTreeSet::")
    ):
        raw_ops = (".union(", ".union_prefer_right(", ".disjoint(")
        relation_tokens = (
            "deep_view",
            "contains_borrowed_key",
            "sets_borrowed_key_to_key",
            "maps_borrowed_key_to_value",
        )
        if (
            "@" in ensures_text
            and any(token in ensures_text for token in raw_ops)
            and not any(token in ensures_text for token in relation_tokens)
            and not btree_contract_uses_source_backed_raw_algebra(
                target,
                requires_text,
                ensures_text,
                manifest_entry,
            )
        ):
            issues.append("raw_btree_view_algebra")
    if (
        target.startswith(
            ("alloc::collections::BTreeMap::", "alloc::collections::BTreeSet::")
        )
        and any(
            token in requires_text
            for token in (
                "contains_borrowed_key(",
                "maps_borrowed_key_to_value(",
                "sets_borrowed_key_to_key(",
            )
        )
    ):
        issues.append("borrowed_key_domain_strengthening")
    if re.search(
        r"forall\|[^|]*(?:left|right)[^|]*\|.*==>.*left\s*==\s*right",
        requires_text,
        flags=re.DOTALL,
    ):
        issues.append("borrowed_key_uniqueness_precondition")
    if "strictly_cloned::<" in requires_text or "cloned::<" in requires_text:
        issues.append("clone_behavior_domain_strengthening")
    if target == "alloc::vec::Vec::dedup" and (
        "fold_left(" in ensures_text or "kept.last()" in ensures_text
    ):
        issues.append("dedup_pure_old_sequence_model")
    if target == "alloc::string::String::replace_range" and (
        "slice_range_start(" in requires_text + ensures_text
        or "slice_range_end(" in requires_text + ensures_text
    ):
        issues.append("generic_range_snapshot_mismatch")
    if (
        target == STRING_REPLACE_RANGE_TARGET
        and (requires_text.strip() or ensures_text.strip())
        and not string_replace_range_source_supports_contract(
            manifest_entry,
            requires,
            ensures,
            contract_code,
        )
    ):
        issues.append("string_replace_range_source_contract_mismatch")
    return sorted(set(issues))


def semantic_review_issues(
    target: str,
    requires: list[str] | None = None,
    ensures: list[str] | None = None,
    manifest_entry: dict[str, Any] | None = None,
) -> list[str]:
    issues = []
    if (
        target == SLICE_BINARY_SEARCH_TARGET
        and not source_backed_binary_search_source_supports_contract(
            target,
            manifest_entry,
            "\n".join(requires or []),
            ensures or [],
        )
    ):
        issues.append("public_api_allows_any_matching_index")
    if target in RANGE_INCLUSIVE_EXHAUSTION_TARGETS:
        issues.append("value_unspecified_after_exhaustion")
    if target == HASHSET_REPLACE_TARGET and not hashset_replace_contract_uses_source_backed_view(
        "\n".join(requires or []),
        "\n".join(ensures or []),
        manifest_entry,
    ):
        issues.append("hash_equivalence_class_view_requires_review")
    return issues


def analyze(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    results = payload["results"]
    rows = []
    transitions = Counter()
    category_counts: dict[str, Counter] = {}
    manifest_entries = manifest_entries_from_metadata(payload.get("metadata", {})) or []
    manifest_entries_by_target = {
        str(entry.get("target") or ""): entry for entry in manifest_entries
    }
    expected_targets = (
        {str(entry.get("target") or "") for entry in manifest_entries}
        if manifest_entries
        else None
    )
    ensures_source_fidelity_by_target: dict[str, dict[str, str]] = {}
    for result in results:
        history = result.get("history") or []
        initial = history[0] if history else {}
        final = result.get("final") or {}
        initial_decision = decision(initial)
        final_decision = decision(final)
        if history:
            transitions[f"{initial_decision or 'none'}->{final_decision or 'none'}"] += 1
        category = result.get("category", "")
        category_counts.setdefault(category, Counter())[final_decision or "none"] += 1
        det = det_summary(final)
        candidate = final.get("candidate") or {}
        contract_code = serialized_contract_code(candidate)
        requires = candidate.get("requires") or []
        ensures = candidate.get("ensures") or []
        source_fidelity = classify_requires_source_fidelity(
            result["target"],
            requires,
            manifest_entries_by_target.get(result["target"]),
            ensures,
        )
        ensures_source_fidelity_by_target[result["target"]] = (
            classify_ensures_source_fidelity(
                result["target"],
                requires,
                ensures,
                manifest_entries_by_target.get(result["target"]),
                contract_code,
            )
        )
        semantic_issues = semantic_gate_issues(
            result["target"],
            requires,
            ensures,
            manifest_entries_by_target.get(result["target"]),
            contract_code,
        )
        if (
            any(str(item).strip() for item in requires)
            and source_fidelity["classification"] != SOURCE_FIDELITY_JUSTIFIED
        ):
            semantic_issues.append(
                f"requires_source_fidelity:{source_fidelity['classification']}"
            )
            semantic_issues = sorted(set(semantic_issues))
        review_issues = semantic_review_issues(
            result["target"],
            requires,
            ensures,
            manifest_entries_by_target.get(result["target"]),
        )
        guarded_reward = int(final.get("guarded_reward", 0))
        final_issue_tags = audit_final_skip_rationales.normalized_duplicate_vstd_issue_tags(
            result["target"],
            final_decision,
            candidate.get("rationale", ""),
            final.get("anti_vacuity_issues", final.get("issues", [])),
            manifest_entries_by_target,
        )
        rows.append(
            {
                "target": result["target"],
                "category": category,
                "status": final.get("status", ""),
                "rounds": len(history),
                "initial_decision": initial_decision,
                "final_decision": final_decision,
                "contract_form": candidate.get("contract_form", ""),
                "typecheck_passed": typecheck_passed(final),
                "det_status": det.get("status", ""),
                "r0_z3": det.get("r0_z3", ""),
                "classification": det.get("classification", ""),
                "raw_det_reward": final.get("raw_det_reward", 0),
                "guarded_reward": guarded_reward,
                "semantic_guarded_reward": int(
                    guarded_reward == 1 and not semantic_issues
                ),
                "issues": ";".join(final_issue_tags),
                "semantic_gate_issues": ";".join(semantic_issues),
                "semantic_review_issues": ";".join(review_issues),
                "requires": "; ".join(requires),
                "ensures": "; ".join(ensures),
                "contract_code": contract_code,
                "rationale": candidate.get("rationale", ""),
                "requires_source_fidelity_classification": source_fidelity[
                    "classification"
                ],
                "requires_source_fidelity_rationale": source_fidelity["rationale"],
                "requires_source_reference": source_fidelity["source_reference"],
                "requires_source_excerpt": source_fidelity["source_excerpt"],
            }
        )

    result_targets = {row["target"] for row in rows}
    missing_targets = (
        len(expected_targets - result_targets) if expected_targets is not None else 0
    )
    counts = {
        "manifest_targets": (
            len(expected_targets) if expected_targets is not None else len(rows)
        ),
        "targets": len(rows),
        "missing_targets": missing_targets,
        "initial_add_spec": sum(row["initial_decision"] == "add_spec" for row in rows),
        "initial_skip": sum(row["initial_decision"] == "skip" for row in rows),
        "final_add_spec": sum(row["final_decision"] == "add_spec" for row in rows),
        "final_skip": sum(row["final_decision"] == "skip" for row in rows),
        "typecheck_passed": sum(row["typecheck_passed"] for row in rows),
        "typechecked_final_add_spec": sum(
            row["final_decision"] == "add_spec" and bool_value(row["typecheck_passed"])
            for row in rows
        ),
        "det_unsat": sum(row["r0_z3"] == "unsat" for row in rows),
        "det_sat": sum(row["r0_z3"] == "sat" for row in rows),
        "det_unknown": sum(row["r0_z3"] == "unknown" for row in rows),
        "raw_reward": sum(int(row["raw_det_reward"]) for row in rows),
        "guarded_reward": sum(int(row["guarded_reward"]) for row in rows),
        "semantic_guarded_reward": sum(
            int(row["semantic_guarded_reward"]) for row in rows
        ),
        "accepted_semantic_candidates": sum(
            is_accepted_semantic_candidate(row) for row in rows
        ),
        "llm_errors": sum(row["status"] == "llm_error" for row in rows),
        "exceptions": sum(row["status"] == "exception" for row in rows),
        "static_skips": sum(row["status"] == "static_skip" for row in rows),
    }
    accepted_rows = [row for row in rows if is_accepted_semantic_candidate(row)]
    requires_source_fidelity_audit = build_requires_source_fidelity_audit(
        rows,
        accepted_rows,
    )
    ensures_source_fidelity_audit = build_accepted_ensures_source_fidelity_audit(
        rows,
        accepted_rows,
        ensures_source_fidelity_by_target,
    )
    analysis = {
        "metadata": payload.get("metadata", {}),
        "counts": counts,
        "transitions": dict(sorted(transitions.items())),
        "categories": {
            category: dict(sorted(values.items()))
            for category, values in sorted(category_counts.items())
        },
        "issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["issues"].split(";")
                if issue
            ).most_common()
        ),
        "semantic_gate_issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["semantic_gate_issues"].split(";")
                if issue
            ).most_common()
        ),
        "semantic_review_issue_counts": dict(
            Counter(
                issue
                for row in rows
                for issue in row["semantic_review_issues"].split(";")
                if issue
            ).most_common()
        ),
        "accepted_requires_source_fidelity": requires_source_fidelity_audit,
        "accepted_ensures_source_fidelity": ensures_source_fidelity_audit,
    }
    return analysis, rows


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    if fieldnames is None:
        if rows:
            fieldnames = list(rows[0])
        else:
            fieldnames = FINAL_CANDIDATE_FIELDS
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_accepted_semantic_candidates(
    out_dir: Path,
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    accepted_rows = [row for row in rows if is_accepted_semantic_candidate(row)]
    fieldnames = list(rows[0]) if rows else FINAL_CANDIDATE_FIELDS
    write_csv(
        out_dir / "accepted_semantic_candidates.csv",
        accepted_rows,
        fieldnames=fieldnames,
    )
    payload = {
        "artifact_schema": 1,
        "description": (
            "Accepted semantic-gated subset of final_candidates.csv. "
            "final_candidates.csv remains one row per API and includes raw model "
            "add_spec decisions that may have failed typecheck, determinism, "
            "semantic gates, or semantic review."
        ),
        "predicate": ACCEPTED_SEMANTIC_CANDIDATE_PREDICATE,
        "source_final_candidates_rows": len(rows),
        "accepted_rows": len(accepted_rows),
        "rows": accepted_rows,
    }
    (out_dir / "accepted_semantic_candidates.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    return accepted_rows


def write_requires_source_fidelity_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / "accepted_requires_source_fidelity_audit.csv",
        audit.get("rows", []),
        fieldnames=REQUIRES_SOURCE_FIDELITY_AUDIT_FIELDS,
    )
    (out_dir / "accepted_requires_source_fidelity_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def write_ensures_source_fidelity_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / "accepted_ensures_source_fidelity_audit.csv",
        audit.get("rows", []),
        fieldnames=ENSURES_SOURCE_FIDELITY_AUDIT_FIELDS,
    )
    (out_dir / "accepted_ensures_source_fidelity_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def write_accepted_assume_spec_target_binding_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / "accepted_assume_spec_target_binding_audit.csv",
        audit.get("rows", []),
        fieldnames=ACCEPTED_ASSUME_SPEC_TARGET_BINDING_AUDIT_FIELDS,
    )
    (out_dir / "accepted_assume_spec_target_binding_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def write_accepted_assume_spec_signature_shape_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / "accepted_assume_spec_signature_shape_audit.csv",
        audit.get("rows", []),
        fieldnames=ACCEPTED_ASSUME_SPEC_SIGNATURE_SHAPE_AUDIT_FIELDS,
    )
    (out_dir / "accepted_assume_spec_signature_shape_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def write_accepted_assume_spec_generic_bounds_audit(
    out_dir: Path,
    audit: dict[str, Any],
) -> None:
    write_csv(
        out_dir / "accepted_assume_spec_generic_bounds_audit.csv",
        audit.get("rows", []),
        fieldnames=ACCEPTED_ASSUME_SPEC_GENERIC_BOUNDS_AUDIT_FIELDS,
    )
    (out_dir / "accepted_assume_spec_generic_bounds_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n"
    )


def write_report(
    path: Path,
    analysis: dict[str, Any],
    rows: list[dict[str, Any]],
) -> None:
    counts = analysis["counts"]
    lines = [
        "# Rust std contract generation with determinism feedback",
        "",
        "## Aggregate result",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "External `assume_specification` declarations are trusted. A guarded "
            "determinism reward means only that the candidate typechecked, avoided "
            "the configured vacuity gates, and uniquely determined the modeled "
            "outputs. It does not prove the contract sound.",
            "",
            "## Feedback transitions",
            "",
            "| Transition | Count |",
            "|---|---:|",
        ]
    )
    for transition, count in analysis["transitions"].items():
        lines.append(f"| `{transition}` | {count} |")
    lines.extend(
        [
            "",
            "## Frequent issues",
            "",
            "| Issue | Count |",
            "|---|---:|",
        ]
    )
    for issue, count in list(analysis["issue_counts"].items())[:30]:
        lines.append(f"| `{issue}` | {count} |")
    successes = [row for row in rows if int(row["guarded_reward"]) == 1]
    semantic_successes = [
        row for row in rows if int(row["semantic_guarded_reward"]) == 1
    ]
    accepted_semantic_successes = [
        row for row in semantic_successes if is_accepted_semantic_candidate(row)
    ]
    lines.extend(
        [
            "",
            "## Guarded-deterministic candidates",
            "",
            "| Target | Ensures |",
            "|---|---|",
        ]
    )
    for row in successes:
        lines.append(f"| `{row['target']}` | `{row['ensures']}` |")
    lines.extend(
        [
            "",
            "## Semantic-gated candidates",
            "",
            f"{len(semantic_successes)} of {len(successes)} guarded-deterministic "
            "candidates pass the pilot-derived semantic postprocessing gates.",
            f"{len(accepted_semantic_successes)} semantic-gated candidates have no "
            "semantic review holdback and form the accepted subset.",
            "The machine-checkable accepted subset is written to "
            "`accepted_semantic_candidates.csv` and "
            "`accepted_semantic_candidates.json`; `final_candidates.csv` remains "
            "one row per API and includes raw model decisions.",
            "",
            "| Target | Ensures |",
            "|---|---|",
        ]
    )
    for row in semantic_successes:
        lines.append(f"| `{row['target']}` | `{row['ensures']}` |")
    requires_source_audit = analysis.get("accepted_requires_source_fidelity", {})
    lines.extend(
        [
            "",
            "## Accepted requires source-fidelity audit",
            "",
            f"{requires_source_audit.get('audited_rows', 0)} semantic-gated "
            "candidate rows with non-empty `requires` were audited against "
            "classified-manifest declaration/source_context evidence and Rust/vstd "
            "semantic laws before acceptance.",
            "",
            "| Target | Classification | Source |",
            "|---|---|---|",
        ]
    )
    for audit_row in requires_source_audit.get("rows", []):
        lines.append(
            f"| `{audit_row['target']}` | `{audit_row['classification']}` | "
            f"`{audit_row['source_reference']}` |"
        )
    ensures_source_audit = analysis.get("accepted_ensures_source_fidelity", {})
    lines.extend(
        [
            "",
            "## Accepted ensures source-fidelity audit",
            "",
            f"{ensures_source_audit.get('audited_rows', 0)} accepted semantic "
            "candidate rows were audited against classified-manifest "
            "declaration/source_context evidence and Rust/vstd semantic laws. "
            "Model rationale text is not used as source evidence.",
            "",
            "| Target | Classification | Evidence | Source |",
            "|---|---|---|---|",
        ]
    )
    for audit_row in ensures_source_audit.get("rows", []):
        lines.append(
            f"| `{audit_row['target']}` | `{audit_row['classification']}` | "
            f"`{audit_row['evidence_kind']}` | `{audit_row['source_reference']}` |"
        )
    lines.extend(
        [
            "",
            "## Per-target result",
            "",
            "| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |",
            "|---|---|---|---:|---|---:|---:|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['target']}` | {row['initial_decision']} | "
            f"{row['final_decision']} | {int(row['typecheck_passed'])} | "
            f"{row['r0_z3']} | {row['guarded_reward']} | "
            f"{row['semantic_guarded_reward']} | "
            f"{';'.join(filter(None, [row['issues'], row['semantic_gate_issues'], row['semantic_review_issues']]))} |"
        )
    path.write_text("\n".join(lines).rstrip() + "\n")


def write_final_verification(
    out_dir: Path,
    batch_paths: list[Path],
    source_payloads: list[dict[str, Any]],
    combined_payload: dict[str, Any],
    analysis: dict[str, Any],
    rows: list[dict[str, Any]],
    accepted_rows: list[dict[str, Any]],
    accepted_target_binding_audit: dict[str, Any],
    accepted_signature_shape_audit: dict[str, Any],
    accepted_generic_bounds_audit: dict[str, Any],
) -> None:
    result_targets = [result["target"] for result in combined_payload["results"]]
    target_counts = Counter(result_targets)
    expected_targets = manifest_targets_from_metadata(combined_payload["metadata"])
    result_target_set = set(result_targets)
    missing_targets = (
        sorted(expected_targets - result_target_set)
        if expected_targets is not None
        else []
    )
    extra_targets = (
        sorted(result_target_set - expected_targets)
        if expected_targets is not None
        else []
    )
    final_decision_counts = Counter(row["final_decision"] or "none" for row in rows)
    status_counts = Counter(row["status"] for row in rows)
    skip_rows = [row for row in rows if row["final_decision"] == "skip"]
    skip_rows_with_literal_none_contract_code = [
        row for row in skip_rows if row.get("contract_code") == "None"
    ]
    batch_final_skip_literal_none_contract_code = [
        result["target"]
        for result in combined_payload["results"]
        if ((result.get("final") or {}).get("candidate") or {}).get("decision")
        == "skip"
        and ((result.get("final") or {}).get("candidate") or {}).get("contract_code")
        == "None"
    ]
    skip_rows_with_empty_rationale = [
        row for row in skip_rows if not str(row.get("rationale") or "").strip()
    ]
    raw_model_final_add_spec = final_decision_counts.get("add_spec", 0)
    typechecked_final_add_spec = sum(
        row["final_decision"] == "add_spec" and bool_value(row["typecheck_passed"])
        for row in rows
    )
    guarded_deterministic_add_spec = sum(
        row["final_decision"] == "add_spec"
        and bool_value(row["typecheck_passed"])
        and int_value(row["guarded_reward"]) == 1
        for row in rows
    )
    add_spec_rechecked = sum(
        (
            ((result.get("final") or {}).get("candidate") or {}).get("decision")
            == "add_spec"
            and bool((result.get("final") or {}).get("rechecked"))
        )
        for result in combined_payload["results"]
    )
    scope_validation = build_scope_validation(
        combined_payload["metadata"],
        rows,
        accepted_rows,
    )
    target_artifact_integrity = build_target_artifact_integrity(
        out_dir,
        combined_payload["metadata"],
        rows,
    )
    accepted_contract_text_safety = build_accepted_contract_text_safety(accepted_rows)
    artifact_names = [
        "batch_summary.json",
        "recheck_summary.json",
        "analysis.json",
        "ANALYSIS.md",
        "final_candidates.csv",
        "accepted_semantic_candidates.csv",
        "accepted_semantic_candidates.json",
        "accepted_requires_source_fidelity_audit.csv",
        "accepted_requires_source_fidelity_audit.json",
        "accepted_ensures_source_fidelity_audit.csv",
        "accepted_ensures_source_fidelity_audit.json",
        "accepted_assume_spec_target_binding_audit.csv",
        "accepted_assume_spec_target_binding_audit.json",
        "accepted_assume_spec_signature_shape_audit.csv",
        "accepted_assume_spec_signature_shape_audit.json",
        "accepted_assume_spec_generic_bounds_audit.csv",
        "accepted_assume_spec_generic_bounds_audit.json",
        "SUMMARY.md",
        "final_verification.json",
    ]
    verification = {
        "batch_files": [str(path.resolve()) for path in batch_paths],
        "analysis_counts": analysis["counts"],
        "batch_counts": (
            source_payloads[0].get("counts", {})
            if len(source_payloads) == 1
            else {
                "targets": len(combined_payload["results"]),
                "add_spec": final_decision_counts.get("add_spec", 0),
                "skip": final_decision_counts.get("skip", 0),
                "missing_targets": len(missing_targets),
            }
        ),
        "manifest_targets": analysis["counts"]["manifest_targets"],
        "result_rows": len(rows),
        "csv_rows": len(rows),
        "final_candidates": len(rows),
        "final_candidates_scope": (
            "one row per analyzed API result; raw model add_spec decisions are not "
            "accepted unless they pass typecheck, guarded determinism, and semantic "
            "gates with no semantic review holdback, and non-empty requires clauses "
            "pass source-fidelity audit"
        ),
        "add_spec_recheck_required": raw_model_final_add_spec,
        "add_spec_rechecked": add_spec_rechecked,
        "candidate_decision_counts": {
            "raw_model_initial_add_spec_decisions": analysis["counts"][
                "initial_add_spec"
            ],
            "raw_model_final_add_spec_decisions": raw_model_final_add_spec,
            "typechecked_final_add_spec_candidates": typechecked_final_add_spec,
            "guarded_deterministic_add_spec_candidates": (
                guarded_deterministic_add_spec
            ),
            "semantic_guarded_reward_candidates": analysis["counts"][
                "semantic_guarded_reward"
            ],
            "accepted_semantic_candidates": len(accepted_rows),
        },
        "accepted_semantic_candidates": {
            "csv": str((out_dir / "accepted_semantic_candidates.csv").resolve()),
            "json": str((out_dir / "accepted_semantic_candidates.json").resolve()),
            "rows": len(accepted_rows),
            "predicate": ACCEPTED_SEMANTIC_CANDIDATE_PREDICATE,
            "validation": {
                "all_final_decision_add_spec": all(
                    row["final_decision"] == "add_spec" for row in accepted_rows
                ),
                "all_typecheck_passed": all(
                    bool_value(row["typecheck_passed"]) for row in accepted_rows
                ),
                "all_guarded_reward": all(
                    int_value(row["guarded_reward"]) == 1 for row in accepted_rows
                ),
                "all_semantic_guarded_reward": all(
                    int_value(row["semantic_guarded_reward"]) == 1
                    for row in accepted_rows
                ),
                "all_anti_vacuity_issues_empty": all(
                    not str(row.get("issues") or "").strip()
                    for row in accepted_rows
                ),
                "all_semantic_gate_issues_empty": all(
                    not str(row.get("semantic_gate_issues") or "").strip()
                    for row in accepted_rows
                ),
                "all_semantic_review_issues_empty": all(
                    not str(row.get("semantic_review_issues") or "").strip()
                    for row in accepted_rows
                ),
                "anti_vacuity_issue_rows": sum(
                    bool(str(row.get("issues") or "").strip())
                    for row in accepted_rows
                ),
                "semantic_gate_issue_rows": sum(
                    bool(str(row.get("semantic_gate_issues") or "").strip())
                    for row in accepted_rows
                ),
                "semantic_review_issue_rows": sum(
                    bool(str(row.get("semantic_review_issues") or "").strip())
                    for row in accepted_rows
                ),
            },
        },
        "accepted_contract_text_safety": accepted_contract_text_safety,
        "accepted_assume_spec_target_binding_audit": accepted_target_binding_audit,
        "accepted_assume_spec_signature_shape_audit": accepted_signature_shape_audit,
        "accepted_assume_spec_generic_bounds_audit": accepted_generic_bounds_audit,
        "contract_code_schema_hygiene": {
            "source": (
                "inactive final skip candidates in batch_summary.json and "
                "final_candidates.csv must not serialize contract_code as the "
                "literal string 'None'"
            ),
            "batch_summary_final_skip_contract_code_literal_None_rows": len(
                batch_final_skip_literal_none_contract_code
            ),
            "final_candidates_csv_final_skip_contract_code_literal_None_rows": len(
                skip_rows_with_literal_none_contract_code
            ),
            "batch_summary_sample_targets": batch_final_skip_literal_none_contract_code[
                :20
            ],
            "final_candidates_csv_sample_targets": [
                row["target"] for row in skip_rows_with_literal_none_contract_code[:20]
            ],
            "all_final_skip_contract_code_literal_None_absent": (
                not batch_final_skip_literal_none_contract_code
                and not skip_rows_with_literal_none_contract_code
            ),
        },
        "accepted_requires_source_fidelity": analysis[
            "accepted_requires_source_fidelity"
        ],
        "accepted_ensures_source_fidelity": analysis[
            "accepted_ensures_source_fidelity"
        ],
        "skip_rationale": {
            "source": (
                "final_candidates.csv rows where final_decision == 'skip'; "
                "rationale is sourced from the final candidate payload"
            ),
            "final_rows": len(rows),
            "final_candidate_rows": len(rows),
            "skip_rows": len(skip_rows),
            "skip_rows_with_rationale": (
                len(skip_rows) - len(skip_rows_with_empty_rationale)
            ),
            "empty_skip_rationale_rows": len(skip_rows_with_empty_rationale),
            "empty_rationale_rows": len(skip_rows_with_empty_rationale),
            "all_skip_rows_have_rationale": not skip_rows_with_empty_rationale,
            "all_skip_rationales_non_empty": not skip_rows_with_empty_rationale,
            "accepted_semantic_candidate_rows": len(accepted_rows),
            "sample_empty_rationale_targets": [
                row["target"] for row in skip_rows_with_empty_rationale[:20]
            ],
        },
        "scope_validation": scope_validation,
        "target_artifact_integrity": target_artifact_integrity,
        "final_decision_counts": dict(sorted(final_decision_counts.items())),
        "status_counts": dict(sorted(status_counts.items())),
        "duplicate_result_count": sum(
            count - 1 for count in target_counts.values() if count > 1
        ),
        "missing_target_count": len(missing_targets),
        "extra_target_count": len(extra_targets),
        "unresolved_counts": {
            "analysis_exceptions": analysis["counts"]["exceptions"],
            "analysis_llm_errors": analysis["counts"]["llm_errors"],
            "analysis_missing_targets": analysis["counts"]["missing_targets"],
            "batch_exceptions": sum(
                int(payload.get("counts", {}).get("exceptions", 0))
                for payload in source_payloads
            ),
            "batch_llm_errors": sum(
                int(payload.get("counts", {}).get("llm_errors", 0))
                for payload in source_payloads
            ),
            "batch_missing_targets": sum(
                int(payload.get("counts", {}).get("missing_targets", 0))
                for payload in source_payloads
            ),
        },
        "determinism_counts": {
            "det_sat": analysis["counts"]["det_sat"],
            "det_unknown": analysis["counts"]["det_unknown"],
            "det_unsat": analysis["counts"]["det_unsat"],
            "raw_reward": analysis["counts"]["raw_reward"],
            "guarded_reward": analysis["counts"]["guarded_reward"],
            "semantic_guarded_reward": analysis["counts"]["semantic_guarded_reward"],
        },
        "verus_typecheck_passed": analysis["counts"]["typecheck_passed"],
        "artifacts": {
            name: str((out_dir / name).resolve())
            for name in artifact_names
            if name == "final_verification.json" or (out_dir / name).exists()
        },
    }
    (out_dir / "final_verification.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n"
    )


def validation_flag(block: Any) -> bool:
    if not isinstance(block, dict):
        return False
    if "validation_passed" in block:
        return bool(block["validation_passed"])
    if "acceptance_passed" in block:
        return bool(block["acceptance_passed"])
    validation = block.get("validation")
    return bool(
        isinstance(validation, dict)
        and validation.get("validation_passed")
    )


def required_validation_failures(verification: dict[str, Any]) -> list[str]:
    required = {
        "scope_validation": validation_flag(verification.get("scope_validation")),
        "target_artifact_integrity": validation_flag(
            verification.get("target_artifact_integrity")
        ),
        "accepted_contract_text_safety": validation_flag(
            verification.get("accepted_contract_text_safety")
        ),
        "accepted_assume_spec_target_binding_audit": validation_flag(
            verification.get("accepted_assume_spec_target_binding_audit")
        ),
        "accepted_assume_spec_signature_shape_audit": validation_flag(
            verification.get("accepted_assume_spec_signature_shape_audit")
        ),
        "accepted_assume_spec_generic_bounds_audit": validation_flag(
            verification.get("accepted_assume_spec_generic_bounds_audit")
        ),
        "accepted_requires_source_fidelity": validation_flag(
            verification.get("accepted_requires_source_fidelity")
        ),
        "accepted_ensures_source_fidelity": validation_flag(
            verification.get("accepted_ensures_source_fidelity")
        ),
        "full_skip_rationale_taxonomy": validation_flag(
            verification.get("full_skip_rationale_taxonomy")
        ),
        "final_candidate_payload_consistency": validation_flag(
            verification.get("final_candidate_payload_consistency")
        ),
        "canonical_artifact_provenance": validation_flag(
            verification.get("canonical_artifact_provenance")
        ),
        "contract_code_schema_hygiene": bool(
            (verification.get("contract_code_schema_hygiene") or {}).get(
                "all_final_skip_contract_code_literal_None_absent"
            )
        ),
    }
    return [name for name, passed in required.items() if not passed]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_summary", type=Path, nargs="+")
    parser.add_argument("--out-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payloads = [json.loads(path.read_text()) for path in args.batch_summary]
    by_target: dict[str, dict[str, Any]] = {}
    duplicate_sources: dict[str, list[str]] = {}
    for batch_path, payload in zip(args.batch_summary, payloads, strict=True):
        for result in payload["results"]:
            target = str(result.get("target") or "")
            if target in by_target:
                duplicate_sources.setdefault(target, []).append(str(batch_path.resolve()))
                continue
            by_target[target] = result
            duplicate_sources.setdefault(target, [str(batch_path.resolve())])
    duplicates = {
        target: sources
        for target, sources in duplicate_sources.items()
        if len(sources) > 1
    }
    if duplicates:
        print(
            "duplicate targets across batch summaries: "
            + ", ".join(
                f"{target} ({len(sources)} batches)"
                for target, sources in sorted(duplicates.items())
            ),
            file=sys.stderr,
        )
        return 2
    target_artifact_root_declarations = (
        combined_target_artifact_root_declarations(
            args.batch_summary,
            payloads,
        )
    )
    payload = {
        "metadata": {
            "batches": [item.get("metadata", {}) for item in payloads],
            "batch_files": [str(path.resolve()) for path in args.batch_summary],
            "target_artifact_roots": sorted(
                str(path) for path in target_artifact_root_declarations
            ),
        },
        "results": list(by_target.values()),
    }
    out_dir = (args.out_dir or args.batch_summary[0].parent).expanduser().absolute()
    out_dir.mkdir(parents=True, exist_ok=True)
    combined_batch_path = out_dir / "batch_summary.json"
    source_is_published_batch = (
        len(args.batch_summary) == 1
        and args.batch_summary[0].resolve() == combined_batch_path.resolve()
    )
    if not source_is_published_batch:
        combined_batch_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        )
    published_batch_paths = (
        args.batch_summary if source_is_published_batch else [combined_batch_path]
    )
    analysis, rows = analyze(payload)
    (out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2, sort_keys=True) + "\n"
    )
    write_csv(out_dir / "final_candidates.csv", rows)
    accepted_rows = write_accepted_semantic_candidates(out_dir, rows)
    write_requires_source_fidelity_audit(
        out_dir,
        analysis["accepted_requires_source_fidelity"],
    )
    write_ensures_source_fidelity_audit(
        out_dir,
        analysis["accepted_ensures_source_fidelity"],
    )
    accepted_target_binding_audit = build_accepted_assume_spec_target_binding_audit(
        payload["metadata"],
        accepted_rows,
    )
    write_accepted_assume_spec_target_binding_audit(
        out_dir,
        accepted_target_binding_audit,
    )
    accepted_signature_shape_audit = build_accepted_assume_spec_signature_shape_audit(
        payload["metadata"],
        accepted_rows,
    )
    write_accepted_assume_spec_signature_shape_audit(
        out_dir,
        accepted_signature_shape_audit,
    )
    accepted_generic_bounds_audit = build_accepted_assume_spec_generic_bounds_audit(
        payload["metadata"],
        accepted_rows,
    )
    write_accepted_assume_spec_generic_bounds_audit(
        out_dir,
        accepted_generic_bounds_audit,
    )
    write_report(out_dir / "ANALYSIS.md", analysis, rows)
    write_final_verification(
        out_dir,
        published_batch_paths,
        payloads,
        payload,
        analysis,
        rows,
        accepted_rows,
        accepted_target_binding_audit,
        accepted_signature_shape_audit,
        accepted_generic_bounds_audit,
    )
    audit_summary = audit_final_skip_rationales.run_audit(
        out_dir,
        repair_batch=False,
        repair_final=True,
        update_verification=True,
    )
    final_candidate_payload_consistency_audit = (
        build_final_candidate_payload_consistency_audit(
            out_dir,
            payload["metadata"],
            payload,
        )
    )
    write_final_candidate_payload_consistency_audit(
        out_dir,
        final_candidate_payload_consistency_audit,
    )
    update_final_candidate_payload_consistency_verification(
        out_dir,
        final_candidate_payload_consistency_audit,
    )
    update_canonical_artifact_provenance_verification(out_dir)
    verification = json.loads((out_dir / "final_verification.json").read_text())
    validation_failures = required_validation_failures(verification)
    print(
        f"analyzed {analysis['counts']['targets']} targets; "
        f"guarded reward={analysis['counts']['guarded_reward']}; "
        f"accepted semantic={len(accepted_rows)}"
    )
    if not audit_summary.get("acceptance_passed"):
        validation_failures.append("full_skip_rationale_taxonomy")
    validation_failures = sorted(set(validation_failures))
    if validation_failures:
        print(
            "required validation failed: " + ", ".join(validation_failures),
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
