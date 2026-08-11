#!/usr/bin/env python3
"""Validate all_slice_specs.rs against inventory and catalog requirements."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from io import StringIO
import json
import re
import sys
from pathlib import Path


EXPECTED_EXISTING_VSTD = {
    "core::slice::copy_from_slice",
    "core::slice::copy_within",
    "core::slice::first",
    "core::slice::first_mut",
    "core::slice::get",
    "core::slice::is_empty",
    "core::slice::iter",
    "core::slice::last",
    "core::slice::last_mut",
    "core::slice::len",
    "core::slice::split_at",
    "core::slice::split_at_mut",
}

REQUIRED_MARKER_FIELDS = {
    "status",
    "family",
    "source",
    "signature",
    "requires",
    "ensures",
    "shared_helpers",
    "typecheck_result",
    "determinism_result",
    "target_binding_result",
    "signature_shape_result",
    "generic_bounds_result",
    "reviewer_notes",
    "contract_text",
}

RELATIONAL_TOKENS = (
    "@",
    "Seq",
    "subrange",
    "update",
    "old(",
    "final(",
    "permutation",
    "sorted",
    "partition",
    "prefix",
    "suffix",
    "pointer",
    "provenance",
    "len",
    "range",
    "remainder",
    "ascii",
    "utf8",
    "initialized",
    "drop",
)

BANNED_CONTRACT_FRAGMENTS = (
    "ensures true",
    "requires false",
    "arbitrary()",
    "fresh_uninterp",
    "fresh uninterp",
    "unconstrained result",
    "result == fresh",
)
FEEDBACK_DETERMINISM_MANIFEST = Path(
    "verification/evidence/slice_feedback_determinism/latest_manifest.json"
)
SHARED_HELPER_TARGET_AUDIT_JSON = Path("verification/shared_helper_target_usage_audit.json")
SHARED_HELPER_TARGET_AUDIT_CSV = Path("verification/shared_helper_target_usage_audit.csv")
STALE_DIRECT_DETERMINISM_FRAGMENTS = (
    "0 exec ensures targets",
    "verusage runner",
    "assume_specification harness",
)
STALE_REVIEWER_NOTE_FRAGMENTS = (
    "determinism checker result recorded honestly as unsupported",
)
UNKNOWN_REASON_CLASSES = {
    "clone-or-callback-effect-boundary",
    "disjoint-mutable-alias-boundary",
    "duplicate-or-callback-search-boundary",
    "iterator-or-subslice-state-boundary",
    "maybeuninit-storage-boundary",
    "mutable-reference-view-boundary",
    "raw-pointer-provenance-boundary",
    "unstable-sort-or-selection-boundary",
}

BOOTSTRAP_EXECUTABLE_CONTRACTS = {
    "core::slice::contains": (
        "pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::contains ]",
        "b <==> slice_contains_value(slice@, *x)",
    ),
    "core::slice::starts_with": (
        "pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::starts_with ]",
        "b <==> slice_is_prefix(slice@, needle@)",
    ),
    "core::slice::ends_with": (
        "pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::ends_with ]",
        "b <==> slice_is_suffix(slice@, needle@)",
    ),
}

FIND_LIKE_SEARCH_EXECUTABLE_CONTRACTS = {
    "core::slice::binary_search": (
        "pub assume_specification<T: core::cmp::Ord>[ <[T]>::binary_search ]",
        "slice_binary_search_result(slice@, *x, result)",
    ),
    "core::slice::binary_search_by": (
        "<[T]>::binary_search_by::<F>",
        "slice_binary_search_by_result(slice@, f, result)",
    ),
    "core::slice::binary_search_by_key": (
        "<[T]>::binary_search_by_key::<B, F>",
        "slice_binary_search_by_key_result::<F, T, B>(slice@, *key, f, result)",
    ),
    "core::slice::partition_point": (
        "pub assume_specification<T, P: core::ops::FnMut(&T) -> bool>[ <[T]>::partition_point::<P> ]",
        "slice_partition_point_result(slice@, pred, index)",
    ),
}

MUTATION_EXECUTABLE_CONTRACTS = {
    "core::slice::clone_from_slice": (
        "pub assume_specification<T: core::clone::Clone>[ <[T]>::clone_from_slice ]",
        "slice_cloned_from(src@, final(dst)@)",
    ),
    "core::slice::fill": (
        "pub assume_specification<T: core::clone::Clone>[ <[T]>::fill ]",
        "slice_filled_with_clone(old(slice)@, value, final(slice)@)",
    ),
    "core::slice::fill_with": (
        "pub assume_specification<T, F: core::ops::FnMut() -> T>[ <[T]>::fill_with::<F> ]",
        "final(slice)@ == zero_arg_fnmut_outputs(f, old(slice)@.len())",
    ),
    "core::slice::reverse": (
        "pub assume_specification<T>[ <[T]>::reverse ]",
        "final(slice)@ == slice_reversed(old(slice)@)",
    ),
    "core::slice::rotate_left": (
        "pub assume_specification<T>[ <[T]>::rotate_left ]",
        "final(slice)@ == slice_rotated_left(old(slice)@, mid as int)",
    ),
    "core::slice::rotate_right": (
        "pub assume_specification<T>[ <[T]>::rotate_right ]",
        "final(slice)@ == slice_rotated_right(old(slice)@, k as int)",
    ),
    "core::slice::swap": (
        "pub assume_specification<T>[ <[T]>::swap ]",
        "final(slice)@ == slice_swapped(old(slice)@, a as int, b as int)",
    ),
    "core::slice::swap_with_slice": (
        "pub assume_specification<T>[ <[T]>::swap_with_slice ]",
        "final(slice)@ == old(other)@",
    ),
}

SPLITTING_ITERATOR_EXECUTABLE_CONTRACTS = {
    "core::slice::split_at_checked": (
        "<[T]>::split_at_checked",
        "ret.unwrap().0@ == slice@.subrange(0, mid as int)",
    ),
    "core::slice::split_at_unchecked": (
        "<[T]>::split_at_unchecked",
        "split_point_in_range(slice@, mid)",
    ),
    "core::slice::split_at_mut_checked": (
        "<[T]>::split_at_mut_checked",
        "final(slice)@ == final(ret.unwrap().0)@ + final(ret.unwrap().1)@",
    ),
    "core::slice::split_at_mut_unchecked": (
        "<[T]>::split_at_mut_unchecked",
        "final(slice)@ == final(ret.0)@ + final(ret.1)@",
    ),
    "core::slice::split_first": (
        "<[T]>::split_first",
        "ret.unwrap().1@ == slice@.subrange(1, slice@.len() as int)",
    ),
    "core::slice::split_last": (
        "<[T]>::split_last",
        "ret.unwrap().1@ == slice@.subrange(0, (slice@.len() - 1) as int)",
    ),
    "core::slice::split_first_mut": (
        "<[T]>::split_first_mut",
        "final(slice)@ == seq![*final(ret.unwrap().0)] + final(ret.unwrap().1)@",
    ),
    "core::slice::split_last_mut": (
        "<[T]>::split_last_mut",
        "final(slice)@ == final(ret.unwrap().1)@ + seq![*final(ret.unwrap().0)]",
    ),
    "core::slice::first_chunk": (
        "<[T]>::first_chunk::<N>",
        "array_ref_view(ret.unwrap()) == slice_fixed_prefix::<T, N>(slice@)",
    ),
    "core::slice::last_chunk": (
        "<[T]>::last_chunk::<N>",
        "array_ref_view(ret.unwrap()) == slice_fixed_suffix::<T, N>(slice@)",
    ),
    "core::slice::first_chunk_mut": (
        "<[T]>::first_chunk_mut::<N>",
        "array_value_view(*final(ret.unwrap()))",
    ),
    "core::slice::last_chunk_mut": (
        "<[T]>::last_chunk_mut::<N>",
        "array_value_view(*final(ret.unwrap()))",
    ),
    "core::slice::split_first_chunk": (
        "<[T]>::split_first_chunk::<N>",
        "array_ref_view(ret.unwrap().0) == slice_fixed_prefix::<T, N>(slice@)",
    ),
    "core::slice::split_last_chunk": (
        "<[T]>::split_last_chunk::<N>",
        "array_ref_view(ret.unwrap().1) == slice_fixed_suffix::<T, N>(slice@)",
    ),
    "core::slice::split_first_chunk_mut": (
        "<[T]>::split_first_chunk_mut::<N>",
        "array_value_view(*final(ret.unwrap().0)) + final(ret.unwrap().1)@",
    ),
    "core::slice::split_last_chunk_mut": (
        "<[T]>::split_last_chunk_mut::<N>",
        "final(ret.unwrap().0)@ + array_value_view(*final(ret.unwrap().1))",
    ),
    "core::slice::as_array": (
        "<[T]>::as_array::<N>",
        "array_ref_view(ret.unwrap()) == slice@",
    ),
    "core::slice::as_mut_array": (
        "<[T]>::as_mut_array::<N>",
        "final(slice)@ == array_value_view(*final(ret.unwrap()))",
    ),
    "core::slice::as_chunks": (
        "<[T]>::as_chunks::<N>",
        "slice_array_chunks_partition::<T, N>(slice@, ret.0@, ret.1@)",
    ),
    "core::slice::as_rchunks": (
        "<[T]>::as_rchunks::<N>",
        "slice_array_rchunks_partition::<T, N>(slice@, ret.0@, ret.1@)",
    ),
    "core::slice::as_chunks_unchecked": (
        "<[T]>::as_chunks_unchecked::<N>",
        "flatten_array_chunks::<T, N>(ret@) == slice@",
    ),
    "core::slice::as_chunks_mut": (
        "<[T]>::as_chunks_mut::<N>",
        "final(slice)@ == flatten_array_chunks::<T, N>(final(ret.0)@) + final(ret.1)@",
    ),
    "core::slice::as_rchunks_mut": (
        "<[T]>::as_rchunks_mut::<N>",
        "final(slice)@ == final(ret.0)@ + flatten_array_chunks::<T, N>(final(ret.1)@)",
    ),
    "core::slice::as_chunks_unchecked_mut": (
        "<[T]>::as_chunks_unchecked_mut::<N>",
        "final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@)",
    ),
    "core::slice::iter_mut": (
        "<[T]>::iter_mut",
        "slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining == old(slice)@",
    ),
    "core::slice::chunks": (
        "<[T]>::chunks",
        "slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remainder.len() == 0",
    ),
    "core::slice::chunks_exact": (
        "<[T]>::chunks_exact",
        "!slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).reverse",
        "slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter))",
    ),
    "core::slice::rchunks": (
        "<[T]>::rchunks",
        "slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remainder.len() == 0",
        "slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).reverse",
    ),
    "core::slice::rchunks_exact": (
        "<[T]>::rchunks_exact",
        "slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0",
        "slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter))",
    ),
    "core::slice::windows": (
        "<[T]>::windows",
        "slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remaining == slice@",
        "slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remainder.len() == 0",
    ),
    "core::slice::array_windows": (
        "<[T]>::array_windows::<N>",
        "slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remaining == slice@",
        "slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remainder.len() == 0",
    ),
    "core::slice::ChunksExact::remainder": (
        "core::slice::ChunksExact::<'a, T>::remainder",
        "ret@ == slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).remainder",
    ),
    "core::slice::ChunksExactMut::into_remainder": (
        "core::slice::ChunksExactMut::<'a, T>::into_remainder",
        "ret@ == slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).remainder",
    ),
    "core::slice::Iter::as_slice": (
        "core::slice::Iter::<'a, T>::as_slice",
        "ret@ == slice_iterator_view::<&core::slice::Iter<'a, T>, T>(iter).remaining",
    ),
    "core::slice::IterMut::as_slice": (
        "core::slice::IterMut::<'a, T>::as_slice",
        "ret@ == slice_iterator_view::<&'b core::slice::IterMut<'a, T>, T>(iter).remaining",
    ),
    "core::slice::IterMut::into_slice": (
        "core::slice::IterMut::<'a, T>::into_slice",
        "ret@ == slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining",
    ),
    "core::slice::RChunksExact::remainder": (
        "core::slice::RChunksExact::<'a, T>::remainder",
        "ret@ == slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).remainder",
    ),
    "core::slice::RChunksExactMut::into_remainder": (
        "core::slice::RChunksExactMut::<'a, T>::into_remainder",
        "ret@ == slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).remainder",
    ),
    "core::slice::chunks_mut": (
        "<[T]>::chunks_mut",
        "slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remainder.len() == 0",
    ),
    "core::slice::chunks_exact_mut": (
        "<[T]>::chunks_exact_mut",
        "!slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).reverse",
        "slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter))",
    ),
    "core::slice::rchunks_mut": (
        "<[T]>::rchunks_mut",
        "slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remainder.len() == 0",
        "slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).reverse",
    ),
    "core::slice::rchunks_exact_mut": (
        "<[T]>::rchunks_exact_mut",
        "slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).yielded_prefix.len() == 0",
        "slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter))",
    ),
    "core::slice::split": (
        "<[T]>::split::<F>",
        "slice_predicate_split_view::<core::slice::Split<'a, T, F>, F, T>",
    ),
    "core::slice::split_mut": (
        "<[T]>::split_mut::<F>",
        "slice_predicate_split_view::<core::slice::SplitMut<'a, T, F>, F, T>",
    ),
    "core::slice::split_inclusive": (
        "<[T]>::split_inclusive::<F>",
        "slice_predicate_split_view::<core::slice::SplitInclusive<'a, T, F>, F, T>",
    ),
    "core::slice::split_inclusive_mut": (
        "<[T]>::split_inclusive_mut::<F>",
        "slice_predicate_split_view::<core::slice::SplitInclusiveMut<'a, T, F>, F, T>",
    ),
    "core::slice::splitn": (
        "<[T]>::splitn::<F>",
        "iter, slice@, pred, false, false, n as int",
    ),
    "core::slice::splitn_mut": (
        "<[T]>::splitn_mut::<F>",
        "iter, old(slice)@, pred, false, false, n as int",
    ),
    "core::slice::rsplit": (
        "<[T]>::rsplit::<F>",
        "iter, slice@, pred, false, true, 0",
    ),
    "core::slice::rsplit_mut": (
        "<[T]>::rsplit_mut::<F>",
        "iter, old(slice)@, pred, false, true, 0",
    ),
    "core::slice::rsplitn": (
        "<[T]>::rsplitn::<F>",
        "iter, slice@, pred, false, true, n as int",
    ),
    "core::slice::rsplitn_mut": (
        "<[T]>::rsplitn_mut::<F>",
        "iter, old(slice)@, pred, false, true, n as int",
    ),
    "core::slice::chunk_by": (
        "<[T]>::chunk_by::<F>",
        "slice_adjacent_chunk_view::<core::slice::ChunkBy<'a, T, F>, F, T>(iter, slice@, pred)",
    ),
    "core::slice::chunk_by_mut": (
        "<[T]>::chunk_by_mut::<F>",
        "slice_adjacent_chunk_view::<core::slice::ChunkByMut<'a, T, F>, F, T>",
    ),
    "core::slice::split_off": (
        "<[T]>::split_off::<R>",
        "ret.is_some() ==> slice_split_off_partition::<T>",
    ),
    "core::slice::split_off_mut": (
        "<[T]>::split_off_mut::<R>",
        "final(ret.unwrap())@",
    ),
    "core::slice::split_off_first": (
        "<[T]>::split_off_first",
        "slice_split_off_first_result::<T>",
    ),
    "core::slice::split_off_first_mut": (
        "<[T]>::split_off_first_mut",
        "seq![*final(ret.unwrap())] + (*final(slice_ref))@",
    ),
    "core::slice::split_off_last": (
        "<[T]>::split_off_last",
        "slice_split_off_last_result::<T>",
    ),
    "core::slice::split_off_last_mut": (
        "<[T]>::split_off_last_mut",
        "(*final(slice_ref))@ + seq![*final(ret.unwrap())]",
    ),
    "core::slice::utf8_chunks": (
        "<[u8]>::utf8_chunks",
        "utf8_chunk_partition::<core::str::Utf8Chunks<'a>>(iter, slice@)",
    ),
}

REQUIRED_SHARED_VOCABULARY = (
    "pub struct ExIterMut",
    "pub struct ExChunks",
    "pub struct ExChunksMut",
    "pub open spec fn slice_subrange",
    "pub open spec fn seq_update",
    "pub uninterp spec fn partial_eq_observed",
    "pub uninterp spec fn ord_cmp_observed",
    "pub open spec fn slice_binary_search_result",
    "pub open spec fn slice_binary_search_by_result",
    "pub open spec fn slice_binary_search_by_key_result",
    "pub open spec fn slice_partition_point_result",
    "pub open spec fn slice_cloned_from",
    "pub open spec fn slice_filled_with_clone",
    "pub open spec fn slice_reversed",
    "pub open spec fn slice_rotated_left",
    "pub open spec fn slice_rotated_right",
    "pub open spec fn slice_swapped",
    "pub open spec fn slice_permutation",
    "pub open spec fn slice_sorted_by_ord",
    "pub uninterp spec fn fnmut_adjacent_bool_outputs",
    "pub uninterp spec fn fnmut_adjacent_key_outputs",
    "pub ghost struct SliceIteratorView",
    "pub open spec fn slice_iterator_well_formed",
    "pub open spec fn slice_predicate_split_view",
    "pub open spec fn slice_split_off_partition",
    "pub open spec fn utf8_chunk_partition",
    "pub open spec fn array_ref_view",
    "pub open spec fn array_value_view",
    "pub open spec fn flatten_array_chunks",
    "pub open spec fn slice_array_chunks_partition",
    "pub ghost struct ComparatorObservation",
    "pub uninterp spec fn comparator_ordering_observed",
    "pub open spec fn comparator_leq_observed",
    "pub uninterp spec fn slice_raw_domain",
    "pub uninterp spec fn slice_raw_mut_domain",
    "pub open spec fn slice_align_to_result",
    "pub open spec fn ascii_eq_ignore_case",
    "pub open spec fn ascii_trim_result",
    "pub uninterp spec fn slice_index_in_range",
    "pub ghost struct MaybeUninitSliceRelation",
    "pub uninterp spec fn maybe_uninit_seq_relation",
)

REQUIRED_SHARED_IMPORTS = (
    "use vstd::prelude::*;",
    "use vstd::seq::*;",
    "use vstd::view::*;",
)

HELPER_CLASS_SOURCE_BACKED = "source-backed"
HELPER_CLASS_LAW_CONSTRAINED = "law-constrained"
HELPER_CLASS_BOUNDARY = "irreducible-boundary-abstraction"
ALLOWED_HELPER_CLASSES = {
    HELPER_CLASS_SOURCE_BACKED,
    HELPER_CLASS_LAW_CONSTRAINED,
    HELPER_CLASS_BOUNDARY,
}
SHARED_HELPER_AUDIT = {
    "partial_eq_observed": HELPER_CLASS_LAW_CONSTRAINED,
    "slice_pattern_view": HELPER_CLASS_BOUNDARY,
    "zero_arg_fnmut_outputs": HELPER_CLASS_LAW_CONSTRAINED,
    "slice_multiplicity": HELPER_CLASS_SOURCE_BACKED,
    "ord_cmp_observed": HELPER_CLASS_LAW_CONSTRAINED,
    "partial_ord_leq_observed": HELPER_CLASS_LAW_CONSTRAINED,
    "fnmut_ordering_observed": HELPER_CLASS_BOUNDARY,
    "fnmut_key_observed": HELPER_CLASS_BOUNDARY,
    "fnmut_adjacent_bool_outputs": HELPER_CLASS_BOUNDARY,
    "fnmut_adjacent_key_outputs": HELPER_CLASS_BOUNDARY,
    "fnmut_predicate_observed": HELPER_CLASS_BOUNDARY,
    "comparator_ordering_observed": HELPER_CLASS_LAW_CONSTRAINED,
    "comparator_observation": HELPER_CLASS_LAW_CONSTRAINED,
    "slice_iterator_view": HELPER_CLASS_LAW_CONSTRAINED,
    "fnmut_adjacent_predicate_observed": HELPER_CLASS_BOUNDARY,
    "array_ref_view": HELPER_CLASS_SOURCE_BACKED,
    "array_mut_ref_view": HELPER_CLASS_SOURCE_BACKED,
    "array_value_view": HELPER_CLASS_SOURCE_BACKED,
    "flatten_array_chunks": HELPER_CLASS_SOURCE_BACKED,
    "slice_raw_domain": HELPER_CLASS_BOUNDARY,
    "slice_raw_mut_domain": HELPER_CLASS_BOUNDARY,
    "slice_start_ptr": HELPER_CLASS_BOUNDARY,
    "slice_start_mut_ptr": HELPER_CLASS_BOUNDARY,
    "slice_ptr_range_result": HELPER_CLASS_BOUNDARY,
    "slice_mut_ptr_range_result": HELPER_CLASS_BOUNDARY,
    "slice_align_to_domain": HELPER_CLASS_BOUNDARY,
    "slice_aligned_middle": HELPER_CLASS_BOUNDARY,
    "slice_element_offset_result": HELPER_CLASS_BOUNDARY,
    "slice_element_in_domain": HELPER_CLASS_BOUNDARY,
    "slice_subslice_range_result": HELPER_CLASS_BOUNDARY,
    "slice_subslice_in_domain": HELPER_CLASS_BOUNDARY,
    "slice_index_in_range": HELPER_CLASS_BOUNDARY,
    "slice_index_result": HELPER_CLASS_BOUNDARY,
    "slice_index_mut_frame": HELPER_CLASS_BOUNDARY,
    "slice_disjoint_indices_valid": HELPER_CLASS_BOUNDARY,
    "maybe_uninit_seq_relation": HELPER_CLASS_BOUNDARY,
    "ascii_lower_byte": HELPER_CLASS_SOURCE_BACKED,
    "ascii_upper_byte": HELPER_CLASS_SOURCE_BACKED,
    "ascii_trim_start_index": HELPER_CLASS_SOURCE_BACKED,
    "ascii_trim_end_index": HELPER_CLASS_SOURCE_BACKED,
    "ascii_escape_seq": HELPER_CLASS_BOUNDARY,
}
EXPECTED_SHARED_HELPER_AUDIT_COUNTS = {
    HELPER_CLASS_SOURCE_BACKED: 9,
    HELPER_CLASS_LAW_CONSTRAINED: 7,
    HELPER_CLASS_BOUNDARY: 25,
}
LAW_CONSTRAINT_SNIPPETS = {
    "partial_eq_observed": (
        "pub broadcast axiom fn axiom_partial_eq_observed_symmetric",
        "pub broadcast axiom fn axiom_partial_eq_observed_transitive",
    ),
    "zero_arg_fnmut_outputs": (
        "pub broadcast axiom fn axiom_zero_arg_fnmut_outputs_len",
    ),
    "ord_cmp_observed": (
        "pub broadcast axiom fn axiom_ord_cmp_observed_reflexive",
        "pub broadcast axiom fn axiom_ord_cmp_observed_dual",
        "pub broadcast axiom fn axiom_ord_cmp_observed_matches_partial_eq",
        "pub broadcast axiom fn axiom_ord_leq_observed_total",
        "pub broadcast axiom fn axiom_ord_leq_observed_transitive",
    ),
    "partial_ord_leq_observed": (
        "pub broadcast axiom fn axiom_partial_ord_leq_observed_matches_partial_eq",
        "pub broadcast axiom fn axiom_partial_ord_leq_observed_antisymmetric",
        "pub broadcast axiom fn axiom_partial_ord_leq_observed_transitive",
    ),
    "comparator_ordering_observed": (
        "pub open spec fn comparator_leq_observed",
        "pub broadcast axiom fn axiom_comparator_ordering_observed_reflexive",
        "pub broadcast axiom fn axiom_comparator_ordering_observed_dual",
        "pub broadcast axiom fn axiom_comparator_leq_observed_total",
        "pub broadcast axiom fn axiom_comparator_leq_observed_transitive",
    ),
    "comparator_observation": (
        "pub broadcast axiom fn axiom_comparator_observation_domain",
        "pub trace_id: int",
    ),
    "slice_iterator_view": (
        "pub open spec fn slice_iterator_well_formed",
        "pub broadcast axiom fn axiom_slice_iterator_view_well_formed",
        "view.yielded_prefix + view.remaining + view.remainder == view.source",
        "view.remainder + view.remaining + view.yielded_prefix == view.source",
    ),
}
BOUNDARY_HELPER_JUSTIFICATIONS = {
    "slice_pattern_view": "SlicePattern is an unstable, potentially unsized pattern trait whose concrete matcher is outside Verus' slice view model.",
    "fnmut_ordering_observed": "Arbitrary FnMut comparison callbacks can be stateful; the contracts constrain their observed order only at target call sites.",
    "fnmut_key_observed": "Arbitrary FnMut key extraction has no source-backed extensional law without a target-local callback specification.",
    "fnmut_adjacent_bool_outputs": "is_sorted_by consumes a stateful FnMut comparator as a source-order adjacent-pair trace with short-circuit behavior.",
    "fnmut_adjacent_key_outputs": "is_sorted_by_key consumes stateful FnMut key extraction in source iteration order and compares only adjacent emitted keys.",
    "fnmut_predicate_observed": "Arbitrary FnMut predicates can be stateful; split and partition contracts constrain only the observed trace they consume.",
    "fnmut_adjacent_predicate_observed": "Adjacent-pair FnMut predicates are user callbacks whose trace is only meaningful within sorted/chunk-by call sites.",
    "slice_raw_domain": "Raw pointer validity depends on allocation provenance, alignment, initialization, and aliasing facts outside Seq semantics.",
    "slice_raw_mut_domain": "Mutable raw pointer validity depends on external provenance and aliasing facts outside the slice model.",
    "slice_start_ptr": "Pointer identity for as_ptr/from_raw_parts is an address/provenance boundary, not recoverable from element sequences.",
    "slice_start_mut_ptr": "Mutable pointer identity is an address/provenance boundary, not recoverable from element sequences.",
    "slice_ptr_range_result": "Pointer range endpoints are provenance/address facts outside Verus Seq equality.",
    "slice_mut_ptr_range_result": "Mutable pointer range endpoints are provenance/address facts outside Verus Seq equality.",
    "slice_align_to_domain": "align_to preconditions depend on layout/alignment validity across two element types.",
    "slice_aligned_middle": "The middle aligned subslice reinterprets storage across element types and cannot be derived from source Seq<T> alone.",
    "slice_element_offset_result": "element_offset depends on reference identity and address distance within an allocation.",
    "slice_element_in_domain": "Element-reference membership depends on alias/provenance identity rather than value equality.",
    "slice_subslice_range_result": "subslice_range returns allocation-relative bounds for a borrowed subslice, which is a provenance fact.",
    "slice_subslice_in_domain": "Subslice membership depends on shared allocation provenance and range bounds.",
    "slice_index_in_range": "SliceIndex covers external range/index forms whose exact domain logic is implemented by the trait.",
    "slice_index_result": "SliceIndex output shape is associated-type-specific and cannot be represented uniformly as Seq<T>.",
    "slice_index_mut_frame": "Mutable SliceIndex framing depends on associated output shape and aliasing discipline.",
    "slice_disjoint_indices_valid": "Disjoint index validation depends on SliceIndex/GetDisjointMutIndex trait behavior for arbitrary index arrays.",
    "maybe_uninit_seq_relation": "MaybeUninit sequence initializedness cannot be recovered from Seq<MaybeUninit<T>> values alone.",
    "ascii_escape_seq": "EscapeAscii produces an iterator over escaped bytes, a formatting transformation outside source slice state.",
}


def fail(message: str) -> None:
    print(f"contract check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing file {path}")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        fail(f"{path} is empty")
    return rows


def parse_blocks(text: str) -> dict[str, dict[str, str]]:
    blocks: dict[str, dict[str, str]] = {}
    pattern = re.compile(
        r"// BEGIN SLICE_SPEC target=(?P<target>\S+)\n(?P<body>.*?)// END SLICE_SPEC",
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        target = match.group("target")
        if target in blocks:
            fail(f"duplicate spec block for {target}")
        body = match.group("body")
        fields: dict[str, str] = {}
        for line in body.splitlines():
            if not line.startswith("// "):
                continue
            content = line[3:]
            if ": " not in content:
                continue
            key, value = content.split(": ", 1)
            fields[key.strip()] = value.strip()
        blocks[target] = fields
    return blocks


def baseline_excerpt(path: Path, start: int, end: int) -> str:
    lines = path.read_text().splitlines()
    return "\n".join(lines[start - 1 : end])


def strip_comments(text: str) -> str:
    def preserve_newlines(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    without_block_comments = re.sub(r"/\*.*?\*/", preserve_newlines, text, flags=re.DOTALL)
    return "\n".join(line.split("//", 1)[0] for line in without_block_comments.splitlines())


def shared_spec_fn_forms(text: str) -> dict[str, str]:
    pattern = re.compile(r"^pub\s+(?P<form>uninterp|open)\s+spec\s+fn\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
    forms: dict[str, str] = {}
    for match in pattern.finditer(text):
        name = match.group("name")
        if name in forms:
            fail(f"shared vocabulary declares helper {name} more than once")
        forms[name] = match.group("form")
    return forms


def extract_shared_helper_calls(text: str, helper_names: set[str]) -> list[str]:
    calls: list[str] = []
    for name in sorted(helper_names):
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])\s*(?:\(|::\s*<)"
        )
        if pattern.search(text):
            calls.append(name)
    return calls


def shared_helper_dependency_graph(shared_vocabulary_text: str) -> dict[str, list[str]]:
    forms = shared_spec_fn_forms(shared_vocabulary_text)
    helper_names = set(forms)
    executable_text = strip_comments(shared_vocabulary_text)
    pattern = re.compile(
        r"^pub\s+(?P<form>uninterp|open)\s+spec\s+fn\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(executable_text))
    dependencies: dict[str, list[str]] = {name: [] for name in forms}
    for index, match in enumerate(matches):
        name = match.group("name")
        if forms[name] != "open":
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(executable_text)
        segment = executable_text[start:end]
        dependencies[name] = [
            helper for helper in extract_shared_helper_calls(segment, helper_names) if helper != name
        ]
    return dependencies


def transitive_shared_helper_usage(
    direct_helpers: list[str],
    dependency_graph: dict[str, list[str]],
) -> list[str]:
    seen: set[str] = set()
    stack = list(direct_helpers)
    while stack:
        helper = stack.pop()
        if helper in seen:
            continue
        seen.add(helper)
        stack.extend(dependency_graph.get(helper, ()))
    return sorted(seen)


def validate_no_target_local_opaque_helpers(generated_specs_text: str) -> None:
    executable_text = strip_comments(generated_specs_text)
    local_uninterp = re.findall(
        r"^pub\s+uninterp\s+spec\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)",
        executable_text,
        re.MULTILINE,
    )
    if local_uninterp:
        fail(f"generated target specs declare target-local uninterpreted helpers {sorted(local_uninterp)}")


def build_shared_helper_target_usage_audit(
    catalog: list[dict[str, str]],
    shared_vocabulary_text: str,
    generated_specs_text: str,
) -> dict[str, object]:
    validate_no_target_local_opaque_helpers(generated_specs_text)
    forms = shared_spec_fn_forms(shared_vocabulary_text)
    dependency_graph = shared_helper_dependency_graph(shared_vocabulary_text)
    helper_names = set(forms)
    generated = sorted(
        (row for row in catalog if row["status"] == "generated-new-real-relation-spec"),
        key=lambda row: row["target"],
    )
    if len(generated) != 120:
        fail(f"shared helper target audit has {len(generated)} generated targets, expected 120")

    per_target: list[dict[str, object]] = []
    targets_by_class: dict[str, set[str]] = {
        helper_class: set() for helper_class in EXPECTED_SHARED_HELPER_AUDIT_COUNTS
    }
    helpers_by_class: dict[str, set[str]] = {
        helper_class: set() for helper_class in EXPECTED_SHARED_HELPER_AUDIT_COUNTS
    }
    helper_references_by_class: dict[str, int] = {
        helper_class: 0 for helper_class in EXPECTED_SHARED_HELPER_AUDIT_COUNTS
    }

    for row in generated:
        direct_helpers = extract_shared_helper_calls(row["contract_text"], helper_names)
        reachable_helpers = transitive_shared_helper_usage(direct_helpers, dependency_graph)
        audited_helpers = sorted(helper for helper in reachable_helpers if helper in SHARED_HELPER_AUDIT)
        audited_by_class: dict[str, list[str]] = {}
        for helper_class in EXPECTED_SHARED_HELPER_AUDIT_COUNTS:
            class_helpers = [
                helper for helper in audited_helpers if SHARED_HELPER_AUDIT[helper] == helper_class
            ]
            audited_by_class[helper_class] = class_helpers
            if class_helpers:
                targets_by_class[helper_class].add(row["target"])
                helpers_by_class[helper_class].update(class_helpers)
                helper_references_by_class[helper_class] += len(class_helpers)

        per_target.append(
            {
                "target": row["target"],
                "semantic_family": row["semantic_family"],
                "direct_shared_helpers": direct_helpers,
                "reachable_shared_helpers": reachable_helpers,
                "audited_shared_helpers": audited_helpers,
                "audited_helper_classes": audited_by_class,
                "catalog_shared_helpers_note": row["shared_helpers"],
            }
        )

    used_audited_helpers = set().union(*helpers_by_class.values()) if helpers_by_class else set()
    return {
        "schema_version": 1,
        "scope": "generated core::slice assume_specification targets",
        "sources": {
            "catalog": "catalog/slice_spec_catalog.csv",
            "generated_specs": "specs/generated_slice_specs.rs",
            "shared_vocabulary": "specs/slice_shared_vocabulary.rs",
        },
        "summary": {
            "generated_targets": len(generated),
            "targets_with_direct_shared_helpers": sum(
                1 for row in per_target if row["direct_shared_helpers"]
            ),
            "targets_with_audited_helpers": sum(
                1 for row in per_target if row["audited_shared_helpers"]
            ),
            "shared_spec_helpers_declared": len(forms),
            "shared_uninterpreted_helpers_declared": sum(
                1 for form in forms.values() if form == "uninterp"
            ),
            "audited_helpers_declared": len(SHARED_HELPER_AUDIT),
            "audited_helper_declarations_by_class": dict(
                sorted(Counter(SHARED_HELPER_AUDIT.values()).items())
            ),
            "unique_audited_helpers_used_by_class": {
                helper_class: sorted(helpers)
                for helper_class, helpers in sorted(helpers_by_class.items())
            },
            "target_counts_by_audited_helper_class": {
                helper_class: len(targets)
                for helper_class, targets in sorted(targets_by_class.items())
            },
            "target_helper_references_by_audited_class": dict(
                sorted(helper_references_by_class.items())
            ),
            "unused_audited_helpers": sorted(set(SHARED_HELPER_AUDIT) - used_audited_helpers),
            "target_local_uninterpreted_helpers": [],
        },
        "per_target": per_target,
    }


def render_shared_helper_target_usage_csv(audit: dict[str, object]) -> str:
    stream = StringIO()
    fieldnames = [
        "target",
        "semantic_family",
        "direct_shared_helpers",
        "reachable_shared_helpers",
        "audited_shared_helpers",
        HELPER_CLASS_SOURCE_BACKED,
        HELPER_CLASS_LAW_CONSTRAINED,
        HELPER_CLASS_BOUNDARY,
        "catalog_shared_helpers_note",
    ]
    writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in audit["per_target"]:
        assert isinstance(row, dict)
        classes = row["audited_helper_classes"]
        assert isinstance(classes, dict)
        writer.writerow(
            {
                "target": row["target"],
                "semantic_family": row["semantic_family"],
                "direct_shared_helpers": ";".join(row["direct_shared_helpers"]),
                "reachable_shared_helpers": ";".join(row["reachable_shared_helpers"]),
                "audited_shared_helpers": ";".join(row["audited_shared_helpers"]),
                HELPER_CLASS_SOURCE_BACKED: ";".join(classes[HELPER_CLASS_SOURCE_BACKED]),
                HELPER_CLASS_LAW_CONSTRAINED: ";".join(classes[HELPER_CLASS_LAW_CONSTRAINED]),
                HELPER_CLASS_BOUNDARY: ";".join(classes[HELPER_CLASS_BOUNDARY]),
                "catalog_shared_helpers_note": row["catalog_shared_helpers_note"],
            }
        )
    return stream.getvalue()


def write_shared_helper_target_usage_audit(root: Path, audit: dict[str, object]) -> None:
    json_text = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    csv_text = render_shared_helper_target_usage_csv(audit)
    (root / SHARED_HELPER_TARGET_AUDIT_JSON).write_text(json_text)
    (root / SHARED_HELPER_TARGET_AUDIT_CSV).write_text(csv_text)


def validate_shared_helper_target_usage_audit(root: Path, audit: dict[str, object]) -> None:
    json_path = root / SHARED_HELPER_TARGET_AUDIT_JSON
    csv_path = root / SHARED_HELPER_TARGET_AUDIT_CSV
    if not json_path.is_file() or not csv_path.is_file():
        fail(
            "missing shared helper target usage audit artifacts; "
            "rerun check_contracts.py with --write-shared-helper-usage-audit"
        )
    expected_json = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    expected_csv = render_shared_helper_target_usage_csv(audit)
    if json_path.read_text() != expected_json:
        fail(f"{SHARED_HELPER_TARGET_AUDIT_JSON} is stale or does not match generated target helper usage")
    if csv_path.read_text() != expected_csv:
        fail(f"{SHARED_HELPER_TARGET_AUDIT_CSV} is stale or does not match generated target helper usage")


def validate_shared_helper_audit(shared_vocabulary_text: str) -> None:
    forms = shared_spec_fn_forms(shared_vocabulary_text)
    executable_shared_vocabulary_text = strip_comments(shared_vocabulary_text)
    audited = set(SHARED_HELPER_AUDIT)
    missing = sorted(audited - set(forms))
    if missing:
        fail(f"shared helper audit mentions missing helpers {missing}")
    if len(audited) != 41:
        fail(f"shared helper audit has {len(audited)} helpers, expected 41")

    unaudited_uninterpreted = sorted(
        name for name, form in forms.items() if form == "uninterp" and name not in audited
    )
    if unaudited_uninterpreted:
        fail(f"shared vocabulary has unaudited uninterpreted helpers {unaudited_uninterpreted}")

    bad_classes = {
        name: helper_class
        for name, helper_class in SHARED_HELPER_AUDIT.items()
        if helper_class not in ALLOWED_HELPER_CLASSES
    }
    if bad_classes:
        fail(f"shared helper audit has invalid classifications {bad_classes}")

    actual_counts = Counter(SHARED_HELPER_AUDIT.values())
    if dict(actual_counts) != EXPECTED_SHARED_HELPER_AUDIT_COUNTS:
        fail(
            "shared helper audit counts changed: "
            f"actual={dict(actual_counts)} expected={EXPECTED_SHARED_HELPER_AUDIT_COUNTS}"
        )

    law_constrained = {
        name
        for name, helper_class in SHARED_HELPER_AUDIT.items()
        if helper_class == HELPER_CLASS_LAW_CONSTRAINED
    }
    if set(LAW_CONSTRAINT_SNIPPETS) != law_constrained:
        fail(
            "law-constrained helper snippet table mismatch: "
            f"missing={sorted(law_constrained - set(LAW_CONSTRAINT_SNIPPETS))} "
            f"extra={sorted(set(LAW_CONSTRAINT_SNIPPETS) - law_constrained)}"
        )
    boundary_helpers = {
        name
        for name, helper_class in SHARED_HELPER_AUDIT.items()
        if helper_class == HELPER_CLASS_BOUNDARY
    }
    if set(BOUNDARY_HELPER_JUSTIFICATIONS) != boundary_helpers:
        fail(
            "boundary helper justification table mismatch: "
            f"missing={sorted(boundary_helpers - set(BOUNDARY_HELPER_JUSTIFICATIONS))} "
            f"extra={sorted(set(BOUNDARY_HELPER_JUSTIFICATIONS) - boundary_helpers)}"
        )
    weak_boundary_justifications = sorted(
        name
        for name, text in BOUNDARY_HELPER_JUSTIFICATIONS.items()
        if len(text.split()) < 8
    )
    if weak_boundary_justifications:
        fail(f"boundary helper justifications are too terse {weak_boundary_justifications}")

    source_backed_not_open = sorted(
        name
        for name, helper_class in SHARED_HELPER_AUDIT.items()
        if helper_class == HELPER_CLASS_SOURCE_BACKED and forms[name] != "open"
    )
    if source_backed_not_open:
        fail(f"source-backed shared helpers are not open definitions {source_backed_not_open}")

    missing_law_snippets: dict[str, list[str]] = {}
    for name, snippets in LAW_CONSTRAINT_SNIPPETS.items():
        absent = [
            snippet
            for snippet in snippets
            if snippet not in executable_shared_vocabulary_text
        ]
        if absent:
            missing_law_snippets[name] = absent
    if missing_law_snippets:
        fail(f"law-constrained shared helpers are missing enforced snippets {missing_law_snippets}")


def feedback_outcome(result: dict[str, object]) -> str:
    status = str(result.get("status", "runner_crash"))
    r0_z3 = result.get("r0_z3")
    if status == "ok":
        if r0_z3 == "unsat":
            return "UNSAT"
        if r0_z3 == "sat":
            return "SAT"
        if r0_z3 == "unknown":
            return "UNKNOWN"
        fail(f"{result.get('target')} has status=ok without a recognized r0_z3")
    if status in {"no_ensures", "unsupported_mut_ref_return"}:
        return "unsupported"
    if status == "verus_error":
        return "Verus error"
    return "runner crash"


def validate_unknown_reason(
    *,
    target: str,
    entry: dict[str, object],
    result: dict[str, object],
    determinism_text: str,
) -> None:
    is_unknown = result.get("status") == "ok" and result.get("r0_z3") == "unknown"
    if not is_unknown:
        if entry.get("unknown_reason_class") or result.get("unknown_reason_class"):
            fail(f"{target} is not R0=UNKNOWN but records an UNKNOWN reason class")
        return
    reason_class = result.get("unknown_reason_class")
    reason = result.get("unknown_reason")
    if not isinstance(reason_class, str) or reason_class not in UNKNOWN_REASON_CLASSES:
        fail(f"{target} R0=UNKNOWN result has missing or unknown reason class")
    if not isinstance(reason, str) or not reason.strip():
        fail(f"{target} R0=UNKNOWN result has empty review reason")
    if entry.get("unknown_reason_class") != reason_class:
        fail(f"{target} manifest UNKNOWN reason class differs from result JSON")
    if entry.get("unknown_reason") != reason:
        fail(f"{target} manifest UNKNOWN reason text differs from result JSON")
    if f"unknown_reason={reason_class}" not in determinism_text:
        fail(f"{target} determinism_result does not record UNKNOWN reason class")


def validate_feedback_determinism(root: Path, catalog: list[dict[str, str]]) -> None:
    generated = [
        row for row in catalog if row["status"] == "generated-new-real-relation-spec"
    ]
    manifest_path = root / FEEDBACK_DETERMINISM_MANIFEST
    if not manifest_path.is_file():
        fail(f"missing feedback determinism manifest {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    entries = manifest.get("results", [])
    if len(entries) != len(generated):
        fail(f"feedback manifest has {len(entries)} results, expected {len(generated)}")
    generated_targets = {row["target"] for row in generated}
    manifest_targets = {entry.get("target") for entry in entries}
    if manifest_targets != generated_targets:
        fail("feedback manifest target set differs from generated catalog targets")
    results: dict[str, dict[str, object]] = {}
    entries_by_target: dict[str, dict[str, object]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            fail("feedback manifest contains a non-object result entry")
        target = str(entry.get("target"))
        rel = entry.get("result_json")
        if not isinstance(rel, str) or not (root / rel).is_file():
            fail(f"{target} manifest entry has missing result_json")
        payload = json.loads((root / rel).read_text())
        if payload.get("target") != target:
            fail(f"{target} feedback result target mismatch")
        results[target] = payload
        entries_by_target[target] = entry
    for row in generated:
        text = row["determinism_result"]
        target = row["target"]
        if any(fragment in text for fragment in STALE_DIRECT_DETERMINISM_FRAGMENTS):
            fail(f"{target} still records stale direct assume-spec determinism evidence")
        result = results[target]
        artifacts = result.get("artifacts", {})
        if not isinstance(artifacts, dict) or artifacts.get("result.json") not in text:
            fail(f"{target} determinism_result does not reference feedback result JSON")
        if f"R0={feedback_outcome(result)}" not in text:
            fail(f"{target} determinism_result does not record feedback outcome")
        validate_unknown_reason(
            target=target,
            entry=entries_by_target[target],
            result=result,
            determinism_text=text,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated core::slice contract artifact.")
    parser.add_argument("--specs", required=True, type=Path)
    parser.add_argument(
        "--inventory",
        type=Path,
        help="optional inventory CSV path; defaults to inventory/slice_exec_fn_inventory.csv under the specs root",
    )
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument(
        "--write-shared-helper-usage-audit",
        action="store_true",
        help="refresh verification/shared_helper_target_usage_audit.{json,csv} before validating it",
    )
    args = parser.parse_args()

    root = args.specs.resolve().parents[1]
    inventory_path = args.inventory or root / "inventory" / "slice_exec_fn_inventory.csv"
    if not inventory_path.is_absolute():
        inventory_path = root / inventory_path
    existing_path = root / "specs" / "existing_vstd_slice_specs.rs"
    generated_path = root / "specs" / "generated_slice_specs.rs"
    shared_vocabulary_path = root / "specs" / "slice_shared_vocabulary.rs"
    vstd_slice = root / "vstd-baseline" / "slice.rs"
    vstd_std_slice = root / "vstd-baseline" / "std_specs" / "slice.rs"
    verus_evidence_path = root / "verification" / "evidence" / "slice_observation_bootstrap.verus.json"
    mutation_verus_evidence_path = root / "verification" / "evidence" / "slice_observation_mutation_batch.verus.json"
    splitting_verus_evidence_path = root / "verification" / "evidence" / "slice_splitting_iterator_batch.verus.json"
    remaining_verus_evidence_path = root / "verification" / "evidence" / "slice_remaining_families_batch.verus.json"
    feedback_manifest_path = root / FEEDBACK_DETERMINISM_MANIFEST

    for path in (
        args.specs,
        args.catalog,
        inventory_path,
        existing_path,
        generated_path,
        shared_vocabulary_path,
        vstd_slice,
        vstd_std_slice,
        verus_evidence_path,
        mutation_verus_evidence_path,
        splitting_verus_evidence_path,
        remaining_verus_evidence_path,
        feedback_manifest_path,
    ):
        if not path.is_file():
            fail(f"missing required artifact {path}")

    inventory = read_csv(inventory_path)
    catalog = read_csv(args.catalog)
    text = args.specs.read_text()
    generated_text = generated_path.read_text()
    shared_vocabulary_text = shared_vocabulary_path.read_text()
    executable_specs_text = strip_comments(text)
    executable_shared_vocabulary_text = strip_comments(shared_vocabulary_text)
    blocks = parse_blocks(text)
    validate_shared_helper_audit(shared_vocabulary_text)
    inventory_targets = {row["canonical_target"] for row in inventory}
    catalog_by_target = {row["target"]: row for row in catalog}

    if len(inventory) != 132:
        fail(f"inventory has {len(inventory)} rows, expected 132")
    if len(catalog_by_target) != 132:
        fail(f"catalog has {len(catalog_by_target)} unique rows, expected 132")
    if len(blocks) != 132:
        fail(f"spec file has {len(blocks)} marked blocks, expected 132")
    if set(blocks) != inventory_targets:
        fail(
            "spec block targets differ from inventory: "
            f"missing={sorted(inventory_targets - set(blocks))} "
            f"extra={sorted(set(blocks) - inventory_targets)}"
        )
    if set(catalog_by_target) != inventory_targets:
        fail(
            "catalog targets differ from inventory: "
            f"missing={sorted(inventory_targets - set(catalog_by_target))} "
            f"extra={sorted(set(catalog_by_target) - inventory_targets)}"
        )
    shared_helper_target_usage_audit = build_shared_helper_target_usage_audit(
        catalog,
        shared_vocabulary_text,
        generated_text,
    )
    if args.write_shared_helper_usage_audit:
        write_shared_helper_target_usage_audit(root, shared_helper_target_usage_audit)
    validate_shared_helper_target_usage_audit(root, shared_helper_target_usage_audit)
    for marker_path, marker_text in (
        (args.specs, text),
        (generated_path, generated_text),
    ):
        for fragment in STALE_REVIEWER_NOTE_FRAGMENTS:
            if fragment in marker_text:
                fail(
                    f"{marker_path} still contains stale reviewer-note determinism wording "
                    f"{fragment!r}"
                )

    existing = {target for target, fields in blocks.items() if fields.get("status") == "existing-vstd"}
    if existing != EXPECTED_EXISTING_VSTD:
        fail(
            "existing-vstd spec block set mismatch: "
            f"missing={sorted(EXPECTED_EXISTING_VSTD - existing)} "
            f"extra={sorted(existing - EXPECTED_EXISTING_VSTD)}"
        )

    for excerpt in (
        baseline_excerpt(vstd_slice, 71, 148),
        baseline_excerpt(vstd_std_slice, 97, 259),
    ):
        if excerpt not in text or excerpt not in existing_path.read_text():
            fail("exact vstd baseline excerpt is missing from specs")

    for snippet in REQUIRED_SHARED_IMPORTS:
        if snippet not in executable_specs_text:
            fail(f"{args.specs} missing non-comment shared import {snippet!r}")
        if snippet not in executable_shared_vocabulary_text:
            fail(f"shared vocabulary missing non-comment import {snippet!r}")

    for snippet in REQUIRED_SHARED_VOCABULARY:
        if snippet not in executable_specs_text:
            fail(f"{args.specs} missing non-comment shared helper {snippet!r}")
        if snippet not in executable_shared_vocabulary_text:
            fail(f"shared vocabulary missing non-comment executable helper {snippet!r}")

    for target, snippets in BOOTSTRAP_EXECUTABLE_CONTRACTS.items():
        for snippet in snippets:
            if snippet not in executable_specs_text:
                fail(
                    f"{target} is missing non-comment executable bootstrap contract snippet "
                    f"{snippet!r} from {args.specs}"
                )

    for target, snippets in FIND_LIKE_SEARCH_EXECUTABLE_CONTRACTS.items():
        for snippet in snippets:
            if snippet not in executable_specs_text:
                fail(
                    f"{target} is missing non-comment executable find-like search contract snippet "
                    f"{snippet!r} from {args.specs}"
                )

    for target, snippets in MUTATION_EXECUTABLE_CONTRACTS.items():
        for snippet in snippets:
            if snippet not in executable_specs_text:
                fail(
                    f"{target} is missing non-comment executable mutation contract snippet "
                    f"{snippet!r} from {args.specs}"
                )

    for target, snippets in SPLITTING_ITERATOR_EXECUTABLE_CONTRACTS.items():
        for snippet in snippets:
            if snippet not in executable_specs_text:
                fail(
                    f"{target} is missing non-comment executable splitting/iterator contract snippet "
                    f"{snippet!r} from {args.specs}"
                )

    verus_evidence = json.loads(verus_evidence_path.read_text())
    if verus_evidence.get("return_code") != 0:
        fail(f"bootstrap Verus typecheck failed: {verus_evidence_path}")
    if verus_evidence.get("harness_path") != "verification/harnesses/slice_observation_bootstrap.rs":
        fail("bootstrap Verus evidence points at the wrong harness")

    mutation_verus_evidence = json.loads(mutation_verus_evidence_path.read_text())
    if mutation_verus_evidence.get("return_code") != 0:
        fail(f"mutation Verus typecheck failed: {mutation_verus_evidence_path}")
    if mutation_verus_evidence.get("harness_path") != "verification/harnesses/slice_observation_mutation_batch.rs":
        fail("mutation Verus evidence points at the wrong harness")

    splitting_verus_evidence = json.loads(splitting_verus_evidence_path.read_text())
    if splitting_verus_evidence.get("return_code") != 0:
        fail(f"splitting/iterator Verus typecheck failed: {splitting_verus_evidence_path}")
    if splitting_verus_evidence.get("harness_path") != "verification/harnesses/slice_splitting_iterator_batch.rs":
        fail("splitting/iterator Verus evidence points at the wrong harness")

    remaining_verus_evidence = json.loads(remaining_verus_evidence_path.read_text())
    if remaining_verus_evidence.get("return_code") != 0:
        fail(f"remaining-family Verus typecheck failed: {remaining_verus_evidence_path}")
    if remaining_verus_evidence.get("harness_path") != "verification/harnesses/slice_remaining_families_batch.rs":
        fail("remaining-family Verus evidence points at the wrong harness")

    validate_feedback_determinism(root, catalog)

    inventory_by_target = {row["canonical_target"]: row for row in inventory}
    for target, fields in blocks.items():
        missing = REQUIRED_MARKER_FIELDS.difference(fields)
        if missing:
            fail(f"{target} missing marker fields {sorted(missing)}")
        catalog_row = catalog_by_target[target]
        if fields["status"] != catalog_row["status"]:
            fail(f"{target} status differs between specs and catalog")
        if fields["family"] != catalog_row["semantic_family"]:
            fail(f"{target} semantic family differs between specs and catalog")
        if fields["signature"] != inventory_by_target[target]["signature"]:
            fail(f"{target} signature differs from inventory")
        if fields["generic_bounds_result"] != inventory_by_target[target]["generic_bounds"]:
            fail(f"{target} generic bounds differ from inventory")

        contract_lower = (fields["requires"] + " " + fields["ensures"] + " " + fields["contract_text"]).lower()
        for fragment in BANNED_CONTRACT_FRAGMENTS:
            if fragment in contract_lower:
                fail(f"{target} contains banned contract fragment {fragment!r}")
        if fields["status"] == "generated-new-real-relation-spec":
            if not any(token.lower() in contract_lower for token in RELATIONAL_TOKENS):
                fail(f"{target} generated contract lacks a checked relation token")
            if "pending-generation" in inventory_by_target[target]["final_contract_or_justified_no_spec_status"]:
                fail(f"{target} inventory final status was not advanced")
            mutation_text = (
                inventory_by_target[target]["source_observable_mutations"]
                + " "
                + inventory_by_target[target]["signature"]
            ).lower()
            if (
                "may mutate" in mutation_text or "&mut self" in mutation_text or "self: &mut" in mutation_text
            ) and "final(" not in contract_lower and "final " not in contract_lower:
                fail(f"{target} mutable generated contract lacks old/final frame relation")
        elif fields["status"] == "justified-no-spec":
            needed = ("strongest weak spec", "missing", "prerequisite", "operator")
            absent = [word for word in needed if word not in contract_lower]
            if absent:
                fail(f"{target} no-spec justification is incomplete: missing {absent}")
        elif fields["status"] != "existing-vstd":
            fail(f"{target} has unexpected status {fields['status']}")

    generated_blocks = [fields for fields in blocks.values() if fields["status"] == "generated-new-real-relation-spec"]
    if len(generated_blocks) != 120:
        fail(f"generated spec count is {len(generated_blocks)}, expected 120")

    print(
        "contracts ok: 132 spec blocks, 12 exact vstd, 120 generated relation specs, "
        "120 executable generated assume_specification contracts typechecked; "
        "shared helper target usage audit enforced"
    )


if __name__ == "__main__":
    main()
