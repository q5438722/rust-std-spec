#!/usr/bin/env python3
"""Generate missing Rust std contracts and run Verus determinism feedback."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import traceback
from typing import Any


SPEC_DET_ROOT = Path("/home/chentianyu/intent_formalization/spec-determinism")
sys.path.insert(0, str(SPEC_DET_ROOT))

from spec_determinism.classify import classify_ok
from spec_determinism.codegen.equal_policy import EqualPolicy
from spec_determinism.codegen.gen_det import build_det_check_spec
from spec_determinism.extract.extractor import extract_spec
from spec_determinism.schema_search import enumerate_schemas, render_guarded_template
from spec_determinism.schema_search.search import build_schema_ctx, run_schema_search
from spec_determinism.view.registry import ViewRegistry


SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS = {
    "alloc::ffi::CString::from_vec_with_nul_unchecked",
    "alloc::string::String::from_utf8_unchecked",
}
SOURCE_BACKED_SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET = (
    "core::slice::split_at_mut_unchecked"
)
SOURCE_BACKED_SLICE_SPLIT_AT_MUT_CHECKED_TARGET = "core::slice::split_at_mut_checked"
SOURCE_BACKED_STR_SPLIT_AT_MUT_CHECKED_TARGET = "core::str::split_at_mut_checked"
SOURCE_BACKED_STR_FROM_UTF8_TARGET = "core::str::from_utf8"
SOURCE_BACKED_STR_FROM_UTF8_CONTRACT_TARGET = "str::from_utf8"
SOURCE_BACKED_STR_FROM_UTF8_MUT_TARGET = "core::str::from_utf8_mut"
SOURCE_BACKED_RAW_POINTER_REPRESENTATION_SKIP_TARGETS = {
    "core::ptr::NonNull::as_ptr": {
        "rationale": (
            "The function exposes NonNull's hidden raw-pointer representation as "
            "a `*mut T`. The source says NonNull is transparent over `*const T` "
            "and casts that representation directly to `*mut T`, but the public "
            "vstd vocabulary has no NonNull view that can soundly relate the "
            "returned raw pointer to the wrapped pointer representation and "
            "provenance. An address-only postcondition would under-specify the "
            "result, while a representation equality would assume private layout."
        ),
        "risks": [
            "A useful contract would need a public NonNull raw-pointer view.",
            (
                "Equating only the result address would leave pointer provenance "
                "and identity underdetermined."
            ),
            (
                "Exposing or assuming NonNull's private representation would be "
                "unsound."
            ),
        ],
        "tokens": (
            "acquires the underlying `*mut` pointer",
            "pub const fn as_ptr(self) -> *mut t",
            "nonnull` is `transparent` over a `*const t`",
        ),
        "issues": [
            "classification:unsafe_or_representation_sensitive",
            "missing_nonnull_pointer_view",
        ],
    },
    "core::ptr::as_mut_array": {
        "rationale": (
            "The method only reinterprets a raw slice pointer as a raw array "
            "pointer when the slice-pointer length metadata equals `N`. A "
            "deterministic contract therefore depends on representation-sensitive "
            "raw pointer metadata and cast equalities. Existing vstd vocabulary "
            "offers no useful ordinary semantic contract for the returned raw "
            "pointer that avoids those representation assumptions."
        ),
        "risks": [
            (
                "A contract that specifies the returned raw array pointer would "
                "depend on pointer metadata and cast representation equality."
            ),
            (
                "A length-only Option result would not characterize the raw "
                "pointer returned in the Some case."
            ),
        ],
        "tokens": (
            "gets a raw, mutable pointer to the underlying array",
            "pub const fn as_mut_array<const n: usize>(self) -> option<*mut [t; n]>",
            "if self.len() == n",
        ),
        "issues": [
            "classification:unsafe_or_representation_sensitive",
            "raw_pointer_representation_contract",
        ],
    },
    "core::ptr::slice_from_raw_parts": {
        "rationale": (
            "The function only constructs a raw slice pointer from pointer "
            "representation fields and length metadata. A deterministic contract "
            "therefore requires trusted representation-sensitive equalities that "
            "make result equality trivial. Existing vstd vocabulary offers no "
            "useful ordinary semantic contract that avoids this issue."
        ),
        "risks": [
            "Skipping leaves raw slice pointer construction opaque to verification."
        ],
        "tokens": (
            "forms a raw slice from a pointer and a length",
            "pub const fn slice_from_raw_parts<t>(data: *const t, len: usize) -> *const [t]",
            "from_raw_parts(data, len)",
        ),
        "issues": [
            "classification:unsafe_or_representation_sensitive",
            "determinism_unsupported_contract_form",
        ],
    },
}
SLICE_AS_MUT_ARRAY_TARGET = "core::slice::as_mut_array"
SLICE_FIRST_CHUNK_MUT_TARGET = "core::slice::first_chunk_mut"
SLICE_LAST_CHUNK_MUT_TARGET = "core::slice::last_chunk_mut"
SLICE_AS_CHUNKS_MUT_TARGET = "core::slice::as_chunks_mut"
SLICE_AS_RCHUNKS_MUT_TARGET = "core::slice::as_rchunks_mut"
SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET = "core::slice::split_first_chunk_mut"
SLICE_SPLIT_LAST_CHUNK_MUT_TARGET = "core::slice::split_last_chunk_mut"
SLICE_SPLIT_FIRST_MUT_TARGET = "core::slice::split_first_mut"
SLICE_SPLIT_LAST_MUT_TARGET = "core::slice::split_last_mut"
SLICE_SPLIT_OFF_TARGET = "core::slice::split_off"
SLICE_SPLIT_OFF_FIRST_MUT_TARGET = "core::slice::split_off_first_mut"
SLICE_SPLIT_OFF_LAST_MUT_TARGET = "core::slice::split_off_last_mut"
BTREEMAP_GET_MUT_TARGET = "alloc::collections::BTreeMap::get_mut"
HASHMAP_GET_MUT_TARGET = "std::collections::HashMap::get_mut"
LINKEDLIST_BACK_MUT_TARGET = "alloc::collections::LinkedList::back_mut"
ARRAY_EACH_MUT_TARGET = "core::array::each_mut"
SOURCE_BACKED_OPTION_MUT_ARRAY_VIEW_TARGETS = {
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
SOURCE_BACKED_MAP_GET_MUT_TARGETS = {
    BTREEMAP_GET_MUT_TARGET,
    HASHMAP_GET_MUT_TARGET,
}
THREAD_RESULT_FLATTEN_TARGET = "std::thread::Result::flatten"
THREAD_RESULT_FLATTEN_CONTRACT_TARGET = (
    "core::result::Result::<core::result::Result<T,E>,E>::flatten"
)
VECDEQUE_AS_MUT_SLICES_TARGET = "alloc::collections::VecDeque::as_mut_slices"
VECDEQUE_AS_MUT_SLICES_SKIP_RATIONALE = (
    "Rust 1.96 documents that VecDeque::as_mut_slices returns the deque "
    "contents as two slices, but unless make_contiguous was previously called "
    "the exact split point depends on implementation details and is not "
    "guaranteed. Without exposing that hidden ring-buffer split point, an exec "
    "spec cannot deterministically specify each returned mutable slice; the "
    "concatenation-only relation is underdetermined, so this target is skipped "
    "instead of emitted as a raw add_spec."
)
PANIC_LOCATION_SKIP_TOKENS = (
    "this method will currently always return [`some`]",
    "pub fn location(&self) -> option<&location<'_>>",
    "some(&self.location)",
)
PANIC_LOCATION_SKIP_RATIONALE = (
    "Rust 1.96 documents PanicInfo/PanicHookInfo::location as currently "
    "always returning Some and implements each target by returning "
    "Some(&self.location). The existing vstd Location view models the fields "
    "of a Location reference, but there is no public PanicInfo/PanicHookInfo "
    "abstraction tying the receiver to its stored location reference. The "
    "residual add_spec attempts either failed typechecking or left the returned "
    "reference semantics underdetermined. Without a new vstd abstraction, an "
    "exec contract would be underchecked and brittle against the documented "
    "future possibility of None, so this source-backed row is skipped."
)
PANIC_LOCATION_SKIP_RISKS = (
    "A Some-only contract does not specify the returned Location reference or its fields.",
    "A precise contract would need a public vstd model for the stored panic location reference.",
)
PANIC_LOCATION_SKIP_ISSUES = (
    "classification:needs_new_vstd_abstraction",
    "panic_location_abstraction_missing",
)
SOURCE_BACKED_RESIDUAL_ADD_SPEC_SKIP_TARGETS = {
    "alloc::borrow::Cow::to_mut": {
        "tokens": (
            "acquires a mutable reference to the owned form of the data",
            "clones the data if it is not already owned",
            "pub fn to_mut(&mut self) -> &mut <b as toowned>::owned",
            "*self = owned(borrowed.to_owned())",
            "owned(ref mut owned) => owned",
        ),
        "rationale": (
            "Rust 1.96 implements Cow::to_mut by returning the existing owned "
            "payload or cloning a borrowed payload into Cow::Owned before "
            "returning a mutable reference to that owned value. Current vstd "
            "vocabulary has no public model that relates the Cow enum payload, "
            "the ToOwned clone result, and the returned mutable reference across "
            "both source branches. The residual contract failed typechecking and "
            "would otherwise rely on unsupported enum-payload/mutable-reference "
            "reasoning, so this source-backed row is skipped rather than emitted "
            "as an underchecked assume_specification."
        ),
        "risks": (
            "A useful contract would need public Cow payload and ToOwned clone-result models.",
            "A branch-only contract leaves the returned mutable reference and final owned payload underdetermined.",
        ),
        "issues": (
            "classification:determinism_checker_unsupported",
            "cow_to_mut_payload_reference_model_missing",
        ),
    },
    "core::result::Result::as_deref_mut": {
        "tokens": (
            "converts from `result<t, e>` (or `&mut result<t, e>`) to `result<&mut <t as derefmut>::target, &mut e>`",
            "coerces the [`ok`] variant of the original [`result`] via [`derefmut`]",
            "pub const fn as_deref_mut(&mut self) -> result<&mut t::target, &mut e>",
            "t: [const] derefmut",
            "self.as_mut().map(derefmut::deref_mut)",
        ),
        "rationale": (
            "Rust 1.96 implements Result::as_deref_mut by taking a mutable view of "
            "the Result and mapping an Ok payload through DerefMut::deref_mut, "
            "while Err returns a mutable reference to the error payload. Current "
            "vstd vocabulary has no public law relating an arbitrary DerefMut "
            "target to the original payload, and the residual variant-only "
            "contract failed typechecking while leaving payload/reference behavior "
            "unmodeled. This source-backed row is skipped rather than emitted as "
            "an underchecked assume_specification."
        ),
        "risks": (
            "A variant-only contract permits arbitrary Ok/Err mutable-reference payloads.",
            "A precise contract would need a public DerefMut target relation and mutable Result payload model.",
        ),
        "issues": (
            "classification:determinism_checker_unsupported",
            "deref_mut_result_payload_model_missing",
        ),
    },
    "std::collections::HashMap::get_disjoint_mut": {
        "tokens": (
            "returns an array of length `n` with the results of each query",
            "`none` will be used if",
            "duplicate keys panic",
            "pub fn get_disjoint_mut<q: ?sized, const n: usize>",
            "self.base.get_disjoint_mut(ks)",
        ),
        "rationale": (
            "Rust 1.96 implements HashMap::get_disjoint_mut by delegating to the "
            "base map, returning an array of optional mutable references for "
            "distinct queried keys, using None for missing keys, and panicking on "
            "duplicates. The residual contract required borrowed-key/hash-builder "
            "semantic assumptions and also depends on unsupported arrays of mutable "
            "references. Rather than adding source-unjustified preconditions or "
            "accepting an unsupported mutable-reference array contract, this "
            "source-backed row is skipped."
        ),
        "risks": (
            "A domain-only contract leaves each returned mutable reference and duplicate-key panic behavior underdetermined.",
            "A precise contract would need source-justified borrowed-key/hash-builder laws plus an array-of-mutable-reference model.",
        ),
        "issues": (
            "classification:determinism_checker_unsupported",
            "hashmap_get_disjoint_mut_reference_array_model_missing",
        ),
    },
    "core::panic::PanicInfo::location": {
        "tokens": PANIC_LOCATION_SKIP_TOKENS,
        "rationale": PANIC_LOCATION_SKIP_RATIONALE,
        "risks": PANIC_LOCATION_SKIP_RISKS,
        "issues": PANIC_LOCATION_SKIP_ISSUES,
    },
    "std::panic::PanicHookInfo::location": {
        "tokens": PANIC_LOCATION_SKIP_TOKENS,
        "rationale": PANIC_LOCATION_SKIP_RATIONALE,
        "risks": PANIC_LOCATION_SKIP_RISKS,
        "issues": PANIC_LOCATION_SKIP_ISSUES,
    },
    "std::panic::PanicInfo::location": {
        "tokens": PANIC_LOCATION_SKIP_TOKENS,
        "rationale": PANIC_LOCATION_SKIP_RATIONALE,
        "risks": PANIC_LOCATION_SKIP_RISKS,
        "issues": PANIC_LOCATION_SKIP_ISSUES,
    },
}
SOURCE_BACKED_HIGHER_ORDER_CLOSURE_SKIP_TARGETS = {
    "alloc::collections::VecDeque::binary_search_by": {
        "tokens": (
            "comparator function should return an order code",
            "if the `vecdeque` is not sorted or if the comparator function does not",
            "unspecified and meaningless",
            "multiple matches",
            "one of the matches could be returned",
            "pub fn binary_search_by<'a, f>(&'a self, mut f: f) -> result<usize, usize>",
            "f: fnmut(&'a t) -> ordering",
            "let cmp_back = back.first().map(|elem| f(elem))",
            "back.binary_search_by(f).map(|idx| idx + front.len()).map_err(|idx| idx + front.len())",
            "front.binary_search_by(f)",
        ),
        "rationale": (
            "Rust 1.96 makes VecDeque::binary_search_by depend on a stateful "
            "higher-order closure: the comparator is `F: FnMut(&T) -> Ordering`, "
            "is called on the split back/front slices, and the docs require it to "
            "be consistent with the sorted order while permitting any duplicate "
            "match. Current vstd vocabulary has no model for those FnMut call "
            "observations or duplicate-match choice, so the prior bounds-only "
            "contract left the comparator relation and selected result "
            "underdetermined. This source-backed row is skipped rather than "
            "emitted as an underdetermined assume_specification."
        ),
        "risks": (
            "A result-bounds-only contract permits outputs unrelated to the comparator closure.",
            "A precise contract would need a public model of FnMut comparator calls and duplicate-match selection.",
        ),
        "issues": (
            "classification:higher_order_contract",
            "higher_order_closure_comparator_underdetermined",
        ),
    },
    "core::iter::Peekable::next_if_eq": {
        "tokens": (
            "pub fn next_if(&mut self, func: impl fnonce(&i::item) -> bool) -> option<i::item>",
            "some(matched) if func(&matched) => some(matched)",
            "self.peeked = some(other)",
            "pub fn next_if_eq<t>(&mut self, expected: &t) -> option<i::item>",
            "i::item: partialeq<t>",
            "self.next_if(|next| next == expected)",
        ),
        "rationale": (
            "Rust 1.96 implements Peekable::next_if_eq by delegating to "
            "`next_if`, whose `FnOnce(&I::Item) -> bool` predicate observes the "
            "candidate item before either consuming it or restoring it into the "
            "hidden `peeked` slot. The equality predicate is supplied as the "
            "closure `|next| next == expected`, but current vstd vocabulary has "
            "no public model for the `next_if` closure observation, `PartialEq` "
            "call result, or hidden Peekable state restoration. The prior "
            "sequence-shaped contract therefore left the consumed-versus-kept "
            "branch underdetermined, so this source-backed row is skipped rather "
            "than emitted as an underdetermined assume_specification."
        ),
        "risks": (
            "A return/sequence-only contract permits outcomes unrelated to the equality predicate observation.",
            "A precise contract would need a public model for Peekable::next_if closure calls, PartialEq results, and hidden peeked-state restoration.",
        ),
        "issues": (
            "classification:iterator_or_adapter_result",
            "peekable_next_if_closure_observation_underdetermined",
        ),
    },
    "core::iter::Peekable::next_if_map_mut": {
        "tokens": (
            "pub fn next_if_map_mut<r>(&mut self, f: impl fnonce(&mut i::item) -> option<r>) -> option<r>",
            "let unpeek = if let some(mut item) = self.next()",
            "match f(&mut item)",
            "some(result) => return some(result)",
            "none => some(item)",
            "self.peeked = some(unpeek)",
        ),
        "rationale": (
            "Rust 1.96 implements Peekable::next_if_map_mut by consuming the next "
            "item, calling an arbitrary `FnOnce(&mut I::Item) -> Option<R>` on a "
            "mutable reference to that item, returning the closure's `Some` "
            "payload when present, or storing the possibly mutated item back into "
            "the hidden `peeked` slot on `None`. Current vstd vocabulary has no "
            "public model for that mutable closure observation, returned `R`, "
            "or hidden Peekable state restoration. The prior observable-shape "
            "contract therefore left both the returned value and kept item "
            "underdetermined, so this source-backed row is skipped rather than "
            "emitted as an underdetermined assume_specification."
        ),
        "risks": (
            "A length/suffix-only contract permits arbitrary returned values and kept items unrelated to the mutable closure call.",
            "A precise contract would need a public model for FnOnce mutable item observations and Peekable's hidden peeked-state update.",
        ),
        "issues": (
            "classification:iterator_or_adapter_result",
            "peekable_next_if_map_mut_closure_observation_underdetermined",
        ),
    },
    "core::ops::Bound::map": {
        "tokens": (
            "maps a `bound<t>` to a `bound<u>` by applying a function to the contained value",
            "returning a `bound` of the same kind",
            "pub fn map<u, f: fnonce(t) -> u>(self, f: f) -> bound<u>",
            "unbounded => unbounded",
            "included(x) => included(f(x))",
            "excluded(x) => excluded(f(x))",
        ),
        "rationale": (
            "Rust 1.96 implements Bound::map by preserving the Bound variant and "
            "calling an arbitrary `F: FnOnce(T) -> U` on the contained payload for "
            "`Included` and `Excluded`. Current vstd vocabulary has no public "
            "model for the consumed closure observation or its returned `U`, so "
            "a variant-only or constructor-shaped contract leaves the mapped "
            "payload underdetermined. This source-backed row is skipped rather "
            "than emitted as an underdetermined assume_specification."
        ),
        "risks": (
            "A variant-preservation contract permits arbitrary payloads unrelated to the FnOnce closure result.",
            "A precise contract would need a public model of FnOnce calls over consumed Bound payloads.",
        ),
        "issues": (
            "classification:higher_order_contract",
            "higher_order_closure_result_underdetermined",
        ),
    },
    "core::slice::binary_search_by": {
        "tokens": (
            "comparator function should return an order code",
            "if the slice is not sorted or if the comparator function does not",
            "unspecified and meaningless",
            "multiple matches",
            "one of the matches could be returned",
            "deterministically, but is subject to change in future versions of rust",
            "pub fn binary_search_by<'a, f>(&'a self, mut f: f) -> result<usize, usize>",
            "f: fnmut(&'a t) -> ordering",
            "let cmp = f(unsafe { self.get_unchecked(mid) })",
            "let cmp = f(unsafe { self.get_unchecked(base) })",
        ),
        "rationale": (
            "Rust 1.96 makes slice::binary_search_by depend on a stateful "
            "higher-order closure: the comparator is `F: FnMut(&T) -> Ordering`, "
            "is called on probed elements, must be consistent with the sorted "
            "order, and duplicate matches may return any matching index with an "
            "implementation choice that can change across Rust versions. Current "
            "vstd vocabulary has no model for those FnMut comparator observations "
            "or duplicate-match choice, so the prior bounds-only contract left "
            "the comparator relation and selected result underdetermined. This "
            "source-backed row is skipped rather than emitted as an "
            "underdetermined assume_specification."
        ),
        "risks": (
            "A result-bounds-only contract permits outputs unrelated to the comparator closure.",
            "A precise contract would need a public model of FnMut comparator calls, sortedness consistency, and duplicate-match selection.",
        ),
        "issues": (
            "classification:higher_order_contract",
            "higher_order_closure_comparator_underdetermined",
        ),
    },
    "core::slice::binary_search_by_key": {
        "tokens": (
            "assumes that the slice is sorted by the key",
            "using the same key extraction function",
            "if the slice is not sorted by the key",
            "unspecified and meaningless",
            "multiple matches",
            "one of the matches could be returned",
            "deterministically, but is subject to change in future versions of rust",
            "pub fn binary_search_by_key<'a, b, f>(&'a self, b: &b, mut f: f) -> result<usize, usize>",
            "f: fnmut(&'a t) -> b",
            "b: ord",
            "self.binary_search_by(|k| f(k).cmp(b))",
        ),
        "rationale": (
            "Rust 1.96 makes slice::binary_search_by_key depend on a stateful "
            "higher-order closure: the key extractor is `F: FnMut(&T) -> B`, "
            "the key type is ordered, and the body delegates to "
            "`binary_search_by` by comparing `f(k)` with the query key. The docs "
            "require sortedness by that same key function and permit any "
            "duplicate match, with the chosen duplicate index subject to future "
            "Rust changes. Current vstd vocabulary has no model for FnMut key "
            "observations or duplicate-match choice, so the prior bounds-only "
            "contract left the key relation and selected result underdetermined. "
            "This source-backed row is skipped rather than emitted as an "
            "underdetermined assume_specification."
        ),
        "risks": (
            "A result-bounds-only contract permits outputs unrelated to the key-extraction closure.",
            "A precise contract would need a public model of FnMut key calls, Ord comparison of extracted keys, and duplicate-match selection.",
        ),
        "issues": (
            "classification:higher_order_contract",
            "higher_order_closure_key_extraction_underdetermined",
        ),
    },
    "core::slice::is_sorted_by_key": {
        "tokens": (
            "checks if the elements of this slice are sorted using the given key extraction function",
            "compares the keys",
            "as determined by `f`",
            "pub fn is_sorted_by_key<'a, f, k>(&'a self, f: f) -> bool",
            "f: fnmut(&'a t) -> k",
            "k: partialord",
            "self.iter().is_sorted_by_key(f)",
        ),
        "rationale": (
            "Rust 1.96 makes slice::is_sorted_by_key depend on a stateful "
            "higher-order closure: the key extractor is `F: FnMut(&T) -> K`, "
            "the key type is only `PartialOrd`, and the body delegates to the "
            "iterator key-sortedness check over values produced by that closure. "
            "Current vstd vocabulary has no model for FnMut key observations or "
            "PartialOrd key comparisons across adjacent elements, so a contract "
            "that only states vacuous empty/singleton behavior leaves the "
            "key-extraction relation and general boolean result underdetermined. "
            "This source-backed row is skipped rather than emitted as an "
            "underdetermined assume_specification."
        ),
        "risks": (
            "An empty/singleton-only contract leaves ordinary multi-element results unrelated to the key closure.",
            "A precise contract would need a public model of FnMut key calls and PartialOrd comparisons on extracted keys.",
        ),
        "issues": (
            "classification:higher_order_contract",
            "higher_order_closure_key_extraction_underdetermined",
        ),
    },
}
STR_RSPLIT_ONCE_TARGET = "core::str::rsplit_once"
STR_RSPLIT_ONCE_SKIP_RATIONALE = (
    "Rust 1.96 implements str::rsplit_once through the generic Pattern "
    "searcher with a ReverseSearcher bound and `next_match_back()`, returning "
    "prefix/suffix slices around the last delimiter match or None when no "
    "match exists. Current vstd vocabulary has no semantic model for generic "
    "Pattern/ReverseSearcher matching, so a structural subrange contract both "
    "fails Verus typechecking on the unstable pattern API and underconstrains "
    "delimiter matching, last-match selection, and None behavior. This target "
    "is therefore source-backed as a skip rather than emitted as an "
    "underdetermined assume_specification."
)
SLICE_SPLIT_OFF_SKIP_RATIONALE = (
    "Rust 1.96 implements slice::split_off for `R: OneSidedRange<usize>` "
    "by using `split_point_of(range)?` to derive a hidden `(Direction, "
    "split_index)`, returning `None` before mutation when `split_index > "
    "self.len()`, then splitting with `split_at(split_index)` and choosing "
    "the returned and retained sides through `Direction::Front` or "
    "`Direction::Back`. Current vstd vocabulary does not expose the "
    "OneSidedRange-to-direction/split-index relation, so a concatenation-only "
    "or Front/Back-disjunctive postcondition leaves the modeled output "
    "underdetermined for a fixed range. A precise deterministic contract would "
    "need a source-backed model of OneSidedRange and split_point_of semantics, "
    "so this target is source-backed as a skip rather than emitted as an "
    "underdetermined assume_specification."
)
SOURCE_BACKED_PATTERN_STRING_SKIP_TARGETS = {
    "core::str::rfind": {
        "tokens": (
            "returns the byte index for the first character of the last match of the pattern",
            "pub fn rfind<p: pattern>",
            "p::searcher<'a>: reversesearcher<'a>",
            "pat.into_searcher(self).next_match_back().map(|(i, _)| i)",
        ),
        "rationale": (
            "Rust 1.96 implements str::rfind through the generic Pattern "
            "searcher with a ReverseSearcher bound and `next_match_back()`, "
            "returning the byte index of the last match or None when the "
            "pattern does not match. Current vstd vocabulary has no semantic "
            "model for generic Pattern/Searcher/ReverseSearcher matching, so "
            "a bound-only index contract leaves the matched-pattern relation, "
            "last-match selection, and None behavior underdetermined. This "
            "target is therefore source-backed as a skip rather than emitted "
            "as an underdetermined assume_specification."
        ),
        "risks": (
            "A contract that only bounds the returned index leaves the actual Pattern match relation underdetermined.",
            "A precise contract would need a vstd model of generic Pattern/Searcher/ReverseSearcher semantics that is not currently available.",
        ),
        "issues": (
            "classification:associated_type_or_projection",
            "generic_pattern_reverse_search_underdetermined",
        ),
    },
    "core::str::trim_start_matches": {
        "tokens": (
            "returns a string slice with all prefixes that match a pattern",
            "repeatedly removed",
            "pub fn trim_start_matches<p: pattern>",
            "let mut matcher = pat.into_searcher(self)",
            "matcher.next_reject()",
            "self.get_unchecked(i..self.len())",
        ),
        "rationale": (
            "Rust 1.96 implements str::trim_start_matches through the generic "
            "Pattern searcher, using `next_reject()` to find the suffix left "
            "after repeatedly removing matching prefixes and then returning an "
            "unchecked slice. Current vstd vocabulary has no semantic model "
            "for generic Pattern/Searcher matching, so a suffix-only contract "
            "leaves the removed-prefix Pattern relation, repeated-removal "
            "maximality, and all-matched case underdetermined. This target is "
            "therefore source-backed as a skip rather than emitted as an "
            "underdetermined assume_specification."
        ),
        "risks": (
            "A contract that only says the result is a suffix leaves which prefixes matched the Pattern underdetermined.",
            "A precise contract would need a vstd model of generic Pattern/Searcher semantics that is not currently available.",
        ),
        "issues": (
            "classification:complex_result_or_pattern_model",
            "generic_pattern_prefix_trim_underdetermined",
        ),
    },
    "core::str::trim_right_matches": {
        "tokens": (
            "returns a string slice with all suffixes that match a pattern",
            "repeatedly removed",
            "pub fn trim_right_matches<p: pattern>",
            "p::searcher<'a>: reversesearcher<'a>",
            "self.trim_end_matches(pat)",
        ),
        "rationale": (
            "Rust 1.96 implements deprecated str::trim_right_matches as a "
            "direct delegation to trim_end_matches under the same generic "
            "Pattern and ReverseSearcher bound, repeatedly removing matching "
            "suffixes. Current vstd vocabulary has no semantic model for "
            "generic Pattern/Searcher/ReverseSearcher matching, so a "
            "prefix-only contract leaves the removed-suffix Pattern relation, "
            "repeated-removal maximality, and all-matched case "
            "underdetermined. This target is therefore source-backed as a "
            "skip rather than emitted as an underdetermined "
            "assume_specification."
        ),
        "risks": (
            "A contract that only says the result is a prefix leaves which suffixes matched the Pattern underdetermined.",
            "A precise contract would need a vstd model of generic Pattern/Searcher/ReverseSearcher semantics that is not currently available.",
        ),
        "issues": (
            "classification:associated_type_or_projection",
            "generic_pattern_suffix_trim_underdetermined",
        ),
    },
}
SELECT_NTH_UNSTABLE_PARTITION_SKIP_TARGETS = {
    "core::slice::select_nth_unstable": (
        "pub fn select_nth_unstable(&mut self, index: usize)",
        "sort::select::partition_at_index",
        "the unsorted subslice before `index`",
        "the unsorted subslice after `index`",
        "we are only guaranteed the slice will be one of the following",
        "about the specified index",
        "assert!(lesser == [-3, -5] || lesser == [-5, -3])",
        "assert!(greater == [4, 2] || greater == [2, 4])",
    ),
    "core::slice::select_nth_unstable_by": (
        "pub fn select_nth_unstable_by<f>",
        "sort::select::partition_at_index",
        "the unsorted subslice after `index`",
        "compare(x, self[index]).is_ge()",
        "we are only guaranteed the slice will be one of the following",
        "about the specified index",
        "assert!(before == [4, 2] || before == [2, 4])",
        "assert!(after == [-3, -5] || after == [-5, -3])",
    ),
    "core::slice::select_nth_unstable_by_key": (
        "pub fn select_nth_unstable_by_key<k, f>",
        "sort::select::partition_at_index",
        "the unsorted subslice after `index`",
        "f(x) >= f(self[index])",
        "we are only guaranteed the slice will be one of the following",
        "about the specified index",
        "assert!(lesser == [1, 2] || lesser == [2, 1])",
        "assert!(greater == [4, -5] || greater == [-5, 4])",
    ),
}
SELECT_NTH_UNSTABLE_PARTITION_SKIP_RATIONALE = (
    "Rust 1.96 source_context documents that select_nth_unstable returns a "
    "three-way partition but leaves the before/after partition order unsorted "
    "and explicitly permits multiple reordered slice outcomes. A deterministic "
    "exec spec for the exact returned mutable slices and final slice would "
    "over-specify that permitted ordering, while a partition-only relation "
    "leaves the outputs underdetermined, so this target is source-backed as a "
    "skip rather than emitted as a raw add_spec."
)
RANGE_INCLUSIVE_EXHAUSTION_TARGETS = {
    "core::ops::RangeInclusive::start",
    "core::ops::RangeInclusive::end",
}
RANGE_INCLUSIVE_EXHAUSTION_SKIP_RATIONALE = (
    "Rust 1.96 documents that when a RangeInclusive is used for iteration, "
    "the values returned by start() and end() are unspecified after iteration "
    "has ended, and separately notes that this accessor's returned value is "
    "unspecified after the range has been iterated to exhaustion. An exec spec "
    "would have to constrain the accessor result in exhausted states that Rust "
    "leaves unspecified, so this target is source-backed as a skip rather than "
    "emitted as a deterministic assume_specification."
)
VSTD_DUPLICATE_ASSUME_SPECIFICATION_TARGETS = {
    "alloc::string::String::try_reserve_exact": {
        "source_file": "std_specs/capacity.rs",
        "source_line": 107,
        "target_fragment": "assume_specification[ String::try_reserve_exact ]",
        "rationale": (
            "Verus vstd already provides a trusted assume_specification for "
            "String::try_reserve_exact in std_specs/capacity.rs:107. Emitting "
            "another Rust std exec spec for the same target would duplicate "
            "existing vstd coverage and can trigger duplicate-specification "
            "failures, so this target is source-backed as a skip."
        ),
    },
    "core::alloc::Layout::array": {
        "source_file": "std_specs/layout_value.rs",
        "source_line": 220,
        "target_fragment": "assume_specification<T>[ Layout::array::<T> ]",
        "rationale": (
            "Verus vstd already provides a trusted assume_specification for "
            "Layout::array::<T> in std_specs/layout_value.rs:220. Emitting "
            "another Rust std exec spec for the same target would duplicate "
            "existing vstd coverage and can trigger duplicate-specification "
            "failures, so this target is source-backed as a skip."
        ),
    },
}
SOURCE_BACKED_MUT_SLICE_CHUNK_PARTITION_TARGETS = {
    SLICE_AS_CHUNKS_MUT_TARGET,
    SLICE_AS_RCHUNKS_MUT_TARGET,
}
SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS = {
    "core::array::from_mut",
    "core::slice::from_mut",
    "core::array::as_mut_slice",
    *SOURCE_BACKED_OPTION_MUT_ARRAY_VIEW_TARGETS,
}
SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_CONTRACT_TARGETS = {
    "core::array::from_mut::<T>": "core::array::from_mut",
    "core::slice::from_mut": "core::slice::from_mut",
    "core::slice::from_mut::<T>": "core::slice::from_mut",
    "<[T; N]>::as_mut_slice": "core::array::as_mut_slice",
    "<[T]>::as_mut_array": SLICE_AS_MUT_ARRAY_TARGET,
    "<[T]>::as_mut_array::<N>": SLICE_AS_MUT_ARRAY_TARGET,
    "<[T]>::first_chunk_mut": SLICE_FIRST_CHUNK_MUT_TARGET,
    "<[T]>::first_chunk_mut::<N>": SLICE_FIRST_CHUNK_MUT_TARGET,
    "<[T]>::last_chunk_mut": SLICE_LAST_CHUNK_MUT_TARGET,
    "<[T]>::last_chunk_mut::<N>": SLICE_LAST_CHUNK_MUT_TARGET,
}
SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_CONTRACT_TARGETS = {
    "<[T]>::split_first_chunk_mut": SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET,
    "<[T]>::split_first_chunk_mut::<N>": SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET,
    "<[T]>::split_last_chunk_mut": SLICE_SPLIT_LAST_CHUNK_MUT_TARGET,
    "<[T]>::split_last_chunk_mut::<N>": SLICE_SPLIT_LAST_CHUNK_MUT_TARGET,
}
SOURCE_BACKED_MUT_SLICE_CHUNK_PARTITION_CONTRACT_TARGETS = {
    "<[T]>::as_chunks_mut": SLICE_AS_CHUNKS_MUT_TARGET,
    "<[T]>::as_chunks_mut::<N>": SLICE_AS_CHUNKS_MUT_TARGET,
    "<[T]>::as_rchunks_mut": SLICE_AS_RCHUNKS_MUT_TARGET,
    "<[T]>::as_rchunks_mut::<N>": SLICE_AS_RCHUNKS_MUT_TARGET,
}
SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_CONTRACT_TARGETS = {
    "<[T]>::split_first_mut": SLICE_SPLIT_FIRST_MUT_TARGET,
    "<[T]>::split_last_mut": SLICE_SPLIT_LAST_MUT_TARGET,
    "<[T]>::split_off_first_mut": SLICE_SPLIT_OFF_FIRST_MUT_TARGET,
    "<[T]>::split_off_last_mut": SLICE_SPLIT_OFF_LAST_MUT_TARGET,
}
SOURCE_BACKED_MAP_GET_MUT_CONTRACT_TARGETS = {
    (
        "alloc::collections::BTreeMap::<Key, Value, A>::get_mut::<Q>"
    ): BTREEMAP_GET_MUT_TARGET,
    (
        "std::collections::HashMap::<Key, Value, S, A>::get_mut::<Q>"
    ): HASHMAP_GET_MUT_TARGET,
}
SOURCE_BACKED_LINKEDLIST_BACK_MUT_CONTRACT_TARGETS = {
    "alloc::collections::LinkedList::<T, A>::back_mut": LINKEDLIST_BACK_MUT_TARGET,
    "LinkedList::<T, A>::back_mut": LINKEDLIST_BACK_MUT_TARGET,
}
SOURCE_BACKED_ARRAY_EACH_MUT_CONTRACT_TARGETS = {
    "<[T; N]>::each_mut": ARRAY_EACH_MUT_TARGET,
}


GENERATION_PROMPT = """\
You are proposing a trusted Verus contract for one Rust standard-library API
used by Nanvix but not currently covered by Verus vstd.

Target:
```json
{target_summary}
```

Rust 1.96 declaration metadata used by the current Verus toolchain:
```json
{verification_declaration}
```

Rust 1.96 source context:
```rust
{verification_source}
```

Nanvix's Rust 1.99 source context:
```rust
{nanvix_source}
```

Related existing vstd contracts:
```rust
{vstd_context}
```

Return JSON only:
{{
  "decision": "add_spec" | "skip",
  "contract_form": "assume_specification" | "external_trait_specification",
  "contract_code": "complete Verus declaration(s), without a verus! wrapper",
  "requires": ["Verus boolean expression", "..."],
  "ensures": ["Verus boolean expression", "..."],
  "feature_gates": ["allocator_api", "..."],
  "imports": ["core::...", "alloc::...", "vstd::..."],
  "useful": true | false,
  "rationale": "short explanation grounded in the supplied source",
  "risks": ["..."]
}}

Rules:
- Do not edit files.
- A Rust external contract is trusted: determinism does not establish soundness.
  Only state facts justified by the supplied Rust implementation or docs.
- Use the exact Rust 1.96 signature. For a non-unit return, bind the result by
  name so the ensures clauses can reference it.
- Preserve impl-level and method-level bounds exactly, including repeated bounds
  that `assume_specification` signature matching may require.
- Every mutable-reference parameter must use `old(x)` or `final(x)` in clauses;
  never write a bare `x@` for an `&mut` parameter.
- Use fully qualified Rust paths where practical.
- Do not add `cfg` or `cfg_attr` attributes; the runner validates the contract
  unconditionally.
- Use existing public vstd specification vocabulary. Do not invent access to
  private fields or hidden runtime state.
- Do not use `true`, `false`, `arbitrary()`, `assume`, `requires false`, or a
  postcondition that merely repeats a precondition.
- Distinguish semantic views from pointer/reference identity.
- If a useful relation only holds under an existing law such as
  `obeys_cmp::<T>()`, make that law a `requires` clause rather than leaving the
  other branch unconstrained behind an implication.
- For I/O, OS, formatting, synchronization, allocation, nondeterministic, or
  hidden-state APIs, choose skip unless a useful sound result relation is
  expressible without modeling hidden state.
- For trait methods, use external_trait_specification only if a complete,
  typecheckable declaration can be given; otherwise choose skip.
- If no useful non-vacuous contract is expressible, choose skip and leave
  contract_code/requires/ensures empty.
"""


FEEDBACK_PROMPT = """\
Revise a proposed trusted Verus contract after typechecking and determinism
feedback.

Target: {target}

Previous proposal:
```json
{candidate}
```

Checker result:
```json
{checker}
```

Semantic and anti-vacuity issues:
```json
{issues}
```

Rust 1.96 declaration/source:
```json
{verification_declaration}
```
```rust
{verification_source}
```

Return JSON only with the same schema as before.

Do not optimize merely for `R0 = unsat`. The declaration must first typecheck,
remain source-justified, use an observable semantic output, and avoid false or
redundant domains. Choose skip when the API cannot receive a useful ordinary
contract in existing vstd vocabulary.
"""


def safe_name(path: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "__", path).strip("_")


def call_copilot(
    *,
    prompt: str,
    model: str,
    copilot_bin: str,
    timeout: int,
    cwd: Path,
    retries: int,
) -> str:
    command = [
        copilot_bin,
        "--model",
        model,
        "-s",
        "--no-auto-update",
        "--allow-all-tools",
        "--allow-all-paths",
        "-p",
        prompt,
    ]
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            process = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if process.returncode == 0:
                return process.stdout
            last_error = RuntimeError(
                process.stderr.strip()
                or f"copilot exited {process.returncode}"
            )
        except subprocess.TimeoutExpired as error:
            last_error = error
        if attempt < retries:
            time.sleep(2)
    assert last_error is not None
    raise last_error


def parse_json_response(text: str) -> dict[str, Any]:
    blocks = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.DOTALL)
    candidates = list(reversed(blocks)) + [text]
    decoder = json.JSONDecoder()
    for candidate in candidates:
        candidate = candidate.strip()
        try:
            value = json.loads(candidate)
            if isinstance(value, dict):
                return value
        except json.JSONDecodeError:
            pass
        for match in re.finditer(r"\{", candidate):
            try:
                value, _ = decoder.raw_decode(candidate[match.start() :])
                if isinstance(value, dict):
                    return value
            except json.JSONDecodeError:
                continue
    raise ValueError("Copilot response did not contain valid JSON")


def strip_code_fences(text: str) -> str:
    text = text.strip()
    match = re.fullmatch(r"```(?:rust)?\s*(.*?)```", text, flags=re.DOTALL)
    return match.group(1).strip() if match else text


def normalized_contract_code(value: Any, decision: str = "") -> str:
    if value is None:
        return ""
    code = strip_code_fences(str(value))
    if decision == "skip" and code.strip() == "None":
        return ""
    return code


def normalize_candidate_contract_code(candidate: dict[str, Any]) -> bool:
    decision = str(candidate.get("decision", "")).strip()
    if "contract_code" not in candidate and decision != "skip":
        return False
    original = candidate.get("contract_code")
    normalized = normalized_contract_code(original, decision)
    if original == normalized:
        return False
    candidate["contract_code"] = normalized
    return True


def normalize_result_contract_codes(result: dict[str, Any]) -> bool:
    changed = False
    records = list(result.get("history") or [])
    final = result.get("final")
    if isinstance(final, dict):
        records.append(final)
    for record in records:
        candidate = record.get("candidate") if isinstance(record, dict) else None
        if isinstance(candidate, dict):
            changed = normalize_candidate_contract_code(candidate) or changed
    return changed


def sanitize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    result = dict(candidate)
    result["decision"] = str(result.get("decision", "")).strip()
    result["contract_form"] = str(result.get("contract_form", "")).strip()
    result["contract_code"] = normalized_contract_code(
        result.get("contract_code"),
        result["decision"],
    )
    for key in ("requires", "ensures", "feature_gates", "imports", "risks"):
        value = result.get(key) or []
        if not isinstance(value, list):
            value = [value]
        result[key] = [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]
    return result


def entry_source_text(entry: dict[str, Any]) -> str:
    pieces: list[str] = []
    for key in ("declarations", "verification_declarations"):
        for declaration in entry.get(key) or []:
            pieces.append(str(declaration.get("source_context") or ""))
    return "\n".join(pieces).lower()


def vecdeque_as_mut_slices_source_documents_hidden_split(
    entry: dict[str, Any],
) -> bool:
    source_text = entry_source_text(entry)
    return (
        entry.get("target") == VECDEQUE_AS_MUT_SLICES_TARGET
        and "exact split point depends on implementation details" in source_text
        and "not guaranteed" in source_text
    )


def vecdeque_as_mut_slices_skip_candidate() -> dict[str, Any]:
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": ["allocator_api"],
        "imports": ["alloc::alloc::Allocator", "alloc::collections::VecDeque"],
        "useful": False,
        "rationale": VECDEQUE_AS_MUT_SLICES_SKIP_RATIONALE,
        "risks": [
            (
                "A contract that constrains only the concatenation leaves the "
                "two returned mutable slices individually underdetermined."
            ),
            (
                "Specifying a concrete split point would expose an "
                "implementation detail Rust explicitly does not guarantee."
            ),
        ],
    }


def residual_add_spec_source_supports_skip(entry: dict[str, Any]) -> bool:
    skip = SOURCE_BACKED_RESIDUAL_ADD_SPEC_SKIP_TARGETS.get(
        str(entry.get("target") or "")
    )
    if skip is None:
        return False
    source_text = re.sub(r"\s+", " ", entry_source_text(entry)).lower()
    return all(str(token).lower() in source_text for token in skip["tokens"])


def residual_add_spec_skip_candidate(target: str) -> dict[str, Any]:
    skip = SOURCE_BACKED_RESIDUAL_ADD_SPEC_SKIP_TARGETS[target]
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": str(skip["rationale"]),
        "risks": [str(risk) for risk in skip["risks"]],
    }


def higher_order_closure_source_documents_underdetermined(
    entry: dict[str, Any],
) -> bool:
    skip = SOURCE_BACKED_HIGHER_ORDER_CLOSURE_SKIP_TARGETS.get(
        str(entry.get("target") or "")
    )
    if skip is None:
        return False
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    return all(str(token).lower() in source_text for token in skip["tokens"])


def higher_order_closure_skip_candidate(target: str) -> dict[str, Any]:
    skip = SOURCE_BACKED_HIGHER_ORDER_CLOSURE_SKIP_TARGETS[target]
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": str(skip["rationale"]),
        "risks": [str(risk) for risk in skip["risks"]],
    }


def str_rsplit_once_source_documents_generic_reverse_search(
    entry: dict[str, Any],
) -> bool:
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    return (
        entry.get("target") == STR_RSPLIT_ONCE_TARGET
        and "splits the string on the last occurrence" in source_text
        and "pub fn rsplit_once<p: pattern>" in source_text
        and "p::searcher<'a>: reversesearcher<'a>" in source_text
        and "delimiter.into_searcher(self).next_match_back()?" in source_text
        and "self.get_unchecked(..start)" in source_text
        and "self.get_unchecked(end..)" in source_text
    )


def str_rsplit_once_skip_candidate() -> dict[str, Any]:
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": STR_RSPLIT_ONCE_SKIP_RATIONALE,
        "risks": [
            (
                "A prefix/suffix-only contract leaves the delimiter relation, "
                "last-match choice, and None case underdetermined."
            ),
            (
                "A precise contract would need a vstd model of generic "
                "Pattern/ReverseSearcher semantics that is not currently "
                "available."
            ),
        ],
    }


def slice_split_off_source_documents_one_sided_range_direction(
    entry: dict[str, Any],
) -> bool:
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    tokens = (
        "onesidedrange<usize>",
        "split_point_of(range)?",
        "if split_index > self.len()",
        "return none;",
        "self.split_at(split_index)",
        "direction::front",
        "direction::back",
    )
    return entry.get("target") == SLICE_SPLIT_OFF_TARGET and all(
        token in source_text for token in tokens
    )


def slice_split_off_skip_candidate() -> dict[str, Any]:
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": SLICE_SPLIT_OFF_SKIP_RATIONALE,
        "risks": [
            (
                "A disjunctive contract that permits both Front and Back outcomes "
                "for the same range leaves the returned slice and retained slice "
                "underdetermined."
            ),
            (
                "A precise contract would need a public model for OneSidedRange, "
                "split_point_of, and the resulting Direction/split-index pair."
            ),
        ],
    }


def pattern_string_source_documents_underdetermined(
    entry: dict[str, Any],
) -> bool:
    skip = SOURCE_BACKED_PATTERN_STRING_SKIP_TARGETS.get(
        str(entry.get("target") or "")
    )
    if skip is None:
        return False
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    return all(str(token).lower() in source_text for token in skip["tokens"])


def pattern_string_skip_candidate(target: str) -> dict[str, Any]:
    skip = SOURCE_BACKED_PATTERN_STRING_SKIP_TARGETS[target]
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": str(skip["rationale"]),
        "risks": [str(risk) for risk in skip["risks"]],
    }


def select_nth_unstable_source_documents_permitted_partition_ordering(
    entry: dict[str, Any],
) -> bool:
    tokens = SELECT_NTH_UNSTABLE_PARTITION_SKIP_TARGETS.get(
        str(entry.get("target") or "")
    )
    if tokens is None:
        return False
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    return all(token in source_text for token in tokens)


def select_nth_unstable_partition_skip_candidate() -> dict[str, Any]:
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": SELECT_NTH_UNSTABLE_PARTITION_SKIP_RATIONALE,
        "risks": [
            (
                "A contract that fixes the exact before/after ordering would "
                "forbid Rust-documented permitted reorderings."
            ),
            (
                "A contract that states only partition predicates would leave "
                "the returned mutable slice contents and final slice order "
                "underdetermined."
            ),
        ],
    }


def range_inclusive_source_documents_unspecified_after_exhaustion(
    entry: dict[str, Any],
) -> bool:
    source_text = entry_source_text(entry)
    return (
        entry.get("target") in RANGE_INCLUSIVE_EXHAUSTION_TARGETS
        and "unspecified after the iteration ended" in source_text
        and "unspecified after the range" in source_text
        and "iterated to exhaustion" in source_text
    )


def range_inclusive_exhaustion_skip_candidate() -> dict[str, Any]:
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": RANGE_INCLUSIVE_EXHAUSTION_SKIP_RATIONALE,
        "risks": [
            (
                "A contract equating the accessor result to a concrete endpoint "
                "would over-specify post-exhaustion behavior Rust explicitly "
                "leaves unspecified."
            ),
            (
                "Adding a non-exhausted precondition would be a source-unjustified "
                "domain restriction for the safe public accessor."
            ),
        ],
    }


def vstd_duplicate_assume_specification_source_exists(target: str) -> bool:
    duplicate = VSTD_DUPLICATE_ASSUME_SPECIFICATION_TARGETS.get(target)
    if duplicate is None:
        return False
    source_path = (
        Path(__file__).resolve().parent
        / "verus"
        / "source"
        / "vstd"
        / duplicate["source_file"]
    )
    if not source_path.is_file():
        return False
    return str(duplicate["target_fragment"]) in source_path.read_text()


def vstd_duplicate_assume_specification_skip_candidate(target: str) -> dict[str, Any]:
    duplicate = VSTD_DUPLICATE_ASSUME_SPECIFICATION_TARGETS[target]
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": str(duplicate["rationale"]),
        "risks": [
            (
                "Duplicating an existing vstd assume_specification can make "
                "downstream Verus harnesses fail before checking any generated "
                "contract content."
            ),
            (
                "Keeping this as a skip preserves the inventory row while "
                "deferring to the already-trusted vstd contract for the target."
            ),
        ],
    }


def raw_pointer_representation_source_supports_skip(entry: dict[str, Any]) -> bool:
    skip = SOURCE_BACKED_RAW_POINTER_REPRESENTATION_SKIP_TARGETS.get(
        str(entry.get("target") or "")
    )
    if skip is None:
        return False
    source_text = re.sub(r"\s+", " ", entry_source_text(entry))
    return all(str(token) in source_text for token in skip["tokens"])


def raw_pointer_representation_skip_candidate(target: str) -> dict[str, Any]:
    skip = SOURCE_BACKED_RAW_POINTER_REPRESENTATION_SKIP_TARGETS[target]
    return {
        "decision": "skip",
        "contract_form": "assume_specification",
        "contract_code": "",
        "requires": [],
        "ensures": [],
        "feature_gates": [],
        "imports": [],
        "useful": False,
        "rationale": str(skip["rationale"]),
        "risks": [str(risk) for risk in skip["risks"]],
    }


def source_backed_skip_final(
    candidate: dict[str, Any],
    anti_vacuity_issues: list[str],
) -> dict[str, Any]:
    return {
        "round": "source_skip",
        "llm_ms": 0,
        "candidate": copy.deepcopy(candidate),
        "checker": {"status": "not_run"},
        "anti_vacuity_issues": anti_vacuity_issues,
        "raw_det_reward": 0,
        "guarded_reward": 0,
        "soundness_status": "source_backed_skip_no_contract",
        "apply_upstream": False,
    }


def source_backed_forced_skip_final(entry: dict[str, Any]) -> dict[str, Any] | None:
    target = str(entry.get("target") or "")
    if vecdeque_as_mut_slices_source_documents_hidden_split(entry):
        return source_backed_skip_final(
            vecdeque_as_mut_slices_skip_candidate(),
            [
                "classification:determinism_checker_unsupported",
                "implementation_dependent_split_point",
            ],
        )
    if str_rsplit_once_source_documents_generic_reverse_search(entry):
        return source_backed_skip_final(
            str_rsplit_once_skip_candidate(),
            [
                "classification:associated_type_or_projection",
                "generic_pattern_reverse_search_underdetermined",
            ],
        )
    if slice_split_off_source_documents_one_sided_range_direction(entry):
        return source_backed_skip_final(
            slice_split_off_skip_candidate(),
            [
                "one_sided_range_split_point_underdetermined",
                "direction_choice_not_modeled",
            ],
        )
    if residual_add_spec_source_supports_skip(entry):
        skip = SOURCE_BACKED_RESIDUAL_ADD_SPEC_SKIP_TARGETS[target]
        return source_backed_skip_final(
            residual_add_spec_skip_candidate(target),
            [str(issue) for issue in skip["issues"]],
        )
    if higher_order_closure_source_documents_underdetermined(entry):
        skip = SOURCE_BACKED_HIGHER_ORDER_CLOSURE_SKIP_TARGETS[target]
        return source_backed_skip_final(
            higher_order_closure_skip_candidate(target),
            [str(issue) for issue in skip["issues"]],
        )
    if pattern_string_source_documents_underdetermined(entry):
        skip = SOURCE_BACKED_PATTERN_STRING_SKIP_TARGETS[target]
        return source_backed_skip_final(
            pattern_string_skip_candidate(target),
            [str(issue) for issue in skip["issues"]],
        )
    if select_nth_unstable_source_documents_permitted_partition_ordering(entry):
        return source_backed_skip_final(
            select_nth_unstable_partition_skip_candidate(),
            [
                "classification:determinism_checker_unsupported",
                "permitted_partition_order_underdetermined",
            ],
        )
    if range_inclusive_source_documents_unspecified_after_exhaustion(entry):
        return source_backed_skip_final(
            range_inclusive_exhaustion_skip_candidate(),
            ["value_unspecified_after_exhaustion"],
        )
    if vstd_duplicate_assume_specification_source_exists(target):
        issues = ["duplicate_vstd_assume_specification"]
        if entry.get("classification") not in {None, "suitable_now"}:
            issues.insert(0, f"classification:{entry.get('classification')}")
        return source_backed_skip_final(
            vstd_duplicate_assume_specification_skip_candidate(target),
            issues,
        )
    if raw_pointer_representation_source_supports_skip(entry):
        skip = SOURCE_BACKED_RAW_POINTER_REPRESENTATION_SKIP_TARGETS[target]
        return source_backed_skip_final(
            raw_pointer_representation_skip_candidate(target),
            [str(issue) for issue in skip["issues"]],
        )
    return None


def common_prefix_length(left: str, right: str) -> int:
    left_parts = left.split("::")
    right_parts = right.split("::")
    count = 0
    for lhs, rhs in zip(left_parts, right_parts):
        if lhs != rhs:
            break
        count += 1
    return count


def related_vstd_context(
    target: str,
    contracts: list[dict[str, Any]],
    vstd_root: Path,
) -> str:
    scored = sorted(
        contracts,
        key=lambda row: (
            common_prefix_length(target, row["api_path"]),
            row["api_path"] == target,
        ),
        reverse=True,
    )
    blocks: list[str] = []
    seen: set[tuple[str, int]] = set()
    for row in scored:
        score = common_prefix_length(target, row["api_path"])
        if score < 2:
            break
        key = (row["source_file"], int(row["source_line"]))
        if key in seen:
            continue
        seen.add(key)
        path = vstd_root / row["source_file"]
        if not path.is_file():
            continue
        lines = path.read_text(errors="replace").splitlines()
        line = key[1]
        start = max(1, line - 10)
        end = min(len(lines), line + 18)
        block = [
            f"// {row['api_path']} — {row['source_file']}:{line}",
            *[
                f"{number:>6}: {lines[number - 1]}"
                for number in range(start, end + 1)
            ],
        ]
        blocks.append("\n".join(block))
        if len(blocks) >= 4:
            break
    return "\n\n".join(blocks) if blocks else "// No closely related vstd contract."


def target_summary(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": entry["target"],
        "category": entry["category"],
        "kinds": entry["kinds"],
        "modules": entry["modules"],
        "semantic_risks": entry["semantic_risks"],
        "classification": entry.get("classification"),
        "classification_reasons": entry.get("classification_reasons", []),
        "recommended_contract_form": entry["recommended_contract_form"],
        "available_in_verus_rust_1_96": entry["available_in_verus_rust_1_96"],
        "declaration_count": entry["declaration_count"],
        "verification_declaration_count": entry["verification_declaration_count"],
    }


def selected_declaration(entry: dict[str, Any], verification: bool) -> dict[str, Any]:
    key = "verification_declarations" if verification else "declarations"
    declarations = entry.get(key) or []
    return declarations[0] if declarations else {}


def prompt_for(
    entry: dict[str, Any],
    contracts: list[dict[str, Any]],
    vstd_root: Path,
) -> str:
    verification = selected_declaration(entry, True)
    nanvix = selected_declaration(entry, False)
    return GENERATION_PROMPT.format(
        target_summary=json.dumps(target_summary(entry), indent=2),
        verification_declaration=json.dumps(
            {
                key: value
                for key, value in verification.items()
                if key != "source_context"
            },
            indent=2,
        ),
        verification_source=verification.get("source_context", ""),
        nanvix_source=nanvix.get("source_context", ""),
        vstd_context=related_vstd_context(entry["target"], contracts, vstd_root),
    )


def feature_attributes(candidate: dict[str, Any]) -> str:
    features = []
    for feature in candidate.get("feature_gates") or []:
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", feature):
            features.append(feature)
    return "".join(f"#![feature({feature})]\n" for feature in sorted(set(features)))


def import_lines(candidate: dict[str, Any]) -> str:
    imports = []
    for path in candidate.get("imports") or []:
        path = path.removeprefix("use ").removesuffix(";").strip()
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_:*{} ,<>]*", path):
            imports.append(path)
    return "".join(f"use {path};\n" for path in sorted(set(imports)))


def build_contract_harness(candidate: dict[str, Any]) -> str:
    code = active_contract_code(candidate)
    return (
        "#![allow(unused_imports, dead_code)]\n"
        f"{feature_attributes(candidate)}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{import_lines(candidate)}\n"
        "verus! {\n"
        f"{code}\n"
        "}\n\n"
        "fn main() {}\n"
    )


def active_contract_code(candidate: dict[str, Any]) -> str:
    code = normalized_contract_code(
        candidate.get("contract_code"),
        str(candidate.get("decision", "")).strip(),
    ).strip()
    code = re.sub(
        r"(?m)^[ \t]*#\s*\[(?:cfg|cfg_attr)\b[^\n]*\][ \t]*\n?",
        "",
        code,
    )
    return code.strip()


def run_verus(
    *,
    verus_bin: Path,
    z3_path: Path,
    file_path: Path,
    timeout: int,
    rlimit: float,
    log_dir: Path | None = None,
    verify_function: str | None = None,
) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["RUSTC_BOOTSTRAP"] = "1"
    environment["VERUS_Z3_PATH"] = str(z3_path)
    rust_lib = (
        Path.home()
        / ".rustup"
        / "toolchains"
        / "1.96.0-x86_64-unknown-linux-gnu"
        / "lib"
    )
    environment["LD_LIBRARY_PATH"] = (
        str(rust_lib) + ":" + environment.get("LD_LIBRARY_PATH", "")
    )
    command = [str(verus_bin), str(file_path), "--rlimit", str(rlimit)]
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        command += ["--log-all", "--log-dir", str(log_dir)]
    if verify_function is not None:
        command += ["--verify-root", "--verify-function", verify_function]
    started = time.monotonic()
    try:
        process = subprocess.run(
            command,
            env=environment,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr,
            "duration_ms": int((time.monotonic() - started) * 1000),
            "command": command,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "returncode": -1,
            "stdout": error.stdout or "",
            "stderr": (error.stderr or "") + f"\n[timeout after {timeout}s]",
            "duration_ms": int((time.monotonic() - started) * 1000),
            "command": command,
        }


def matching_delimiter(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    for index in range(start, len(text)):
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            if closing == ">" and index > 0 and text[index - 1] == "-":
                continue
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unclosed {opening}")


def split_assume_specification(
    contract_code: str,
) -> tuple[str, str]:
    match = re.search(r"\bassume_specification\b", contract_code)
    if match is None:
        raise ValueError("contract_code has no assume_specification")
    line_start = contract_code.rfind("\n", 0, match.start()) + 1
    item_start = (
        line_start
        if re.fullmatch(
            r"\s*(?:pub(?:\s*\([^)]*\))?\s+)?",
            contract_code[line_start : match.start()],
        )
        else match.start()
    )
    cursor = match.end()
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    generics = ""
    if cursor < len(contract_code) and contract_code[cursor] == "<":
        end = matching_delimiter(contract_code, cursor, "<", ">")
        generics = contract_code[cursor : end + 1]
        cursor = end + 1
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    if cursor >= len(contract_code) or contract_code[cursor] != "[":
        raise ValueError("assume_specification target bracket not found")
    target_end = matching_delimiter(contract_code, cursor, "[", "]")
    rest_start = target_end + 1

    paren = bracket = brace = 0
    semicolon = None
    for index in range(rest_start, len(contract_code)):
        char = contract_code[index]
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
        raise ValueError("assume_specification terminator not found")
    rest = contract_code[rest_start:semicolon].strip()
    local_declarations = "\n\n".join(
        part
        for part in (
            contract_code[:item_start].strip(),
            contract_code[semicolon + 1 :].strip(),
        )
        if part
    )
    synthetic_fn = (
        f"pub exec fn __rust_std_candidate{generics}{rest}\n"
        "    { loop { } }\n"
    )
    return local_declarations, synthetic_fn


def assume_specification_target(contract_code: str) -> str:
    match = re.search(r"\bassume_specification\b", contract_code)
    if match is None:
        raise ValueError("contract_code has no assume_specification")
    cursor = match.end()
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    if cursor < len(contract_code) and contract_code[cursor] == "<":
        cursor = matching_delimiter(contract_code, cursor, "<", ">") + 1
    while cursor < len(contract_code) and contract_code[cursor].isspace():
        cursor += 1
    if cursor >= len(contract_code) or contract_code[cursor] != "[":
        raise ValueError("assume_specification target bracket not found")
    target_end = matching_delimiter(contract_code, cursor, "[", "]")
    return contract_code[cursor + 1 : target_end].strip()


def assume_to_synthetic(contract_code: str) -> str:
    local_declarations, synthetic_fn = split_assume_specification(contract_code)
    if local_declarations:
        return f"{local_declarations}\n\n{synthetic_fn}"
    return synthetic_fn


def candidate_local_declarations(candidate: dict[str, Any]) -> str:
    local_declarations, _ = split_assume_specification(active_contract_code(candidate))
    return local_declarations


def equal_fn_is_trivial(equal_fn_def: str) -> bool:
    match = re.search(
        r"->\s*bool\s*\{(?P<body>.*)\}\s*$",
        equal_fn_def,
        flags=re.DOTALL,
    )
    if not match:
        return False
    body = re.sub(r"/\*.*?\*/", "", match.group("body"), flags=re.DOTALL)
    body = re.sub(r"//.*", "", body)
    body = re.sub(r"[\s()]", "", body)
    return body == "true"


def spec_bytes_equal_expr(lhs: str, rhs: str) -> str:
    return (
        f"(({lhs}).spec_bytes().len() == ({rhs}).spec_bytes().len()"
        f" && forall|i: int| 0 <= i < ({lhs}).spec_bytes().len()"
        f" ==> #[trigger] ({lhs}).spec_bytes()[i] as int"
        f" == ({rhs}).spec_bytes()[i] as int)"
    )


def replace_str_view_equality(body: str, lhs: str, rhs: str) -> str:
    rewritten = spec_bytes_equal_expr(lhs, rhs)
    escaped_lhs = re.escape(lhs)
    escaped_rhs = re.escape(rhs)
    for pattern in (
        rf"\(\(\s*{escaped_lhs}\s*\)@\s*==\s*\(\s*{escaped_rhs}\s*\)@\)",
        rf"\(\s*{escaped_lhs}@\s*==\s*{escaped_rhs}@\s*\)",
        rf"\(?\b{escaped_lhs}\s*=~=\s*{escaped_rhs}\b\)?",
    ):
        body = re.sub(pattern, rewritten, body)
    return body


def borrow_unsized_str_parameters(body: str) -> str:
    str_params = set(
        re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*str(?=\s*[,)])", body)
    )
    tuple_str_params = set(
        re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\((?=[^)]*str\b)"
            r"[^)]*&(?:mut\s+)?str[^)]*\)",
            body,
        )
    )
    option_tuple_str_params = set(
        re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*"
            r"(?:[A-Za-z_][A-Za-z0-9_]*::)*Option\s*<\s*\("
            r"\s*&(?:mut\s+)?str\s*,"
            r"\s*&(?:mut\s+)?str\s*\)\s*>",
            body,
        )
    )
    body = re.sub(r"(:\s*)str(\s*[,)])", r"\1&str\2", body)
    for lhs in str_params:
        for rhs in str_params:
            body = replace_str_view_equality(body, lhs, rhs)
    for lhs in tuple_str_params:
        for rhs in tuple_str_params:
            for index in range(4):
                body = replace_str_view_equality(
                    body,
                    f"{lhs}.{index}",
                    f"{rhs}.{index}",
                )
    for lhs in option_tuple_str_params:
        for rhs in option_tuple_str_params:
            for index in range(4):
                body = replace_str_view_equality(
                    body,
                    f"{lhs}->Some_0.{index}",
                    f"{rhs}->Some_0.{index}",
                )
    return body


def borrow_unsized_slice_parameters(body: str) -> str:
    slice_params = set(
        re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\[[^\]]+\](?=\s*[,)])",
            body,
        )
    )
    tuple_slice_params = set(
        re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*\((?=[^)]*\[[^\]]+\])"
            r"[^)]*&(?:mut\s+)?\[[^\]]+\][^)]*\)",
            body,
        )
    )
    option_tuple_slice_params = set(
        re.findall(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:\s*"
            r"(?:[A-Za-z_][A-Za-z0-9_]*::)*Option\s*<\s*\("
            r"\s*&(?:mut\s+)?\[[^\]]+\]\s*,"
            r"\s*&(?:mut\s+)?\[[^\]]+\]\s*\)\s*>",
            body,
        )
    )
    mutable_tuple_slice_fields: set[tuple[str, int]] = set()
    for match in re.finditer(
        r"\b(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*\((?P<fields>[^)]*)\)",
        body,
    ):
        name = match.group("name")
        if name not in tuple_slice_params:
            continue
        for index, field in enumerate(match.group("fields").split(",")):
            if "[" in field and re.search(r"&\s*mut\s+\[", field):
                mutable_tuple_slice_fields.add((name, index))
    body = re.sub(r"(:\s*)\[([^\]]+)\](\s*[,)])", r"\1&[\2]\3", body)

    def replace_ext_equal(lhs: str, rhs: str, rewritten: str) -> None:
        nonlocal body
        body = re.sub(
            rf"\(?\b{re.escape(lhs)}\s*=~=\s*{re.escape(rhs)}\b\)?",
            rewritten,
            body,
        )

    for lhs in slice_params:
        for rhs in slice_params:
            replace_ext_equal(lhs, rhs, f"({lhs}@ == {rhs}@)")
    for lhs in tuple_slice_params:
        for rhs in tuple_slice_params:
            for index in range(4):
                replace_ext_equal(
                    f"{lhs}.{index}",
                    f"{rhs}.{index}",
                    f"({lhs}.{index}@ == {rhs}.{index}@)",
                )
    for lhs in option_tuple_slice_params:
        for rhs in option_tuple_slice_params:
            for index in range(4):
                replace_ext_equal(
                    f"{lhs}->Some_0.{index}",
                    f"{rhs}->Some_0.{index}",
                    f"({lhs}->Some_0.{index}@ == {rhs}->Some_0.{index}@)",
                )
    marker = "\n\nproof fn "
    prefix, separator, proof_body = body.partition(marker)
    if separator:
        for name, index in mutable_tuple_slice_fields:
            proof_body = re.sub(
                rf"(?<!old\()(?<!final\()"
                rf"\b{re.escape(name)}\.{index}@",
                f"old({name}.{index})@",
                proof_body,
            )
        body = prefix + separator + proof_body
    return body


def direct_mut_view_adapter_target_for_candidate(candidate: dict[str, Any]) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def option_mut_tuple_view_target_for_candidate(candidate: dict[str, Any]) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def mut_slice_chunk_partition_target_for_candidate(
    candidate: dict[str, Any],
) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_MUT_SLICE_CHUNK_PARTITION_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def single_element_mut_split_target_for_candidate(
    candidate: dict[str, Any],
) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def map_get_mut_target_for_candidate(candidate: dict[str, Any]) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_MAP_GET_MUT_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def linkedlist_back_mut_target_for_candidate(
    candidate: dict[str, Any],
) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_LINKEDLIST_BACK_MUT_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def array_each_mut_target_for_candidate(candidate: dict[str, Any]) -> str | None:
    try:
        target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return None
    return SOURCE_BACKED_ARRAY_EACH_MUT_CONTRACT_TARGETS.get(
        re.sub(r"\s+", " ", target).strip()
    )


def direct_mut_view_adapter_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = direct_mut_view_adapter_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = {
        "core::array::from_mut": [
            "out@[0] == *old(s)",
            "final(out)@ == out@",
            "*final(s) == final(out)@[0]",
        ],
        "core::slice::from_mut": [
            "ret@ == seq![*old(s)]",
            "final(ret)@ == ret@",
            "final(ret)@ == seq![*final(s)]",
            "*final(s) == *old(s)",
        ],
        "core::array::as_mut_slice": [
            "out@ == old(ar)@",
            "final(out)@ == out@",
            "final(out)@ == final(ar)@",
        ],
        SLICE_AS_MUT_ARRAY_TARGET: [
            "ret is Some == (old(slice)@.len() == N)",
            (
                "ret matches Some(out) ==> { "
                "&&& out@ == old(slice)@ "
                "&&& final(out)@ == out@ "
                "&&& final(slice)@ == final(out)@ }"
            ),
            "ret is None ==> final(slice)@ == old(slice)@",
        ],
        SLICE_FIRST_CHUNK_MUT_TARGET: [
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
        SLICE_LAST_CHUNK_MUT_TARGET: [
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
    }
    return (
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(ensures, expected_ensures[target])
    )


def option_mut_tuple_view_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = option_mut_tuple_view_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_TARGETS:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = {
        SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET: [
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
        SLICE_SPLIT_LAST_CHUNK_MUT_TARGET: [
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
    }
    return (
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(ensures, expected_ensures[target])
    )


def mut_slice_chunk_partition_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = mut_slice_chunk_partition_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_MUT_SLICE_CHUNK_PARTITION_TARGETS:
        return False
    def normalized_recovery_expr(expression: str) -> str:
        return normalize_expr(expression).rstrip(",")

    requires = [
        normalized_recovery_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalized_recovery_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = {
        SLICE_AS_CHUNKS_MUT_TARGET: [
            (
                "{ let chunks = choose|candidate: Seq<[T; N]>| { &&& "
                "candidate.len() == old(slice)@.len() / (N as nat) &&& "
                "forall|i: int| 0 <= i < candidate.len() ==> "
                "(#[trigger] candidate[i])@ == old(slice)@.subrange(i * (N as int), "
                "(i + 1) * (N as int)) }; &&& ret.0@ == chunks &&& "
                "ret.0@.len() == old(slice)@.len() / (N as nat) &&& "
                "ret.1@ == old(slice)@.subrange("
                "((old(slice)@.len() / (N as nat)) * (N as nat)) as int, "
                "old(slice)@.len() as int) &&& final(ret.0)@ == ret.0@ &&& "
                "final(ret.1)@ == ret.1@ &&& final(slice)@ == old(slice)@ }"
            )
        ],
        SLICE_AS_RCHUNKS_MUT_TARGET: [
            "ret.0@ == old(slice)@.subrange(0, (old(slice)@.len() % (N as nat)) as int)",
            (
                "ret.1@ == Seq::new(old(slice)@.len() / (N as nat), |i: int| "
                "choose|chunk: [T; N]| chunk@ == old(slice)@.subrange("
                "(old(slice)@.len() % (N as nat)) as int + i * (N as int), "
                "(old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int)))"
            ),
            (
                "forall|i: int| i >= 0 && ret.1@.len() > i ==> "
                "(#[trigger] ret.1@[i])@ == old(slice)@.subrange("
                "(old(slice)@.len() % (N as nat)) as int + i * (N as int), "
                "(old(slice)@.len() % (N as nat)) as int + (i + 1) * (N as int))"
            ),
            "final(ret.0)@ == ret.0@",
            "final(ret.1)@ == ret.1@",
            "final(slice)@ == old(slice)@",
        ],
    }
    if candidate.get("decision") != "add_spec" or requires != [
        normalized_recovery_expr("N != 0")
    ]:
        return False
    expected = [
        normalized_recovery_expr(expression) for expression in expected_ensures[target]
    ]
    if target == SLICE_AS_RCHUNKS_MUT_TARGET:
        required_prefixes = [
            "ret.0@==old(slice)@.subrange(0,(old(slice)@.len()%(Nasnat))asint",
            (
                "ret.1@==Seq::new(old(slice)@.len()/(Nasnat),|i:int|"
                "choose|chunk:[T;N]|chunk@==old(slice)@.subrange("
                "(old(slice)@.len()%(Nasnat))asint+i*(Nasint),"
                "(old(slice)@.len()%(Nasnat))asint+(i+1)*(Nasint)"
            ),
            (
                "forall|i:int|i>=0&&ret.1@.len()>i==>"
                "(#[trigger]ret.1@[i])@==old(slice)@.subrange("
                "(old(slice)@.len()%(Nasnat))asint+i*(Nasint),"
                "(old(slice)@.len()%(Nasnat))asint+(i+1)*(Nasint)"
            ),
            normalized_recovery_expr("final(ret.0)@ == ret.0@"),
            normalized_recovery_expr("final(ret.1)@ == ret.1@"),
            normalized_recovery_expr("final(slice)@ == old(slice)@"),
        ]
        return len(ensures) == len(expected) and all(
            any(clause.startswith(prefix) for clause in ensures)
            for prefix in required_prefixes
        )
    return ensures == expected


def single_element_mut_split_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = single_element_mut_split_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = {
        SLICE_SPLIT_FIRST_MUT_TARGET: [
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
        SLICE_SPLIT_LAST_MUT_TARGET: [
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
        SLICE_SPLIT_OFF_FIRST_MUT_TARGET: [
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
        SLICE_SPLIT_OFF_LAST_MUT_TARGET: [
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
    }
    return (
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(ensures, expected_ensures[target])
    )


def map_get_mut_candidate_matches(candidate: dict[str, Any]) -> bool:
    target = map_get_mut_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_MAP_GET_MUT_TARGETS:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures_text = "\n".join(
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    )
    expected_requires = {
        BTREEMAP_GET_MUT_TARGET: ["obeys_cmp::<Key>()"],
        HASHMAP_GET_MUT_TARGET: [
            "obeys_key_model::<Key>()",
            "builds_valid_hashers::<S>()",
        ],
    }
    required_ensure_tokens = [
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
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, expected_requires[target])
        and all(token in ensures_text for token in required_ensure_tokens)
    )


def linkedlist_back_mut_candidate_matches(candidate: dict[str, Any]) -> bool:
    if linkedlist_back_mut_target_for_candidate(candidate) != LINKEDLIST_BACK_MUT_TARGET:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = [
        "result is Some == (old(list)@.len() != 0)",
        "result is None == (old(list)@.len() == 0)",
        (
            "result matches Some(value) ==> { "
            "&&& *value == old(list)@.last() "
            "&&& *final(value) == *value "
            "&&& final(list)@ == old(list)@ }"
        ),
        "result is None ==> final(list)@ == old(list)@",
    ]
    return (
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(ensures, expected_ensures)
    )


def array_each_mut_candidate_matches(candidate: dict[str, Any]) -> bool:
    if array_each_mut_target_for_candidate(candidate) != ARRAY_EACH_MUT_TARGET:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    expected_ensures = [
        "forall|i: int| #![auto] 0 <= i < N ==> *out[i] == old(ar)@[i]",
        "forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == *out[i]",
        "forall|i: int| #![auto] 0 <= i < N ==> *final(out[i]) == final(ar)@[i]",
    ]
    return (
        candidate.get("decision") == "add_spec"
        and exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(ensures, expected_ensures)
    )


def enable_direct_mut_return_view(spec: Any) -> None:
    if not str(spec.return_type.name or "").strip().startswith("&mut "):
        return
    view = copy.deepcopy(spec.return_type)
    view.name = re.sub(r"^&\s*mut\s*", "", view.name).strip()
    view.spec_view = None
    spec.return_type.spec_view = view


def normalize_direct_mut_return_adapter_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    target = direct_mut_view_adapter_target_for_candidate(candidate)
    if target in SOURCE_BACKED_OPTION_MUT_ARRAY_VIEW_TARGETS:
        return body
    if not direct_mut_view_adapter_candidate_matches(candidate):
        return body
    if not det_spec.equal_fn_name:
        return body
    body = re.sub(
        r"\(\((r[12])\)@\s*=~=\s*\((r[12])\)@\)",
        r"((\1)@ == (\2)@)",
        body,
    )
    body = re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            "(old(r1), old(r2),"
        ),
        body,
    )
    prefix, separator, proof_body = body.partition("\n\nproof fn ")
    if not separator:
        return body
    proof_header, body_separator, proof_block = proof_body.rpartition("\n{")
    if not body_separator:
        return body
    for name in ("r1", "r2"):
        proof_header = re.sub(
            rf"(?<!old\()(?<!final\()"
            rf"\b{re.escape(name)}@",
            f"old({name})@",
            proof_header,
        )
    return prefix + separator + proof_header + body_separator + proof_block


def normalize_option_mut_array_view_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    target = direct_mut_view_adapter_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_OPTION_MUT_ARRAY_VIEW_TARGETS:
        return body
    body = re.sub(
        r"\(?\b(r[12])->Some_0\s*=~=\s*(r[12])->Some_0\b\)?",
        r"(\1->Some_0@ == \2->Some_0@)",
        body,
    )
    if not det_spec.equal_fn_name:
        return body
    old_r1 = "(if r1 is Some { Some(old(r1->Some_0)) } else { None })"
    old_r2 = "(if r2 is Some { Some(old(r2->Some_0)) } else { None })"
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_option_mut_tuple_view_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    if not option_mut_tuple_view_candidate_matches(candidate):
        return body
    for index in range(2):
        body = re.sub(
            rf"\(?\b(r[12])->Some_0\.{index}\s*=~=\s*(r[12])->Some_0\.{index}\b\)?",
            rf"(\1->Some_0.{index}@ == \2->Some_0.{index}@)",
            body,
        )
    if not det_spec.equal_fn_name:
        return body
    old_r1 = (
        "(if r1 is Some { "
        "Some((old(r1->Some_0.0), old(r1->Some_0.1))) "
        "} else { None })"
    )
    old_r2 = (
        "(if r2 is Some { "
        "Some((old(r2->Some_0.0), old(r2->Some_0.1))) "
        "} else { None })"
    )
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_mut_slice_chunk_partition_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    if not mut_slice_chunk_partition_candidate_matches(candidate):
        return body
    if not det_spec.equal_fn_name:
        return body
    old_r1 = "(old(r1.0), old(r1.1))"
    old_r2 = "(old(r2.0), old(r2.1))"
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_single_element_mut_split_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    target = single_element_mut_split_target_for_candidate(candidate)
    if target not in SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS:
        return body
    if not single_element_mut_split_candidate_matches(candidate):
        return body
    if target in {SLICE_SPLIT_FIRST_MUT_TARGET, SLICE_SPLIT_LAST_MUT_TARGET}:
        body = re.sub(
            r"\(?\b(r[12])->Some_0\.0\s*==\s*(r[12])->Some_0\.0\b\)?",
            r"(*(\1->Some_0.0) == *(\2->Some_0.0))",
            body,
        )
        body = re.sub(
            r"\(?\b(r[12])->Some_0\.1\s*=~=\s*(r[12])->Some_0\.1\b\)?",
            r"(\1->Some_0.1@ == \2->Some_0.1@)",
            body,
        )
        if not det_spec.equal_fn_name:
            return body
        old_r1 = (
            "(if r1 is Some { "
            "Some((old(r1->Some_0.0), old(r1->Some_0.1))) "
            "} else { None })"
        )
        old_r2 = (
            "(if r2 is Some { "
            "Some((old(r2->Some_0.0), old(r2->Some_0.1))) "
            "} else { None })"
        )
    else:
        body = re.sub(
            r"\(?\b(r[12])->Some_0\s*==\s*(r[12])->Some_0\b\)?",
            r"(*(\1->Some_0) == *(\2->Some_0))",
            body,
        )
        if not det_spec.equal_fn_name:
            return body
        old_r1 = "(if r1 is Some { Some(old(r1->Some_0)) } else { None })"
        old_r2 = "(if r2 is Some { Some(old(r2->Some_0)) } else { None })"
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_map_get_mut_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    if not map_get_mut_candidate_matches(candidate):
        return body
    body = re.sub(
        r"\(?\b(r[12])->Some_0\s*==\s*(r[12])->Some_0\b\)?",
        r"(*(\1->Some_0) == *(\2->Some_0))",
        body,
    )
    if not det_spec.equal_fn_name:
        return body
    old_r1 = "(if r1 is Some { Some(old(r1->Some_0)) } else { None })"
    old_r2 = "(if r2 is Some { Some(old(r2->Some_0)) } else { None })"
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_linkedlist_back_mut_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    if not linkedlist_back_mut_candidate_matches(candidate):
        return body
    body = re.sub(
        r"\(?\b(r[12])->Some_0\s*==\s*(r[12])->Some_0\b\)?",
        r"(*(\1->Some_0) == *(\2->Some_0))",
        body,
    )
    if not det_spec.equal_fn_name:
        return body
    old_r1 = "(if r1 is Some { Some(old(r1->Some_0)) } else { None })"
    old_r2 = "(if r2 is Some { Some(old(r2->Some_0)) } else { None })"
    return re.sub(
        rf"\b{re.escape(det_spec.equal_fn_name)}(?P<gen>::<[^>]+>)?\(r1, r2,",
        lambda match: (
            f"{det_spec.equal_fn_name}{match.group('gen') or ''}"
            f"({old_r1}, {old_r2},"
        ),
        body,
    )


def normalize_array_each_mut_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    body: str,
) -> str:
    if not array_each_mut_candidate_matches(candidate):
        return body
    if not det_spec.equal_fn_name:
        return body
    equal_name = re.escape(det_spec.equal_fn_name)
    body = re.sub(
        rf"spec fn {equal_name}<T, const N: usize>"
        r"\(r1: &\[&mut T; N\], r2: &\[&mut T; N\], "
        r"post1_ar: &\[T; N\], post2_ar: &\[T; N\]\) -> bool \{\n.*?\n\}",
        (
            f"spec fn {det_spec.equal_fn_name}<T, const N: usize>"
            "(r1: &[&mut T; N], r2: &[&mut T; N], "
            "post1_ar: &[T; N], post2_ar: &[T; N]) -> bool {\n"
            "    (forall|i: int| #![auto] 0 <= i < N ==> *r1[i] == *r2[i])\n"
            "    && (forall|i: int| #![auto] 0 <= i < N ==> post1_ar@[i] == post2_ar@[i])\n"
            "}"
        ),
        body,
        flags=re.S,
    )
    antecedent = (
        "({\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *r1[i] == pre_ar@[i])\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *final(r1[i]) == *r1[i])\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *final(r1[i]) == post1_ar@[i])\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *r2[i] == pre_ar@[i])\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *final(r2[i]) == *r2[i])\n"
        "            &&& (forall|i: int| #![auto] 0 <= i < N ==> *final(r2[i]) == post2_ar@[i])\n"
        "        })"
    )
    proof = (
        f"    if {antecedent} {{\n"
        "        assert forall|i: int| #![auto] 0 <= i < N ==> *r1[i] == *r2[i] by {\n"
        "            if 0 <= i < N {\n"
        "                assert(*r1[i] == pre_ar@[i]);\n"
        "                assert(*r2[i] == pre_ar@[i]);\n"
        "            }\n"
        "        }\n"
        "        assert forall|i: int| #![auto] 0 <= i < N ==> post1_ar@[i] == post2_ar@[i] by {\n"
        "            if 0 <= i < N {\n"
        "                assert(*final(r1[i]) == *r1[i]);\n"
        "                assert(*r1[i] == pre_ar@[i]);\n"
        "                assert(*final(r1[i]) == post1_ar@[i]);\n"
        "                assert(*final(r2[i]) == *r2[i]);\n"
        "                assert(*r2[i] == pre_ar@[i]);\n"
        "                assert(*final(r2[i]) == post2_ar@[i]);\n"
        "            }\n"
        "        }\n"
        f"        assert({det_spec.equal_fn_name}::<T, N>(r1, r2, post1_ar, post2_ar));\n"
        "    }\n"
    )
    return re.sub(
        rf"(?m)^    if g_neq_tuple \{{ assume\(!{equal_name}::<T, N>\(r1, r2, post1_ar, post2_ar\)\); \}}\n",
        lambda match: proof + match.group(0),
        body,
        count=1,
    )


def build_det_harness(
    candidate: dict[str, Any],
    det_spec: Any,
    schemas: list[Any],
) -> str:
    local_declarations = candidate_local_declarations(candidate)
    local_block = f"{local_declarations}\n\n" if local_declarations else ""
    body = det_spec.equal_fn_def + "\n\n" + render_guarded_template(
        det_spec,
        schemas,
    )
    body = borrow_unsized_str_parameters(body)
    body = borrow_unsized_slice_parameters(body)
    body = normalize_direct_mut_return_adapter_harness(candidate, det_spec, body)
    body = normalize_option_mut_array_view_harness(candidate, det_spec, body)
    body = normalize_option_mut_tuple_view_harness(candidate, det_spec, body)
    body = normalize_mut_slice_chunk_partition_harness(candidate, det_spec, body)
    body = normalize_single_element_mut_split_harness(candidate, det_spec, body)
    body = normalize_map_get_mut_harness(candidate, det_spec, body)
    body = normalize_linkedlist_back_mut_harness(candidate, det_spec, body)
    body = normalize_array_each_mut_harness(candidate, det_spec, body)
    for spec_name in det_spec.opened_closed_specs:
        body = re.sub(
            rf"^[ \t]*reveal\((?:[A-Za-z_][A-Za-z0-9_]*::)*"
            rf"{re.escape(spec_name)}\);[ \t]*\n?",
            "",
            body,
            flags=re.MULTILINE,
        )
    return (
        "#![allow(unused_imports, dead_code)]\n"
        f"{feature_attributes(candidate)}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{import_lines(candidate)}\n"
        "verus! {\n"
        f"{local_block}"
        f"{body}\n"
        "}\n\n"
        "fn main() {}\n"
    )


def build_determinism_artifacts(
    candidate: dict[str, Any],
    view_registry: ViewRegistry,
) -> dict[str, Any]:
    synthetic_fn = assume_to_synthetic(active_contract_code(candidate))
    synthetic_source = (
        "#![allow(unused_imports)]\n"
        f"{feature_attributes(candidate)}"
        "extern crate alloc;\n"
        "use vstd::prelude::*;\n"
        f"{import_lines(candidate)}\n"
        "verus! {\n"
        f"{synthetic_fn}"
        "}\n"
    )
    spec = extract_spec(
        synthetic_source,
        "__rust_std_candidate",
        type_sources=[synthetic_source],
    )
    prepared: dict[str, Any] = {
        "status": "ready",
        "synthetic_source": synthetic_source,
        "spec": spec,
    }
    if not spec.ensures:
        prepared["status"] = "no_ensures"
        return prepared
    if spec.return_type.name.strip().startswith("&mut "):
        if not direct_mut_view_adapter_candidate_matches(candidate):
            prepared["status"] = "unsupported_mut_ref_return"
            return prepared
        enable_direct_mut_return_view(spec)

    det_spec = build_det_check_spec(
        spec,
        source=synthetic_source,
        equal_policy=EqualPolicy(
            compare_raw_pointers=False,
            source="rust_std_specgen",
        ),
        view_registry=view_registry,
    )
    schemas = enumerate_schemas(det_spec)
    prepared.update(
        {
            "det_spec": det_spec,
            "schemas": schemas,
            "harness": build_det_harness(candidate, det_spec, schemas),
        }
    )
    return prepared


def run_determinism(
    *,
    candidate: dict[str, Any],
    round_dir: Path,
    view_registry: ViewRegistry,
    verus_bin: Path,
    z3_path: Path,
    timeout: int,
    rlimit: float,
) -> dict[str, Any]:
    result: dict[str, Any] = {"status": "runner_crash"}
    try:
        prepared = build_determinism_artifacts(candidate, view_registry)
        synthetic_source = prepared["synthetic_source"]
        (round_dir / "synthetic_spec.rs").write_text(synthetic_source)
        spec = prepared["spec"]
        result["requires"] = list(spec.requires)
        result["ensures"] = list(spec.ensures)
        if prepared["status"] != "ready":
            result["status"] = prepared["status"]
            return result
        det_spec = prepared["det_spec"]
        schemas = prepared["schemas"]
        harness = prepared["harness"]
        harness_path = round_dir / "det_harness.rs"
        harness_path.write_text(harness)
        (round_dir / "det_spec.json").write_text(det_spec.to_json())
        result["det_function"] = det_spec.check_fn_name
        result["equal_fn_trivial"] = equal_fn_is_trivial(det_spec.equal_fn_def)
        result["n_schemas"] = len(schemas)

        log_dir = round_dir / "verus_log"
        raw = run_verus(
            verus_bin=verus_bin,
            z3_path=z3_path,
            file_path=harness_path,
            timeout=timeout,
            rlimit=rlimit,
            log_dir=log_dir,
            verify_function=det_spec.check_fn_name,
        )
        result["verus_returncode"] = raw["returncode"]
        result["verus_ms"] = raw["duration_ms"]
        (round_dir / "det_stdout.txt").write_text(raw["stdout"])
        (round_dir / "det_stderr.txt").write_text(raw["stderr"])
        if raw["returncode"] != 0:
            stderr = raw["stderr"]
            expected = (
                "postcondition not satisfied" in stderr
                or "assertion failed" in stderr.lower()
            )
            if not expected and "error:" in stderr:
                result["status"] = "verus_error"
                result["stderr_tail"] = stderr[-4000:]
                return result

        smt2_candidates = sorted(
            log_dir.rglob("*.smt2"),
            key=lambda path: path.stat().st_size,
        )
        if not smt2_candidates:
            result["status"] = "no_smt2"
            return result
        smt2 = smt2_candidates[-1]
        schema_ctx = build_schema_ctx(
            smt2,
            det_spec.check_fn_name,
            schemas,
            safe_name(det_spec.check_fn_name),
        )
        witness = run_schema_search(det_spec, schema_ctx)
        result["r0_z3"] = witness.r0_z3
        result["n_rounds"] = len(witness.trace or [])
        result["assumes"] = [
            assume.expression for assume in (witness.assumes or [])
        ]
        result["status"] = "ok"
        result["permitted"] = False
        raw_classification = classify_ok(result)
        result["classification"] = (
            "invalid_equal_fn_trivial"
            if result["equal_fn_trivial"]
            else raw_classification
        )
        return result
    except Exception as error:
        result["error"] = (
            f"{type(error).__name__}: {error}\n"
            f"{traceback.format_exc()[-4000:]}"
        )
        return result


def normalize_expr(expression: str) -> str:
    normalized = re.sub(r"\s+", "", expression).strip("()")
    normalized = normalized.replace("&&&", "&&")
    normalized = re.sub(r"(?<=\{)&&", "", normalized)
    return re.sub(r",(?=\))", "", normalized)


def normalize_path(path: str) -> str:
    return re.sub(r"\s+", "", path)


def source_context_for_entry(entry: dict[str, Any]) -> str:
    declarations = []
    declarations.extend(entry.get("verification_declarations") or [])
    declarations.extend(entry.get("declarations") or [])
    source = "\n".join(str(item.get("source_context") or "") for item in declarations)
    source = re.sub(r"(?m)^\s*\d+:\s?", "", source)
    source = re.sub(r"(?m)^\s*///\s?", "", source)
    return source


def exact_normalized_exprs(actual: list[str], expected: list[str]) -> bool:
    return actual == [normalize_expr(expression) for expression in expected]


def declaration_is_core_result_flatten(declaration: dict[str, Any]) -> bool:
    owner = declaration.get("owner") or {}
    owner_path = (owner.get("resolved_owner_path") or [])
    span = declaration.get("span") or {}
    return (
        declaration.get("name") == "flatten"
        and owner_path == ["core", "result", "Result"]
        and span.get("filename") == "core/src/result.rs"
    )


def source_backed_thread_result_flatten_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != THREAD_RESULT_FLATTEN_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    try:
        contract_target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return False
    if normalize_path(contract_target) != THREAD_RESULT_FLATTEN_CONTRACT_TARGET:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    exact_result_match = (
        "result==matchvalue{core::result::Result::Ok(inner)=>inner,"
        "core::result::Result::Err(e)=>core::result::Result::Err(e)}"
    )
    exact_result_match_trailing_comma = (
        "result==matchvalue{core::result::Result::Ok(inner)=>inner,"
        "core::result::Result::Err(e)=>core::result::Result::Err(e),}"
    )
    exact_result_match_error_name = (
        "result==matchvalue{core::result::Result::Ok(inner)=>inner,"
        "core::result::Result::Err(error)=>core::result::Result::Err(error)}"
    )
    exact_result_match_error_name_trailing_comma = (
        "result==matchvalue{core::result::Result::Ok(inner)=>inner,"
        "core::result::Result::Err(error)=>core::result::Result::Err(error),}"
    )
    exact_branch_match = (
        "matchvalue{core::result::Result::Ok(inner)=>result==inner,"
        "core::result::Result::Err(e)=>result==core::result::Result::Err(e)}"
    )
    exact_branch_match_trailing_comma = (
        "matchvalue{core::result::Result::Ok(inner)=>result==inner,"
        "core::result::Result::Err(e)=>result==core::result::Result::Err(e),}"
    )
    if requires or ensures not in (
        [exact_result_match],
        [exact_result_match_trailing_comma],
        [exact_result_match_error_name],
        [exact_result_match_error_name_trailing_comma],
        [exact_branch_match],
        [exact_branch_match_trailing_comma],
    ):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    declarations = [
        *(entry.get("verification_declarations") or []),
        *(entry.get("declarations") or []),
    ]
    return (
        any(declaration_is_core_result_flatten(declaration) for declaration in declarations)
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


def source_backed_split_at_mut_unchecked_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != SOURCE_BACKED_SLICE_SPLIT_AT_MUT_UNCHECKED_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return (
        exact_normalized_exprs(
            requires,
            ["mid as int <= old(slice)@.len()"],
        )
        and exact_normalized_exprs(
            ensures,
            [
                "ret.0@ == old(slice)@.subrange(0, mid as int)",
                "ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)",
                "final(ret.0)@ == ret.0@",
                "final(ret.1)@ == ret.1@",
                "final(slice)@ == final(ret.0)@ + final(ret.1)@",
            ],
        )
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


def source_backed_split_at_mut_checked_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != SOURCE_BACKED_SLICE_SPLIT_AT_MUT_CHECKED_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return (
        exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(
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


def source_backed_str_split_at_mut_checked_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != SOURCE_BACKED_STR_SPLIT_AT_MUT_CHECKED_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return (
        exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(
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


def source_backed_str_from_utf8_mut_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != SOURCE_BACKED_STR_FROM_UTF8_MUT_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    try:
        contract_target = assume_specification_target(active_contract_code(candidate))
    except Exception:
        return False
    if normalize_path(contract_target) != SOURCE_BACKED_STR_FROM_UTF8_MUT_TARGET:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return (
        exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(
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


def source_backed_str_from_utf8_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != SOURCE_BACKED_STR_FROM_UTF8_TARGET:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    contract_code = active_contract_code(candidate)
    if len(re.findall(r"\bassume_specification\b", contract_code)) != 1:
        return False
    try:
        contract_target = assume_specification_target(contract_code)
    except Exception:
        return False
    if normalize_path(contract_target) != SOURCE_BACKED_STR_FROM_UTF8_CONTRACT_TARGET:
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return (
        exact_normalized_exprs(requires, [])
        and exact_normalized_exprs(
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


def source_backed_direct_mut_view_adapter_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_DIRECT_MUT_VIEW_ADAPTER_TARGETS:
        return False
    if direct_mut_view_adapter_target_for_candidate(candidate) != target:
        return False
    if not direct_mut_view_adapter_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    evidence_tokens = {
        "core::array::from_mut": (
            "converts a mutable reference to `t` into a mutable reference to an array of length 1",
            "without copying",
            "pub const fn from_mut",
            "(s as *mut t).cast::<[t; 1]>()",
        ),
        "core::slice::from_mut": (
            "converts a reference to t into a slice of length 1",
            "without copying",
            "pub const fn from_mut",
            "array::from_mut(s)",
        ),
        "core::array::as_mut_slice": (
            "returns a mutable slice containing the entire array",
            "equivalent to `&mut s[..]`",
            "pub const fn as_mut_slice",
            "self",
        ),
        SLICE_AS_MUT_ARRAY_TARGET: (
            "gets a mutable reference to the slice's underlying array",
            "if `n` is not exactly equal to the length of `self`, then this method returns `none`",
            "pub const fn as_mut_array",
            "if self.len() == n",
            "self.as_mut_ptr().cast_array()",
            "let me = unsafe { &mut *ptr }",
            "some(me)",
        ),
        SLICE_FIRST_CHUNK_MUT_TARGET: (
            "returns a mutable array reference to the first `n` items in the slice",
            "if the slice is not at least `n` in length, this will return `none`",
            "pub const fn first_chunk_mut",
            "if self.len() < n",
            "some(unsafe { &mut *(self.as_mut_ptr().cast_array()) })",
        ),
        SLICE_LAST_CHUNK_MUT_TARGET: (
            "returns a mutable array reference to the last `n` items in the slice",
            "if the slice is not at least `n` in length, this will return `none`",
            "pub const fn last_chunk_mut",
            "checked_sub(n)",
            "let (_, last) = self.split_at_mut(index)",
            "some(unsafe { &mut *(last.as_mut_ptr().cast_array()) })",
        ),
    }
    return all(token in source_lower for token in evidence_tokens[target])


def source_backed_option_mut_tuple_view_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_OPTION_MUT_TUPLE_VIEW_TARGETS:
        return False
    if option_mut_tuple_view_target_for_candidate(candidate) != target:
        return False
    if not option_mut_tuple_view_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    evidence_tokens = {
        SLICE_SPLIT_FIRST_CHUNK_MUT_TARGET: (
            "returns a mutable array reference to the first `n` items in the slice and the remaining slice",
            "if the slice is not at least `n` in length, this will return `none`",
            "pub const fn split_first_chunk_mut",
            "let some((first, tail)) = self.split_at_mut_checked(n) else { return none }",
            "first.as_mut_ptr().cast_array()",
            "some((unsafe { &mut *(first.as_mut_ptr().cast_array()) }, tail))",
        ),
        SLICE_SPLIT_LAST_CHUNK_MUT_TARGET: (
            "returns a mutable array reference to the last `n` items in the slice and the remaining slice",
            "if the slice is not at least `n` in length, this will return `none`",
            "pub const fn split_last_chunk_mut",
            "let some(index) = self.len().checked_sub(n) else { return none }",
            "let (init, last) = self.split_at_mut(index)",
            "some((init, unsafe { &mut *(last.as_mut_ptr().cast_array()) }))",
        ),
    }
    return all(token in source_lower for token in evidence_tokens[target])


def source_backed_mut_slice_chunk_partition_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_MUT_SLICE_CHUNK_PARTITION_TARGETS:
        return False
    if mut_slice_chunk_partition_target_for_candidate(candidate) != target:
        return False
    if not mut_slice_chunk_partition_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    evidence_tokens = {
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
    return all(token in source_lower for token in evidence_tokens[target])


def source_backed_single_element_mut_split_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_SINGLE_ELEMENT_MUT_SPLIT_TARGETS:
        return False
    if single_element_mut_split_target_for_candidate(candidate) != target:
        return False
    if not single_element_mut_split_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    evidence_tokens = {
        SLICE_SPLIT_FIRST_MUT_TARGET: (
            "pub const fn split_first_mut",
            "if let [first, tail @ ..] = self",
            "some((first, tail))",
        ),
        SLICE_SPLIT_LAST_MUT_TARGET: (
            "pub const fn split_last_mut",
            "if let [init @ .., last] = self",
            "some((last, init))",
        ),
        SLICE_SPLIT_OFF_FIRST_MUT_TARGET: (
            "pub const fn split_off_first_mut",
            "mem::replace(self, &mut []).split_first_mut()",
            "let some((first, rem))",
            "*self = rem",
            "some(first)",
        ),
        SLICE_SPLIT_OFF_LAST_MUT_TARGET: (
            "pub const fn split_off_last_mut",
            "mem::replace(self, &mut []).split_last_mut()",
            "let some((last, rem))",
            "*self = rem",
            "some(last)",
        ),
    }
    return all(token in source_lower for token in evidence_tokens[target])


def source_backed_map_get_mut_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_MAP_GET_MUT_TARGETS:
        return False
    if map_get_mut_target_for_candidate(candidate) != target:
        return False
    if not map_get_mut_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    evidence_tokens = {
        HASHMAP_GET_MUT_TARGET: (
            "returns a mutable reference to the value corresponding to the key",
            "the key may be any borrowed form of the map's key type",
            "hash",
            "eq",
            "self.base.get_mut(k)",
        ),
        BTREEMAP_GET_MUT_TARGET: (
            "returns a mutable reference to the value corresponding to the key",
            "*must* match the ordering on the key type",
            "search_tree(key)",
            "found(handle) => some(handle.into_val_mut())",
            "godown(_) => none",
        ),
    }
    return all(token in source_lower for token in evidence_tokens[target])


def source_backed_linkedlist_back_mut_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != LINKEDLIST_BACK_MUT_TARGET:
        return False
    if linkedlist_back_mut_target_for_candidate(candidate) != LINKEDLIST_BACK_MUT_TARGET:
        return False
    if not linkedlist_back_mut_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
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


def source_backed_array_each_mut_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    if str(entry.get("target") or "") != ARRAY_EACH_MUT_TARGET:
        return False
    if array_each_mut_target_for_candidate(candidate) != ARRAY_EACH_MUT_TARGET:
        return False
    if not array_each_mut_candidate_matches(candidate):
        return False
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    return all(
        token in source_lower
        for token in (
            "borrows each element mutably and returns an array of mutable references",
            "pub const fn each_mut(&mut self) -> [&mut t; n]",
            "buf[i] = &raw mut self[i]",
            "`*mut t` has the same layout as `&mut t`",
            "transmute_unchecked(buf)",
        )
    )


def source_backed_unsafe_constructor_matches(
    entry: dict[str, Any],
    candidate: dict[str, Any],
) -> bool:
    target = str(entry.get("target") or "")
    if target not in SOURCE_BACKED_UNSAFE_CONSTRUCTOR_TARGETS:
        return False
    if candidate.get("decision") != "add_spec":
        return False
    requires = [
        normalize_expr(expression)
        for expression in candidate.get("requires") or []
        if str(expression).strip()
    ]
    ensures = [
        normalize_expr(expression)
        for expression in candidate.get("ensures") or []
        if str(expression).strip()
    ]
    source_lower = re.sub(r"\s+", " ", source_context_for_entry(entry)).lower()
    if target == "alloc::ffi::CString::from_vec_with_nul_unchecked":
        return (
            exact_normalized_exprs(requires, ["c_string_bytes_with_nul_valid(bytes@)"])
            and exact_normalized_exprs(ensures, ["result@ == bytes@.drop_last()"])
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
    if target == "alloc::string::String::from_utf8_unchecked":
        return (
            exact_normalized_exprs(
                requires,
                [
                    "exists|chars: vstd::prelude::Seq<char>| "
                    "vstd::utf8::encode_utf8(chars) == bytes@"
                ],
            )
            and exact_normalized_exprs(
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


def anti_vacuity_issues(
    entry: dict[str, Any],
    candidate: dict[str, Any],
    typecheck: dict[str, Any] | None,
    checker: dict[str, Any] | None,
) -> list[str]:
    issues: list[str] = []
    if entry.get("classification") not in {
        None,
        "suitable_now",
    } and not (
        source_backed_unsafe_constructor_matches(entry, candidate)
        or source_backed_split_at_mut_unchecked_matches(entry, candidate)
        or source_backed_split_at_mut_checked_matches(entry, candidate)
        or source_backed_str_split_at_mut_checked_matches(entry, candidate)
        or source_backed_str_from_utf8_matches(entry, candidate)
        or source_backed_str_from_utf8_mut_matches(entry, candidate)
        or source_backed_direct_mut_view_adapter_matches(entry, candidate)
        or source_backed_option_mut_tuple_view_matches(entry, candidate)
        or source_backed_mut_slice_chunk_partition_matches(entry, candidate)
        or source_backed_single_element_mut_split_matches(entry, candidate)
        or source_backed_map_get_mut_matches(entry, candidate)
        or source_backed_linkedlist_back_mut_matches(entry, candidate)
        or source_backed_array_each_mut_matches(entry, candidate)
        or source_backed_thread_result_flatten_matches(entry, candidate)
    ):
        issues.append(f"classification:{entry.get('classification')}")
    ensures = [
        expression
        for expression in candidate.get("ensures") or []
        if expression.strip()
    ]
    requires = [
        expression
        for expression in candidate.get("requires") or []
        if expression.strip()
    ]
    normalized_ensures = {normalize_expr(expression) for expression in ensures}
    normalized_requires = {normalize_expr(expression) for expression in requires}
    if candidate.get("decision") == "add_spec":
        if not candidate.get("contract_code"):
            issues.append("missing_contract_code")
        if not ensures:
            issues.append("no_candidate_postcondition")
        if normalized_ensures & {"true", "false"}:
            issues.append("constant_postcondition")
        if "false" in normalized_requires:
            issues.append("false_precondition")
        if normalized_ensures and normalized_ensures <= normalized_requires:
            issues.append("postcondition_implied_by_requires")
    if not entry.get("available_in_verus_rust_1_96"):
        issues.append("not_in_verus_rust_1_96")
    if not any(
        declaration["observability"]["has_modeled_output"]
        for declaration in entry.get("verification_declarations") or []
    ):
        issues.append("no_modeled_observable_output")
    if typecheck is not None and typecheck.get("returncode") != 0:
        issues.append("contract_typecheck_failed")
    if candidate.get("contract_form") != "assume_specification":
        issues.append("determinism_unsupported_contract_form")
    if checker is not None:
        checker_requires = {
            normalize_expr(expression)
            for expression in checker.get("requires", [])
        }
        checker_ensures = {
            normalize_expr(expression)
            for expression in checker.get("ensures", [])
        }
        if (
            checker_requires != normalized_requires
            or checker_ensures != normalized_ensures
        ):
            issues.append("structured_contract_mismatch")
        if checker.get("status") != "ok":
            issues.append(f"checker_status:{checker.get('status')}")
        elif checker.get("r0_z3") != "unsat":
            issues.append(f"determinism_not_proved:{checker.get('r0_z3')}")
        if checker.get("equal_fn_trivial"):
            issues.append("trivial_equal_fn")
    return sorted(set(issues))


def checker_summary(
    typecheck: dict[str, Any] | None,
    checker: dict[str, Any] | None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if typecheck is not None:
        summary["typecheck"] = {
            "returncode": typecheck.get("returncode"),
            "duration_ms": typecheck.get("duration_ms"),
            "stderr_tail": (typecheck.get("stderr") or "")[-4000:],
        }
    if checker is not None:
        keys = (
            "status",
            "r0_z3",
            "classification",
            "requires",
            "ensures",
            "equal_fn_trivial",
            "stderr_tail",
            "error",
        )
        summary["determinism"] = {
            key: checker[key]
            for key in keys
            if key in checker
        }
    return summary or {"status": "not_run"}


def run_one(
    *,
    entry: dict[str, Any],
    contracts: list[dict[str, Any]],
    vstd_root: Path,
    out_root: Path,
    view_registry: ViewRegistry,
    verus_bin: Path,
    z3_path: Path,
    model: str,
    copilot_bin: str,
    llm_timeout: int,
    llm_retries: int,
    check_timeout: int,
    rlimit: float,
    feedback_rounds: int,
    seed_candidate: dict[str, Any] | None,
    include_non_suitable: bool,
    include_unavailable: bool,
) -> dict[str, Any]:
    target_dir = out_root / "targets" / safe_name(entry["target"])
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "target.json").write_text(
        json.dumps(entry, indent=2, sort_keys=True) + "\n"
    )

    forced_skip_final = source_backed_forced_skip_final(entry)
    if forced_skip_final is not None:
        result = {
            "target": entry["target"],
            "category": entry["category"],
            "history": [copy.deepcopy(forced_skip_final)],
            "final": forced_skip_final,
        }
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result

    if (
        not entry.get("available_in_verus_rust_1_96")
        and not include_unavailable
    ):
        result = {
            "target": entry["target"],
            "category": entry["category"],
            "history": [],
            "final": {
                "status": "static_skip",
                "decision": "skip",
                "issues": ["not_in_verus_rust_1_96"],
            },
        }
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result
    if (
        entry.get("classification") not in {None, "suitable_now"}
        and not include_non_suitable
    ):
        result = {
            "target": entry["target"],
            "category": entry["category"],
            "history": [],
            "final": {
                "status": "static_skip",
                "decision": "skip",
                "issues": [f"classification:{entry.get('classification')}"],
            },
        }
        (target_dir / "summary.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result

    prompt = prompt_for(entry, contracts, vstd_root)
    history = []
    verification = selected_declaration(entry, True)
    for round_index in range(feedback_rounds + 1):
        round_dir = target_dir / f"round_{round_index:02d}"
        round_dir.mkdir(exist_ok=True)
        (round_dir / "prompt.md").write_text(prompt)
        if round_index == 0 and seed_candidate is not None:
            llm_ms = 0
            candidate = sanitize_candidate(seed_candidate)
            (round_dir / "candidate.json").write_text(
                json.dumps(candidate, indent=2) + "\n"
            )
            (round_dir / "response.txt").write_text(
                "[seeded from batch first-pass generation]\n"
            )
        else:
            started = time.monotonic()
            try:
                response = call_copilot(
                    prompt=prompt,
                    model=model,
                    copilot_bin=copilot_bin,
                    timeout=llm_timeout,
                    cwd=round_dir,
                    retries=llm_retries,
                )
                llm_ms = int((time.monotonic() - started) * 1000)
                (round_dir / "response.txt").write_text(response)
                candidate = sanitize_candidate(parse_json_response(response))
                (round_dir / "candidate.json").write_text(
                    json.dumps(candidate, indent=2) + "\n"
                )
            except Exception as error:
                record = {
                    "round": round_index,
                    "status": "llm_error",
                    "error": f"{type(error).__name__}: {error}",
                }
                history.append(record)
                break

        typecheck = None
        checker = None
        if (
            candidate.get("decision") == "add_spec"
            and candidate.get("contract_code")
            and entry.get("available_in_verus_rust_1_96")
        ):
            contract_harness = build_contract_harness(candidate)
            contract_path = round_dir / "contract_harness.rs"
            contract_path.write_text(contract_harness)
            typecheck = run_verus(
                verus_bin=verus_bin,
                z3_path=z3_path,
                file_path=contract_path,
                timeout=check_timeout,
                rlimit=rlimit,
            )
            (round_dir / "typecheck_stdout.txt").write_text(typecheck["stdout"])
            (round_dir / "typecheck_stderr.txt").write_text(typecheck["stderr"])
            if (
                typecheck["returncode"] == 0
                and candidate.get("contract_form") == "assume_specification"
            ):
                checker = run_determinism(
                    candidate=candidate,
                    round_dir=round_dir,
                    view_registry=view_registry,
                    verus_bin=verus_bin,
                    z3_path=z3_path,
                    timeout=check_timeout,
                    rlimit=rlimit,
                )

        issues = anti_vacuity_issues(entry, candidate, typecheck, checker)
        raw_reward = int(
            checker is not None
            and checker.get("status") == "ok"
            and checker.get("r0_z3") == "unsat"
        )
        guarded_reward = int(
            raw_reward == 1
            and typecheck is not None
            and typecheck.get("returncode") == 0
            and not issues
        )
        record = {
            "round": round_index,
            "llm_ms": llm_ms,
            "candidate": candidate,
            "checker": checker_summary(typecheck, checker),
            "anti_vacuity_issues": issues,
            "raw_det_reward": raw_reward,
            "guarded_reward": guarded_reward,
            "soundness_status": "unverified_trusted_external_contract",
            "apply_upstream": False,
        }
        history.append(record)
        (round_dir / "round_result.json").write_text(
            json.dumps(record, indent=2) + "\n"
        )
        if (
            candidate.get("decision") == "skip"
            or guarded_reward == 1
            or round_index >= feedback_rounds
        ):
            break
        prompt = FEEDBACK_PROMPT.format(
            target=entry["target"],
            candidate=json.dumps(candidate, indent=2),
            checker=json.dumps(checker_summary(typecheck, checker), indent=2),
            issues=json.dumps(issues, indent=2),
            verification_declaration=json.dumps(
                {
                    key: value
                    for key, value in verification.items()
                    if key != "source_context"
                },
                indent=2,
            ),
            verification_source=verification.get("source_context", ""),
        )

    final = history[-1] if history else {"status": "no_round"}
    result = {
        "target": entry["target"],
        "category": entry["category"],
        "history": history,
        "final": final,
    }
    (target_dir / "summary.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    return result


def metadata_nodes(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def collect(node: dict[str, Any]) -> None:
        nodes.append(node)
        batches = node.get("batches") or []
        if not isinstance(batches, list):
            raise ValueError("metadata.batches must be a list")
        for batch in batches:
            if not isinstance(batch, dict):
                raise ValueError("metadata.batches contains a non-object entry")
            collect(batch)

    collect(metadata)
    return nodes


def manifest_paths_from_metadata(metadata: dict[str, Any]) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for node in metadata_nodes(metadata):
        value = node.get("manifest")
        if not value:
            continue
        path = Path(str(value)).expanduser().resolve(strict=False)
        if path in seen:
            continue
        seen.add(path)
        paths.append(path)
    return paths


def manifest_entries_from_metadata(
    metadata: dict[str, Any],
) -> list[dict[str, Any]] | None:
    manifest_paths = manifest_paths_from_metadata(metadata)
    if not manifest_paths:
        return None

    entries: list[dict[str, Any]] = []
    entries_by_target: dict[str, tuple[dict[str, Any], Path]] = {}
    for manifest_path in manifest_paths:
        payload = json.loads(manifest_path.read_text())
        manifest_entries = (
            payload.get("targets", payload) if isinstance(payload, dict) else payload
        )
        if not isinstance(manifest_entries, list):
            raise ValueError(f"manifest is not a target list: {manifest_path}")
        for entry in manifest_entries:
            if not isinstance(entry, dict):
                raise ValueError(
                    f"manifest contains non-object targets: {manifest_path}"
                )
            target = str(entry.get("target") or "")
            if not target:
                raise ValueError(f"manifest target is empty: {manifest_path}")
            previous = entries_by_target.get(target)
            if previous is not None:
                previous_entry, previous_path = previous
                duplicate_kind = (
                    "duplicate" if previous_entry == entry else "conflicting"
                )
                raise ValueError(
                    f"{duplicate_kind} manifest definitions for {target!r}: "
                    f"{previous_path} and {manifest_path}"
                )
            entries_by_target[target] = (entry, manifest_path)
            entries.append(entry)
    return entries


def metadata_summary_value(
    metadata: dict[str, Any],
    key: str,
    default: str,
) -> str:
    values: list[str] = []
    for node in metadata_nodes(metadata):
        value = str(node.get(key) or "").strip()
        if value and value not in values:
            values.append(value)
    if not values:
        return default
    if len(values) == 1:
        return values[0]
    return "mixed: " + ", ".join(values)


def write_batch_summary(
    out_dir: Path,
    results: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    for result in results:
        normalize_result_contract_codes(result)
    finals = []
    for result in results:
        final = result.get("final") or {}
        candidate = final.get("candidate") or {}
        finals.append(
            {
                "target": result["target"],
                "category": result.get("category", ""),
                "status": final.get("status", ""),
                "decision": candidate.get("decision", final.get("decision", "")),
                "contract_form": candidate.get("contract_form", ""),
                "useful_claim": candidate.get("useful"),
                "raw_det_reward": final.get("raw_det_reward", 0),
                "guarded_reward": final.get("guarded_reward", 0),
                "issues": final.get("anti_vacuity_issues", final.get("issues", [])),
                "soundness_status": final.get("soundness_status", ""),
            }
        )
    manifest_entries = manifest_entries_from_metadata(metadata)
    expected_targets = (
        {str(entry["target"]) for entry in manifest_entries}
        if manifest_entries is not None
        else None
    )
    result_target_counts = Counter(str(result["target"]) for result in results)
    duplicate_result_targets = sorted(
        target for target, count in result_target_counts.items() if count > 1
    )
    if duplicate_result_targets:
        raise ValueError(
            "duplicate result targets: " + ", ".join(duplicate_result_targets)
        )
    result_targets = set(result_target_counts)
    counts = {
        "manifest_targets": (
            len(expected_targets) if expected_targets is not None else len(results)
        ),
        "targets": len(results),
        "missing_targets": (
            len(expected_targets - result_targets)
            if expected_targets is not None
            else 0
        ),
        "extra_targets": (
            len(result_targets - expected_targets)
            if expected_targets is not None
            else 0
        ),
        "add_spec": sum(item["decision"] == "add_spec" for item in finals),
        "skip": sum(item["decision"] == "skip" for item in finals),
        "raw_reward": sum(item["raw_det_reward"] for item in finals),
        "guarded_reward": sum(item["guarded_reward"] for item in finals),
        "static_skip": sum(item["status"] == "static_skip" for item in finals),
        "llm_errors": sum(item["status"] == "llm_error" for item in finals),
        "exceptions": sum(item["status"] == "exception" for item in finals),
    }
    payload = {
        "metadata": metadata,
        "counts": counts,
        "results": results,
        "final_candidates": finals,
    }
    (out_dir / "batch_summary.json").write_text(
        json.dumps(payload, indent=2) + "\n"
    )
    lines = [
        "# Rust std missing-contract generation with determinism feedback",
        "",
        f"- Model: `{metadata_summary_value(metadata, 'model', '<unknown>')}`",
        f"- Manifest targets: {counts['manifest_targets']}",
        f"- Targets: {counts['targets']}",
        f"- Missing targets: {counts['missing_targets']}",
        f"- Extra targets: {counts['extra_targets']}",
        f"- Add-spec decisions: {counts['add_spec']}",
        f"- Skip decisions: {counts['skip']}",
        f"- Static skips: {counts['static_skip']}",
        f"- Raw determinism reward: {counts['raw_reward']}",
        f"- Guarded reward: {counts['guarded_reward']}",
        f"- LLM errors: {counts['llm_errors']}",
        f"- Exceptions: {counts['exceptions']}",
        "- Soundness: external contracts remain unverified; no candidate is "
        "automatically eligible for upstream application.",
        "",
        "| Target | Category | Decision | Raw | Guarded | Issues |",
        "|---|---|---|---:|---:|---|",
    ]
    for item in sorted(finals, key=lambda value: value["target"]):
        lines.append(
            f"| `{item['target']}` | {item['category']} | {item['decision']} | "
            f"{item['raw_det_reward']} | {item['guarded_reward']} | "
            f"{', '.join(item['issues'])} |"
        )
    (out_dir / "SUMMARY.md").write_text("\n".join(lines).rstrip() + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    workspace = Path(__file__).resolve().parent
    parser.add_argument(
        "--manifest",
        type=Path,
        default=workspace / "specgen" / "pilot-manifest.json",
    )
    parser.add_argument(
        "--contracts",
        type=Path,
        default=workspace / "results" / "vstd_contracts.json",
    )
    parser.add_argument(
        "--vstd-root",
        type=Path,
        default=workspace / "verus" / "source" / "vstd",
    )
    parser.add_argument(
        "--verus-bin",
        type=Path,
        default=workspace
        / "verus"
        / "source"
        / "target-verus"
        / "release"
        / "verus",
    )
    parser.add_argument(
        "--z3-path",
        type=Path,
        default=workspace / "verus" / "source" / "z3",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=workspace / "specgen" / "pilot-gpt56sol",
    )
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--copilot-bin", default="copilot")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--include-non-suitable", action="store_true")
    parser.add_argument("--include-unavailable", action="store_true")
    parser.add_argument("--seed-candidates", type=Path)
    parser.add_argument("--feedback-rounds", type=int, default=2)
    parser.add_argument("--llm-timeout", type=int, default=420)
    parser.add_argument("--llm-retries", type=int, default=1)
    parser.add_argument("--check-timeout", type=int, default=240)
    parser.add_argument("--rlimit", type=float, default=60)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_payload = json.loads(args.manifest.read_text())
    entries = manifest_payload.get("targets", manifest_payload)
    if args.limit is not None:
        entries = entries[: args.limit]
    contracts = json.loads(args.contracts.read_text())
    seed_candidates = (
        json.loads(args.seed_candidates.read_text())
        if args.seed_candidates is not None
        else {}
    )
    args.out.mkdir(parents=True, exist_ok=True)
    logging.getLogger("spec_determinism").setLevel(logging.ERROR)
    view_registry = ViewRegistry.from_project(args.vstd_root)
    verus_version = subprocess.check_output(
        [str(args.verus_bin), "--version"],
        text=True,
    ).strip()
    metadata = {
        "model": args.model,
        "manifest": str(args.manifest.resolve()),
        "vstd_root": str(args.vstd_root.resolve()),
        "verus_bin": str(args.verus_bin.resolve()),
        "verus_version": verus_version,
        "feedback_rounds": args.feedback_rounds,
        "contract_soundness": "unverified_trusted_external_contract",
        "seed_candidates": (
            str(args.seed_candidates.resolve())
            if args.seed_candidates is not None
            else None
        ),
        "include_non_suitable": args.include_non_suitable,
        "include_unavailable": args.include_unavailable,
    }
    results = []
    pending_entries = []
    for entry in entries:
        summary_path = (
            args.out
            / "targets"
            / safe_name(entry["target"])
            / "summary.json"
        )
        if args.resume and summary_path.is_file():
            saved = json.loads(summary_path.read_text())
            final = saved.get("final") or {}
            if final.get("status") not in {"llm_error", "exception", "no_round"}:
                results.append(saved)
                continue
        pending_entries.append(entry)
    if results:
        print(f"resumed {len(results)} completed targets", flush=True)
        write_batch_summary(args.out, results, metadata)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_one,
                entry=entry,
                contracts=contracts,
                vstd_root=args.vstd_root,
                out_root=args.out,
                view_registry=view_registry,
                verus_bin=args.verus_bin,
                z3_path=args.z3_path,
                model=args.model,
                copilot_bin=args.copilot_bin,
                llm_timeout=args.llm_timeout,
                llm_retries=args.llm_retries,
                check_timeout=args.check_timeout,
                rlimit=args.rlimit,
                feedback_rounds=args.feedback_rounds,
                seed_candidate=seed_candidates.get(entry["target"]),
                include_non_suitable=args.include_non_suitable,
                include_unavailable=args.include_unavailable,
            ): entry
            for entry in pending_entries
        }
        for index, future in enumerate(as_completed(futures), start=1):
            entry = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {
                    "target": entry["target"],
                    "category": entry["category"],
                    "history": [],
                    "final": {
                        "status": "exception",
                        "error": f"{type(error).__name__}: {error}",
                    },
                }
            results.append(result)
            final = result.get("final") or {}
            candidate = final.get("candidate") or {}
            print(
                f"[{len(results)}/{len(entries)}] {entry['target']} "
                f"decision={candidate.get('decision', final.get('decision'))} "
                f"raw={final.get('raw_det_reward', 0)} "
                f"guarded={final.get('guarded_reward', 0)}",
                flush=True,
            )
            write_batch_summary(args.out, results, metadata)
    write_batch_summary(args.out, results, metadata)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
