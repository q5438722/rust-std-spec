#!/usr/bin/env python3
"""Shared, result-neutral support for the Slice authority/design gate."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


SURVEY = Path("/home/chentianyu/nanvix-rust-std-spec-survey")
OUT = Path(__file__).resolve().parents[1]
SPECGEN = SURVEY / "nanvix-rust-std-slice-specgen-2026-08-11"
IMPLPROOF = SURVEY / "nanvix-rust-std-slice-vec-implproof-2026-08-12"
RUST_LIBRARY = SURVEY / "rust-1.96/library"
VERUS = SURVEY / "verus/source/target-verus/release/verus"

LATEST_MANIFEST = (
    SPECGEN
    / "verification/evidence/slice_feedback_determinism/latest_manifest.json"
)
CATALOG = SPECGEN / "catalog/slice_spec_catalog.csv"
GENERATED_SPECS = SPECGEN / "specs/generated_slice_specs.rs"
SHARED_VOCABULARY = SPECGEN / "specs/slice_shared_vocabulary.rs"
TARGETS_180 = IMPLPROOF / "proof_inventory/targets_180.csv"
PROOF_ORDER = IMPLPROOF / "proof_inventory/proof_order.csv"

GENERATED_STATUS = "generated-new-real-relation-spec"
EXACT_VSTD_STATUS = "existing-vstd"

EXPECTED_DRIFT_TARGETS = {
    "core::slice::as_chunks",
    "core::slice::as_chunks_mut",
    "core::slice::as_chunks_unchecked",
    "core::slice::as_chunks_unchecked_mut",
    "core::slice::as_rchunks",
    "core::slice::as_rchunks_mut",
}

BINARY_SEARCH_TARGETS = {
    "core::slice::binary_search",
    "core::slice::binary_search_by",
    "core::slice::binary_search_by_key",
}
UNSTABLE_SORT_TARGETS = {
    "core::slice::sort_unstable",
    "core::slice::sort_unstable_by",
    "core::slice::sort_unstable_by_key",
}
SELECTION_TARGETS = {
    "core::slice::select_nth_unstable",
    "core::slice::select_nth_unstable_by",
    "core::slice::select_nth_unstable_by_key",
}

TRUST_SEMANTIC_AUDIT_VERSION = "slice-unknown-authority-v3"
DEPENDENCY_AUDIT_INPUT_SHA256 = (
    "af4c1296d61382a5ea3fbe6377ee85785321afbde5cc770d6637952507fb1495"
)
EXTERNAL_AUDIT_INPUT_SHA256 = (
    "f05a969973f468d656c3f7e63a681dde9ea7761aceb5896d65f4004b1c56cc89"
)

EXTERNAL_SEMANTIC_CATEGORY_POLICY = {
    "complete-target-postcondition": {
        "semantic_disposition": "inadmissible-complete-target-postcondition",
        "target_postcondition_coverage": "complete-target",
        "rationale": (
            "The retained contract states the target's complete principal return "
            "and/or final-state postcondition. Source backing cannot make a whole "
            "target answer an admissible Boundary_T observation."
        ),
    },
    "complete-branch-postcondition": {
        "semantic_disposition": "inadmissible-complete-branch-postcondition",
        "target_postcondition_coverage": "complete-on-target-branch",
        "rationale": (
            "Under the helper's branch preconditions, its contract supplies every "
            "remaining public postcondition for that target branch."
        ),
    },
    "answer-equivalent-result": {
        "semantic_disposition": "inadmissible-answer-equivalent-result",
        "target_postcondition_coverage": "answer-equivalent",
        "rationale": (
            "The retained transition fixes the target discriminant, aggregate "
            "result, or aggregate final storage strongly enough to encode the "
            "public answer even though it uses different predicate spelling."
        ),
    },
    "opaque-whole-algorithm": {
        "semantic_disposition": "inadmissible-opaque-whole-algorithm",
        "target_postcondition_coverage": "complete-target-or-final-state",
        "rationale": (
            "The trusted private algorithm supplies the target's aggregate "
            "permutation, partition, sortedness, pivot, or returned-borrow result."
        ),
    },
    "pointer-layout-provenance-transition": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The contract isolates a pointer cast/copy, layout, address, or "
            "provenance transition and does not state the enclosing target answer."
        ),
    },
    "intermediate-raw-slice-constructor": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The raw-slice constructor describes an intermediate derived view; "
            "additional source steps are required to derive the public result."
        ),
    },
    "intermediate-subrange-split": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The contract exposes an intermediate source split, not the enclosing "
            "target's complete return/final-state relation."
        ),
    },
    "derived-borrow-source-callee": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The helper operates on a derived sub-borrow or lower source callee; "
            "the caller must still construct the target result."
        ),
    },
    "arithmetic-or-offset-fact": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The proof exposes only an arithmetic fit, length, or offset fact "
            "consumed by later source-backed transitions."
        ),
    },
    "panic-edge": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The contract models a source panic/divergence edge and supplies no "
            "normal target return or aggregate final state."
        ),
    },
    "callback-or-element-effect": {
        "semantic_disposition": "admissible-source-backed-lower-boundary",
        "target_postcondition_coverage": "partial-or-lower-level",
        "rationale": (
            "The contract records one callback, element read, clone, or write "
            "effect rather than the target's aggregate result."
        ),
    },
}

# Exhaustive, fail-closed semantic audit of all 86 selected external-body sites.
EXTERNAL_SITE_SEMANTIC_AUDIT = {
    # Complete target postconditions.
    ("core::slice::from_raw_parts", "rust_1_96_from_raw_parts_ub_checked_raw_slice"): "complete-target-postcondition",
    ("core::slice::from_raw_parts_mut", "rust_1_96_from_raw_parts_mut_ub_checked_raw_slice"): "complete-target-postcondition",
    ("core::slice::get_unchecked", "rust_1_96_sliceindex_get_unchecked_ref"): "complete-target-postcondition",
    ("core::slice::get_unchecked_mut", "rust_1_96_sliceindex_get_unchecked_mut_ref"): "complete-target-postcondition",
    ("core::slice::assume_init_mut", "rust_1_96_assume_init_mut_raw_cast"): "complete-target-postcondition",
    ("core::slice::assume_init_drop", "rust_1_96_assume_init_drop_in_place"): "complete-target-postcondition",
    ("core::slice::from_mut", "from_mut"): "complete-target-postcondition",
    ("core::slice::get_disjoint_unchecked_mut", "rust_1_96_fill_disjoint_mut_array_and_assume_init"): "complete-target-postcondition",
    ("core::slice::split_at_mut_unchecked", "rust_1_96_split_at_mut_unchecked_raw_parts"): "complete-target-postcondition",
    ("core::slice::as_chunks_unchecked_mut", "rust_1_96_from_raw_parts_mut_array_chunks"): "complete-target-postcondition",
    ("core::slice::as_flattened_mut", "rust_1_96_from_raw_parts_mut_flat"): "complete-target-postcondition",
    # Complete branch postconditions.
    ("core::slice::align_to", "rust_1_96_align_to_zst_or_overflow_result"): "complete-branch-postcondition",
    ("core::slice::align_to", "rust_1_96_align_to_split_raw_parts_result"): "complete-branch-postcondition",
    ("core::slice::align_to_mut", "rust_1_96_align_to_mut_zst_or_overflow"): "complete-branch-postcondition",
    ("core::slice::align_to_mut", "rust_1_96_align_to_mut_from_split_raw_parts"): "complete-branch-postcondition",
    ("core::slice::as_mut_array", "rust_1_96_as_mut_array_ref"): "complete-branch-postcondition",
    ("core::slice::first_chunk_mut", "rust_1_96_first_chunk_mut_array_ref"): "complete-branch-postcondition",
    ("core::slice::split_at_mut_checked", "rust_1_96_split_at_mut_unchecked_raw_parts"): "complete-branch-postcondition",
    ("core::slice::get_disjoint_mut", "rust_1_96_fill_disjoint_mut_array_and_assume_init"): "complete-branch-postcondition",
    ("core::slice::element_offset", "rust_1_96_element_offset_unaligned_bridge"): "complete-branch-postcondition",
    ("core::slice::element_offset", "rust_1_96_element_offset_oob_bridge"): "complete-branch-postcondition",
    ("core::slice::element_offset", "rust_1_96_element_offset_some_bridge"): "complete-branch-postcondition",
    ("core::slice::subslice_range", "rust_1_96_subslice_range_unaligned_bridge"): "complete-branch-postcondition",
    ("core::slice::subslice_range", "rust_1_96_subslice_range_oob_bridge"): "complete-branch-postcondition",
    ("core::slice::subslice_range", "rust_1_96_subslice_range_some_bridge"): "complete-branch-postcondition",
    # Definitionally answer-equivalent results.
    ("core::slice::as_ptr_range", "rust_1_96_ptr_add_range_end"): "answer-equivalent-result",
    ("core::slice::as_mut_ptr_range", "rust_1_96_mut_ptr_add_range_end"): "answer-equivalent-result",
    ("core::slice::binary_search", "binary_search_by"): "answer-equivalent-result",
    ("core::slice::binary_search", "rust_1_96_binary_search_ord_result_bridge"): "answer-equivalent-result",
    ("core::slice::binary_search_by_key", "rust_1_96_binary_search_by_key_delegate"): "answer-equivalent-result",
    ("core::slice::binary_search_by_key", "rust_1_96_binary_search_by_key_result_bridge"): "answer-equivalent-result",
    ("core::slice::partition_point", "rust_1_96_partition_point_binary_search_by_predicate"): "answer-equivalent-result",
    ("core::slice::get_disjoint_mut", "get_disjoint_check_valid"): "answer-equivalent-result",
    ("core::slice::write_copy_of_slice", "rust_1_96_maybe_uninit_copy_from_slice_effect"): "answer-equivalent-result",
    # Opaque whole-algorithm results.
    ("core::slice::select_nth_unstable", "partition_at_index"): "opaque-whole-algorithm",
    ("core::slice::select_nth_unstable_by", "partition_at_index_by_compare"): "opaque-whole-algorithm",
    ("core::slice::select_nth_unstable_by_key", "partition_at_index_by_key"): "opaque-whole-algorithm",
    ("core::slice::sort_unstable", "sort"): "opaque-whole-algorithm",
    ("core::slice::sort_unstable_by", "sort"): "opaque-whole-algorithm",
    ("core::slice::sort_unstable_by_key", "sort"): "opaque-whole-algorithm",
    # Admissible pointer/layout/provenance transitions.
    ("core::slice::align_to", "rust_1_96_ptr_align_offset"): "pointer-layout-provenance-transition",
    ("core::slice::align_to_mut", "rust_1_96_ptr_align_offset"): "pointer-layout-provenance-transition",
    ("core::slice::as_chunks_unchecked", "rust_1_96_ptr_cast_array_chunks"): "pointer-layout-provenance-transition",
    ("core::slice::as_chunks_unchecked", "rust_1_96_from_raw_parts_array_chunks"): "pointer-layout-provenance-transition",
    ("core::slice::as_chunks_unchecked_mut", "rust_1_96_mut_ptr_cast_array_chunks"): "pointer-layout-provenance-transition",
    ("core::slice::as_flattened_mut", "rust_1_96_array_mut_ptr_cast_relation"): "pointer-layout-provenance-transition",
    ("core::slice::as_mut_array", "rust_1_96_mut_ptr_cast_array"): "pointer-layout-provenance-transition",
    ("core::slice::first_chunk_mut", "rust_1_96_mut_ptr_cast_array"): "pointer-layout-provenance-transition",
    ("core::slice::split_first_chunk_mut", "rust_1_96_mut_ptr_cast_array"): "pointer-layout-provenance-transition",
    ("core::slice::element_offset", "rust_1_96_ptr_from_ref"): "pointer-layout-provenance-transition",
    ("core::slice::write_copy_of_slice", "rust_1_96_maybe_uninit_slice_as_ptr"): "pointer-layout-provenance-transition",
    ("core::slice::write_copy_of_slice", "rust_1_96_maybe_uninit_slice_as_mut_ptr"): "pointer-layout-provenance-transition",
    ("core::slice::write_copy_of_slice", "copy_nonoverlapping"): "pointer-layout-provenance-transition",
    ("core::slice::write_copy_of_slice", "rust_1_96_same_layout_transmute_src"): "pointer-layout-provenance-transition",
    # Admissible intermediate raw-slice constructors.
    ("core::slice::as_chunks", "from_raw_parts"): "intermediate-raw-slice-constructor",
    ("core::slice::as_chunks_mut", "from_raw_parts_mut"): "intermediate-raw-slice-constructor",
    ("core::slice::split_at_mut_checked", "from_raw_parts_mut"): "intermediate-raw-slice-constructor",
    ("core::slice::split_at_mut_unchecked", "from_raw_parts_mut"): "intermediate-raw-slice-constructor",
    ("core::slice::split_first_chunk_mut", "from_raw_parts_mut"): "intermediate-raw-slice-constructor",
    # Admissible intermediate source splits.
    ("core::slice::as_chunks", "rust_1_96_split_at_unchecked_raw_parts"): "intermediate-subrange-split",
    ("core::slice::as_chunks_mut", "rust_1_96_split_at_mut_unchecked_raw_parts"): "intermediate-subrange-split",
    ("core::slice::split_first_chunk_mut", "rust_1_96_split_at_mut_unchecked_raw_parts"): "intermediate-subrange-split",
    # Admissible lower callees on derived borrows.
    ("core::slice::as_chunks", "as_chunks_unchecked"): "derived-borrow-source-callee",
    ("core::slice::as_chunks_mut", "as_chunks_unchecked_mut"): "derived-borrow-source-callee",
    ("core::slice::as_rchunks", "rust_1_96_as_chunks_unchecked_view"): "derived-borrow-source-callee",
    ("core::slice::as_rchunks_mut", "rust_1_96_as_chunks_unchecked_mut_view"): "derived-borrow-source-callee",
    ("core::slice::last_chunk_mut", "rust_1_96_last_chunk_mut_array_ref"): "derived-borrow-source-callee",
    ("core::slice::split_first_chunk_mut", "rust_1_96_split_first_chunk_mut_array_ref"): "derived-borrow-source-callee",
    ("core::slice::split_last_chunk_mut", "rust_1_96_split_last_chunk_mut_array_ref"): "derived-borrow-source-callee",
    ("core::slice::write_clone_of_slice", "rust_1_96_assume_init_mut_raw_cast"): "derived-borrow-source-callee",
    ("core::slice::write_copy_of_slice", "rust_1_96_assume_init_mut_raw_cast"): "derived-borrow-source-callee",
    ("core::slice::align_to", "rust_1_96_align_to_from_raw_parts"): "derived-borrow-source-callee",
    # Admissible arithmetic and offset facts.
    ("core::slice::align_to", "rust_1_96_align_to_offsets_mul_fits"): "arithmetic-or-offset-fact",
    ("core::slice::align_to_mut", "rust_1_96_align_to_offsets_mul_fits"): "arithmetic-or-offset-fact",
    ("core::slice::align_to", "rust_1_96_align_to_offsets_view_bridge"): "arithmetic-or-offset-fact",
    ("core::slice::as_flattened_mut", "rust_1_96_unchecked_mul"): "arithmetic-or-offset-fact",
    # Admissible panic edges.
    ("core::slice::as_flattened_mut", "rust_1_96_slice_len_overflow_panic"): "panic-edge",
    ("core::slice::element_offset", "rust_1_96_element_offset_zst_panic"): "panic-edge",
    ("core::slice::subslice_range", "rust_1_96_subslice_range_zst_panic"): "panic-edge",
    # Admissible callback and individual-element effects.
    ("core::slice::binary_search", "rust_1_96_ord_cmp_observe"): "callback-or-element-effect",
    ("core::slice::binary_search_by", "rust_1_96_sliceindex_get_unchecked_ref"): "callback-or-element-effect",
    ("core::slice::binary_search_by", "rust_1_96_fnmut_ordering_observe"): "callback-or-element-effect",
    ("core::slice::clone_from_slice", "rust_1_96_clone_from_at"): "callback-or-element-effect",
    ("core::slice::fill", "rust_1_96_clone_from_value_at"): "callback-or-element-effect",
    ("core::slice::write_clone_of_slice", "rust_1_96_write_cloned_at"): "callback-or-element-effect",
    ("core::slice::write_clone_of_slice", "rust_1_96_write_clone_iteration_effect"): "callback-or-element-effect",
}

# Every selected dependency record is explicitly present in exactly one base
# category. Linked external-site dispositions are propagated after this audit.
DEPENDENCY_CONTEXT_ONLY_RECORD_IDS = frozenset(
    """
TS-008-D001 TS-009-D001 TS-012-D001 TS-013-D001 TS-014-D001 TS-015-D001
TS-017-D001 TS-018-D001 TS-019-D002 TS-020-D001 TS-021-D002 TS-022-D001
TS-023-D001 TS-024-D001 TS-025-D001 TS-026-D001 TS-028-D001 TS-029-D001
TS-030-D001 TS-037-D001 TS-039-D001 TS-043-D001 TS-046-D001 TS-047-D002
TS-048-D001 TS-049-D001 TS-051-D001 TS-052-D001 TS-053-D002 TS-054-D001
TS-055-D001 TS-062-D001 TS-065-D001 TS-077-D001 TS-078-D001 TS-079-D001
TS-080-D001 TS-081-D001 TS-082-D001 TS-085-D001 TS-086-D001 TS-090-D001
TS-096-D001 TS-111-D001 TS-119-D001 TS-120-D001
""".split()
)
DEPENDENCY_ADMISSIBLE_RECORD_IDS = frozenset(
    """
TS-008-D002 TS-008-D003 TS-008-D004 TS-009-D002 TS-009-D003 TS-009-D004
TS-012-D002 TS-012-D003 TS-012-D004 TS-013-D002 TS-013-D003 TS-013-D004
TS-014-D002 TS-014-D003 TS-014-D004 TS-014-D005 TS-014-D006 TS-015-D002
TS-015-D003 TS-015-D004 TS-015-D005 TS-015-D006 TS-017-D002 TS-017-D003
TS-017-D004 TS-017-D005 TS-017-D006 TS-018-D002 TS-018-D003 TS-018-D004
TS-020-D002 TS-020-D003 TS-020-D004 TS-022-D002
TS-022-D003 TS-022-D004 TS-023-D002 TS-023-D003 TS-023-D004 TS-024-D002
TS-024-D003 TS-024-D004 TS-025-D002 TS-025-D003 TS-026-D002 TS-028-D002
TS-028-D003 TS-028-D004 TS-029-D002 TS-029-D003 TS-029-D004 TS-029-D005
TS-030-D002 TS-030-D003 TS-030-D004 TS-030-D005 TS-030-D006 TS-032-D001
TS-032-D002 TS-032-D003 TS-032-D004 TS-035-D001 TS-035-D002 TS-035-D003
TS-035-D004 TS-035-D005 TS-036-D001 TS-036-D002 TS-036-D003 TS-036-D004
TS-037-D002 TS-037-D003 TS-037-D004 TS-039-D002 TS-039-D003 TS-039-D004
TS-039-D005 TS-039-D006 TS-043-D002 TS-043-D003 TS-043-D004 TS-043-D005
TS-046-D002 TS-046-D003 TS-046-D004 TS-047-D001 TS-048-D002 TS-049-D002
TS-051-D002 TS-051-D003 TS-051-D004 TS-052-D002 TS-052-D003 TS-052-D004
TS-054-D002 TS-055-D002 TS-062-D002 TS-062-D003 TS-065-D002 TS-065-D003
TS-068-D001 TS-068-D002 TS-068-D003 TS-068-D004 TS-068-D005 TS-069-D001
TS-069-D002 TS-069-D003 TS-069-D004 TS-074-D001 TS-074-D002 TS-074-D003
TS-074-D004 TS-076-D001 TS-076-D002 TS-076-D003 TS-076-D004 TS-077-D002
TS-077-D003 TS-078-D002 TS-078-D003 TS-078-D004 TS-079-D002 TS-079-D003
TS-079-D004 TS-080-D002 TS-080-D003 TS-081-D002 TS-081-D003 TS-081-D004
TS-082-D002 TS-082-D003 TS-082-D004 TS-085-D002 TS-085-D003 TS-086-D002
TS-086-D003 TS-086-D004 TS-086-D005 TS-090-D002 TS-090-D003 TS-090-D004
TS-091-D001 TS-093-D001 TS-093-D002 TS-093-D003 TS-093-D004 TS-096-D002
TS-096-D003 TS-097-D001 TS-098-D001 TS-098-D002 TS-098-D003 TS-098-D004
TS-099-D001 TS-099-D002 TS-099-D003 TS-101-D001 TS-101-D002 TS-101-D003
TS-103-D001 TS-103-D002 TS-103-D003 TS-104-D001 TS-104-D002 TS-104-D003
TS-104-D004 TS-106-D001 TS-106-D002 TS-106-D003 TS-106-D004 TS-111-D002
TS-111-D003 TS-111-D004 TS-111-D005 TS-111-D006 TS-119-D002 TS-119-D003
TS-119-D004 TS-120-D002 TS-120-D003 TS-120-D004 TS-120-D005
""".split()
)
DEPENDENCY_INTRINSIC_INADMISSIBLE = {
    "TS-019-D001": (
        "The synthetic as_mut_ptr helper constructs a null-provenance pointer "
        "whose address is the slice length and ensures the complete public "
        "slice-start/final-frame postcondition. Canonical Rust 1.96 instead uses "
        "`self as *mut [T] as *mut T`; this helper repeats the target answer "
        "rather than modeling that cast."
    ),
    "TS-021-D001": (
        "The synthetic as_ptr helper constructs a null-provenance pointer whose "
        "address is the slice length and ensures the complete public slice-start "
        "postcondition. Canonical Rust 1.96 instead uses "
        "`self as *const [T] as *const T`; this helper repeats the target answer "
        "rather than modeling that cast."
    ),
    "TS-053-D001": (
        "The SliceIndex::get_mut trait-method contract is definitionally identical "
        "to the public get_mut target contract, and the target body is only that "
        "delegation."
    ),
}
AUDITED_DEPENDENCY_RECORD_IDS = (
    DEPENDENCY_CONTEXT_ONLY_RECORD_IDS
    | DEPENDENCY_ADMISSIBLE_RECORD_IDS
    | DEPENDENCY_INTRINSIC_INADMISSIBLE.keys()
)

PREVIOUSLY_UNLINKED_EXTERNAL_SITES = {
    (
        "core::slice::align_to",
        "rust_1_96_align_to_zst_or_overflow_result",
    ),
    ("core::slice::as_chunks", "from_raw_parts"),
    (
        "core::slice::as_chunks",
        "rust_1_96_split_at_unchecked_raw_parts",
    ),
    ("core::slice::as_chunks_mut", "from_raw_parts_mut"),
    (
        "core::slice::as_chunks_mut",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ),
    (
        "core::slice::as_flattened_mut",
        "rust_1_96_slice_len_overflow_panic",
    ),
    ("core::slice::as_flattened_mut", "rust_1_96_unchecked_mul"),
    ("core::slice::clone_from_slice", "rust_1_96_clone_from_at"),
    ("core::slice::split_at_mut_checked", "from_raw_parts_mut"),
    (
        "core::slice::split_at_mut_checked",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ),
    ("core::slice::split_first_chunk_mut", "from_raw_parts_mut"),
    (
        "core::slice::split_first_chunk_mut",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ),
    (
        "core::slice::write_clone_of_slice",
        "rust_1_96_assume_init_mut_raw_cast",
    ),
    (
        "core::slice::write_copy_of_slice",
        "rust_1_96_assume_init_mut_raw_cast",
    ),
}

# Local dependency-record indices used when symbol spelling alone cannot bind an
# external-body site to the source-backed manifest record that explains it.
EXTERNAL_DEPENDENCY_LINK_OVERRIDES = {
    (
        "core::slice::align_to",
        "rust_1_96_align_to_zst_or_overflow_result",
    ): (1,),
    (
        "core::slice::align_to",
        "rust_1_96_align_to_split_raw_parts_result",
    ): (4,),
    (
        "core::slice::align_to_mut",
        "rust_1_96_align_to_mut_zst_or_overflow",
    ): (4,),
    (
        "core::slice::align_to_mut",
        "rust_1_96_align_to_mut_from_split_raw_parts",
    ): (4,),
    (
        "core::slice::as_chunks",
        "from_raw_parts",
    ): (2,),
    (
        "core::slice::as_chunks",
        "rust_1_96_split_at_unchecked_raw_parts",
    ): (2,),
    (
        "core::slice::as_chunks_mut",
        "from_raw_parts_mut",
    ): (2,),
    (
        "core::slice::as_chunks_mut",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ): (2,),
    (
        "core::slice::as_flattened_mut",
        "rust_1_96_slice_len_overflow_panic",
    ): (4,),
    (
        "core::slice::as_flattened_mut",
        "rust_1_96_unchecked_mul",
    ): (4,),
    (
        "core::slice::clone_from_slice",
        "rust_1_96_clone_from_at",
    ): (2, 3),
    (
        "core::slice::get_disjoint_mut",
        "get_disjoint_check_valid",
    ): (2,),
    (
        "core::slice::split_at_mut_checked",
        "from_raw_parts_mut",
    ): (2,),
    (
        "core::slice::split_at_mut_checked",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ): (2,),
    (
        "core::slice::split_first_chunk_mut",
        "from_raw_parts_mut",
    ): (2,),
    (
        "core::slice::split_first_chunk_mut",
        "rust_1_96_split_at_mut_unchecked_raw_parts",
    ): (2,),
    (
        "core::slice::write_clone_of_slice",
        "rust_1_96_assume_init_mut_raw_cast",
    ): (2,),
    (
        "core::slice::write_copy_of_slice",
        "rust_1_96_assume_init_mut_raw_cast",
    ): (5,),
    (
        "core::slice::select_nth_unstable",
        "partition_at_index",
    ): (2,),
    (
        "core::slice::select_nth_unstable_by",
        "partition_at_index_by_compare",
    ): (2, 3),
    (
        "core::slice::select_nth_unstable_by_key",
        "partition_at_index_by_key",
    ): (2, 3),
    (
        "core::slice::sort_unstable",
        "sort",
    ): (2,),
    (
        "core::slice::sort_unstable_by",
        "sort",
    ): (2, 3),
    (
        "core::slice::sort_unstable_by_key",
        "sort",
    ): (2, 3),
}

CLASSIFICATION_VOCABULARY = [
    "conditional-complete",
    "conditional-incomplete",
    "boundary-insufficient",
    "missing-source-backed-model",
    "checker-unsupported",
    "solver-unknown",
]

BOUNDARY_SCHEMAS: dict[str, dict[str, Any]] = {
    "iterator-or-subslice-state-boundary": {
        "schema_id": "iterator_private_state_v1",
        "allowed_observations": [
            "input borrow and allocation identity",
            "iterator front/back cursor and remaining source range",
            "private chunk or split state read by the implementation proof",
            "individual source-backed raw-slice constructor observations",
        ],
        "assumption": (
            "Boundary_T fixes the input borrow/allocation identity and only the "
            "iterator, range, or raw-slice-constructor observations consumed by "
            "the proof. Target-returned references, aggregate post-state, and a "
            "complete execution trace remain outside b."
        ),
        "model_requirement": (
            "The target definition must derive returned subranges and borrow "
            "observations from these inputs with source-backed transitions."
        ),
    },
    "raw-pointer-provenance-boundary": {
        "schema_id": "raw_input_memory_provenance_v1",
        "allowed_observations": [
            "input allocation identity, base address, provenance, and alive range",
            "input length and pointer metadata",
            "source and destination element layouts, alignment, and ZST flags",
            "individual source-backed pointer arithmetic or alignment-helper observations",
        ],
        "assumption": (
            "Boundary_T fixes the hidden raw representation of the input and "
            "only source-used pointer/layout helper observations. It does not "
            "contain the returned pointer, returned ranges, aggregate post-state, "
            "or an encoding of the selected output."
        ),
        "model_requirement": (
            "The target definition must compute pointer/range observations from "
            "the fixed input memory model and reviewed Rust transition semantics."
        ),
    },
    "mutable-reference-view-boundary": {
        "schema_id": "mutable_borrow_transition_v1",
        "allowed_observations": [
            "input root allocation, provenance, and borrow identity",
            "source-backed subrange and alias-permission transitions",
            "individual caller mutation events and their local state transitions",
        ],
        "assumption": (
            "Boundary_T fixes the input mutable-borrow identity and any genuine "
            "caller mutation transitions already represented by the proof. It "
            "does not freeze returned references, aggregate post-state, or a "
            "complete target trace."
        ),
        "model_requirement": (
            "The target definition must construct returned borrow identities and "
            "frames from source-backed range and ownership transitions."
        ),
    },
    "unstable-sort-or-selection-boundary": {
        "schema_id": "comparator_state_transition_v1",
        "allowed_observations": [
            "callback or comparator arguments and results at source invocation sites",
            "callback pre/post state transitions and panic observations",
            "input element identity and initial sequence",
        ],
        "assumption": (
            "Boundary_T fixes genuine comparator/callback observations and state "
            "transitions used by the proof. It never fixes pivots, swaps, a final "
            "permutation, the selected element, aggregate post-state, or a full "
            "algorithm trace."
        ),
        "model_requirement": (
            "The private sort/selection transitions must be modeled from Rust "
            "source; an opaque functionality relation is not admissible."
        ),
    },
    "duplicate-or-callback-search-boundary": {
        "schema_id": "search_callback_transition_v1",
        "allowed_observations": [
            "comparison or predicate arguments and results at source invocation sites",
            "callback pre/post state transitions, call count, and panic observations",
            "input sequence identity and sortedness assumptions in Requires_T",
        ],
        "assumption": (
            "Boundary_T fixes only comparator/predicate observations and callback "
            "state transitions actually consumed by the search proof. It does not "
            "contain a chosen index, insertion point, returned Result, or an "
            "equivalent answer encoding."
        ),
        "model_requirement": (
            "The source search loop must derive an Ok matching index or the exact "
            "Err insertion point from the shared input and callback observations."
        ),
    },
    "maybeuninit-storage-boundary": {
        "schema_id": "maybeuninit_storage_transition_v1",
        "allowed_observations": [
            "input storage identity, slot initialization mask, and initialized values",
            "individual source-backed raw copy, write, read, or drop transitions",
            "destructor or clone callback results and local state transitions",
        ],
        "assumption": (
            "Boundary_T fixes the initial raw-storage state and only primitive "
            "memory/destructor observations used by the proof. It does not contain "
            "the aggregate resulting storage, returned reference, selected output, "
            "or a complete target execution trace."
        ),
        "model_requirement": (
            "The target definition must compose the primitive storage transitions "
            "with explicit initialization and provenance semantics."
        ),
    },
    "clone-or-callback-effect-boundary": {
        "schema_id": "clone_callback_transition_v1",
        "allowed_observations": [
            "per-call Clone or comparison arguments and return observations",
            "callback pre/post state transitions and panic observations",
            "source-backed per-element write transition observations",
        ],
        "assumption": (
            "Boundary_T fixes each genuine user trait/callback observation and its "
            "local state transition. It does not freeze the aggregate destination "
            "state or repeat the target postcondition."
        ),
        "model_requirement": (
            "The target definition must fold source-ordered callback and write "
            "transitions rather than appeal to a functionality axiom."
        ),
    },
    "disjoint-mutable-alias-boundary": {
        "schema_id": "disjoint_index_provenance_v1",
        "allowed_observations": [
            "input allocation, provenance, and mutable borrow permissions",
            "SliceIndex input-to-range resolution observations",
            "source-backed pairwise disjointness and raw-slice construction transitions",
        ],
        "assumption": (
            "Boundary_T fixes input provenance/permissions and hidden SliceIndex "
            "range resolution used by the proof. It does not contain the returned "
            "reference array, aggregate post-state, or an answer-equivalent alias map."
        ),
        "model_requirement": (
            "The target definition must derive returned disjoint borrows from the "
            "resolved input ranges and Rust ownership/provenance transitions."
        ),
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_ws(text: str) -> str:
    return " ".join(text.split())


def canonical_contract(text: str) -> str:
    text = re.sub(r"#\[\s*verifier::allow\([^\]]+\)\s*\]", "", text)
    canonical = re.sub(r"\s+", "", text)
    while ",)" in canonical:
        canonical = canonical.replace(",)", ")")
    canonical = canonical.replace(",;", ";")
    canonical = re.sub(r",(requires|ensures|recommends)", r"\1", canonical)
    return canonical


def safe_name(value: str) -> str:
    return re.sub(
        r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", value)
    ).strip("_")


def target_artifact_id(target: str, input_order: int) -> str:
    return f"{input_order:03d}_{safe_name(target)}"


def json_compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def relpath(path: Path) -> str:
    return path.resolve().relative_to(OUT.resolve()).as_posix()


def extract_active_run_id(result_path: str) -> str:
    parts = Path(result_path).parts
    try:
        index = parts.index("slice_feedback_determinism")
    except ValueError as exc:
        raise ValueError(f"result path lacks determinism directory: {result_path}") from exc
    if index + 1 >= len(parts):
        raise ValueError(f"result path lacks active run id: {result_path}")
    return parts[index + 1]


def derive_scope() -> dict[str, Any]:
    manifest = json.loads(LATEST_MANIFEST.read_text())
    catalog_rows = read_csv(CATALOG)
    proof_rows = [
        row for row in read_csv(TARGETS_180) if row.get("module") == "slice"
    ]
    proof_order_rows = [
        row for row in read_csv(PROOF_ORDER) if row.get("module") == "slice"
    ]

    manifest_rows = manifest.get("results", [])
    if len({row["target"] for row in manifest_rows}) != len(manifest_rows):
        raise ValueError("active feedback manifest contains duplicate targets")
    if len({row["target"] for row in catalog_rows}) != len(catalog_rows):
        raise ValueError("active catalog contains duplicate targets")
    if len({row["target"] for row in proof_rows}) != len(proof_rows):
        raise ValueError("Slice implementation-proof inventory contains duplicate targets")

    catalog_by_target = {row["target"]: row for row in catalog_rows}
    proof_by_target = {row["target"]: row for row in proof_rows}
    proof_order_by_target = {row["target"]: row for row in proof_order_rows}
    generated_targets = {
        row["target"] for row in catalog_rows if row["status"] == GENERATED_STATUS
    }
    exact_vstd_targets = {
        row["target"] for row in catalog_rows if row["status"] == EXACT_VSTD_STATUS
    }
    manifest_targets = {row["target"] for row in manifest_rows}
    if manifest_targets != generated_targets:
        raise ValueError(
            "active feedback manifest target set does not equal generated catalog rows"
        )

    computed_r0 = Counter(row["r0_z3"] for row in manifest_rows)
    if dict(computed_r0) != manifest.get("r0_z3_counts"):
        raise ValueError("active feedback manifest headline counts do not match rows")
    if any(row.get("status") != "ok" for row in manifest_rows):
        raise ValueError("active feedback manifest contains a non-ok row")

    missing_proof = generated_targets - proof_by_target.keys()
    if missing_proof:
        raise ValueError(f"generated targets missing implementation proofs: {missing_proof}")
    missing_order = generated_targets - proof_order_by_target.keys()
    if missing_order:
        raise ValueError(f"generated targets missing proof-order rows: {missing_order}")

    selected_manifest_rows = [
        row
        for row in manifest_rows
        if row["r0_z3"] == "unknown"
        and catalog_by_target[row["target"]]["status"] == GENERATED_STATUS
    ]
    selected_manifest_rows.sort(
        key=lambda row: int(proof_by_target[row["target"]]["input_order"])
    )
    selected_targets = [row["target"] for row in selected_manifest_rows]
    run_ids = {extract_active_run_id(row["result_json"]) for row in manifest_rows}
    if len(run_ids) != 1:
        raise ValueError(f"active feedback rows span multiple runs: {run_ids}")

    return {
        "manifest": manifest,
        "manifest_rows": manifest_rows,
        "catalog_rows": catalog_rows,
        "catalog_by_target": catalog_by_target,
        "proof_rows": proof_rows,
        "proof_by_target": proof_by_target,
        "proof_order_by_target": proof_order_by_target,
        "generated_targets": generated_targets,
        "exact_vstd_targets": exact_vstd_targets,
        "selected_manifest_rows": selected_manifest_rows,
        "selected_targets": selected_targets,
        "active_run_id": next(iter(run_ids)),
        "active_run_dir": (
            SPECGEN
            / "verification/evidence/slice_feedback_determinism"
            / next(iter(run_ids))
        ),
        "counts": {
            "catalog_total": len(catalog_rows),
            "generated": len(generated_targets),
            "exact_vstd": len(exact_vstd_targets),
            "r0_unknown": computed_r0["unknown"],
            "r0_unsat": computed_r0["unsat"],
            "selected": len(selected_targets),
        },
        "reason_counts": dict(
            Counter(row["unknown_reason_class"] for row in selected_manifest_rows)
        ),
    }


def proof_paths(target: str, input_order: int) -> dict[str, Path]:
    artifact_id = target_artifact_id(target, input_order)
    manifest_dir = IMPLPROOF / "proof_manifests" / artifact_id
    harness_dir = IMPLPROOF / "proof_harnesses" / artifact_id
    return {
        "artifact_id": Path(artifact_id),
        "harness": harness_dir / "harness.rs",
        "source_body": manifest_dir / "source_body.json",
        "transformation": manifest_dir / "transformation_manifest.json",
        "dependency": manifest_dir / "dependency_assumption_manifest.json",
    }


def extract_generated_declarations(path: Path = GENERATED_SPECS) -> list[dict[str, Any]]:
    lines = path.read_text().splitlines()
    declarations: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        if not lines[index].startswith("pub assume_specification"):
            index += 1
            continue
        start = index
        while start > 0 and lines[start - 1].strip().startswith("#["):
            start -= 1
        while index < len(lines) and lines[index].strip() != ";":
            index += 1
        if index >= len(lines):
            raise ValueError(f"unterminated generated declaration at line {start + 1}")
        text = "\n".join(lines[start : index + 1]) + "\n"
        declarations.append(
            {
                "start_line": start + 1,
                "end_line": index + 1,
                "text": text,
                "normalized": normalize_ws(text),
                "canonical": canonical_contract(text),
                "sha256": sha256_text(text),
            }
        )
        index += 1
    return declarations


def bind_generated_declarations(
    catalog_rows: Iterable[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    by_normalized: dict[str, list[dict[str, Any]]] = {}
    for declaration in extract_generated_declarations():
        by_normalized.setdefault(declaration["canonical"], []).append(declaration)

    bound: dict[str, dict[str, Any]] = {}
    for row in catalog_rows:
        if row["status"] != GENERATED_STATUS:
            continue
        matches = by_normalized.get(canonical_contract(row["contract_text"]), [])
        if len(matches) != 1:
            raise ValueError(
                f"{row['target']}: expected one executable generated declaration, "
                f"found {len(matches)}"
            )
        bound[row["target"]] = matches[0]
    return bound


def canonical_source_record(source_body_manifest: dict[str, Any]) -> dict[str, Any]:
    relative = source_body_manifest["source_reference_path"]
    if not relative.startswith("core/"):
        raise ValueError(f"selected target source is not canonical core: {relative}")
    path = RUST_LIBRARY / relative
    lines = path.read_text().splitlines()
    span = source_body_manifest["span"]
    start = int(span["signature_start_line"])
    end = int(span["body_end_line"])
    item_text = "\n".join(lines[start - 1 : end]) + "\n"

    nearest_doc: int | None = None
    for cursor in range(start - 2, max(-1, start - 302), -1):
        stripped = lines[cursor].strip()
        if stripped.startswith("///"):
            nearest_doc = cursor
            break
        if re.search(r"\bpub(?:\s+const|\s+unsafe)?\s+fn\b", stripped):
            break
    accepted: list[tuple[int, str]] = []
    if nearest_doc is not None:
        cursor = nearest_doc
        while cursor >= 0 and lines[cursor].strip().startswith("///"):
            accepted.append((cursor + 1, lines[cursor]))
            cursor -= 1
        accepted.reverse()
    docs_text = "\n".join(
        line.split("///", 1)[1].lstrip()
        for _, line in accepted
        if line.strip().startswith("///")
    ).strip()
    docs_text = docs_text + ("\n" if docs_text else "")
    doc_lines = [line_number for line_number, _ in accepted]
    doc_reference = (
        f"{relative}:{min(doc_lines)}-{max(doc_lines)}" if doc_lines else ""
    )
    return {
        "path": path,
        "relative_path": relative,
        "source_file_sha256": sha256(path),
        "source_item_text": item_text,
        "source_item_sha256": sha256_text(item_text),
        "source_item_start_line": start,
        "source_item_end_line": end,
        "public_docs_text": docs_text,
        "public_docs_sha256": sha256_text(docs_text),
        "public_docs_reference": doc_reference,
        "public_docs_start_line": min(doc_lines) if doc_lines else "",
        "public_docs_end_line": max(doc_lines) if doc_lines else "",
    }


def external_body_sites(harness: Path) -> list[dict[str, Any]]:
    lines = harness.read_text().splitlines()
    sites: list[dict[str, Any]] = []
    attribute = re.compile(r"#\s*\[\s*verifier::external_body\s*\]")
    function = re.compile(r"\bfn\s+([A-Za-z_][A-Za-z0-9_]*)")
    for index, line in enumerate(lines):
        if not attribute.search(line):
            continue
        declaration_index: int | None = None
        symbol = ""
        for cursor in range(index + 1, min(len(lines), index + 50)):
            match = function.search(lines[cursor])
            if match:
                declaration_index = cursor
                symbol = match.group(1)
                break
            if attribute.search(lines[cursor]):
                break
        if declaration_index is None:
            raise ValueError(
                f"{harness}:{index + 1}: external_body has no following function"
            )
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
                f"{harness}:{declaration_index + 1}: external_body contract has no body"
            )
        signature_lines: list[str] = []
        depth = 0
        for cursor in range(declaration_index, min(len(lines), declaration_index + 60)):
            signature_lines.append(lines[cursor].strip())
            depth += lines[cursor].count("(") - lines[cursor].count(")")
            if depth <= 0 and (
                "{" in lines[cursor]
                or lines[cursor].strip().endswith(";")
                or lines[cursor].strip().startswith(("requires", "ensures"))
            ):
                break
        sites.append(
            {
                "attribute_line": index + 1,
                "declaration_line": declaration_index + 1,
                "symbol": symbol,
                "signature": " ".join(signature_lines),
                "contract_end_line": contract_end_line,
                "contract_text": "\n".join(contract_lines).strip() + "\n",
            }
        )
    return sites


def target_function_is_external(
    harness: Path,
    target_leaf: str,
    sites: list[dict[str, Any]] | None = None,
) -> bool:
    lines = harness.read_text().splitlines()
    depth = 0
    target_declarations: list[tuple[int, int]] = []
    pattern = re.compile(rf"\bfn\s+{re.escape(target_leaf)}\b")
    for index, line in enumerate(lines, start=1):
        if pattern.search(line):
            target_declarations.append((index, depth))
        code = line.split("//", 1)[0]
        depth += code.count("{") - code.count("}")
    if not target_declarations:
        raise ValueError(f"{harness}: no function declaration for {target_leaf}")
    shallowest = min(item[1] for item in target_declarations)
    target_lines = {
        item[0] for item in target_declarations if item[1] == shallowest
    }
    external_lines = {
        item["declaration_line"] for item in (sites or external_body_sites(harness))
    }
    return bool(target_lines & external_lines)


def equivalence_for_target(target: str) -> dict[str, str]:
    if target in BINARY_SEARCH_TARGETS:
        return {
            "kind": "matching-index-equivalence",
            "exact_observation_policy": (
                "Err insertion indices and all callback states remain exact; two Ok "
                "returns are equivalent only when each index names a matching element."
            ),
            "positive_witness": "evidence/equivalence/binary_search_duplicate.positive.smt2",
            "negative_witness": "evidence/equivalence/binary_search_duplicate.negative.smt2",
        }
    if target in UNSTABLE_SORT_TARGETS:
        return {
            "kind": "equal-key-reordering-equivalence",
            "exact_observation_policy": (
                "Unit return, exact identity multiplicities over both result "
                "sequences, position-wise key order, callback state, and all "
                "non-tie observations remain exact; only identities within an "
                "equal-key class may reorder."
            ),
            "positive_witness": "evidence/equivalence/unstable_sort_equal_keys.positive.smt2",
            "negative_witness": "evidence/equivalence/unstable_sort_equal_keys.negative.smt2",
        }
    return {
        "kind": "exact-principal-return-and-final-state",
        "exact_observation_policy": (
            "Principal return values, returned reference identities, and final-state "
            "observations are compared by exact equality."
        ),
        "positive_witness": "",
        "negative_witness": "",
    }
