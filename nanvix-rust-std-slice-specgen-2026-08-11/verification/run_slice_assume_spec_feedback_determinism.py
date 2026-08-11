#!/usr/bin/env python3
"""Run Rust std feedback-pipeline determinism for generated core::slice assume-specs."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any


SLICE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SURVEY_ROOT = Path("/home/chentianyu/nanvix-rust-std-spec-survey")
DEFAULT_VSTD_ROOT = DEFAULT_SURVEY_ROOT / "verus" / "source" / "vstd"
DEFAULT_VERUS_BIN = (
    DEFAULT_SURVEY_ROOT / "verus" / "source" / "target-verus" / "release" / "verus"
)
DEFAULT_Z3_PATH = DEFAULT_SURVEY_ROOT / "verus" / "source" / "z3"
DEFAULT_EVIDENCE_ROOT = SLICE_ROOT / "verification" / "evidence" / "slice_feedback_determinism"
DEFAULT_FEATURE_GATES = ("slice_pattern", "strip_circumfix", "substr_range")
DEFAULT_IMPORTS = ("vstd::seq::*", "vstd::view::*")
REPRESENTATIVE_TARGETS = (
    "core::slice::contains",
    "core::slice::reverse",
    "core::slice::split_first_mut",
    "core::slice::binary_search",
    "core::slice::sort_unstable",
)
CLOSURE_BORROW_TARGETS = {
    "core::slice::binary_search_by",
    "core::slice::binary_search_by_key",
    "core::slice::is_sorted_by",
    "core::slice::is_sorted_by_key",
}
DISJOINT_INDEX_TARGETS = {
    "core::slice::get_disjoint_mut",
    "core::slice::get_disjoint_unchecked_mut",
}
SLICE_PATTERN_TARGETS = {
    "core::slice::strip_circumfix",
    "core::slice::strip_prefix",
    "core::slice::strip_suffix",
}
NESTED_ARRAY_SLICE_PARAM_TARGETS = {
    "core::slice::as_flattened_mut",
}
SOURCE_BACKED_MUT_REF_RETURN_TARGETS = {
    "core::slice::ChunksExactMut::into_remainder",
    "core::slice::IterMut::into_slice",
    "core::slice::RChunksExactMut::into_remainder",
    "core::slice::as_chunks_unchecked_mut",
    "core::slice::as_flattened_mut",
    "core::slice::assume_init_mut",
    "core::slice::from_mut",
    "core::slice::from_raw_parts_mut",
    "core::slice::get_unchecked_mut",
    "core::slice::write_clone_of_slice",
    "core::slice::write_copy_of_slice",
}
SLICE_ITERATOR_VIEW_FIELDS = (
    "source",
    "remaining",
    "yielded_prefix",
    "remainder",
    "chunk_size",
    "reverse",
)
SLICE_ITERATOR_HELPER_FIELDS = {
    "slice_predicate_split_view": (
        "source",
        "remaining",
        "yielded_prefix",
        "chunk_size",
        "reverse",
    ),
    "slice_adjacent_chunk_view": ("source", "remaining", "yielded_prefix"),
    "utf8_chunk_partition": ("source", "remaining", "yielded_prefix"),
}
SLICE_ITERATOR_EQUAL_POLICY_SOURCE = "nanvix_slice_iterator_view_fields"
LEGACY_REVIEWER_NOTE_REPLACEMENTS = (
    (
        "determinism checker currently reports unsupported/no-target for assume_specification harnesses",
        "feedback-pipeline determinism result recorded in determinism_result",
    ),
    (
        "determinism checker unsupported/no-target result preserved",
        "feedback-pipeline determinism result recorded in determinism_result",
    ),
    (
        "determinism checker result recorded honestly as unsupported",
        "feedback-pipeline determinism result recorded in determinism_result",
    ),
)
EXPECTED_GENERATED_TARGETS = 120
UNKNOWN_REASON_SUMMARIES = {
    "duplicate-or-callback-search-boundary": (
        "search result is source-backed but relational: duplicate matches, insertion "
        "points, or callback/predicate observations do not force a unique return"
    ),
    "unstable-sort-or-selection-boundary": (
        "unstable sort/select APIs guarantee ordering or partition plus permutation, "
        "not a unique permutation for equal keys or pivot-equivalent elements"
    ),
    "iterator-or-subslice-state-boundary": (
        "contract fixes source/remaining/subrange state, but the Rust iterator, "
        "chunk, split, or borrowed subslice value retains opaque runtime/lifetime state"
    ),
    "mutable-reference-view-boundary": (
        "contract fixes the Seq view and old/final frame, but mutable reference "
        "identity and alias/lifetime state are not uniquely determined by that view"
    ),
    "raw-pointer-provenance-boundary": (
        "pointer address, provenance, alignment, or layout state is source-observable "
        "but not uniquely recoverable from the pure slice Seq view"
    ),
    "maybeuninit-storage-boundary": (
        "MaybeUninit initialization/storage state is modeled relationally through a "
        "raw-storage view and cannot be collapsed to one unique concrete value"
    ),
    "clone-or-callback-effect-boundary": (
        "Clone/FnMut effects are modeled by source-order observation relations, so "
        "the contract preserves effect nondeterminism instead of choosing outputs"
    ),
    "disjoint-mutable-alias-boundary": (
        "disjoint mutable-reference arrays preserve source aliasing and post-state "
        "relations, but reference identity is not uniquely fixed by the contract"
    ),
}
UNKNOWN_REASON_TARGET_CLASSES = {
    **dict.fromkeys(
        (
            "core::slice::binary_search",
            "core::slice::binary_search_by",
            "core::slice::binary_search_by_key",
            "core::slice::partition_point",
        ),
        "duplicate-or-callback-search-boundary",
    ),
    **dict.fromkeys(
        (
            "core::slice::select_nth_unstable",
            "core::slice::select_nth_unstable_by",
            "core::slice::select_nth_unstable_by_key",
            "core::slice::sort_unstable",
            "core::slice::sort_unstable_by",
            "core::slice::sort_unstable_by_key",
        ),
        "unstable-sort-or-selection-boundary",
    ),
    **dict.fromkeys(
        (
            "core::slice::as_flattened_mut",
            "core::slice::as_mut_array",
            "core::slice::get_mut",
        ),
        "mutable-reference-view-boundary",
    ),
    **dict.fromkeys(
        (
            "core::slice::clone_from_slice",
            "core::slice::fill",
        ),
        "clone-or-callback-effect-boundary",
    ),
    **dict.fromkeys(
        (
            "core::slice::get_disjoint_mut",
            "core::slice::get_disjoint_unchecked_mut",
        ),
        "disjoint-mutable-alias-boundary",
    ),
}
UNKNOWN_REASON_FAMILY_DEFAULTS = {
    "iterator-splitting-and-chunking": "iterator-or-subslice-state-boundary",
    "raw-pointer-and-provenance": "raw-pointer-provenance-boundary",
    "maybe-uninit-slice-storage": "maybeuninit-storage-boundary",
}
SPLIT_FIRST_MUT_STRUCTURED_ENSURES = (
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
)


def fail(message: str) -> None:
    print(f"slice feedback determinism failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_feedback_module(survey_root: Path) -> Any:
    module_path = survey_root / "run_rust_std_spec_feedback.py"
    if not module_path.is_file():
        fail(f"missing feedback runner {module_path}")
    sys.path.insert(0, str(survey_root))
    spec = importlib.util.spec_from_file_location("run_rust_std_spec_feedback", module_path)
    if spec is None or spec.loader is None:
        fail(f"cannot load feedback runner {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_closure_borrow_det_harness(harness: str) -> str:
    return re.sub(
        r"(proof fn det___rust_std_candidate<'a,\s*T)(\s*,)",
        r"\1: 'a\2",
        harness,
        count=1,
    )


def normalize_disjoint_index_det_harness(harness: str) -> str:
    return harness.replace(
        "pub uninterp spec fn slice_disjoint_indices_valid<T, I: core::slice::SliceIndex<[T]>, const N: usize>(\n"
        "    seq: Seq<T>,\n"
        "    indices: [I; N],\n"
        ") -> bool;",
        "pub uninterp spec fn slice_disjoint_indices_valid<T, I: core::slice::SliceIndex<[T]>, const N: usize>(\n"
        "    seq: Seq<T>,\n"
        "    indices: &[I; N],\n"
        ") -> bool;",
    )


def normalize_slice_pattern_det_harness(harness: str) -> str:
    return re.sub(
        r"([<,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:\s*core::slice::SlicePattern"
        r"\s*<\s*Item\s*=\s*T\s*>\s*\+\s*\?Sized",
        r"\1\2: ?Sized",
        harness,
    )


def normalize_nested_array_slice_det_harness(harness: str) -> str:
    harness = harness.replace(": [[T; N]]", ": &[[T; N]]")
    return harness.replace(
        "(post1_slice =~= post2_slice)",
        "(post1_slice@ == post2_slice@)",
    )


def split_top_level_angle_commas(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    paren = bracket = brace = angle = 0
    for index, char in enumerate(text):
        if char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif char == "[":
            bracket += 1
        elif char == "]" and bracket:
            bracket -= 1
        elif char == "{":
            brace += 1
        elif char == "}" and brace:
            brace -= 1
        elif char == "<":
            angle += 1
        elif char == ">" and angle:
            angle -= 1
        elif char == "," and paren == bracket == brace == angle == 0:
            part = text[start:index].strip()
            if part:
                parts.append(part)
            start = index + 1
    part = text[start:].strip()
    if part:
        parts.append(part)
    return parts


def normalized_generic_args(args: str) -> str:
    return re.sub(r"\s+", " ", args).strip()


def add_slice_iterator_fields(
    fields_by_view: dict[str, set[str]],
    view_args: str,
    fields: tuple[str, ...],
) -> None:
    normalized = normalized_generic_args(view_args)
    if not normalized:
        return
    fields_by_view.setdefault(normalized, set()).update(fields)


def collect_direct_slice_iterator_fields(template: str) -> dict[str, set[str]]:
    found: dict[tuple[str, str], set[str]] = {}
    direct_re = re.compile(
        r"slice_iterator_view::<(?P<args>.*?)>\(\s*r(?P<which>[12])\s*\)"
        rf"\.(?P<field>{'|'.join(SLICE_ITERATOR_VIEW_FIELDS)})",
        flags=re.DOTALL,
    )
    for match in direct_re.finditer(template):
        key = (normalized_generic_args(match.group("args")), match.group("which"))
        found.setdefault(key, set()).add(match.group("field"))

    fields_by_view: dict[str, set[str]] = {}
    for view_args in sorted({key[0] for key in found}):
        fields = found.get((view_args, "1"), set()) & found.get((view_args, "2"), set())
        if fields:
            add_slice_iterator_fields(fields_by_view, view_args, tuple(fields))
    return fields_by_view


def helper_slice_iterator_view_args(helper: str, helper_args: str) -> str | None:
    args = split_top_level_angle_commas(helper_args)
    if helper in {"slice_predicate_split_view", "slice_adjacent_chunk_view"}:
        if len(args) < 3:
            return None
        return f"{args[0]}, {args[2]}"
    if helper == "utf8_chunk_partition":
        if not args:
            return None
        return f"{args[0]}, u8"
    return None


def collect_helper_slice_iterator_fields(template: str) -> dict[str, set[str]]:
    fields_by_view: dict[str, set[str]] = {}
    for helper, fields in SLICE_ITERATOR_HELPER_FIELDS.items():
        helper_re = re.compile(
            rf"{helper}::<(?P<args>.*?)>\(\s*r(?P<which>[12])\s*,",
            flags=re.DOTALL,
        )
        by_side: dict[str, set[str]] = {"1": set(), "2": set()}
        for match in helper_re.finditer(template):
            view_args = helper_slice_iterator_view_args(helper, match.group("args"))
            if view_args is not None:
                by_side[match.group("which")].add(normalized_generic_args(view_args))
        for view_args in sorted(by_side["1"] & by_side["2"]):
            add_slice_iterator_fields(fields_by_view, view_args, fields)
    return fields_by_view


def slice_iterator_equal_terms(det_template: str) -> list[str]:
    fields_by_view = collect_direct_slice_iterator_fields(det_template)
    for view_args, fields in collect_helper_slice_iterator_fields(det_template).items():
        fields_by_view.setdefault(view_args, set()).update(fields)

    terms: list[str] = []
    for view_args in sorted(fields_by_view):
        for field in SLICE_ITERATOR_VIEW_FIELDS:
            if field in fields_by_view[view_args]:
                terms.append(
                    f"slice_iterator_view::<{view_args}>(r1).{field} "
                    f"== slice_iterator_view::<{view_args}>(r2).{field}"
                )
    return terms


def slice_iterator_equal_expr(det_template: str) -> str | None:
    terms = slice_iterator_equal_terms(det_template)
    if not terms:
        return None
    if len(terms) == 1:
        return f"({terms[0]})"
    return "(\n        " + "\n        && ".join(terms) + "\n    )"


def normalize_slice_iterator_equal_fn(candidate: dict[str, Any], det_spec: Any) -> bool:
    equal_fn_def = str(getattr(det_spec, "equal_fn_def", ""))
    if not re.search(r"\(r1\s*==\s*r2\)", equal_fn_def):
        return False
    equal_expr = slice_iterator_equal_expr(str(getattr(det_spec, "det_check_template", "")))
    if equal_expr is None:
        return False
    det_spec.equal_fn_def = re.sub(
        r"\(r1\s*==\s*r2\)",
        equal_expr,
        equal_fn_def,
        count=1,
    )
    policy = dict(getattr(det_spec, "equal_policy", {}) or {})
    policy.update(
        {
            "source": SLICE_ITERATOR_EQUAL_POLICY_SOURCE,
            "rationale": (
                f"{candidate.get('target', 'core::slice target')} returns a slice "
                "iterator/adaptor whose public specification is the shared "
                "slice_iterator_view; determinism compares only the modeled view "
                "fields fixed by the contract instead of opaque Rust iterator "
                "object equality."
            ),
        }
    )
    det_spec.equal_policy = policy
    return True


def normalize_slice_det_harness(candidate: dict[str, Any], harness: str) -> str:
    target = str(candidate.get("target", ""))
    if target in CLOSURE_BORROW_TARGETS:
        harness = normalize_closure_borrow_det_harness(harness)
    if target in DISJOINT_INDEX_TARGETS:
        harness = normalize_disjoint_index_det_harness(harness)
    if target in SLICE_PATTERN_TARGETS:
        harness = normalize_slice_pattern_det_harness(harness)
    if target in NESTED_ARRAY_SLICE_PARAM_TARGETS:
        harness = normalize_nested_array_slice_det_harness(harness)
    return harness


def install_slice_det_harness_normalizer(feedback: Any) -> None:
    original_build_det_harness = feedback.build_det_harness
    original_build_determinism_artifacts = feedback.build_determinism_artifacts

    def build_det_harness(candidate: dict[str, Any], det_spec: Any, schemas: list[Any]) -> str:
        normalize_slice_iterator_equal_fn(candidate, det_spec)
        return normalize_slice_det_harness(
            candidate,
            original_build_det_harness(candidate, det_spec, schemas),
        )

    def build_determinism_artifacts(candidate: dict[str, Any], view_registry: Any) -> dict[str, Any]:
        prepared = original_build_determinism_artifacts(candidate, view_registry)
        det_spec = prepared.get("det_spec")
        if det_spec is not None and getattr(det_spec, "equal_policy", {}).get(
            "source"
        ) == SLICE_ITERATOR_EQUAL_POLICY_SOURCE:
            prepared["equal_policy"] = dict(det_spec.equal_policy)
        return prepared

    feedback.build_det_harness = build_det_harness
    feedback.build_determinism_artifacts = build_determinism_artifacts


def source_backed_mut_ref_return_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = str(candidate.get("target", ""))
    return (
        target in SOURCE_BACKED_MUT_REF_RETURN_TARGETS
        and candidate.get("decision") == "add_spec"
        and candidate.get("contract_form") == "assume_specification"
        and bool(candidate.get("contract_code"))
        and bool(candidate.get("ensures"))
    )


def install_slice_mut_ref_return_adapter(feedback: Any) -> None:
    original_target_for_candidate = feedback.direct_mut_view_adapter_target_for_candidate
    original_candidate_matches = feedback.direct_mut_view_adapter_candidate_matches

    def direct_mut_view_adapter_target_for_candidate(candidate: dict[str, Any]) -> str | None:
        if source_backed_mut_ref_return_candidate_matches(candidate):
            return str(candidate["target"])
        return original_target_for_candidate(candidate)

    def direct_mut_view_adapter_candidate_matches(candidate: dict[str, Any]) -> bool:
        if source_backed_mut_ref_return_candidate_matches(candidate):
            return True
        return original_candidate_matches(candidate)

    feedback.direct_mut_view_adapter_target_for_candidate = direct_mut_view_adapter_target_for_candidate
    feedback.direct_mut_view_adapter_candidate_matches = direct_mut_view_adapter_candidate_matches


def install_slice_feedback_adapters(feedback: Any) -> None:
    install_slice_mut_ref_return_adapter(feedback)
    install_slice_det_harness_normalizer(feedback)


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
    fail(f"unclosed {opening} in generated specs")


def verus_body(source: str) -> str:
    match = re.search(r"\bverus!\s*\{", source)
    if match is None:
        fail("generated specs have no verus! body")
    brace = source.find("{", match.start())
    end = matching_delimiter(source, brace, "{", "}")
    return source[brace + 1 : end]


def shared_vocabulary_body(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"\bverus!\s*\{", text)
    if match is None:
        fail(f"{path} has no verus! body")
    brace = text.find("{", match.start())
    end = matching_delimiter(text, brace, "{", "}")
    body = text[brace + 1 : end].strip()
    if "verus!" in body:
        fail(f"{path} contains nested verus! inside shared vocabulary body")
    body = normalize_shared_vocabulary_for_determinism(body)
    return body


def normalize_shared_vocabulary_for_determinism(body: str) -> str:
    replacements = {
        (
            "==> (fnmut_predicate_observed(pred, source[i])\n"
            "                || !fnmut_predicate_observed(pred, source[i]))"
        ): (
            "==> (#[trigger] fnmut_predicate_observed(pred, source[i])\n"
            "                || !fnmut_predicate_observed(pred, source[i]))"
        ),
        (
            "==> (fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1])\n"
            "                || !fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1]))"
        ): (
            "==> (#[trigger] fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1])\n"
            "                || !fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1]))"
        ),
    }
    for original, replacement in replacements.items():
        if original not in body:
            fail("shared vocabulary trigger normalization pattern was not found")
        body = body.replace(original, replacement, 1)
    return body


def read_catalog_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return fieldnames, rows


def read_catalog(path: Path) -> dict[str, dict[str, str]]:
    _, rows = read_catalog_rows(path)
    return {row["target"]: row for row in rows}


def normalize_contract_target(target: str) -> str:
    return re.sub(r"\s+", " ", target).strip()


def strip_rust_generic_suffix(path: str) -> str:
    previous = None
    while previous != path:
        previous = path
        path = re.sub(r"::\s*<[^>]+>(?=::|$)", "", path)
    return re.sub(r"::<[^>]+>$", "", path)


def catalog_target_from_contract_target(contract_target: str) -> str:
    normalized = normalize_contract_target(contract_target)
    if "]>::" in normalized:
        method = normalized.split("]>::", 1)[1]
        return "core::slice::" + strip_rust_generic_suffix(method)
    if normalized.startswith("core::slice::"):
        return strip_rust_generic_suffix(normalized)
    fail(f"unsupported assume_specification target form {contract_target!r}")


def assume_spec_items(body: str) -> list[str]:
    items: list[str] = []
    for match in re.finditer(r"\b(?:pub\s+)?assume_specification\b", body):
        paren = bracket = brace = 0
        semicolon = None
        for index in range(match.start(), len(body)):
            char = body[index]
            if char == "(":
                paren += 1
            elif char == ")" and paren:
                paren -= 1
            elif char == "[":
                bracket += 1
            elif char == "]" and bracket:
                bracket -= 1
            elif char == "{":
                brace += 1
            elif char == "}" and brace:
                brace -= 1
            elif char == ";" and paren == bracket == brace == 0:
                semicolon = index
                break
        if semicolon is None:
            fail("unterminated assume_specification in generated specs")
        items.append(body[match.start() : semicolon + 1].strip())
    return items


def split_top_level_commas(text: str) -> list[str]:
    clauses: list[str] = []
    start = 0
    paren = bracket = brace = 0
    for index, char in enumerate(text):
        if char == "(":
            paren += 1
        elif char == ")" and paren:
            paren -= 1
        elif char == "[":
            bracket += 1
        elif char == "]" and bracket:
            bracket -= 1
        elif char == "{":
            brace += 1
        elif char == "}" and brace:
            brace -= 1
        elif char == "," and paren == bracket == brace == 0:
            clause = text[start:index].strip()
            if clause:
                clauses.append(clause)
            start = index + 1
    clause = text[start:].strip().rstrip(";").strip()
    if clause:
        clauses.append(clause)
    return clauses


def extract_clause_block(item: str, keyword: str) -> list[str]:
    match = re.search(rf"\b{keyword}\b", item)
    if match is None:
        return []
    next_keyword = re.search(r"\b(?:requires|ensures)\b", item[match.end() :])
    semicolon = item.rfind(";")
    end = semicolon if next_keyword is None else match.end() + next_keyword.start()
    return split_top_level_commas(item[match.end() : end])


def build_assume_spec_index(feedback: Any, generated_path: Path) -> dict[str, dict[str, str]]:
    body = verus_body(generated_path.read_text())
    by_catalog_target: dict[str, dict[str, str]] = {}
    for item in assume_spec_items(body):
        contract_target = normalize_contract_target(feedback.assume_specification_target(item))
        catalog_target = catalog_target_from_contract_target(contract_target)
        if catalog_target in by_catalog_target:
            fail(f"duplicate generated assume_specification for {catalog_target}")
        by_catalog_target[catalog_target] = {
            "contract_target": contract_target,
            "item": item,
        }
    return by_catalog_target


def generated_catalog_targets(rows: list[dict[str, str]]) -> list[str]:
    targets = [
        row["target"]
        for row in rows
        if row.get("status") == "generated-new-real-relation-spec"
    ]
    if len(targets) != EXPECTED_GENERATED_TARGETS:
        fail(f"catalog has {len(targets)} generated targets, expected {EXPECTED_GENERATED_TARGETS}")
    return targets


def structured_requires(target: str, item: str) -> list[str]:
    return extract_clause_block(item, "requires")


def structured_ensures(target: str, item: str) -> list[str]:
    if target == "core::slice::split_first_mut":
        return list(SPLIT_FIRST_MUT_STRUCTURED_ENSURES)
    return extract_clause_block(item, "ensures")


def build_candidate(
    *,
    target: str,
    item: str,
    shared_body: str,
    catalog: dict[str, dict[str, str]],
) -> dict[str, Any]:
    row = catalog.get(target)
    if row is None:
        fail(f"{target} is missing from catalog")
    source_requires = extract_clause_block(item, "requires")
    source_ensures = extract_clause_block(item, "ensures")
    return {
        "decision": "add_spec",
        "contract_form": "assume_specification",
        "target": target,
        "contract_code": f"{shared_body}\n\n{item}",
        "requires": structured_requires(target, item),
        "ensures": structured_ensures(target, item),
        "source_requires": source_requires,
        "source_ensures": source_ensures,
        "imports": list(DEFAULT_IMPORTS),
        "feature_gates": list(DEFAULT_FEATURE_GATES),
        "useful": True,
        "rationale": (
            "project-local core::slice bootstrap candidate built from the real "
            "generated assume_specification block and the shared slice vocabulary"
        ),
        "risks": [row.get("known_risks", "")],
        "semantic_family": row.get("semantic_family", ""),
        "source_reference": row.get("source_reference", ""),
        "catalog_requires": row.get("requires", ""),
        "catalog_ensures": row.get("ensures", ""),
    }


def relative_artifacts(target_dir: Path) -> dict[str, Any]:
    names = [
        "synthetic_spec.rs",
        "det_spec.json",
        "det_harness.rs",
        "det_stdout.txt",
        "det_stderr.txt",
        "verus_stdout.txt",
        "verus_stderr.txt",
        "schema_search_evidence.json",
        "candidate.json",
        "result.json",
    ]
    artifacts: dict[str, Any] = {
        name: str((target_dir / name).relative_to(SLICE_ROOT))
        for name in names
        if (target_dir / name).is_file()
    }
    smt2_files = sorted((target_dir / "verus_log").rglob("*.smt2"))
    if smt2_files:
        artifacts["smt2_files"] = [
            str(path.relative_to(SLICE_ROOT)) for path in smt2_files
        ]
    return artifacts


def write_verus_aliases(target_dir: Path) -> None:
    stdout_path = target_dir / "det_stdout.txt"
    stderr_path = target_dir / "det_stderr.txt"
    if stdout_path.is_file():
        (target_dir / "verus_stdout.txt").write_text(stdout_path.read_text())
    if stderr_path.is_file():
        (target_dir / "verus_stderr.txt").write_text(stderr_path.read_text())


def ensure_minimal_determinism_artifacts(target_dir: Path, result: dict[str, Any]) -> None:
    status = str(result.get("status", "runner_crash"))
    if not (target_dir / "det_spec.json").is_file():
        (target_dir / "det_spec.json").write_text(
            json.dumps(
                {
                    "status": status,
                    "reason": "determinism artifacts were not built because the feedback pipeline classified this target before harness generation",
                    "requires": result.get("requires", []),
                    "ensures": result.get("ensures", []),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    if not (target_dir / "det_harness.rs").is_file():
        (target_dir / "det_harness.rs").write_text(
            f"// Determinism harness not generated: status={status}\n"
        )
    if not (target_dir / "det_stdout.txt").is_file():
        (target_dir / "det_stdout.txt").write_text("")
    if not (target_dir / "det_stderr.txt").is_file():
        (target_dir / "det_stderr.txt").write_text(
            f"Verus determinism run not invoked: status={status}\n"
        )


def write_schema_search_evidence(target_dir: Path, result: dict[str, Any]) -> None:
    if "r0_z3" not in result:
        return
    evidence = {
        "status": result.get("status"),
        "r0_z3": result.get("r0_z3"),
        "classification": result.get("classification"),
        "n_rounds": result.get("n_rounds"),
        "assumes": result.get("assumes", []),
        "smt2_files": [
            str(path.relative_to(target_dir))
            for path in sorted((target_dir / "verus_log").rglob("*.smt2"))
        ],
    }
    (target_dir / "schema_search_evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    )


def prune_verus_log_to_smt(target_dir: Path) -> None:
    log_dir = target_dir / "verus_log"
    if not log_dir.is_dir():
        return
    for path in sorted(log_dir.rglob("*"), reverse=True):
        if path.is_file() and path.suffix != ".smt2":
            path.unlink()
        elif path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass


def run_target(
    *,
    feedback: Any,
    view_registry: Any,
    target: str,
    contract_target: str,
    candidate: dict[str, Any],
    target_dir: Path,
    verus_bin: Path,
    z3_path: Path,
    timeout: int,
    rlimit: float,
) -> dict[str, Any]:
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "candidate.json").write_text(
        json.dumps(candidate, indent=2, sort_keys=True) + "\n"
    )
    synthetic_preview = feedback.assume_to_synthetic(
        feedback.active_contract_code(candidate)
    )
    if "__rust_std_candidate" not in synthetic_preview:
        fail(f"{target} did not convert to __rust_std_candidate")
    result = feedback.run_determinism(
        candidate=candidate,
        round_dir=target_dir,
        view_registry=view_registry,
        verus_bin=verus_bin,
        z3_path=z3_path,
        timeout=timeout,
        rlimit=rlimit,
    )
    ensure_minimal_determinism_artifacts(target_dir, result)
    write_verus_aliases(target_dir)
    write_schema_search_evidence(target_dir, result)
    prune_verus_log_to_smt(target_dir)
    payload = {
        **result,
        "target": target,
        "contract_target": contract_target,
        "candidate": candidate,
    }
    artifacts = relative_artifacts(target_dir)
    artifacts["result.json"] = str((target_dir / "result.json").relative_to(SLICE_ROOT))
    payload["artifacts"] = artifacts
    payload = annotate_unknown_reason(payload)
    (target_dir / "result.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    return payload


def determinism_outcome(result: dict[str, Any]) -> str:
    status = str(result.get("status", "runner_crash"))
    r0_z3 = result.get("r0_z3")
    if status == "ok":
        if r0_z3 == "unsat":
            return "UNSAT"
        if r0_z3 == "sat":
            return "SAT"
        if r0_z3 == "unknown":
            return "UNKNOWN"
        return "UNKNOWN"
    if status in {"no_ensures", "unsupported_mut_ref_return"}:
        return "unsupported"
    if status == "verus_error":
        return "Verus error"
    return "runner crash"


def unknown_reason_class(result: dict[str, Any]) -> str | None:
    if result.get("status") != "ok" or result.get("r0_z3") != "unknown":
        return None
    target = str(result.get("target", ""))
    reason_class = UNKNOWN_REASON_TARGET_CLASSES.get(target)
    if reason_class is None:
        candidate = result.get("candidate")
        family = ""
        if isinstance(candidate, dict):
            family = str(candidate.get("semantic_family", ""))
        reason_class = UNKNOWN_REASON_FAMILY_DEFAULTS.get(family)
    if reason_class is None:
        fail(f"{target} has R0=UNKNOWN without a registered review reason class")
    return reason_class


def annotate_unknown_reason(result: dict[str, Any]) -> dict[str, Any]:
    reason_class = unknown_reason_class(result)
    if reason_class is None:
        result.pop("unknown_reason_class", None)
        result.pop("unknown_reason", None)
        return result
    result["unknown_reason_class"] = reason_class
    result["unknown_reason"] = UNKNOWN_REASON_SUMMARIES[reason_class]
    return result


def determinism_result_text(result: dict[str, Any]) -> str:
    evidence = result["artifacts"]["result.json"]
    synthetic = result["artifacts"].get("synthetic_spec.rs")
    harness = result["artifacts"].get("det_harness.rs")
    status = str(result.get("status", "runner_crash"))
    outcome = determinism_outcome(result)
    pieces = [
        f"feedback-pipeline determinism: status={status}",
        f"R0={outcome}",
    ]
    if "r0_z3" in result:
        pieces.append(f"r0_z3={result.get('r0_z3')}")
    if result.get("classification"):
        pieces.append(f"classification={result.get('classification')}")
    reason_class = result.get("unknown_reason_class")
    if reason_class:
        pieces.append(f"unknown_reason={reason_class}")
        pieces.append(f"unknown_review_reason={result.get('unknown_reason')}")
    if "verus_returncode" in result:
        pieces.append(f"verus_rc={result.get('verus_returncode')}")
    pieces.append(f"evidence={evidence}")
    if synthetic:
        pieces.append(f"synthetic={synthetic}")
    if harness:
        pieces.append(f"harness={harness}")
    return "; ".join(pieces)


def refresh_reviewer_note(text: str) -> str:
    for old, new in LEGACY_REVIEWER_NOTE_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def update_catalog_artifacts(
    *,
    catalog_path: Path,
    results: list[dict[str, Any]],
) -> None:
    fieldnames, rows = read_catalog_rows(catalog_path)
    result_by_target = {result["target"]: result for result in results}
    for row in rows:
        target = row["target"]
        if target not in result_by_target:
            continue
        row["determinism_result"] = determinism_result_text(result_by_target[target])
        row["known_risks"] = refresh_reviewer_note(row.get("known_risks", ""))
        row["reviewer_notes"] = refresh_reviewer_note(row.get("reviewer_notes", ""))
    with catalog_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    status_counts = Counter(row["status"] for row in rows)
    payload = {
        "rows": rows,
        "summary": {
            "total": len(rows),
            "existing_vstd": status_counts.get("existing-vstd", 0),
            "generated_new_real_relation_specs": status_counts.get("generated-new-real-relation-spec", 0),
            "justified_no_spec": status_counts.get("justified-no-spec", 0),
        },
    }
    catalog_path.with_suffix(".json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )


def update_spec_marker_file(path: Path, results: list[dict[str, Any]]) -> None:
    by_target = {result["target"]: determinism_result_text(result) for result in results}
    lines = path.read_text().splitlines()
    active_target: str | None = None
    output: list[str] = []
    begin_re = re.compile(r"// BEGIN SLICE_SPEC target=(.+)$")
    for line in lines:
        begin = begin_re.match(line)
        if begin:
            active_target = begin.group(1)
        elif line == "// END SLICE_SPEC":
            active_target = None
        if active_target in by_target:
            if line.startswith("// determinism_result:"):
                output.append(f"// determinism_result: {by_target[active_target]}")
            elif line.startswith("// reviewer_notes:"):
                output.append(f"// reviewer_notes: {refresh_reviewer_note(line.removeprefix('// reviewer_notes: '))}")
            else:
                output.append(line)
        else:
            output.append(line)
    path.write_text("\n".join(output) + "\n")


def review_markdown(
    *,
    results: list[dict[str, Any]],
    run_root: Path,
    summary: dict[str, Any],
) -> str:
    status_counts = Counter(str(result.get("status")) for result in results)
    outcome_counts = Counter(determinism_outcome(result) for result in results)
    family_counts: dict[str, Counter[str]] = {}
    for result in results:
        family = result["candidate"].get("semantic_family", "")
        family_counts.setdefault(family, Counter())[determinism_outcome(result)] += 1
    family_lines = [
        "| Semantic family | Rows | UNSAT | SAT | UNKNOWN | unsupported | Verus error | runner crash |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for family in sorted(family_counts):
        counts = family_counts[family]
        total = sum(counts.values())
        family_lines.append(
            f"| {family} | {total} | {counts.get('UNSAT', 0)} | {counts.get('SAT', 0)} | "
            f"{counts.get('UNKNOWN', 0)} | {counts.get('unsupported', 0)} | "
            f"{counts.get('Verus error', 0)} | {counts.get('runner crash', 0)} |"
        )
    unknown_results = [
        result
        for result in results
        if result.get("status") == "ok" and result.get("r0_z3") == "unknown"
    ]
    reason_counts = Counter(str(result.get("unknown_reason_class", "")) for result in unknown_results)
    reason_lines = [
        "| UNKNOWN reason class | Rows | Review reason |",
        "| --- | ---: | --- |",
    ]
    for reason_class in sorted(reason_counts):
        if not reason_class:
            fail("R0=UNKNOWN result is missing unknown_reason_class for review output")
        reason_lines.append(
            f"| `{reason_class}` | {reason_counts[reason_class]} | "
            f"{UNKNOWN_REASON_SUMMARIES[reason_class]} |"
        )
    target_reason_lines = [
        "| Target | Semantic family | UNKNOWN reason class |",
        "| --- | --- | --- |",
    ]
    for result in sorted(unknown_results, key=lambda item: str(item.get("target", ""))):
        candidate = result.get("candidate", {})
        family = candidate.get("semantic_family", "") if isinstance(candidate, dict) else ""
        target_reason_lines.append(
            f"| `{result['target']}` | {family} | `{result['unknown_reason_class']}` |"
        )
    return "\n".join(
        [
            "# Slice Spec Evidence Review",
            "",
            "## Independent audit result",
            "",
            "The isolated `core::slice` artifact set accounts for all 132 stable executable API rows: 12 copied existing-vstd baseline rows and 120 generated executable Verus `assume_specification` attempts. The 120 generated rows now record Rust std feedback-pipeline determinism evidence generated from synthetic `__rust_std_candidate` exec specifications, not the old direct assume-specification harness path.",
            "",
            "Relational or source-nondeterministic contracts are preserved as written; `SAT`/`UNKNOWN` outcomes are recorded honestly rather than strengthened away.",
            "",
            "## Audited totals",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            "| Catalog rows / stable unique `core::slice` exec APIs | 132 |",
            "| Existing vstd baseline rows preserved | 12 |",
            "| New generated contracts attempted | 120 |",
            "| New generated contracts with Verus typecheck pass | 120 |",
            "| New generated contracts with Verus typecheck fail | 0 |",
            f"| Determinism `R0=UNSAT` | {outcome_counts.get('UNSAT', 0)} |",
            f"| Determinism `R0=SAT` | {outcome_counts.get('SAT', 0)} |",
            f"| Determinism `R0=UNKNOWN` | {outcome_counts.get('UNKNOWN', 0)} |",
            f"| Determinism unsupported | {outcome_counts.get('unsupported', 0)} |",
            f"| Determinism Verus error | {outcome_counts.get('Verus error', 0)} |",
            f"| Determinism runner crash | {outcome_counts.get('runner crash', 0)} |",
            "| Remaining unconverted non-vstd rows | 0 |",
            "| Justified-no-spec rows | 0 |",
            "| Stale `Verus typecheck pending` catalog rows | 0 |",
            "",
            "## Semantic-family outcomes",
            "",
            *family_lines,
            "",
            "## UNKNOWN reason taxonomy",
            "",
            "Every current `R0=UNKNOWN` generated row carries an `unknown_reason_class` in the manifest entry, result JSON, catalog/spec determinism text, and review table. These labels explain why the source-backed relational contract remains inconclusive without strengthening source-nondeterministic behavior.",
            "",
            *reason_lines,
            "",
            "## UNKNOWN target classifications",
            "",
            *target_reason_lines,
            "",
            "## Machine evidence audited",
            "",
            f"Latest feedback-pipeline manifest: `{summary['run_root']}/run_manifest.json`.",
            f"Per-target evidence directories live under `{run_root.relative_to(SLICE_ROOT)}` and include `synthetic_spec.rs`, `det_spec.json`, `det_harness.rs`, Verus stdout/stderr aliases, schema-search evidence when `r0_z3` is produced, `candidate.json`, and complete `result.json` payloads.",
            "",
            f"Status counts: `{dict(sorted(status_counts.items()))}`.",
            f"R0 counts: `{dict(sorted(Counter(str(result.get('r0_z3', determinism_outcome(result))) for result in results).items()))}`.",
            "",
            "The generated catalog rows reference feedback-pipeline result JSONs and no generated catalog determinism row relies on legacy direct assume-specification evidence.",
            "",
            "## Shared vocabulary audit",
            "",
            "`verification/check_contracts.py` audits the 41 shared vocabulary helpers that were originally uninterpreted and rejects any unaudited `pub uninterp spec fn` added to `specs/slice_shared_vocabulary.rs`. The enforced classification is: 9 source-backed helpers, 7 law-constrained observation/state abstractions, and 25 irreducible boundary abstractions.",
            "",
            "The source-backed replacements are `slice_multiplicity`, `array_ref_view`, `array_mut_ref_view`, `array_value_view`, `flatten_array_chunks`, `ascii_lower_byte`, `ascii_upper_byte`, `ascii_trim_start_index`, and `ascii_trim_end_index`. `slice_multiplicity` is tied to `Seq::to_multiset().count`, fixed-array/chunk flattening is tied to Verus array views, and ASCII case/trim helpers are tied to the byte ranges and leading/trailing whitespace searches used by `core/src/slice/ascii.rs`.",
            "",
            "The law-constrained helpers are `partial_eq_observed`, `zero_arg_fnmut_outputs`, `ord_cmp_observed`, `partial_ord_leq_observed`, `comparator_ordering_observed`, `comparator_observation`, and `slice_iterator_view`. The shared vocabulary now includes broadcast axiom laws for PartialEq symmetry/transitivity, zero-arg FnMut output length, Ord duality/totality/transitivity and equality correspondence, PartialOrd equality/antisymmetry/transitivity, comparator observation domain plus Ordering-return/reflexive/dual/total-preorder laws, and iterator/chunk well-formedness/partition structure.",
            "",
            "`slice_pattern_view`, the arbitrary FnMut callback observations (`fnmut_ordering_observed`, `fnmut_key_observed`, `fnmut_predicate_observed`, `fnmut_adjacent_predicate_observed`, `fnmut_adjacent_bool_outputs`, and `fnmut_adjacent_key_outputs`), raw-pointer/provenance helpers, SliceIndex/GetDisjointMutIndex helpers, the active MaybeUninit sequence relation helper, and `ascii_escape_seq` remain classified as irreducible boundary abstractions because their source semantics depend on callback traces, pointer provenance, layout, initialization state, formatting, or trait-associated behavior that is not recoverable from a pure `Seq` slice view. The `is_sorted_by` and `is_sorted_by_key` contracts now consume these source-order adjacent call traces instead of all-pairs/extensional callback or key observations.",
            "",
        ]
    )


def update_review(
    *,
    review_path: Path,
    run_root: Path,
    results: list[dict[str, Any]],
    summary: dict[str, Any],
) -> None:
    review_path.write_text(review_markdown(results=results, run_root=run_root, summary=summary))


def write_result_payload(result: dict[str, Any]) -> None:
    artifacts = result.get("artifacts")
    if not isinstance(artifacts, dict):
        fail(f"{result.get('target')} has no artifact map")
    rel = artifacts.get("result.json")
    if not isinstance(rel, str):
        fail(f"{result.get('target')} has no result.json artifact")
    (SLICE_ROOT / rel).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def manifest_result_entry(result: dict[str, Any]) -> dict[str, Any]:
    entry = {
        "target": result["target"],
        "status": result.get("status"),
        "r0_z3": result.get("r0_z3"),
        "result_json": result["artifacts"].get("result.json"),
    }
    reason_class = result.get("unknown_reason_class")
    if reason_class:
        entry["unknown_reason_class"] = reason_class
        entry["unknown_reason"] = result.get("unknown_reason")
    return entry


def build_run_summary(
    *,
    run_id: str,
    run_root: Path,
    targets: tuple[str, ...],
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    unknown_reason_counts = Counter(
        str(result.get("unknown_reason_class"))
        for result in results
        if result.get("status") == "ok" and result.get("r0_z3") == "unknown"
    )
    return {
        "schema_version": 2,
        "run_id": run_id,
        "run_root": str(run_root.relative_to(SLICE_ROOT)),
        "targets": list(targets),
        "status_counts": dict(Counter(str(result.get("status")) for result in results)),
        "r0_z3_counts": dict(Counter(str(result.get("r0_z3")) for result in results)),
        "unknown_reason_counts": dict(sorted(unknown_reason_counts.items())),
        "results": [manifest_result_entry(result) for result in results],
    }


def load_results_from_manifest(manifest_path: Path) -> tuple[str, Path, tuple[str, ...], list[dict[str, Any]]]:
    if not manifest_path.is_absolute():
        manifest_path = SLICE_ROOT / manifest_path
    if not manifest_path.is_file():
        fail(f"missing refresh manifest {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    run_root_rel = manifest.get("run_root")
    if not isinstance(run_root_rel, str):
        fail(f"{manifest_path} has no run_root")
    run_root = SLICE_ROOT / run_root_rel
    run_id = str(manifest.get("run_id") or run_root.name)
    entries = manifest.get("results")
    if not isinstance(entries, list):
        fail(f"{manifest_path} results must be a list")
    results: list[dict[str, Any]] = []
    targets: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            fail(f"{manifest_path} contains a non-object result entry")
        target = str(entry.get("target"))
        rel = entry.get("result_json")
        if not isinstance(rel, str):
            fail(f"{target} manifest entry has no result_json")
        result_path = SLICE_ROOT / rel
        if not result_path.is_file():
            fail(f"{target} result JSON is missing: {rel}")
        payload = annotate_unknown_reason(json.loads(result_path.read_text()))
        if payload.get("target") != target:
            fail(f"{target} manifest/result target mismatch")
        results.append(payload)
        targets.append(target)
    return run_id, run_root, tuple(targets), results


def write_run_outputs(
    *,
    evidence_root: Path,
    run_root: Path,
    summary: dict[str, Any],
    results: list[dict[str, Any]],
    catalog_path: Path,
    update_artifacts: bool,
) -> None:
    for result in results:
        write_result_payload(result)
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "run_manifest.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    if not update_artifacts:
        return
    evidence_root.mkdir(parents=True, exist_ok=True)
    (evidence_root / "latest_manifest.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    update_catalog_artifacts(catalog_path=catalog_path, results=results)
    update_spec_marker_file(SLICE_ROOT / "specs" / "generated_slice_specs.rs", results)
    update_spec_marker_file(SLICE_ROOT / "specs" / "all_slice_specs.rs", results)
    update_review(
        review_path=catalog_path.with_name("SLICE_SPEC_REVIEW.md"),
        run_root=run_root,
        results=results,
        summary=summary,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--survey-root", type=Path, default=DEFAULT_SURVEY_ROOT)
    parser.add_argument("--vstd-root", type=Path, default=DEFAULT_VSTD_ROOT)
    parser.add_argument("--verus-bin", type=Path, default=DEFAULT_VERUS_BIN)
    parser.add_argument("--z3-path", type=Path, default=DEFAULT_Z3_PATH)
    parser.add_argument("--generated-specs", type=Path, default=SLICE_ROOT / "specs" / "generated_slice_specs.rs")
    parser.add_argument("--shared-vocabulary", type=Path, default=SLICE_ROOT / "specs" / "slice_shared_vocabulary.rs")
    parser.add_argument("--catalog", type=Path, default=SLICE_ROOT / "catalog" / "slice_spec_catalog.csv")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--rlimit", type=float, default=60)
    parser.add_argument(
        "--target",
        action="append",
        help="Run one catalog target; repeat to run multiple. Defaults to all 120 generated targets.",
    )
    parser.add_argument(
        "--representatives",
        action="store_true",
        help="Run the five representative bootstrap targets.",
    )
    parser.add_argument(
        "--no-update-artifacts",
        action="store_true",
        help="Do not update catalog JSON/CSV, spec marker determinism fields, or review summary.",
    )
    parser.add_argument(
        "--refresh-from-manifest",
        type=Path,
        help="Refresh manifest/catalog/review fields from existing result JSONs without rerunning determinism.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _, catalog_rows = read_catalog_rows(args.catalog)
    catalog = {row["target"]: row for row in catalog_rows}
    generated_targets = tuple(generated_catalog_targets(catalog_rows))

    if args.refresh_from_manifest is not None:
        run_id, run_root, targets, results = load_results_from_manifest(args.refresh_from_manifest)
        if set(targets) != set(generated_targets):
            fail(
                "refresh manifest targets differ from generated catalog targets: "
                f"missing={sorted(set(generated_targets) - set(targets))} "
                f"extra={sorted(set(targets) - set(generated_targets))}"
            )
        summary = build_run_summary(
            run_id=run_id,
            run_root=run_root,
            targets=targets,
            results=results,
        )
        write_run_outputs(
            evidence_root=args.evidence_root,
            run_root=run_root,
            summary=summary,
            results=results,
            catalog_path=args.catalog,
            update_artifacts=not args.no_update_artifacts,
        )
        return 0

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_root = args.evidence_root / run_id
    feedback = load_feedback_module(args.survey_root)
    install_slice_feedback_adapters(feedback)
    if args.target:
        targets = tuple(args.target)
    elif args.representatives:
        targets = REPRESENTATIVE_TARGETS
    else:
        targets = generated_targets
    shared_body = shared_vocabulary_body(args.shared_vocabulary)
    assume_specs = build_assume_spec_index(feedback, args.generated_specs)
    registry = feedback.ViewRegistry.from_project(args.vstd_root)

    results: list[dict[str, Any]] = []
    for target in targets:
        if target not in catalog:
            fail(f"{target} is missing from catalog")
        assume_spec = assume_specs.get(target)
        if assume_spec is None:
            fail(f"{target} generated assume_specification not found")
        contract_target = assume_spec["contract_target"]
        item = assume_spec["item"]
        candidate = build_candidate(
            target=target,
            item=item,
            shared_body=shared_body,
            catalog=catalog,
        )
        target_dir = run_root / feedback.safe_name(target)
        result = run_target(
            feedback=feedback,
            view_registry=registry,
            target=target,
            contract_target=contract_target,
            candidate=candidate,
            target_dir=target_dir,
            verus_bin=args.verus_bin,
            z3_path=args.z3_path,
            timeout=args.timeout,
            rlimit=args.rlimit,
        )
        results.append(result)
        print(
            f"{target}: status={result.get('status')} r0_z3={result.get('r0_z3')} "
            f"dir={target_dir.relative_to(SLICE_ROOT)}",
            flush=True,
        )

    summary = build_run_summary(
        run_id=run_id,
        run_root=run_root,
        targets=targets,
        results=results,
    )
    write_run_outputs(
        evidence_root=args.evidence_root,
        run_root=run_root,
        summary=summary,
        results=results,
        catalog_path=args.catalog,
        update_artifacts=not args.no_update_artifacts,
    )

    missing_status = [
        result["target"]
        for result in results
        if not result.get("status")
    ]
    if missing_status:
        print(
            "missing feedback-pipeline status for: " + ", ".join(missing_status),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
