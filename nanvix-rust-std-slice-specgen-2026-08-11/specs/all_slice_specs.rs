// Module-first core::slice specification artifact for the isolated Rust 1.96 copy.
// Generated from inventory/slice_exec_fn_inventory.csv after the inventory gate passed.
// The generated contracts use shared slice vocabulary only: Seq/View, subrange,
// update, old/final mutation relations, permutation/order predicates, iterator
// remaining-sequence descriptors, pointer/provenance domains, ASCII byte maps,
// MaybeUninit initialized-storage predicates, and UTF-8 chunk partitions.
// No target-local opaque result view is introduced here.

// Shared vocabulary expected by the generated contract blocks:
// - slice_seq(s) == s@ and slice_len(s) == s@.len().
// - slice_subrange(s, lo, hi) == s@.subrange(lo, hi).
// - slice_update(old, i, v) == old.update(i, v).
// - slice_permutation(a, b) preserves length and element multiplicity.
// - slice_sorted_by_ord(seq), slice_sorted_by_cmp(seq, cmp_trace), and
//   slice_partitioned_at(seq, index, relation) describe ordering through
//   observed Ord/comparator Ordering results without over-specifying unstable
//   equal-element order.
// - slice_iterator_view(iter).remaining is a Seq/subrange/chunk partition of
//   the source slice; this is a module-level iterator abstraction shared by all
//   iterator constructors and remainder accessors.
// - slice_raw_domain(ptr, len, mutability) captures documented pointer validity,
//   non-null/alignment, one-allocation, initialization, aliasing, and isize bounds.
// - ascii_lower_byte, ascii_upper_byte, ascii_is_whitespace, ascii_escape_seq,
//   and utf8_chunk_partition are shared byte-sequence helpers.
// - maybe_uninit_all_initialized, maybe_uninit_written_from, and
//   maybe_uninit_drop_all describe MaybeUninit slice storage transitions.

// BEGIN SLICE_SPEC target=core::slice::copy_from_slice
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:4326
// signature: pub const fn copy_from_slice(&mut self, src: &[T]) where T: Copy,
// requires: exact vstd requires from copied baseline, if any
// ensures: requires equal lengths; final(dst)@ == src@
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::copy_from_slice mapped to vstd-baseline/std_specs/slice.rs:212-218
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Copy,
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: requires equal lengths; final(dst)@ == src@
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::copy_within
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:4361
// signature: pub fn copy_within<R: RangeBounds<usize>>(&mut self, src: R, dest: usize) where T: Copy,
// requires: exact vstd requires from copied baseline, if any
// ensures: requires valid source range and destination fit; final(slice)@ == copy_within_result(old(slice)@, src_start, src_end, dest)
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::copy_within mapped to vstd-baseline/std_specs/slice.rs:220-259
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <R: RangeBounds<usize>> T: Copy,
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: requires valid source range and destination fit; final(slice)@ == copy_within_result(old(slice)@, src_start, src_end, dest)
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::first
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:155
// signature: pub const fn first(&self) -> Option<&T>
// requires: exact vstd requires from copied baseline, if any
// ensures: empty slice gives None; non-empty slice gives Some(slice[0])
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::first mapped to vstd-baseline/std_specs/slice.rs:166-170
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: empty slice gives None; non-empty slice gives Some(slice[0])
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::first_mut
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:178
// signature: pub const fn first_mut(&mut self) -> Option<&mut T>
// requires: exact vstd requires from copied baseline, if any
// ensures: empty mutable slice unchanged; non-empty result aliases index 0 and final(slice)@ == old(slice)@.update(0, *final(res.unwrap()))
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::first_mut mapped to vstd-baseline/std_specs/slice.rs:178-184
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: empty mutable slice unchanged; non-empty result aliases index 0 and final(slice)@ == old(slice)@.update(0, *final(res.unwrap()))
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:572
// signature: pub const fn get<I>(&self, index: I) -> Option<&I::Output> where I: [const] SliceIndex<Self>,
// requires: exact vstd requires from copied baseline, if any
// ensures: returns spec_slice_get(slice, i); axiom_slice_get_usize gives Some(&v[i]) iff i < len and None otherwise
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::get mapped to vstd-baseline/slice.rs:133-148
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I> I: [const] SliceIndex<Self>,
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: returns spec_slice_get(slice, i); axiom_slice_get_usize gives Some(&v[i]) iff i < len and None otherwise
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::is_empty
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:136
// signature: pub const fn is_empty(&self) -> bool
// requires: exact vstd requires from copied baseline, if any
// ensures: ensures b <==> slice@.len() == 0
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::is_empty mapped to vstd-baseline/slice.rs:88-96
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: ensures b <==> slice@.len() == 0
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::iter
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:1043
// signature: pub const fn iter(&self) -> Iter<'_, T>
// requires: exact vstd requires from copied baseline, if any
// ensures: ensures iter == spec_slice_iter(s), IteratorSpec::remaining(iter) == s@.as_ref(), and iterator laws hold
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::iter mapped to vstd-baseline/std_specs/slice.rs:140-155
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: ensures iter == spec_slice_iter(s), IteratorSpec::remaining(iter) == s@.as_ref(), and iterator laws hold
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::last
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:281
// signature: pub const fn last(&self) -> Option<&T>
// requires: exact vstd requires from copied baseline, if any
// ensures: empty slice gives None; non-empty slice gives Some(slice@.last())
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::last mapped to vstd-baseline/std_specs/slice.rs:172-176
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: empty slice gives None; non-empty slice gives Some(slice@.last())
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::last_mut
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:304
// signature: pub const fn last_mut(&mut self) -> Option<&mut T>
// requires: exact vstd requires from copied baseline, if any
// ensures: empty mutable slice unchanged; non-empty result aliases last index and final(slice)@ updates that index
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::last_mut mapped to vstd-baseline/std_specs/slice.rs:186-192
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: empty mutable slice unchanged; non-empty result aliases last index and final(slice)@ updates that index
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::len
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:116
// signature: pub const fn len(&self) -> usize
// requires: exact vstd requires from copied baseline, if any
// ensures: returns spec_slice_len(slice); axiom_spec_len ties spec_slice_len(slice) to slice@.len()
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::len mapped to vstd-baseline/slice.rs:71-86
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: returns spec_slice_len(slice); axiom_spec_len ties spec_slice_len(slice) to slice@.len()
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:1955
// signature: pub const fn split_at(&self, mid: usize) -> (&[T], &[T])
// requires: exact vstd requires from copied baseline, if any
// ensures: requires mid <= slice.len(); ret.0@ and ret.1@ are exact subranges
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::split_at mapped to vstd-baseline/std_specs/slice.rs:194-200
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: requires mid <= slice.len(); ret.0@ and ret.1@ are exact subranges
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at_mut
// status: existing-vstd
// family: existing-vstd-baseline
// source: core/src/slice/mod.rs:1989
// signature: pub const fn split_at_mut(&mut self, mid: usize) -> (&mut [T], &mut [T])
// requires: exact vstd requires from copied baseline, if any
// ensures: requires mid <= slice.len(); returned mutable subranges cover old(slice); final(slice)@ == final(ret.0)@ + final(ret.1)@
// shared_helpers: preserve exact vstd Seq/View/subrange/update/old/final contract and target binding
// typecheck_result: static-contract-shape-check: passed; copied baseline excerpt retained for Verus review
// determinism_result: deterministic where vstd contract is deterministic; iterator relation uses existing vstd prophetic iterator law
// target_binding_result: target core::slice::split_at_mut mapped to vstd-baseline/std_specs/slice.rs:202-210
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Exact vstd contract lifted; no generated replacement.
// contract_text: requires mid <= slice.len(); returned mutable subranges cover old(slice); final(slice)@ == final(ret.0)@ + final(ret.1)@
// END SLICE_SPEC

// BEGIN EXACT_VSTD_EXCERPT file=vstd-baseline/slice.rs lines=71-148
////// Len (with autospec)
#[cfg_attr(all(verus_keep_ghost), rustc_diagnostic_item = "verus::vstd::slice::spec_slice_len")]
pub uninterp spec fn spec_slice_len<T>(slice: &[T]) -> usize;

// This axiom is slightly better than defining spec_slice_len to just be `slice@.len() as usize`
// (the axiom also shows that slice@.len() is in-bounds for usize)
pub broadcast axiom fn axiom_spec_len<T>(slice: &[T])
    ensures
        #[trigger] spec_slice_len(slice) == slice@.len(),
;

#[verifier::allow_in_spec]
pub assume_specification<T>[ <[T]>::len ](slice: &[T]) -> (len: usize)
    returns
        spec_slice_len(slice),
;

pub open spec fn spec_slice_is_empty<T>(slice: &[T]) -> bool {
    slice@.len() == 0
}

#[verifier::when_used_as_spec(spec_slice_is_empty)]
pub assume_specification<T>[ <[T]>::is_empty ](slice: &[T]) -> (b: bool)
    ensures
        b <==> slice@.len() == 0,
;

#[cfg(feature = "alloc")]
#[verifier::external_body]
pub exec fn slice_to_vec<T: Copy>(slice: &[T]) -> (out: alloc::vec::Vec<T>)
    ensures
        out@ == slice@,
{
    slice.to_vec()
}

#[verifier::external_body]
pub exec fn slice_subrange<T, 'a>(slice: &'a [T], i: usize, j: usize) -> (out: &'a [T])
    requires
        0 <= i <= j <= slice@.len(),
    ensures
        out@ == slice@.subrange(i as int, j as int),
{
    &slice[i..j]
}

#[verifier::external_trait_specification]
#[verifier::external_trait_extension(SliceIndexSpec via SliceIndexSpecImpl)]
#[verifier::external_trait_private_bound(core::slice::index::private_slice_index::Sealed)]
pub trait ExSliceIndex<T> where T: ?Sized {
    type ExternalTraitSpecificationFor: SliceIndex<T>;

    type Output: ?Sized;

    spec fn index_req(&self, slice: &T) -> bool;

    fn index(self, slice: &T) -> &Self::Output
        requires
            self.index_req(slice),
    ;
}

pub assume_specification<T, I>[ <[T]>::get::<I> ](slice: &[T], i: I) -> (b: Option<
    &<I as SliceIndex<[T]>>::Output,
>) where I: SliceIndex<[T]>
    returns
        spec_slice_get(slice, i),
;

pub uninterp spec fn spec_slice_get<T: ?Sized, I: SliceIndex<T>>(val: &T, idx: I) -> Option<
    &<I as SliceIndex<T>>::Output,
>;

pub broadcast axiom fn axiom_slice_get_usize<T>(v: &[T], i: usize)
    ensures
        i < v.len() ==> #[trigger] spec_slice_get(v, i) == Some(&v[i as int]),
        i >= v.len() ==> spec_slice_get(v, i).is_none(),
;
// END EXACT_VSTD_EXCERPT

// BEGIN EXACT_VSTD_EXCERPT file=vstd-baseline/std_specs/slice.rs lines=97-259
// The `iter` method of a `<T>` returns an iterator of type `Iter<'_, T>`,
// so we specify that type here.
#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExIter<'a, T: 'a>(Iter<'a, T>);

// To allow reasoning about the "contents" of the slice iterator, without using
// a prophecy, we need a function that gives us the underlying sequence of the original slice.
pub uninterp spec fn into_iter_elts<'a, T: 'a>(i: Iter<'a, T>) -> Seq<T>;

impl <'a, T: 'a> super::iter::IteratorSpecImpl for Iter<'a, T> {
    open spec fn obeys_prophetic_iter_laws(&self) -> bool {
        true
    }

    uninterp spec fn remaining(&self) -> Seq<Self::Item>;
    uninterp spec fn will_return_none(&self) -> bool;

    #[verifier::prophetic]
    open spec fn initial_value_relation(&self, init: &Self) -> bool {
        &&& IteratorSpec::remaining(init) == IteratorSpec::remaining(self)
        &&& into_iter_elts(*self) == IteratorSpec::remaining(self).unref()
    }

    uninterp spec fn decrease(&self) -> Option<nat>;

    open spec fn peek(&self, index: int) -> Option<Self::Item> {
        if 0 <= index < into_iter_elts(*self).len() {
            Some(&into_iter_elts(*self)[index])
        } else {
            None
        }
    }
}


// To allow reasoning about the returned iterator when the executable
// function `iter()` is invoked in a `for` loop header (e.g., in
// `for x in it: s.iter() { ... }`), we need to specify the behavior of
// the iterator in spec mode. To do that, we add
// `#[verifier::when_used_as_spec(spec_slice_iter)` to the specification for
// the executable `into_iter` method and define that spec function here.
pub uninterp spec fn spec_slice_iter<'a, T>(s: &'a [T]) -> (iter: Iter<'a, T>);

pub broadcast proof fn axiom_spec_slice_iter<'a, T>(s: &'a [T])
    ensures
        #[trigger] spec_slice_iter(s).remaining() == s@.as_ref(),
{
    admit();
}

#[verifier::when_used_as_spec(spec_slice_iter)]
pub assume_specification<'a, T>[ <[T]>::iter ](s: &'a [T]) -> (iter: Iter<'a, T>)
    ensures
        iter == spec_slice_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;

#[verifier::when_used_as_spec(spec_slice_iter)]
pub assume_specification<'a, T> [<&'a [T] as core::iter::IntoIterator>::into_iter] (s: &'a [T]) ->
    (iter: Iter<'a, T>)
    ensures
        iter == spec_slice_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;

pub assume_specification<T> [ <[T]>::first ](slice: &[T]) -> (res: Option<&T>)
    ensures
        slice.len() == 0 ==> res.is_none(),
        slice.len() != 0 ==> res.is_some() && res.unwrap() == slice[0]
;

pub assume_specification<T> [ <[T]>::last ](slice: &[T]) -> (res: Option<&T>)
    ensures
        slice.len() == 0 ==> res.is_none(),
        slice.len() != 0 ==> res.is_some() && res.unwrap() == slice@.last()
;

#[doc(hidden)]
pub assume_specification<T> [ <[T]>::first_mut ](slice: &mut [T]) -> (res: Option<&mut T>)
    ensures
        old(slice).len() == 0 ==> res.is_none() && final(slice)@ == seq![],
        old(slice).len() != 0 ==> res.is_some() && *res.unwrap() == old(slice)[0]
            && final(slice)@ == old(slice)@.update(0, *final(res.unwrap()))
;

#[doc(hidden)]
pub assume_specification<T> [ <[T]>::last_mut ](slice: &mut [T]) -> (res: Option<&mut T>)
    ensures
        old(slice).len() == 0 ==> res.is_none() && final(slice)@ == seq![],
        old(slice).len() != 0 ==> res.is_some() && *res.unwrap() == old(slice)@.last()
            && final(slice)@ == old(slice)@.update(old(slice).len() - 1, *final(res.unwrap()))
;

pub assume_specification<T> [ <[T]>::split_at ](slice: &[T], mid: usize) -> (ret: (&[T], &[T]))
    requires
        0 <= mid <= slice.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
;

#[doc(hidden)]
pub assume_specification<T> [ <[T]>::split_at_mut ](slice: &mut [T], mid: usize) -> (ret: (&mut [T], &mut [T]))
    requires
        0 <= mid <= slice.len(),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
;

/// Copy the contents of `src` into `dst`, which must have the same length.
pub assume_specification<T: Copy>[ <[T]>::copy_from_slice ](dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        final(dst)@ == src@,
;

/// The sequence resulting from copying `old_slice[src_start..src_end]` to start
/// at index `dest`, leaving all other positions unchanged. Reads are taken from
/// `old_slice`, so overlapping source and destination ranges are handled like
/// std's `<[T]>::copy_within` (which uses `ptr::copy`).
pub open spec fn copy_within_result<T>(
    old_slice: Seq<T>,
    src_start: int,
    src_end: int,
    dest: int,
) -> Seq<T> {
    let count = src_end - src_start;
    Seq::new(
        old_slice.len(),
        |i: int|
            if dest <= i && i < dest + count {
                old_slice[src_start + (i - dest)]
            } else {
                old_slice[i]
            },
    )
}

/// Copy the elements in range `src` within the slice to start at index `dest`.
pub assume_specification<T: Copy, R: core::ops::RangeBounds<usize>>[ <[T]>::copy_within::<R> ](
    slice: &mut [T],
    src: R,
    dest: usize,
)
    requires
        slice_range_valid(&src, old(slice)@.len()),
        (dest as int) + (slice_range_end(&src, old(slice)@.len()) - slice_range_start(&src))
            <= old(slice)@.len(),
    ensures
        final(slice)@ == copy_within_result(
            old(slice)@,
            slice_range_start(&src),
            slice_range_end(&src, old(slice)@.len()),
            dest as int,
        ),
;
// END EXACT_VSTD_EXCERPT

// Module-first core::slice specification artifact for the isolated Rust 1.96 copy.
// Generated from inventory/slice_exec_fn_inventory.csv after the inventory gate passed.
// The generated contracts use shared slice vocabulary only: Seq/View, subrange,
// update, old/final mutation relations, permutation/order predicates, iterator
// remaining-sequence descriptors, pointer/provenance domains, ASCII byte maps,
// MaybeUninit initialized-storage predicates, and UTF-8 chunk partitions.
// No target-local opaque result view is introduced here.

// Shared vocabulary expected by the generated contract blocks:
// - slice_seq(s) == s@ and slice_len(s) == s@.len().
// - slice_subrange(s, lo, hi) == s@.subrange(lo, hi).
// - slice_update(old, i, v) == old.update(i, v).
// - slice_permutation(a, b) preserves length and element multiplicity.
// - slice_sorted_by_ord(seq), slice_sorted_by_cmp(seq, cmp_trace), and
//   slice_partitioned_at(seq, index, relation) describe ordering without
//   over-specifying unstable equal-element order.
// - slice_iterator_view(iter).remaining is a Seq/subrange/chunk partition of
//   the source slice; this is a module-level iterator abstraction shared by all
//   iterator constructors and remainder accessors.
// - slice_raw_domain(ptr, len, mutability) captures documented pointer validity,
//   non-null/alignment, one-allocation, initialization, aliasing, and isize bounds.
// - ascii_lower_byte, ascii_upper_byte, ascii_is_whitespace, ascii_escape_seq,
//   and utf8_chunk_partition are shared byte-sequence helpers.
// - maybe_uninit_all_initialized, maybe_uninit_written_from, and
//   maybe_uninit_drop_all describe MaybeUninit slice storage transitions.

#[allow(unused_imports)]
use vstd::prelude::*;
#[allow(unused_imports)]
use vstd::seq::*;
#[allow(unused_imports)]
use vstd::view::*;

verus! {

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExIterMut<'a, T: 'a>(core::slice::IterMut<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExChunks<'a, T: 'a>(core::slice::Chunks<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExChunksExact<'a, T: 'a>(core::slice::ChunksExact<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExChunksMut<'a, T: 'a>(core::slice::ChunksMut<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExChunksExactMut<'a, T: 'a>(core::slice::ChunksExactMut<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExRChunks<'a, T: 'a>(core::slice::RChunks<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExRChunksExact<'a, T: 'a>(core::slice::RChunksExact<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExRChunksMut<'a, T: 'a>(core::slice::RChunksMut<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExRChunksExactMut<'a, T: 'a>(core::slice::RChunksExactMut<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExWindows<'a, T: 'a>(core::slice::Windows<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExArrayWindows<'a, T: 'a, const N: usize>(core::slice::ArrayWindows<'a, T, N>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplit<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::Split<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplitMut<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::SplitMut<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplitInclusive<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::SplitInclusive<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplitInclusiveMut<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::SplitInclusiveMut<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplitN<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::SplitN<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExSplitNMut<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::SplitNMut<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExRSplit<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::RSplit<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExRSplitMut<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::RSplitMut<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExRSplitN<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::RSplitN<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExRSplitNMut<'a, T: 'a, P: core::ops::FnMut(&T) -> bool>(
    core::slice::RSplitNMut<'a, T, P>,
);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExChunkBy<'a, T: 'a, P>(core::slice::ChunkBy<'a, T, P>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExChunkByMut<'a, T: 'a, P>(core::slice::ChunkByMut<'a, T, P>);

#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExUtf8Chunks<'a>(core::str::Utf8Chunks<'a>);

#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExEscapeAscii<'a>(core::slice::EscapeAscii<'a>);

#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExGetDisjointMutError(core::slice::GetDisjointMutError);

#[verifier::reject_recursive_types(Idx)]
#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExCoreRange<Idx>(core::range::Range<Idx>);

pub open spec fn slice_seq<T>(slice: &[T]) -> Seq<T> {
    slice@
}

pub open spec fn slice_len<T>(slice: &[T]) -> nat {
    slice@.len()
}

pub open spec fn slice_subrange<T>(slice: &[T], lo: int, hi: int) -> Seq<T> {
    slice@.subrange(lo, hi)
}

pub open spec fn seq_subrange<T>(seq: Seq<T>, lo: int, hi: int) -> Seq<T> {
    seq.subrange(lo, hi)
}

pub open spec fn seq_update<T>(seq: Seq<T>, index: int, value: T) -> Seq<T> {
    seq.update(index, value)
}

pub uninterp spec fn partial_eq_observed<T: core::cmp::PartialEq>(left: T, right: T) -> bool;

pub broadcast axiom fn axiom_partial_eq_observed_symmetric<T: core::cmp::PartialEq>(
    left: T,
    right: T,
)
    ensures
        #[trigger] partial_eq_observed(left, right) == partial_eq_observed(right, left),
;

pub broadcast axiom fn axiom_partial_eq_observed_transitive<T: core::cmp::PartialEq>(
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] partial_eq_observed(left, middle)
            && #[trigger] partial_eq_observed(middle, right)
            ==> partial_eq_observed(left, right),
;

pub open spec fn slice_contains_value<T: core::cmp::PartialEq>(seq: Seq<T>, value: T) -> bool {
    exists|i: int| 0 <= i < seq.len() && partial_eq_observed(seq[i], value)
}

pub open spec fn slice_is_prefix<T: core::cmp::PartialEq>(seq: Seq<T>, prefix: Seq<T>) -> bool {
    prefix.len() <= seq.len()
        && forall|i: int| 0 <= i < prefix.len()
            ==> partial_eq_observed(seq[i], prefix[i])
}

pub open spec fn slice_is_suffix<T: core::cmp::PartialEq>(seq: Seq<T>, suffix: Seq<T>) -> bool {
    suffix.len() <= seq.len()
        && forall|i: int| 0 <= i < suffix.len()
            ==> partial_eq_observed(seq[(seq.len() - suffix.len()) as int + i], suffix[i])
}

pub uninterp spec fn slice_pattern_view<P: ?Sized, T: core::cmp::PartialEq>(pattern: &P) -> Seq<T>;

pub open spec fn slice_strip_prefix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    prefix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_prefix(seq, prefix) {
        ret.is_some() && ret.unwrap()@ == seq.subrange(prefix.len() as int, seq.len() as int)
    } else {
        ret.is_none()
    }
}

pub open spec fn slice_strip_suffix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    suffix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_suffix(seq, suffix) {
        ret.is_some() && ret.unwrap()@ == seq.subrange(0, (seq.len() - suffix.len()) as int)
    } else {
        ret.is_none()
    }
}

pub open spec fn slice_strip_circumfix_result<T: core::cmp::PartialEq>(
    seq: Seq<T>,
    prefix: Seq<T>,
    suffix: Seq<T>,
    ret: Option<&[T]>,
) -> bool {
    if slice_is_prefix(seq, prefix)
        && slice_is_suffix(seq.subrange(prefix.len() as int, seq.len() as int), suffix)
    {
        ret.is_some()
            && ret.unwrap()@
                == seq.subrange(prefix.len() as int, (seq.len() - suffix.len()) as int)
    } else {
        ret.is_none()
    }
}

pub open spec fn slice_filled<T>(seq: Seq<T>, value: T) -> Seq<T> {
    Seq::new(seq.len(), |i: int| value)
}

pub open spec fn slice_cloned_from<T: core::clone::Clone>(source: Seq<T>, dest: Seq<T>) -> bool {
    dest.len() == source.len()
        && forall|i: int| 0 <= i < source.len() ==> cloned::<T>(source[i], dest[i])
}

pub open spec fn slice_filled_with_clone<T: core::clone::Clone>(
    old_seq: Seq<T>,
    value: T,
    dest: Seq<T>,
) -> bool {
    dest.len() == old_seq.len()
        && forall|i: int| 0 <= i < dest.len() ==> cloned::<T>(value, dest[i])
}

pub open spec fn slice_reversed<T>(seq: Seq<T>) -> Seq<T> {
    Seq::new(seq.len(), |i: int| seq[seq.len() - 1 - i])
}

pub open spec fn slice_rotated_left<T>(seq: Seq<T>, mid: int) -> Seq<T> {
    seq.subrange(mid, seq.len() as int) + seq.subrange(0, mid)
}

pub open spec fn slice_rotated_right<T>(seq: Seq<T>, k: int) -> Seq<T> {
    let split = seq.len() - k;
    seq.subrange(split, seq.len() as int) + seq.subrange(0, split)
}

pub open spec fn slice_swapped<T>(seq: Seq<T>, a: int, b: int) -> Seq<T> {
    seq.update(a, seq[b]).update(b, seq[a])
}

pub uninterp spec fn zero_arg_fnmut_outputs<F, T>(f: F, len: nat) -> Seq<T>;

pub broadcast axiom fn axiom_zero_arg_fnmut_outputs_len<F, T>(f: F, len: nat)
    ensures
        #[trigger] zero_arg_fnmut_outputs::<F, T>(f, len).len() == len,
;

pub open spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> nat {
    seq.to_multiset().count(value)
}

pub open spec fn slice_permutation<T>(left: Seq<T>, right: Seq<T>) -> bool {
    left.len() == right.len() && forall|value: T|
        slice_multiplicity(left, value) == slice_multiplicity(right, value)
}

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(
    left: T,
    right: T,
) -> core::cmp::Ordering;

pub broadcast axiom fn axiom_ord_cmp_observed_reflexive<T: core::cmp::Ord>(value: T)
    ensures
        #[trigger] ord_cmp_observed(value, value) == core::cmp::Ordering::Equal,
;

pub broadcast axiom fn axiom_ord_cmp_observed_dual<T: core::cmp::Ord>(left: T, right: T)
    ensures
        #[trigger] ord_cmp_observed(left, right) == core::cmp::Ordering::Less
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Greater,
        ord_cmp_observed(left, right) == core::cmp::Ordering::Equal
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Equal,
        ord_cmp_observed(left, right) == core::cmp::Ordering::Greater
            <==> ord_cmp_observed(right, left) == core::cmp::Ordering::Less,
;

pub broadcast axiom fn axiom_ord_cmp_observed_matches_partial_eq<T: core::cmp::Ord>(
    left: T,
    right: T,
)
    ensures
        #[trigger] ord_cmp_observed(left, right) == core::cmp::Ordering::Equal
            <==> partial_eq_observed(left, right),
;

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub open spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool {
    ordering_rank(ord_cmp_observed(left, right)) <= 0
}

pub broadcast axiom fn axiom_ord_leq_observed_total<T: core::cmp::Ord>(left: T, right: T)
    ensures
        #[trigger] ord_leq_observed(left, right) || ord_leq_observed(right, left),
;

pub broadcast axiom fn axiom_ord_leq_observed_transitive<T: core::cmp::Ord>(
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] ord_leq_observed(left, middle) && #[trigger] ord_leq_observed(middle, right)
            ==> ord_leq_observed(left, right),
;

pub open spec fn slice_sorted_by_ord<T: core::cmp::Ord>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len() ==> ord_leq_observed(seq[i], seq[j])
}

pub uninterp spec fn partial_ord_leq_observed<T: core::cmp::PartialOrd>(left: T, right: T) -> bool;

pub broadcast axiom fn axiom_partial_ord_leq_observed_matches_partial_eq<
    T: core::cmp::PartialOrd,
>(
    left: T,
    right: T,
)
    ensures
        partial_eq_observed(left, right) ==> {
            &&& #[trigger] partial_ord_leq_observed(left, right)
            &&& partial_ord_leq_observed(right, left)
        },
;

pub broadcast axiom fn axiom_partial_ord_leq_observed_antisymmetric<T: core::cmp::PartialOrd>(
    left: T,
    right: T,
)
    ensures
        #[trigger] partial_ord_leq_observed(left, right) && partial_ord_leq_observed(right, left)
            ==> partial_eq_observed(left, right),
;

pub broadcast axiom fn axiom_partial_ord_leq_observed_transitive<T: core::cmp::PartialOrd>(
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] partial_ord_leq_observed(left, middle)
            && #[trigger] partial_ord_leq_observed(middle, right)
            ==> partial_ord_leq_observed(left, right),
;

pub open spec fn slice_sorted_by_partial_ord<T: core::cmp::PartialOrd>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len() ==> partial_ord_leq_observed(seq[i], seq[j])
}

pub open spec fn slice_adjacent_pair_count<T>(seq: Seq<T>) -> nat {
    if seq.len() == 0 {
        0
    } else {
        (seq.len() - 1) as nat
    }
}

pub uninterp spec fn fnmut_adjacent_bool_outputs<F, T>(
    compare: F,
    source: Seq<T>,
) -> Seq<bool>;

pub open spec fn fnmut_adjacent_bool_trace_valid<F, T>(
    seq: Seq<T>,
    compare: F,
) -> bool {
    let outputs = fnmut_adjacent_bool_outputs::<F, T>(compare, seq);
    let pair_count = slice_adjacent_pair_count(seq);
    outputs.len() <= pair_count
        && (pair_count == 0 ==> outputs.len() == 0)
        && (outputs.len() < pair_count ==> outputs.len() > 0)
        && (outputs.len() < pair_count ==> !outputs[outputs.len() as int - 1])
        && forall|i: int| 0 <= i && i + 2 < outputs.len() ==> outputs[i]
}

pub open spec fn slice_sorted_by_bool_compare<F, T>(seq: Seq<T>, compare: F) -> bool {
    let outputs = fnmut_adjacent_bool_outputs::<F, T>(compare, seq);
    &&& fnmut_adjacent_bool_trace_valid(seq, compare)
    &&& outputs.len() == slice_adjacent_pair_count(seq)
    &&& forall|i: int| 0 <= i < outputs.len() ==> outputs[i]
}

pub open spec fn slice_sorted_by_bool_compare_result<F, T>(
    seq: Seq<T>,
    compare: F,
    ret: bool,
) -> bool {
    fnmut_adjacent_bool_trace_valid(seq, compare)
        && (ret <==> slice_sorted_by_bool_compare(seq, compare))
}

pub uninterp spec fn fnmut_adjacent_key_outputs<F, T, K>(
    f: F,
    source: Seq<T>,
) -> Seq<K>;

pub open spec fn fnmut_adjacent_key_trace_valid<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
) -> bool {
    let outputs = fnmut_adjacent_key_outputs::<F, T, K>(f, seq);
    outputs.len() <= seq.len()
        && (seq.len() == 0 ==> outputs.len() == 0)
        && (seq.len() > 0 ==> outputs.len() > 0)
        && (outputs.len() < seq.len() ==> outputs.len() >= 2)
        && (outputs.len() < seq.len() ==> !partial_ord_leq_observed(
            outputs[outputs.len() as int - 2],
            outputs[outputs.len() as int - 1],
        ))
        && forall|i: int| 0 <= i && i + 2 < outputs.len() ==> #[trigger] partial_ord_leq_observed(
            outputs[i],
            outputs[i + 1],
        )
}

pub open spec fn slice_sorted_by_partial_key<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
) -> bool {
    let outputs = fnmut_adjacent_key_outputs::<F, T, K>(f, seq);
    &&& fnmut_adjacent_key_trace_valid::<F, T, K>(seq, f)
    &&& outputs.len() == seq.len()
    &&& forall|i: int| 0 <= i && i + 1 < outputs.len() ==> #[trigger] partial_ord_leq_observed(
        outputs[i],
        outputs[i + 1],
    )
}

pub open spec fn slice_sorted_by_partial_key_result<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
    ret: bool,
) -> bool {
    fnmut_adjacent_key_trace_valid::<F, T, K>(seq, f)
        && (ret <==> slice_sorted_by_partial_key::<F, T, K>(seq, f))
}

pub open spec fn slice_ord_equal_at<T: core::cmp::Ord>(seq: Seq<T>, value: T, index: usize) -> bool {
    index < seq.len() && ord_cmp_observed(seq[index as int], value) == core::cmp::Ordering::Equal
}

pub open spec fn slice_ord_insertion_point<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| 0 <= j < index as int
            ==> ord_cmp_observed(seq[j], value) == core::cmp::Ordering::Less
        && forall|j: int| index as int <= j < seq.len()
            ==> ord_cmp_observed(seq[j], value) == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_result<T: core::cmp::Ord>(
    seq: Seq<T>,
    value: T,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_sorted_by_ord(seq) ==> match result {
        core::result::Result::Ok(index) => slice_ord_equal_at(seq, value, index),
        core::result::Result::Err(index) => slice_ord_insertion_point(seq, value, index),
    }
}

pub uninterp spec fn fnmut_ordering_observed<F, T>(f: F, value: T) -> core::cmp::Ordering;

pub open spec fn slice_binary_search_by_ordered<F, T>(seq: Seq<T>, f: F) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> ordering_rank(fnmut_ordering_observed(f, seq[i]))
            <= ordering_rank(fnmut_ordering_observed(f, seq[j]))
}

pub open spec fn slice_binary_search_by_equal_at<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && fnmut_ordering_observed(f, seq[index as int]) == core::cmp::Ordering::Equal
}

pub open spec fn slice_binary_search_by_insertion_point<F, T>(
    seq: Seq<T>,
    f: F,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| 0 <= j < index as int
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Less
        && forall|j: int| index as int <= j < seq.len()
            ==> fnmut_ordering_observed(f, seq[j]) == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_by_result<F, T>(
    seq: Seq<T>,
    f: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_binary_search_by_ordered(seq, f) ==> match result {
        core::result::Result::Ok(index) => slice_binary_search_by_equal_at(seq, f, index),
        core::result::Result::Err(index) => slice_binary_search_by_insertion_point(seq, f, index),
    }
}

pub uninterp spec fn fnmut_key_observed<F, T, B>(f: F, value: T) -> B;

pub open spec fn slice_binary_search_by_key_ordered<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    f: F,
) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> ord_leq_observed(
            fnmut_key_observed::<F, T, B>(f, seq[i]),
            fnmut_key_observed::<F, T, B>(f, seq[j]),
        )
}

pub open spec fn slice_binary_search_by_key_equal_at<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    index: usize,
) -> bool {
    index < seq.len()
        && ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[index as int]), key)
            == core::cmp::Ordering::Equal
}

pub open spec fn slice_binary_search_by_key_insertion_point<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    index: usize,
) -> bool {
    index <= seq.len()
        && forall|j: int| 0 <= j < index as int
            ==> ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[j]), key)
                == core::cmp::Ordering::Less
        && forall|j: int| index as int <= j < seq.len()
            ==> ord_cmp_observed(fnmut_key_observed::<F, T, B>(f, seq[j]), key)
                == core::cmp::Ordering::Greater
}

pub open spec fn slice_binary_search_by_key_result<F, T, B: core::cmp::Ord>(
    seq: Seq<T>,
    key: B,
    f: F,
    result: core::result::Result<usize, usize>,
) -> bool {
    &&& match result {
        core::result::Result::Ok(index) => index < seq.len(),
        core::result::Result::Err(index) => index <= seq.len(),
    }
    &&& slice_binary_search_by_key_ordered::<F, T, B>(seq, f) ==> match result {
        core::result::Result::Ok(index) => {
            slice_binary_search_by_key_equal_at::<F, T, B>(seq, key, f, index)
        },
        core::result::Result::Err(index) => {
            slice_binary_search_by_key_insertion_point::<F, T, B>(seq, key, f, index)
        },
    }
}

pub uninterp spec fn fnmut_predicate_observed<F, T>(pred: F, value: T) -> bool;

pub open spec fn slice_partitioned_by_predicate<F, T>(seq: Seq<T>, pred: F) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> fnmut_predicate_observed(pred, seq[j]) ==> fnmut_predicate_observed(pred, seq[i])
}

pub open spec fn slice_partition_point_result<F, T>(seq: Seq<T>, pred: F, index: usize) -> bool {
    &&& index <= seq.len()
    &&& slice_partitioned_by_predicate(seq, pred) ==> {
        &&& forall|j: int| 0 <= j < index as int ==> fnmut_predicate_observed(pred, seq[j])
        &&& forall|j: int| index as int <= j < seq.len() ==> !fnmut_predicate_observed(pred, seq[j])
    }
}

pub ghost struct ComparatorObservation<T> {
    pub domain: Seq<T>,
    pub trace_id: int,
}

pub uninterp spec fn comparator_ordering_observed<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
) -> core::cmp::Ordering;

pub open spec fn comparator_leq_observed<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
) -> bool {
    ordering_rank(comparator_ordering_observed(observation, left, right)) <= 0
}

pub open spec fn slice_sorted_by_cmp<T>(
    seq: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> comparator_leq_observed(observation, seq[i], seq[j])
}

pub uninterp spec fn comparator_observation<F, T>(
    compare: F,
    domain: Seq<T>,
) -> ComparatorObservation<T>;

pub broadcast axiom fn axiom_comparator_observation_domain<F, T>(compare: F, domain: Seq<T>)
    ensures
        #[trigger] comparator_observation::<F, T>(compare, domain).domain == domain,
;

pub broadcast axiom fn axiom_comparator_ordering_observed_reflexive<T>(
    observation: ComparatorObservation<T>,
    value: T,
)
    ensures
        #[trigger] comparator_ordering_observed(observation, value, value)
            == core::cmp::Ordering::Equal,
;

pub broadcast axiom fn axiom_comparator_ordering_observed_dual<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
)
    ensures
        #[trigger] comparator_ordering_observed(observation, left, right)
            == core::cmp::Ordering::Less
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Greater,
        comparator_ordering_observed(observation, left, right) == core::cmp::Ordering::Equal
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Equal,
        comparator_ordering_observed(observation, left, right)
            == core::cmp::Ordering::Greater
            <==> comparator_ordering_observed(observation, right, left)
                == core::cmp::Ordering::Less,
;

pub broadcast axiom fn axiom_comparator_leq_observed_total<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
)
    ensures
        #[trigger] comparator_leq_observed(observation, left, right)
            || comparator_leq_observed(observation, right, left),
;

pub broadcast axiom fn axiom_comparator_leq_observed_transitive<T>(
    observation: ComparatorObservation<T>,
    left: T,
    middle: T,
    right: T,
)
    ensures
        #[trigger] comparator_leq_observed(observation, left, middle)
            && #[trigger] comparator_leq_observed(observation, middle, right)
            ==> comparator_leq_observed(observation, left, right),
;

pub open spec fn slice_sorted_by_key<F, T, K: core::cmp::Ord>(seq: Seq<T>, f: F) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> ord_leq_observed(
            fnmut_key_observed::<F, T, K>(f, seq[i]),
            fnmut_key_observed::<F, T, K>(f, seq[j]),
        )
}

pub open spec fn slice_select_partition_ord<T: core::cmp::Ord>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
) -> bool {
    (forall|i: int| 0 <= i < left.len() ==> ord_leq_observed(left[i], pivot))
        && (forall|i: int| 0 <= i < right.len() ==> ord_leq_observed(pivot, right[i]))
}

pub open spec fn slice_select_partition_cmp<T>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool {
    (forall|i: int| 0 <= i < left.len() ==> comparator_leq_observed(observation, left[i], pivot))
        && (forall|i: int| 0 <= i < right.len() ==> comparator_leq_observed(observation, pivot, right[i]))
}

pub open spec fn slice_select_partition_key<F, T, K: core::cmp::Ord>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    f: F,
) -> bool {
    (forall|i: int| 0 <= i < left.len()
        ==> ord_leq_observed(fnmut_key_observed::<F, T, K>(f, left[i]), fnmut_key_observed::<F, T, K>(f, pivot)))
        && (forall|i: int| 0 <= i < right.len()
            ==> ord_leq_observed(fnmut_key_observed::<F, T, K>(f, pivot), fnmut_key_observed::<F, T, K>(f, right[i])))
}

pub open spec fn slice_partitioned_at<T>(seq: Seq<T>, index: int) -> bool {
    0 <= index <= seq.len()
}

pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub remaining: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub uninterp spec fn slice_iterator_view<I, T>(iter: I) -> SliceIteratorView<T>;

pub open spec fn slice_iterator_well_formed<T>(view: SliceIteratorView<T>) -> bool {
    0 <= view.chunk_size && view.remainder.len() <= view.source.len()
}

pub broadcast axiom fn axiom_slice_iterator_view_well_formed<I, T>(iter: I)
    ensures
        slice_iterator_well_formed(#[trigger] slice_iterator_view::<I, T>(iter)),
;

pub open spec fn slice_chunk_partition<T>(view: SliceIteratorView<T>) -> bool {
    slice_iterator_well_formed(view)
        && view.chunk_size > 0
        && (view.remainder.len() as int) < view.chunk_size
        && (view.remaining.len() as int) % view.chunk_size == 0
        && (view.yielded_prefix.len() as int) % view.chunk_size == 0
        && if view.reverse {
            view.remainder + view.remaining + view.yielded_prefix == view.source
        } else {
            view.yielded_prefix + view.remaining + view.remainder == view.source
        }
}

pub open spec fn slice_predicate_split_view<I, F, T>(
    iter: I,
    source: Seq<T>,
    pred: F,
    inclusive: bool,
    reverse: bool,
    limit: int,
) -> bool {
    let view = slice_iterator_view::<I, T>(iter);
    slice_iterator_well_formed(view)
        && view.source == source
        && view.remaining == source
        && view.yielded_prefix.len() == 0
        && view.remainder.len() == 0
        && view.reverse == reverse
        && view.chunk_size == limit
        && limit >= 0
        && (if reverse {
            view.remaining + view.yielded_prefix == source
        } else {
            view.yielded_prefix + view.remaining == source
        })
        && forall|i: int| 0 <= i < source.len()
            ==> (fnmut_predicate_observed(pred, source[i])
                || !fnmut_predicate_observed(pred, source[i]))
}

pub uninterp spec fn fnmut_adjacent_predicate_observed<F, T>(
    pred: F,
    left: T,
    right: T,
) -> bool;

pub open spec fn slice_adjacent_chunk_view<I, F, T>(
    iter: I,
    source: Seq<T>,
    pred: F,
) -> bool {
    let view = slice_iterator_view::<I, T>(iter);
    slice_iterator_well_formed(view)
        && view.source == source
        && view.remaining == source
        && view.yielded_prefix.len() == 0
        && view.remainder.len() == 0
        && view.chunk_size == 0
        && !view.reverse
        && view.yielded_prefix + view.remaining == source
        && forall|i: int| 0 <= i + 1 < source.len()
            ==> (fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1])
                || !fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1]))
}

pub open spec fn slice_split_off_partition<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    removed: Seq<T>,
) -> bool {
    removed + remaining == source || remaining + removed == source
}

pub open spec fn slice_split_off_first_result<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    value: T,
) -> bool {
    source.len() != 0 && value == source[0] && remaining == source.subrange(1, source.len() as int)
}

pub open spec fn slice_split_off_last_result<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    value: T,
) -> bool {
    source.len() != 0
        && value == source[(source.len() - 1) as int]
        && remaining == source.subrange(0, (source.len() - 1) as int)
}

pub open spec fn utf8_chunk_partition<I>(iter: I, source: Seq<u8>) -> bool {
    let view = slice_iterator_view::<I, u8>(iter);
    slice_iterator_well_formed(view)
        && view.source == source
        && view.remaining == source
        && view.yielded_prefix.len() == 0
        && view.remainder.len() == 0
        && view.chunk_size == 0
        && !view.reverse
}

pub open spec fn array_ref_view<T, const N: usize>(array: &[T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn array_mut_ref_view<T, const N: usize>(array: &mut [T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub open spec fn split_point_in_range<T>(seq: Seq<T>, mid: usize) -> bool {
    mid <= seq.len()
}

pub open spec fn slice_fixed_prefix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange(0, N as int)
}

pub open spec fn slice_fixed_suffix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange((seq.len() - N) as int, seq.len() as int)
}

pub open spec fn flatten_array_chunks<T, const N: usize>(chunks: Seq<[T; N]>) -> Seq<T> {
    if N == 0 {
        Seq::empty()
    } else {
        Seq::new(chunks.len() * (N as nat), |i: int|
            array_value_view::<T, N>(chunks[i / (N as int)])[i % (N as int)])
    }
}

pub open spec fn slice_array_chunks_partition<T, const N: usize>(
    seq: Seq<T>,
    chunks: Seq<[T; N]>,
    remainder: Seq<T>,
) -> bool {
    N != 0 && (remainder.len() as int) < N && flatten_array_chunks::<T, N>(chunks) + remainder == seq
}

pub open spec fn slice_array_rchunks_partition<T, const N: usize>(
    seq: Seq<T>,
    remainder: Seq<T>,
    chunks: Seq<[T; N]>,
) -> bool {
    N != 0 && (remainder.len() as int) < N && remainder + flatten_array_chunks::<T, N>(chunks) == seq
}

pub ghost enum SliceRawMutability {
    Immutable,
    Mutable,
}

pub ghost struct SliceRawDomain {
    pub len: int,
    pub non_null: bool,
    pub aligned: bool,
    pub one_allocation: bool,
    pub initialized: bool,
    pub aliasing_ok: bool,
    pub within_isize: bool,
    pub mutability: SliceRawMutability,
}

pub uninterp spec fn slice_raw_domain<T>(
    ptr: *const T,
    len: usize,
    mutability: SliceRawMutability,
) -> SliceRawDomain;

pub uninterp spec fn slice_raw_mut_domain<T>(
    ptr: *mut T,
    len: usize,
    mutability: SliceRawMutability,
) -> SliceRawDomain;

pub open spec fn slice_raw_domain_valid(domain: SliceRawDomain) -> bool {
    0 <= domain.len
        && domain.non_null
        && domain.aligned
        && domain.one_allocation
        && domain.initialized
        && domain.aliasing_ok
        && domain.within_isize
}

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub uninterp spec fn slice_ptr_range_result<T>(seq: Seq<T>, range: core::ops::Range<*const T>) -> bool;

pub uninterp spec fn slice_mut_ptr_range_result<T>(seq: Seq<T>, range: core::ops::Range<*mut T>) -> bool;

pub open spec fn slice_from_raw_parts_result<T>(ptr: *const T, len: usize, ret: &[T]) -> bool {
    ret@.len() == len && slice_start_ptr(ret@, ptr)
}

pub open spec fn slice_from_raw_parts_mut_result<T>(
    ptr: *mut T,
    len: usize,
    ret: &mut [T],
) -> bool {
    ret@.len() == len && slice_start_mut_ptr(ret@, ptr)
}

pub uninterp spec fn slice_align_to_domain<T, U>(source: Seq<T>) -> bool;

pub uninterp spec fn slice_aligned_middle<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool;

pub open spec fn slice_align_to_result<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool {
    prefix.len() <= source.len()
        && suffix.len() <= source.len()
        && prefix == source.subrange(0, prefix.len() as int)
        && suffix == source.subrange((source.len() - suffix.len()) as int, source.len() as int)
        && slice_aligned_middle::<T, U>(source, prefix, middle, suffix)
}

pub open spec fn slice_align_to_mut_result<T, U>(
    old_source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
    final_prefix: Seq<T>,
    final_middle: Seq<U>,
    final_suffix: Seq<T>,
    final_source: Seq<T>,
) -> bool {
    slice_align_to_result::<T, U>(old_source, prefix, middle, suffix)
        && final_source.len() == old_source.len()
        && final_prefix.len() == prefix.len()
        && final_middle.len() == middle.len()
        && final_suffix.len() == suffix.len()
}

pub uninterp spec fn slice_element_offset_result<T>(seq: Seq<T>, element: &T, index: usize) -> bool;

pub uninterp spec fn slice_element_in_domain<T>(seq: Seq<T>, element: &T) -> bool;

pub uninterp spec fn slice_subslice_range_result<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    range: core::range::Range<usize>,
) -> bool;

pub uninterp spec fn slice_subslice_in_domain<T>(seq: Seq<T>, subslice: Seq<T>) -> bool;

pub uninterp spec fn slice_index_in_range<T, I: core::slice::SliceIndex<[T]>>(
    seq: Seq<T>,
    index: I,
) -> bool;

pub uninterp spec fn slice_index_result<T, I: core::slice::SliceIndex<[T]>>(
    seq: Seq<T>,
    index: I,
    output: &<I as core::slice::SliceIndex<[T]>>::Output,
) -> bool;

pub uninterp spec fn slice_index_mut_frame<T, I: core::slice::SliceIndex<[T]>>(
    old_seq: Seq<T>,
    index: I,
    final_seq: Seq<T>,
) -> bool;

pub uninterp spec fn slice_disjoint_indices_valid<T, I: core::slice::SliceIndex<[T]>, const N: usize>(
    seq: Seq<T>,
    indices: [I; N],
) -> bool;

pub ghost struct MaybeUninitSliceRelation<T> {
    pub initialized: Seq<bool>,
    pub values: Seq<T>,
}

pub uninterp spec fn maybe_uninit_seq_relation<T>(
    storage: Seq<core::mem::MaybeUninit<T>>,
) -> MaybeUninitSliceRelation<T>;

pub open spec fn maybe_uninit_relation_well_formed<T>(
    relation: MaybeUninitSliceRelation<T>,
    len: int,
) -> bool {
    0 <= len && relation.initialized.len() == len && relation.values.len() == len
}

pub open spec fn maybe_uninit_all_initialized<T>(
    relation: MaybeUninitSliceRelation<T>,
) -> bool {
    relation.initialized.len() == relation.values.len()
        && forall|i: int| 0 <= i < relation.initialized.len() ==> relation.initialized[i]
}

pub open spec fn maybe_uninit_written_from<T>(
    before: MaybeUninitSliceRelation<T>,
    after: MaybeUninitSliceRelation<T>,
    source: Seq<T>,
) -> bool {
    before.initialized.len() == after.initialized.len()
        && after.values.len() == after.initialized.len()
        && source.len() <= after.values.len()
        && forall|i: int| 0 <= i < source.len()
            ==> after.initialized[i] && after.values[i] == source[i]
}

pub open spec fn maybe_uninit_drop_all<T>(
    before: MaybeUninitSliceRelation<T>,
    after: MaybeUninitSliceRelation<T>,
) -> bool {
    before.initialized.len() == after.initialized.len()
        && after.values.len() == before.values.len()
        && forall|i: int| 0 <= i < after.initialized.len() ==> !after.initialized[i]
}

pub open spec fn ascii_is_uppercase(byte: u8) -> bool {
    0x41 <= (byte as int) && (byte as int) <= 0x5a
}

pub open spec fn ascii_is_lowercase(byte: u8) -> bool {
    0x61 <= (byte as int) && (byte as int) <= 0x7a
}

pub open spec fn ascii_lower_byte(byte: u8) -> u8 {
    if ascii_is_uppercase(byte) {
        ((byte as int) + 0x20) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_upper_byte(byte: u8) -> u8 {
    if ascii_is_lowercase(byte) {
        ((byte as int) - 0x20) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_is_byte(byte: u8) -> bool {
    (byte as int) <= 0x7f
}

pub open spec fn ascii_is_whitespace(byte: u8) -> bool {
    byte == 0x09u8
        || byte == 0x0au8
        || byte == 0x0bu8
        || byte == 0x0cu8
        || byte == 0x0du8
        || byte == 0x20u8
}

pub open spec fn ascii_all(seq: Seq<u8>) -> bool {
    forall|i: int| 0 <= i < seq.len() ==> ascii_is_byte(seq[i])
}

pub open spec fn ascii_lower_seq(seq: Seq<u8>) -> Seq<u8> {
    Seq::new(seq.len(), |i: int| ascii_lower_byte(seq[i]))
}

pub open spec fn ascii_upper_seq(seq: Seq<u8>) -> Seq<u8> {
    Seq::new(seq.len(), |i: int| ascii_upper_byte(seq[i]))
}

pub open spec fn ascii_eq_ignore_case(left: Seq<u8>, right: Seq<u8>) -> bool {
    left.len() == right.len()
        && forall|i: int| 0 <= i < left.len() ==> ascii_lower_byte(left[i]) == ascii_lower_byte(right[i])
}

pub open spec fn ascii_trim_start_boundary(seq: Seq<u8>, i: int) -> bool {
    0 <= i <= seq.len()
        && (forall|j: int| 0 <= j < i ==> #[trigger] ascii_is_whitespace(seq[j]))
        && (i < seq.len() ==> !ascii_is_whitespace(seq[i]))
}

pub open spec fn ascii_trim_end_boundary(seq: Seq<u8>, i: int) -> bool {
    0 <= i <= seq.len()
        && (forall|j: int| i <= j < seq.len() ==> #[trigger] ascii_is_whitespace(seq[j]))
        && (0 < i ==> !ascii_is_whitespace(seq[i - 1]))
}

pub open spec fn ascii_trim_start_index(seq: Seq<u8>) -> int {
    choose|i: int| #[trigger] ascii_trim_start_boundary(seq, i)
}

pub open spec fn ascii_trim_end_index(seq: Seq<u8>) -> int {
    choose|i: int| #[trigger] ascii_trim_end_boundary(seq, i)
}

pub open spec fn ascii_trim_start_result(seq: Seq<u8>, ret: &[u8]) -> bool {
    0 <= ascii_trim_start_index(seq) <= seq.len()
        && ret@ == seq.subrange(ascii_trim_start_index(seq), seq.len() as int)
        && (forall|i: int| 0 <= i < ascii_trim_start_index(seq) ==> ascii_is_whitespace(seq[i]))
        && (ascii_trim_start_index(seq) < seq.len() ==> !ascii_is_whitespace(seq[ascii_trim_start_index(seq)]))
}

pub open spec fn ascii_trim_end_result(seq: Seq<u8>, ret: &[u8]) -> bool {
    0 <= ascii_trim_end_index(seq) <= seq.len()
        && ret@ == seq.subrange(0, ascii_trim_end_index(seq))
        && (forall|i: int| ascii_trim_end_index(seq) <= i < seq.len() ==> ascii_is_whitespace(seq[i]))
        && (0 < ascii_trim_end_index(seq) ==> !ascii_is_whitespace(seq[ascii_trim_end_index(seq) - 1]))
}

pub open spec fn ascii_trim_result(seq: Seq<u8>, ret: &[u8]) -> bool {
    let start = ascii_trim_start_index(seq);
    let end = ascii_trim_end_index(seq);
    0 <= start <= end <= seq.len()
        && ret@ == seq.subrange(start, end)
        && (forall|i: int| 0 <= i < start ==> ascii_is_whitespace(seq[i]))
        && (forall|i: int| end <= i < seq.len() ==> ascii_is_whitespace(seq[i]))
}

pub uninterp spec fn ascii_escape_seq(seq: Seq<u8>) -> Seq<u8>;

} // verus!

verus! {

pub assume_specification<T: core::cmp::Ord>[ <[T]>::binary_search ](
    slice: &[T],
    x: &T,
) -> (result: core::result::Result<usize, usize>)
    ensures
        slice_binary_search_result(slice@, *x, result),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&'a T) -> core::cmp::Ordering>[
    <[T]>::binary_search_by::<F>
](
    slice: &'a [T],
    f: F,
) -> (result: core::result::Result<usize, usize>)
    ensures
        slice_binary_search_by_result(slice@, f, result),
;

pub assume_specification<'a, T, B: core::cmp::Ord, F: core::ops::FnMut(&'a T) -> B>[
    <[T]>::binary_search_by_key::<B, F>
](
    slice: &'a [T],
    key: &B,
    f: F,
) -> (result: core::result::Result<usize, usize>)
    ensures
        slice_binary_search_by_key_result::<F, T, B>(slice@, *key, f, result),
;

pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::contains ](
    slice: &[T],
    x: &T,
) -> (b: bool)
    ensures
        b <==> slice_contains_value(slice@, *x),
;

pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::starts_with ](
    slice: &[T],
    needle: &[T],
) -> (b: bool)
    ensures
        b <==> slice_is_prefix(slice@, needle@),
;

pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::ends_with ](
    slice: &[T],
    needle: &[T],
) -> (b: bool)
    ensures
        b <==> slice_is_suffix(slice@, needle@),
;

pub assume_specification<T, P: core::ops::FnMut(&T) -> bool>[ <[T]>::partition_point::<P> ](
    slice: &[T],
    pred: P,
) -> (index: usize)
    ensures
        slice_partition_point_result(slice@, pred, index),
;

pub assume_specification<T>[ <[T]>::split_at_checked ](
    slice: &[T],
    mid: usize,
) -> (ret: Option<(&[T], &[T])>)
    ensures
        mid <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, mid as int)
            && ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
        mid > slice@.len() ==> ret.is_none(),
;

pub assume_specification<T>[ <[T]>::split_at_unchecked ](
    slice: &[T],
    mid: usize,
) -> (ret: (&[T], &[T]))
    requires
        split_point_in_range(slice@, mid),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
;

pub assume_specification<T>[ <[T]>::split_at_mut_checked ](
    slice: &mut [T],
    mid: usize,
) -> (ret: Option<(&mut [T], &mut [T])>)
    ensures
        mid <= old(slice)@.len() ==> ret.is_some()
            && ret.unwrap().0@ == old(slice)@.subrange(0, mid as int)
            && ret.unwrap().1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            && final(slice)@ == final(ret.unwrap().0)@ + final(ret.unwrap().1)@,
        mid > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T>[ <[T]>::split_at_mut_unchecked ](
    slice: &mut [T],
    mid: usize,
) -> (ret: (&mut [T], &mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
;

pub assume_specification<T>[ <[T]>::split_first ](
    slice: &[T],
) -> (ret: Option<(&T, &[T])>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == slice@[0]
            && ret.unwrap().1@ == slice@.subrange(1, slice@.len() as int),
;

pub assume_specification<T>[ <[T]>::split_last ](
    slice: &[T],
) -> (ret: Option<(&T, &[T])>)
    ensures
        slice@.len() == 0 ==> ret.is_none(),
        slice@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == slice@[(slice@.len() - 1) as int]
            && ret.unwrap().1@ == slice@.subrange(0, (slice@.len() - 1) as int),
;

pub assume_specification<T>[ <[T]>::split_first_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == old(slice)@[0]
            && ret.unwrap().1@ == old(slice)@.subrange(1, old(slice)@.len() as int)
            && final(slice)@ == seq![*final(ret.unwrap().0)] + final(ret.unwrap().1)@,
;

pub assume_specification<T>[ <[T]>::split_last_mut ](
    slice: &mut [T],
) -> (ret: Option<(&mut T, &mut [T])>)
    ensures
        old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@,
        old(slice)@.len() != 0 ==> ret.is_some()
            && *ret.unwrap().0 == old(slice)@[(old(slice)@.len() - 1) as int]
            && ret.unwrap().1@ == old(slice)@.subrange(0, (old(slice)@.len() - 1) as int)
            && final(slice)@ == final(ret.unwrap().1)@ + seq![*final(ret.unwrap().0)],
;

pub assume_specification<T, const N: usize>[ <[T]>::first_chunk::<N> ](
    slice: &[T],
) -> (ret: Option<&[T; N]>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view(ret.unwrap()) == slice_fixed_prefix::<T, N>(slice@),
        (N as int) > slice@.len() ==> ret.is_none(),
;

pub assume_specification<T, const N: usize>[ <[T]>::last_chunk::<N> ](
    slice: &[T],
) -> (ret: Option<&[T; N]>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view(ret.unwrap()) == slice_fixed_suffix::<T, N>(slice@),
        (N as int) > slice@.len() ==> ret.is_none(),
;

pub assume_specification<T, const N: usize>[ <[T]>::first_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && array_mut_ref_view(ret.unwrap()) == slice_fixed_prefix::<T, N>(old(slice)@)
            && final(slice)@
                == array_value_view(*final(ret.unwrap()))
                    + old(slice)@.subrange(N as int, old(slice)@.len() as int),
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::last_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && array_mut_ref_view(ret.unwrap()) == slice_fixed_suffix::<T, N>(old(slice)@)
            && final(slice)@
                == old(slice)@.subrange(0, (old(slice)@.len() - N) as int)
                    + array_value_view(*final(ret.unwrap())),
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::split_first_chunk::<N> ](
    slice: &[T],
) -> (ret: Option<(&[T; N], &[T])>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view(ret.unwrap().0) == slice_fixed_prefix::<T, N>(slice@)
            && ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int),
        (N as int) > slice@.len() ==> ret.is_none(),
;

pub assume_specification<T, const N: usize>[ <[T]>::split_last_chunk::<N> ](
    slice: &[T],
) -> (ret: Option<(&[T], &[T; N])>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, (slice@.len() - N) as int)
            && array_ref_view(ret.unwrap().1) == slice_fixed_suffix::<T, N>(slice@),
        (N as int) > slice@.len() ==> ret.is_none(),
;

pub assume_specification<T, const N: usize>[ <[T]>::split_first_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<(&mut [T; N], &mut [T])>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && array_mut_ref_view(ret.unwrap().0) == slice_fixed_prefix::<T, N>(old(slice)@)
            && ret.unwrap().1@ == old(slice)@.subrange(N as int, old(slice)@.len() as int)
            && final(slice)@
                == array_value_view(*final(ret.unwrap().0)) + final(ret.unwrap().1)@,
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::split_last_chunk_mut::<N> ](
    slice: &mut [T],
) -> (ret: Option<(&mut [T], &mut [T; N])>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && ret.unwrap().0@ == old(slice)@.subrange(0, (old(slice)@.len() - N) as int)
            && array_mut_ref_view(ret.unwrap().1) == slice_fixed_suffix::<T, N>(old(slice)@)
            && final(slice)@
                == final(ret.unwrap().0)@ + array_value_view(*final(ret.unwrap().1)),
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::as_array::<N> ](
    slice: &[T],
) -> (ret: Option<&[T; N]>)
    ensures
        slice@.len() == N ==> ret.is_some()
            && array_ref_view(ret.unwrap()) == slice@,
        slice@.len() != N ==> ret.is_none(),
;

pub assume_specification<T, const N: usize>[ <[T]>::as_mut_array::<N> ](
    slice: &mut [T],
) -> (ret: Option<&mut [T; N]>)
    ensures
        old(slice)@.len() == N ==> ret.is_some()
            && array_mut_ref_view(ret.unwrap()) == old(slice)@
            && final(slice)@ == array_value_view(*final(ret.unwrap())),
        old(slice)@.len() != N ==> ret.is_none() && final(slice)@ == old(slice)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks::<N> ](
    slice: &[T],
) -> (ret: (&[[T; N]], &[T]))
    requires
        N != 0,
    ensures
        slice_array_chunks_partition::<T, N>(slice@, ret.0@, ret.1@),
;

pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks::<N> ](
    slice: &[T],
) -> (ret: (&[T], &[[T; N]]))
    requires
        N != 0,
    ensures
        slice_array_rchunks_partition::<T, N>(slice@, ret.0@, ret.1@),
;

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_unchecked::<N> ](
    slice: &[T],
) -> (ret: &[[T; N]])
    requires
        N != 0,
        slice@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == slice@,
;

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_mut::<N> ](
    slice: &mut [T],
) -> (ret: (&mut [[T; N]], &mut [T]))
    requires
        N != 0,
    ensures
        slice_array_chunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@),
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret.0)@) + final(ret.1)@,
;

pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks_mut::<N> ](
    slice: &mut [T],
) -> (ret: (&mut [T], &mut [[T; N]]))
    requires
        N != 0,
    ensures
        slice_array_rchunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@),
        final(slice)@ == final(ret.0)@ + flatten_array_chunks::<T, N>(final(ret.1)@),
;

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_unchecked_mut::<N> ](
    slice: &mut [T],
) -> (ret: &mut [[T; N]])
    requires
        N != 0,
        old(slice)@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
;

pub assume_specification<'a, T>[ <[T]>::iter_mut ](
    slice: &'a mut [T],
) -> (iter: core::slice::IterMut<'a, T>)
    ensures
        slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining == old(slice)@,
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T>[ <[T]>::chunks ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::Chunks<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::chunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter)),
;

pub assume_specification<'a, T>[ <[T]>::rchunks ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunks<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ <[T]>::rchunks_exact ](
    slice: &'a [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksExact<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter)),
;

pub assume_specification<'a, T>[ <[T]>::windows ](
    slice: &'a [T],
    size: usize,
) -> (iter: core::slice::Windows<'a, T>)
    requires
        size != 0,
    ensures
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).chunk_size == size as int,
        !slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).reverse,
;

pub assume_specification<'a, T, const N: usize>[ <[T]>::array_windows::<N> ](
    slice: &'a [T],
) -> (iter: core::slice::ArrayWindows<'a, T, N>)
    requires
        N != 0,
    ensures
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).source == slice@,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remaining == slice@,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).chunk_size == N as int,
        !slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).reverse,
;

pub assume_specification<'a, T>[ core::slice::ChunksExact::<'a, T>::remainder ](
    iter: &core::slice::ChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::ChunksExactMut::<'a, T>::into_remainder ](
    iter: core::slice::ChunksExactMut<'a, T>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::Iter::<'a, T>::as_slice ](
    iter: &core::slice::Iter<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::Iter<'a, T>, T>(iter).remaining,
;

pub assume_specification<'a, 'b, T>[ core::slice::IterMut::<'a, T>::as_slice ](
    iter: &'b core::slice::IterMut<'a, T>,
) -> (ret: &'b [T])
    ensures
        ret@ == slice_iterator_view::<&'b core::slice::IterMut<'a, T>, T>(iter).remaining,
;

pub assume_specification<'a, T>[ core::slice::IterMut::<'a, T>::into_slice ](
    iter: core::slice::IterMut<'a, T>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining,
;

pub assume_specification<'a, T>[ core::slice::RChunksExact::<'a, T>::remainder ](
    iter: &core::slice::RChunksExact<'a, T>,
) -> (ret: &'a [T])
    ensures
        ret@ == slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ core::slice::RChunksExactMut::<'a, T>::into_remainder ](
    iter: core::slice::RChunksExactMut<'a, T>,
) -> (ret: &'a mut [T])
    ensures
        ret@ == slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).remainder,
        ret@.len() < slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size,
;

pub assume_specification<'a, T>[ <[T]>::chunks_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remaining == old(slice)@,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).reverse,
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T>[ <[T]>::chunks_exact_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::ChunksExactMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        !slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter)),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T>[ <[T]>::rchunks_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remaining == old(slice)@,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remainder.len() == 0,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).reverse,
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T>[ <[T]>::rchunks_exact_mut ](
    slice: &'a mut [T],
    chunk_size: usize,
) -> (iter: core::slice::RChunksExactMut<'a, T>)
    requires
        chunk_size != 0,
    ensures
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).source == old(slice)@,
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).yielded_prefix.len() == 0,
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int,
        slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).reverse,
        slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter)),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::Split<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::Split<'a, T, F>, F, T>(
            iter, slice@, pred, false, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::SplitMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, false, 0,
        ),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_inclusive::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::SplitInclusive<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitInclusive<'a, T, F>, F, T>(
            iter, slice@, pred, true, false, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[
    <[T]>::split_inclusive_mut::<F>
](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::SplitInclusiveMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitInclusiveMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, true, false, 0,
        ),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn::<F> ](
    slice: &'a [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::SplitN<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitN<'a, T, F>, F, T>(
            iter, slice@, pred, false, false, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn_mut::<F> ](
    slice: &'a mut [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::SplitNMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::SplitNMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, false, n as int,
        ),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::RSplit<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplit<'a, T, F>, F, T>(
            iter, slice@, pred, false, true, 0,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::RSplitMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, true, 0,
        ),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn::<F> ](
    slice: &'a [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::RSplitN<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitN<'a, T, F>, F, T>(
            iter, slice@, pred, false, true, n as int,
        ),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn_mut::<F> ](
    slice: &'a mut [T],
    n: usize,
    pred: F,
) -> (iter: core::slice::RSplitNMut<'a, T, F>)
    ensures
        slice_predicate_split_view::<core::slice::RSplitNMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred, false, true, n as int,
        ),
        final(slice)@ == old(slice)@,
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by::<F> ](
    slice: &'a [T],
    pred: F,
) -> (iter: core::slice::ChunkBy<'a, T, F>)
    ensures
        slice_adjacent_chunk_view::<core::slice::ChunkBy<'a, T, F>, F, T>(iter, slice@, pred),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by_mut::<F> ](
    slice: &'a mut [T],
    pred: F,
) -> (iter: core::slice::ChunkByMut<'a, T, F>)
    ensures
        slice_adjacent_chunk_view::<core::slice::ChunkByMut<'a, T, F>, F, T>(
            iter, old(slice)@, pred,
        ),
        final(slice)@ == old(slice)@,
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[ <[T]>::split_off::<R> ](
    slice_ref: &mut &'a [T],
    range: R,
) -> (ret: Option<&'a [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@,
        ),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[
    <[T]>::split_off_mut::<R>
](
    slice_ref: &mut &'a mut [T],
    range: R,
) -> (ret: Option<&'a mut [T]>)
    ensures
        ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@,
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@,
        ),
        ret.is_some() ==> slice_split_off_partition::<T>(
            (*old(slice_ref))@, (*final(slice_ref))@, final(ret.unwrap())@,
        ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_first_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            )
            && (seq![*final(ret.unwrap())] + (*final(slice_ref))@).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last ](
    slice_ref: &mut &'a [T],
) -> (ret: Option<&'a T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            ),
;

pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ](
    slice_ref: &mut &'a mut [T],
) -> (ret: Option<&'a mut T>)
    ensures
        (*old(slice_ref))@.len() == 0 ==> ret.is_none()
            && (*final(slice_ref))@ == (*old(slice_ref))@,
        (*old(slice_ref))@.len() != 0 ==> ret.is_some()
            && slice_split_off_last_result::<T>(
                (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(),
            )
            && ((*final(slice_ref))@ + seq![*final(ret.unwrap())]).len()
                == (*old(slice_ref))@.len(),
;

pub assume_specification<'a>[ <[u8]>::utf8_chunks ](
    slice: &'a [u8],
) -> (iter: core::str::Utf8Chunks<'a>)
    ensures
        utf8_chunk_partition::<core::str::Utf8Chunks<'a>>(iter, slice@),
;

pub assume_specification<T: core::clone::Clone>[ <[T]>::clone_from_slice ](
    dst: &mut [T],
    src: &[T],
)
    requires
        old(dst)@.len() == src@.len(),
    ensures
        slice_cloned_from(src@, final(dst)@),
;

pub assume_specification<T: core::clone::Clone>[ <[T]>::fill ](
    slice: &mut [T],
    value: T,
)
    ensures
        slice_filled_with_clone(old(slice)@, value, final(slice)@),
;

pub assume_specification<T, F: core::ops::FnMut() -> T>[ <[T]>::fill_with::<F> ](
    slice: &mut [T],
    f: F,
)
    ensures
        final(slice)@ == zero_arg_fnmut_outputs(f, old(slice)@.len()),
        zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len()).len() == old(slice)@.len(),
;

pub assume_specification<T>[ <[T]>::reverse ](
    slice: &mut [T],
)
    ensures
        final(slice)@ == slice_reversed(old(slice)@),
;

pub assume_specification<T>[ <[T]>::rotate_left ](
    slice: &mut [T],
    mid: usize,
)
    requires
        mid <= old(slice)@.len(),
    ensures
        final(slice)@ == slice_rotated_left(old(slice)@, mid as int),
;

pub assume_specification<T>[ <[T]>::rotate_right ](
    slice: &mut [T],
    k: usize,
)
    requires
        k <= old(slice)@.len(),
    ensures
        final(slice)@ == slice_rotated_right(old(slice)@, k as int),
;

pub assume_specification<T>[ <[T]>::swap ](
    slice: &mut [T],
    a: usize,
    b: usize,
)
    requires
        a < old(slice)@.len(),
        b < old(slice)@.len(),
    ensures
        final(slice)@ == slice_swapped(old(slice)@, a as int, b as int),
;

pub assume_specification<T>[ <[T]>::swap_with_slice ](
    slice: &mut [T],
    other: &mut [T],
)
    requires
        old(slice)@.len() == old(other)@.len(),
    ensures
        final(slice)@ == old(other)@,
        final(other)@ == old(slice)@,
;

pub assume_specification<T, U>[ <[T]>::align_to::<U> ](
    slice: &[T],
) -> (ret: (&[T], &[U], &[T]))
    requires
        slice_align_to_domain::<T, U>(slice@),
    ensures
        slice_align_to_result::<T, U>(slice@, ret.0@, ret.1@, ret.2@),
;

pub assume_specification<T, U>[ <[T]>::align_to_mut::<U> ](
    slice: &mut [T],
) -> (ret: (&mut [T], &mut [U], &mut [T]))
    requires
        slice_align_to_domain::<T, U>(old(slice)@),
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
;

pub assume_specification<T, const N: usize>[ <[[T; N]]>::as_flattened ](
    slice: &[[T; N]],
) -> (ret: &[T])
    ensures
        ret@ == flatten_array_chunks::<T, N>(slice@),
;

pub assume_specification<T, const N: usize>[ <[[T; N]]>::as_flattened_mut ](
    slice: &mut [[T; N]],
) -> (ret: &mut [T])
    ensures
        ret@ == flatten_array_chunks::<T, N>(old(slice)@),
        flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@,
;

pub assume_specification<T>[ <[T]>::as_mut_ptr ](
    slice: &mut [T],
) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
;

pub assume_specification<T>[ <[T]>::as_mut_ptr_range ](
    slice: &mut [T],
) -> (range: core::ops::Range<*mut T>)
    ensures
        slice_mut_ptr_range_result(old(slice)@, range),
        final(slice)@ == old(slice)@,
;

pub assume_specification<T>[ <[T]>::as_ptr ](
    slice: &[T],
) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
;

pub assume_specification<T>[ <[T]>::as_ptr_range ](
    slice: &[T],
) -> (range: core::ops::Range<*const T>)
    ensures
        slice_ptr_range_result(slice@, range),
;

pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_drop ](
    slice: &mut [core::mem::MaybeUninit<T>],
)
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)),
    ensures
        maybe_uninit_drop_all(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
        ),
;

pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_mut ](
    slice: &mut [core::mem::MaybeUninit<T>],
) -> (ret: &mut [T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)),
    ensures
        ret@ == maybe_uninit_seq_relation(old(slice)@).values,
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
;

pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_ref ](
    slice: &[core::mem::MaybeUninit<T>],
) -> (ret: &[T])
    requires
        maybe_uninit_all_initialized(maybe_uninit_seq_relation(slice@)),
    ensures
        ret@ == maybe_uninit_seq_relation(slice@).values,
;

pub assume_specification<T>[ <[T]>::element_offset ](
    slice: &[T],
    element: &T,
) -> (ret: Option<usize>)
    ensures
        ret.is_some() ==> ret.unwrap() < slice@.len()
            && slice_element_offset_result(slice@, element, ret.unwrap()),
        ret.is_none() ==> !slice_element_in_domain(slice@, element),
;

pub assume_specification[ <[u8]>::eq_ignore_ascii_case ](
    slice: &[u8],
    other: &[u8],
) -> (ret: bool)
    ensures
        ret <==> ascii_eq_ignore_case(slice@, other@),
;

pub assume_specification<'a>[ <[u8]>::escape_ascii ](
    slice: &'a [u8],
) -> (iter: core::slice::EscapeAscii<'a>)
    ensures
        slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).source == slice@,
        slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).remaining
            == ascii_escape_seq(slice@),
;

pub assume_specification<'a, T>[ core::slice::from_mut::<T> ](
    value: &'a mut T,
) -> (ret: &'a mut [T])
    ensures
        ret@ == seq![*old(value)],
        final(ret)@ == seq![*final(value)],
;

pub assume_specification<'a, T>[ core::slice::from_raw_parts::<T> ](
    data: *const T,
    len: usize,
) -> (ret: &'a [T])
    requires
        slice_raw_domain_valid(slice_raw_domain(data, len, SliceRawMutability::Immutable)),
    ensures
        slice_from_raw_parts_result(data, len, ret),
;

pub assume_specification<'a, T>[ core::slice::from_raw_parts_mut::<T> ](
    data: *mut T,
    len: usize,
) -> (ret: &'a mut [T])
    requires
        slice_raw_domain_valid(slice_raw_mut_domain(data, len, SliceRawMutability::Mutable)),
    ensures
        slice_from_raw_parts_mut_result(data, len, ret),
;

pub assume_specification<'a, T>[ core::slice::from_ref::<T> ](
    value: &'a T,
) -> (ret: &'a [T])
    ensures
        ret@ == seq![*value],
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I, const N: usize>[ <[T]>::get_disjoint_mut::<I, N> ](
    slice: &mut [T],
    indices: [I; N],
) -> (ret: core::result::Result<
    [&mut <I as core::slice::SliceIndex<[T]>>::Output; N],
    core::slice::GetDisjointMutError,
>) where I: core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]>
    ensures
        ret.is_ok() ==> slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices)
            && final(slice)@.len() == old(slice)@.len(),
        ret.is_err() ==> !slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices)
            && final(slice)@ == old(slice)@,
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I, const N: usize>[ <[T]>::get_disjoint_unchecked_mut::<I, N> ](
    slice: &mut [T],
    indices: [I; N],
) -> (ret: [&mut <I as core::slice::SliceIndex<[T]>>::Output; N])
    where I: core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]>
    requires
        slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices),
    ensures
        final(slice)@.len() == old(slice)@.len(),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I>[ <[T]>::get_mut::<I> ](
    slice: &mut [T],
    index: I,
) -> (ret: Option<&mut <I as core::slice::SliceIndex<[T]>>::Output>)
    where I: core::slice::SliceIndex<[T]>
    ensures
        ret.is_some() ==> slice_index_in_range(old(slice)@, index)
            && slice_index_mut_frame(old(slice)@, index, final(slice)@),
        ret.is_none() ==> !slice_index_in_range(old(slice)@, index)
            && final(slice)@ == old(slice)@,
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I>[ <[T]>::get_unchecked::<I> ](
    slice: &[T],
    index: I,
) -> (ret: &<I as core::slice::SliceIndex<[T]>>::Output)
    where I: core::slice::SliceIndex<[T]>
    requires
        slice_index_in_range(slice@, index),
    ensures
        slice_index_result(slice@, index, ret),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<T, I>[ <[T]>::get_unchecked_mut::<I> ](
    slice: &mut [T],
    index: I,
) -> (ret: &mut <I as core::slice::SliceIndex<[T]>>::Output)
    where I: core::slice::SliceIndex<[T]>
    requires
        slice_index_in_range(old(slice)@, index),
    ensures
        slice_index_mut_frame(old(slice)@, index, final(slice)@),
;

pub assume_specification[ <[u8]>::is_ascii ](
    slice: &[u8],
) -> (ret: bool)
    ensures
        ret <==> ascii_all(slice@),
;

pub assume_specification<T: core::cmp::PartialOrd>[ <[T]>::is_sorted ](
    slice: &[T],
) -> (ret: bool)
    ensures
        ret <==> slice_sorted_by_partial_ord(slice@),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&'a T, &'a T) -> bool>[
    <[T]>::is_sorted_by::<F>
](
    slice: &'a [T],
    compare: F,
) -> (ret: bool)
    ensures
        slice_sorted_by_bool_compare_result(slice@, compare, ret),
;

pub assume_specification<'a, T, F: core::ops::FnMut(&'a T) -> K, K: core::cmp::PartialOrd>[
    <[T]>::is_sorted_by_key::<F, K>
](
    slice: &'a [T],
    f: F,
) -> (ret: bool)
    ensures
        slice_sorted_by_partial_key_result::<F, T, K>(slice@, f, ret),
;

pub assume_specification[ <[u8]>::make_ascii_lowercase ](
    slice: &mut [u8],
)
    ensures
        final(slice)@ == ascii_lower_seq(old(slice)@),
;

pub assume_specification[ <[u8]>::make_ascii_uppercase ](
    slice: &mut [u8],
)
    ensures
        final(slice)@ == ascii_upper_seq(old(slice)@),
;

pub assume_specification<T: core::cmp::Ord>[ <[T]>::select_nth_unstable ](
    slice: &mut [T],
    index: usize,
) -> (ret: (&mut [T], &mut T, &mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_ord(final(ret.0)@, *final(ret.1), final(ret.2)@),
;

pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> core::cmp::Ordering>[
    <[T]>::select_nth_unstable_by::<F>
](
    slice: &mut [T],
    index: usize,
    compare: F,
) -> (ret: (&mut [T], &mut T, &mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_cmp(
            final(ret.0)@,
            *final(ret.1),
            final(ret.2)@,
            comparator_observation(compare, old(slice)@),
        ),
;

pub assume_specification<T, K: core::cmp::Ord, F: core::ops::FnMut(&T) -> K>[
    <[T]>::select_nth_unstable_by_key::<K, F>
](
    slice: &mut [T],
    index: usize,
    f: F,
) -> (ret: (&mut [T], &mut T, &mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_key::<F, T, K>(final(ret.0)@, *final(ret.1), final(ret.2)@, f),
;

pub assume_specification<T: core::cmp::Ord>[ <[T]>::sort_unstable ](
    slice: &mut [T],
)
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_ord(final(slice)@),
;

pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> core::cmp::Ordering>[
    <[T]>::sort_unstable_by::<F>
](
    slice: &mut [T],
    compare: F,
)
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_cmp(final(slice)@, comparator_observation(compare, old(slice)@)),
;

pub assume_specification<T, K: core::cmp::Ord, F: core::ops::FnMut(&T) -> K>[
    <[T]>::sort_unstable_by_key::<K, F>
](
    slice: &mut [T],
    f: F,
)
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_key::<F, T, K>(final(slice)@, f),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<
    'a,
    'p,
    T: core::cmp::PartialEq,
    P: core::slice::SlicePattern<Item = T> + ?Sized,
>[
    <[T]>::strip_prefix::<P>
](
    slice: &'a [T],
    prefix: &'p P,
) -> (ret: Option<&'a [T]>)
    ensures
        slice_strip_prefix_result(slice@, slice_pattern_view::<P, T>(prefix), ret),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<
    'a,
    'p,
    T: core::cmp::PartialEq,
    P: core::slice::SlicePattern<Item = T> + ?Sized,
>[
    <[T]>::strip_suffix::<P>
](
    slice: &'a [T],
    suffix: &'p P,
) -> (ret: Option<&'a [T]>)
    ensures
        slice_strip_suffix_result(slice@, slice_pattern_view::<P, T>(suffix), ret),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<
    'a,
    'p,
    's,
    T: core::cmp::PartialEq,
    S: core::slice::SlicePattern<Item = T> + ?Sized,
    P: core::slice::SlicePattern<Item = T> + ?Sized,
>[ <[T]>::strip_circumfix::<S, P> ](
    slice: &'a [T],
    prefix: &'p P,
    suffix: &'s S,
) -> (ret: Option<&'a [T]>)
    ensures
        slice_strip_circumfix_result(
            slice@,
            slice_pattern_view::<P, T>(prefix),
            slice_pattern_view::<S, T>(suffix),
            ret,
        ),
;

pub assume_specification<T>[ <[T]>::subslice_range ](
    slice: &[T],
    subslice: &[T],
) -> (ret: Option<core::range::Range<usize>>)
    ensures
        ret.is_some() ==> slice_subslice_range_result(slice@, subslice@, ret.unwrap()),
        ret.is_none() ==> !slice_subslice_in_domain(slice@, subslice@),
;

pub assume_specification[ <[u8]>::trim_ascii ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_result(slice@, ret),
;

pub assume_specification[ <[u8]>::trim_ascii_end ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_end_result(slice@, ret),
;

pub assume_specification[ <[u8]>::trim_ascii_start ](
    slice: &[u8],
) -> (ret: &[u8])
    ensures
        ascii_trim_start_result(slice@, ret),
;

pub assume_specification<'a, 'b, T: core::clone::Clone>[
    <[core::mem::MaybeUninit<T>]>::write_clone_of_slice
](
    slice: &'a mut [core::mem::MaybeUninit<T>],
    src: &'b [T],
) -> (ret: &'a mut [T])
    requires
        old(slice)@.len() == src@.len(),
    ensures
        ret@ == src@,
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
            src@,
        ),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
;

pub assume_specification<'a, 'b, T: core::marker::Copy>[
    <[core::mem::MaybeUninit<T>]>::write_copy_of_slice
](
    slice: &'a mut [core::mem::MaybeUninit<T>],
    src: &'b [T],
) -> (ret: &'a mut [T])
    requires
        old(slice)@.len() == src@.len(),
    ensures
        ret@ == src@,
        maybe_uninit_written_from(
            maybe_uninit_seq_relation(old(slice)@),
            maybe_uninit_seq_relation(final(slice)@),
            src@,
        ),
        maybe_uninit_seq_relation(final(slice)@).values == final(ret)@,
;

} // verus!

// BEGIN SLICE_SPEC target=core::slice::ChunksExact::remainder
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:1876
// signature: pub fn remainder(&self) -> &'a [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the shared exact chunk iterator remainder and has length below the iterator chunk size
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExact__remainder/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExact__remainder/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExact__remainder/det_harness.rs
// target_binding_result: target core::slice::ChunksExact::remainder bound from inventory declaration core:33656 at core/src/slice/iter.rs:1876
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::ChunksExact::<'a, T>::remainder ]( iter: &core::slice::ChunksExact<'a, T>, ) -> (ret: &'a [T]) ensures ret@ == slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).remainder, ret@.len() < slice_iterator_view::<&core::slice::ChunksExact<'a, T>, T>(iter).chunk_size, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::ChunksExactMut::into_remainder
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:2039
// signature: pub fn into_remainder(self) -> &'a mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the shared mutable exact chunk iterator remainder and has length below the iterator chunk size
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExactMut__into_remainder/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExactMut__into_remainder/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ChunksExactMut__into_remainder/det_harness.rs
// target_binding_result: target core::slice::ChunksExactMut::into_remainder bound from inventory declaration core:33672 at core/src/slice/iter.rs:2039
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::ChunksExactMut::<'a, T>::into_remainder ]( iter: core::slice::ChunksExactMut<'a, T>, ) -> (ret: &'a mut [T]) ensures ret@ == slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).remainder, ret@.len() < slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::Iter::as_slice
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:135
// signature: pub fn as_slice(&self) -> &'a [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the immutable iterator remaining sequence in the shared iterator view
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__Iter__as_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__Iter__as_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__Iter__as_slice/det_harness.rs
// target_binding_result: target core::slice::Iter::as_slice bound from inventory declaration core:33478 at core/src/slice/iter.rs:135
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::Iter::<'a, T>::as_slice ]( iter: &core::slice::Iter<'a, T>, ) -> (ret: &'a [T]) ensures ret@ == slice_iterator_view::<&core::slice::Iter<'a, T>, T>(iter).remaining, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::IterMut::as_slice
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:311
// signature: pub fn as_slice(&self) -> &[T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the mutable iterator remaining sequence in the shared iterator view
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__as_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__as_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__as_slice/det_harness.rs
// target_binding_result: target core::slice::IterMut::as_slice bound from inventory declaration core:33494 at core/src/slice/iter.rs:311
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, 'b, T>[ core::slice::IterMut::<'a, T>::as_slice ]( iter: &'b core::slice::IterMut<'a, T>, ) -> (ret: &'b [T]) ensures ret@ == slice_iterator_view::<&'b core::slice::IterMut<'a, T>, T>(iter).remaining, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::IterMut::into_slice
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:274
// signature: pub fn into_slice(self) -> &'a mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the mutable iterator remaining sequence in the shared iterator view
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__into_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__into_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__IterMut__into_slice/det_harness.rs
// target_binding_result: target core::slice::IterMut::into_slice bound from inventory declaration core:33493 at core/src/slice/iter.rs:274
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::IterMut::<'a, T>::into_slice ]( iter: core::slice::IterMut<'a, T>, ) -> (ret: &'a mut [T]) ensures ret@ == slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::RChunksExact::remainder
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:2686
// signature: pub const fn remainder(&self) -> &'a [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the shared reverse exact chunk iterator remainder and has length below the iterator chunk size
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExact__remainder/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExact__remainder/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExact__remainder/det_harness.rs
// target_binding_result: target core::slice::RChunksExact::remainder bound from inventory declaration core:33721 at core/src/slice/iter.rs:2686
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::RChunksExact::<'a, T>::remainder ]( iter: &core::slice::RChunksExact<'a, T>, ) -> (ret: &'a [T]) ensures ret@ == slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).remainder, ret@.len() < slice_iterator_view::<&core::slice::RChunksExact<'a, T>, T>(iter).chunk_size, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::RChunksExactMut::into_remainder
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/iter.rs:2855
// signature: pub const fn into_remainder(self) -> &'a mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: ret@ equals the shared mutable reverse exact chunk iterator remainder and has length below the iterator chunk size
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExactMut__into_remainder/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExactMut__into_remainder/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__RChunksExactMut__into_remainder/det_harness.rs
// target_binding_result: target core::slice::RChunksExactMut::into_remainder bound from inventory declaration core:33736 at core/src/slice/iter.rs:2855
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ core::slice::RChunksExactMut::<'a, T>::into_remainder ]( iter: core::slice::RChunksExactMut<'a, T>, ) -> (ret: &'a mut [T]) ensures ret@ == slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).remainder, ret@.len() < slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::align_to
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:4506
// signature: pub unsafe fn align_to<U>(&self) -> (&[T], &[U], &[T])
// requires: documented align_to transmute domain holds for T/U validity and alignment; returned middle region is within the original allocation
// ensures: ret.0@ + reinterpret_as_U_seq(ret.1@) + ret.2@ covers the same byte range as old(self)@; ret.1 pointer is aligned for U and ret.0/ret.2 are the maximal T-prefix/suffix outside that aligned middle region
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to/det_harness.rs
// target_binding_result: target core::slice::align_to bound from inventory declaration core:61130 at core/src/slice/mod.rs:4506
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <U>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, U>[ <[T]>::align_to::<U> ]( slice: &[T], ) -> (ret: (&[T], &[U], &[T])) requires slice_align_to_domain::<T, U>(slice@), ensures slice_align_to_result::<T, U>(slice@, ret.0@, ret.1@, ret.2@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::align_to_mut
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:4571
// signature: pub unsafe fn align_to_mut<U>(&mut self) -> (&mut [T], &mut [U], &mut [T])
// requires: documented align_to transmute domain holds for T/U validity and alignment; returned middle region is within the original allocation
// ensures: ret.0@ + reinterpret_as_U_seq(ret.1@) + ret.2@ covers the same byte range as old(self)@; ret.1 pointer is aligned for U and ret.0/ret.2 are the maximal T-prefix/suffix outside that aligned middle region; final(self) byte sequence is final(ret.0) + final(ret.1 reinterpreted as T bytes) + final(ret.2) with no bytes outside the slice changed
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__align_to_mut/det_harness.rs
// target_binding_result: target core::slice::align_to_mut bound from inventory declaration core:61131 at core/src/slice/mod.rs:4571
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <U>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, U>[ <[T]>::align_to_mut::<U> ]( slice: &mut [T], ) -> (ret: (&mut [T], &mut [U], &mut [T])) requires slice_align_to_domain::<T, U>(old(slice)@), ensures slice_align_to_mut_result::<T, U>( old(slice)@, ret.0@, ret.1@, ret.2@, final(ret.0)@, final(ret.1)@, final(ret.2)@, final(slice)@, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::array_windows
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1649
// signature: pub const fn array_windows<const N: usize>(&self) -> ArrayWindows<'_, T, N>
// requires: N != 0
// ensures: slice_iterator_view(result) records self@ as source/remaining, empty yielded_prefix and remainder, N as window size, and forward overlapping-window state
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__array_windows/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__array_windows/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__array_windows/det_harness.rs
// target_binding_result: target core::slice::array_windows bound from inventory declaration core:33684 at core/src/slice/mod.rs:1649
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T, const N: usize>[ <[T]>::array_windows::<N> ]( slice: &'a [T], ) -> (iter: core::slice::ArrayWindows<'a, T, N>) requires N != 0, ensures slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).source == slice@, slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remaining == slice@, slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).chunk_size == N as int, !slice_iterator_view::<core::slice::ArrayWindows<'a, T, N>, T>(iter).reverse, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_array
// status: generated-new-real-relation-spec
// family: views-and-fixed-subranges
// source: core/src/slice/mod.rs:853
// signature: pub const fn as_array<const N: usize>(&self) -> Option<&[T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() == N; when Some(a), array_view(a) == old(self)@ and array length is N; when mutable Some(a), final(self)@ == array_view(final(a)); when None, final(self)@ == old(self)@
// shared_helpers: Seq fixed-size array/chunk/subrange view helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_array/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_array/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_array/det_harness.rs
// target_binding_result: target core::slice::as_array bound from inventory declaration core:61076 at core/src/slice/mod.rs:853
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_array::<N> ]( slice: &[T], ) -> (ret: Option<&[T; N]>) ensures slice@.len() == N ==> ret.is_some() && array_ref_view(ret.unwrap()) == slice@, slice@.len() != N ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_chunks
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1399
// signature: pub const fn as_chunks<const N: usize>(&self) -> (&[[T; N]], &[T])
// requires: N != 0
// ensures: returned chunks then remainder partition old(self)@ exactly; chunks@.len() == old(self)@.len() / N and remainder@.len() == old(self)@.len() % N; flatten_array_chunks(chunks@, N) + remainder@, in source order, equals old(self)@
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks/det_harness.rs
// target_binding_result: target core::slice::as_chunks bound from inventory declaration core:61081 at core/src/slice/mod.rs:1399
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_chunks::<N> ]( slice: &[T], ) -> (ret: (&[[T; N]], &[T])) requires N != 0, ensures slice_array_chunks_partition::<T, N>(slice@, ret.0@, ret.1@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_chunks_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1555
// signature: pub const fn as_chunks_mut<const N: usize>(&mut self) -> (&mut [[T; N]], &mut [T])
// requires: N != 0
// ensures: returned chunks then remainder partition old(self)@ exactly; chunks@.len() == old(self)@.len() / N and remainder@.len() == old(self)@.len() % N; flatten_array_chunks(chunks@, N) + remainder@, in source order, equals old(self)@; final(self)@ is final mutable chunks flattened with final remainder, preserving source order and full frame
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_mut/det_harness.rs
// target_binding_result: target core::slice::as_chunks_mut bound from inventory declaration core:61082 at core/src/slice/mod.rs:1555
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_mut::<N> ]( slice: &mut [T], ) -> (ret: (&mut [[T; N]], &mut [T])) requires N != 0, ensures slice_array_chunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@), final(slice)@ == flatten_array_chunks::<T, N>(final(ret.0)@) + final(ret.1)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_chunks_unchecked
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1341
// signature: pub const unsafe fn as_chunks_unchecked<const N: usize>(&self) -> &[[T; N]]
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes; N != 0 && old(self)@.len() % N == 0
// ensures: flatten_array_chunks(result@, N) == old(self)@; result@.len() == old(self)@.len() / N
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked/det_harness.rs
// target_binding_result: target core::slice::as_chunks_unchecked bound from inventory declaration core:61085 at core/src/slice/mod.rs:1341
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_unchecked::<N> ]( slice: &[T], ) -> (ret: &[[T; N]]) requires N != 0, slice@.len() % (N as nat) == 0, ensures flatten_array_chunks::<T, N>(ret@) == slice@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_chunks_unchecked_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1501
// signature: pub const unsafe fn as_chunks_unchecked_mut<const N: usize>(&mut self) -> &mut [[T; N]]
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes; N != 0 && old(self)@.len() % N == 0
// ensures: flatten_array_chunks(result@, N) == old(self)@; result@.len() == old(self)@.len() / N; final(self)@ == flatten_array_chunks(final(result)@, N)
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_chunks_unchecked_mut/det_harness.rs
// target_binding_result: target core::slice::as_chunks_unchecked_mut bound from inventory declaration core:61088 at core/src/slice/mod.rs:1501
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_unchecked_mut::<N> ]( slice: &mut [T], ) -> (ret: &mut [[T; N]]) requires N != 0, old(slice)@.len() % (N as nat) == 0, ensures flatten_array_chunks::<T, N>(ret@) == old(slice)@, final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_flattened
// status: generated-new-real-relation-spec
// family: views-and-fixed-subranges
// source: core/src/slice/mod.rs:5451
// signature: pub const fn as_flattened(&self) -> &[T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@ == flatten_array_chunks(old(self)@, array_width_of_self); result@.len() == old(self)@.len() * array_width_of_self
// shared_helpers: Seq fixed-size array/chunk/subrange view helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened/det_harness.rs
// target_binding_result: target core::slice::as_flattened bound from inventory declaration core:61083 at core/src/slice/mod.rs:5451
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[[T; N]]>::as_flattened ]( slice: &[[T; N]], ) -> (ret: &[T]) ensures ret@ == flatten_array_chunks::<T, N>(slice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_flattened_mut
// status: generated-new-real-relation-spec
// family: views-and-fixed-subranges
// source: core/src/slice/mod.rs:5493
// signature: pub const fn as_flattened_mut(&mut self) -> &mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@ == flatten_array_chunks(old(self)@, array_width_of_self); result@.len() == old(self)@.len() * array_width_of_self; flatten_array_chunks(final(self)@, array_width_of_self) == final(result)@
// shared_helpers: Seq fixed-size array/chunk/subrange view helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=mutable-reference-view-boundary; unknown_review_reason=contract fixes the Seq view and old/final frame, but mutable reference identity and alias/lifetime state are not uniquely determined by that view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_flattened_mut/det_harness.rs
// target_binding_result: target core::slice::as_flattened_mut bound from inventory declaration core:61086 at core/src/slice/mod.rs:5493
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[[T; N]]>::as_flattened_mut ]( slice: &mut [[T; N]], ) -> (ret: &mut [T]) ensures ret@ == flatten_array_chunks::<T, N>(old(slice)@), flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_mut_array
// status: generated-new-real-relation-spec
// family: views-and-fixed-subranges
// source: core/src/slice/mod.rs:872
// signature: pub const fn as_mut_array<const N: usize>(&mut self) -> Option<&mut [T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() == N; when Some(a), array_view(a) == old(self)@ and array length is N; when mutable Some(a), final(self)@ == array_view(final(a)); when None, final(self)@ == old(self)@
// shared_helpers: Seq fixed-size array/chunk/subrange view helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=mutable-reference-view-boundary; unknown_review_reason=contract fixes the Seq view and old/final frame, but mutable reference identity and alias/lifetime state are not uniquely determined by that view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_array/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_array/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_array/det_harness.rs
// target_binding_result: target core::slice::as_mut_array bound from inventory declaration core:61077 at core/src/slice/mod.rs:872
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_mut_array::<N> ]( slice: &mut [T], ) -> (ret: Option<&mut [T; N]>) ensures old(slice)@.len() == N ==> ret.is_some() && array_mut_ref_view(ret.unwrap()) == old(slice)@ && final(slice)@ == array_value_view(*final(ret.unwrap())), old(slice)@.len() != N ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_mut_ptr
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:760
// signature: pub const fn as_mut_ptr(&mut self) -> *mut T
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result is the start pointer of self and pointer_range(result, old(self)@.len()) covers exactly the slice allocation; final(self)@ == old(self)@ at function return
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr/det_harness.rs
// target_binding_result: target core::slice::as_mut_ptr bound from inventory declaration core:61074 at core/src/slice/mod.rs:760
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::as_mut_ptr ]( slice: &mut [T], ) -> (ptr: *mut T) ensures slice_start_mut_ptr(old(slice)@, ptr), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_mut_ptr_range
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:839
// signature: pub const fn as_mut_ptr_range(&mut self) -> Range<*mut T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.start is the slice start pointer and result.end == result.start + old(self)@.len(); pointer_range(result.start, old(self)@.len()) covers exactly self; final(self)@ == old(self)@ at function return
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr_range/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr_range/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_mut_ptr_range/det_harness.rs
// target_binding_result: target core::slice::as_mut_ptr_range bound from inventory declaration core:33775 at core/src/slice/mod.rs:839
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::as_mut_ptr_range ]( slice: &mut [T], ) -> (range: core::ops::Range<*mut T>) ensures slice_mut_ptr_range_result(old(slice)@, range), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_ptr
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:728
// signature: pub const fn as_ptr(&self) -> *const T
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result is the start pointer of self and pointer_range(result, old(self)@.len()) covers exactly the slice allocation; final(self)@ == old(self)@ at function return
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr/det_harness.rs
// target_binding_result: target core::slice::as_ptr bound from inventory declaration core:61075 at core/src/slice/mod.rs:728
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::as_ptr ]( slice: &[T], ) -> (ptr: *const T) ensures slice_start_ptr(slice@, ptr), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_ptr_range
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:796
// signature: pub const fn as_ptr_range(&self) -> Range<*const T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.start is the slice start pointer and result.end == result.start + old(self)@.len(); pointer_range(result.start, old(self)@.len()) covers exactly self; final(self)@ == old(self)@ at function return
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr_range/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr_range/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_ptr_range/det_harness.rs
// target_binding_result: target core::slice::as_ptr_range bound from inventory declaration core:33773 at core/src/slice/mod.rs:796
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::as_ptr_range ]( slice: &[T], ) -> (range: core::ops::Range<*const T>) ensures slice_ptr_range_result(slice@, range), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_rchunks
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1446
// signature: pub const fn as_rchunks<const N: usize>(&self) -> (&[T], &[[T; N]])
// requires: N != 0
// ensures: returned remainder then chunks partition old(self)@ exactly; chunks@.len() == old(self)@.len() / N and remainder@.len() == old(self)@.len() % N; flatten_array_chunks(chunks@, N) + remainder@, in source order, equals old(self)@
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks/det_harness.rs
// target_binding_result: target core::slice::as_rchunks bound from inventory declaration core:61084 at core/src/slice/mod.rs:1446
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks::<N> ]( slice: &[T], ) -> (ret: (&[T], &[[T; N]])) requires N != 0, ensures slice_array_rchunks_partition::<T, N>(slice@, ret.0@, ret.1@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::as_rchunks_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1608
// signature: pub const fn as_rchunks_mut<const N: usize>(&mut self) -> (&mut [T], &mut [[T; N]])
// requires: N != 0
// ensures: returned remainder then chunks partition old(self)@ exactly; chunks@.len() == old(self)@.len() / N and remainder@.len() == old(self)@.len() % N; flatten_array_chunks(chunks@, N) + remainder@, in source order, equals old(self)@; final(self)@ is final mutable chunks flattened with final remainder, preserving source order and full frame
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__as_rchunks_mut/det_harness.rs
// target_binding_result: target core::slice::as_rchunks_mut bound from inventory declaration core:61087 at core/src/slice/mod.rs:1608
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks_mut::<N> ]( slice: &mut [T], ) -> (ret: (&mut [T], &mut [[T; N]])) requires N != 0, ensures slice_array_rchunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@), final(slice)@ == final(ret.0)@ + flatten_array_chunks::<T, N>(final(ret.1)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::assume_init_drop
// status: generated-new-real-relation-spec
// family: maybe-uninit-slice-storage
// source: core/src/mem/maybe_uninit.rs:1487
// signature: pub const unsafe fn assume_init_drop(&mut self) where T: [const] Destruct,
// requires: maybe_uninit_all_initialized(old(self)@) and all T invariants required by the operation hold
// ensures: maybe_uninit_drop_all(old(self)@) records each initialized element dropped exactly once; storage length is preserved for the slice object at function return; final(self)@ == old(self)@ at function return unless later mutation occurs through a returned mutable reference explicitly modeled above
// shared_helpers: MaybeUninit initialization/raw-storage view plus old/final write-frame helper
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=maybeuninit-storage-boundary; unknown_review_reason=MaybeUninit initialization/storage state is modeled relationally through a raw-storage view and cannot be collapsed to one unique concrete value; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_drop/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_drop/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_drop/det_harness.rs
// target_binding_result: target core::slice::assume_init_drop bound from inventory declaration core:61036 at core/src/mem/maybe_uninit.rs:1487
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: [const] Destruct,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_drop ]( slice: &mut [core::mem::MaybeUninit<T>], ) requires maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)), ensures maybe_uninit_drop_all( maybe_uninit_seq_relation(old(slice)@), maybe_uninit_seq_relation(final(slice)@), ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::assume_init_mut
// status: generated-new-real-relation-spec
// family: maybe-uninit-slice-storage
// source: core/src/mem/maybe_uninit.rs:1528
// signature: pub const unsafe fn assume_init_mut(&mut self) -> &mut [T]
// requires: maybe_uninit_all_initialized(old(self)@) and all T invariants required by the operation hold
// ensures: result@.len() == old(self)@.len(); result@ is the initialized T view of the same storage as old(self)@; final(self)@ is the MaybeUninit representation of final(result)@
// shared_helpers: MaybeUninit initialization/raw-storage view plus old/final write-frame helper
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=maybeuninit-storage-boundary; unknown_review_reason=MaybeUninit initialization/storage state is modeled relationally through a raw-storage view and cannot be collapsed to one unique concrete value; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_mut/det_harness.rs
// target_binding_result: target core::slice::assume_init_mut bound from inventory declaration core:61038 at core/src/mem/maybe_uninit.rs:1528
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_mut ]( slice: &mut [core::mem::MaybeUninit<T>], ) -> (ret: &mut [T]) requires maybe_uninit_all_initialized(maybe_uninit_seq_relation(old(slice)@)), ensures ret@ == maybe_uninit_seq_relation(old(slice)@).values, maybe_uninit_seq_relation(final(slice)@).values == final(ret)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::assume_init_ref
// status: generated-new-real-relation-spec
// family: maybe-uninit-slice-storage
// source: core/src/mem/maybe_uninit.rs:1509
// signature: pub const unsafe fn assume_init_ref(&self) -> &[T]
// requires: maybe_uninit_all_initialized(old(self)@) and all T invariants required by the operation hold
// ensures: result@.len() == old(self)@.len(); result@ is the initialized T view of the same storage as old(self)@
// shared_helpers: MaybeUninit initialization/raw-storage view plus old/final write-frame helper
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_ref/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_ref/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__assume_init_ref/det_harness.rs
// target_binding_result: target core::slice::assume_init_ref bound from inventory declaration core:61037 at core/src/mem/maybe_uninit.rs:1509
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[core::mem::MaybeUninit<T>]>::assume_init_ref ]( slice: &[core::mem::MaybeUninit<T>], ) -> (ret: &[T]) requires maybe_uninit_all_initialized(maybe_uninit_seq_relation(slice@)), ensures ret@ == maybe_uninit_seq_relation(slice@).values, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::binary_search
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2925
// signature: pub fn binary_search(&self, x: &T) -> Result<usize, usize> where T: Ord,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_binary_search_result(slice@, *x, result)
// shared_helpers: ord_cmp_observed, FnMut ordering/key observation, predicate observation, sortedness, and partition helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=duplicate-or-callback-search-boundary; unknown_review_reason=search result is source-backed but relational: duplicate matches, insertion points, or callback/predicate observations do not force a unique return; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search/det_harness.rs
// target_binding_result: target core::slice::binary_search bound from inventory declaration core:61097 at core/src/slice/mod.rs:2925
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Ord,
// reviewer_notes: Executable find-like search assume_specification uses shared Ord observation bridge and conditional sorted/insertion-point relation; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::Ord>[ <[T]>::binary_search ](slice: &[T], x: &T) -> (result: core::result::Result<usize, usize>) ensures slice_binary_search_result(slice@, *x, result);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::binary_search_by
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2976
// signature: pub fn binary_search_by<'a, F>(&'a self, mut f: F) -> Result<usize, usize> where F: FnMut(&'a T) -> Ordering,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_binary_search_by_result(slice@, f, result)
// shared_helpers: ord_cmp_observed, FnMut ordering/key observation, predicate observation, sortedness, and partition helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=duplicate-or-callback-search-boundary; unknown_review_reason=search result is source-backed but relational: duplicate matches, insertion points, or callback/predicate observations do not force a unique return; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by/det_harness.rs
// target_binding_result: target core::slice::binary_search_by bound from inventory declaration core:61106 at core/src/slice/mod.rs:2976
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, F> F: FnMut(&'a T) -> Ordering,
// reviewer_notes: Executable find-like search assume_specification uses shared FnMut ordering observation bridge and conditional order-consistent insertion relation; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&'a T) -> core::cmp::Ordering>[ <[T]>::binary_search_by::<F> ](slice: &'a [T], f: F) -> (result: core::result::Result<usize, usize>) ensures slice_binary_search_by_result(slice@, f, result);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::binary_search_by_key
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:3077
// signature: pub fn binary_search_by_key<'a, B, F>(&'a self, b: &B, mut f: F) -> Result<usize, usize> where F: FnMut(&'a T) -> B, B: Ord,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_binary_search_by_key_result::<F, T, B>(slice@, *key, f, result)
// shared_helpers: ord_cmp_observed, FnMut ordering/key observation, predicate observation, sortedness, and partition helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=duplicate-or-callback-search-boundary; unknown_review_reason=search result is source-backed but relational: duplicate matches, insertion points, or callback/predicate observations do not force a unique return; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by_key/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by_key/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__binary_search_by_key/det_harness.rs
// target_binding_result: target core::slice::binary_search_by_key bound from inventory declaration core:61107 at core/src/slice/mod.rs:3077
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, B, F> F: FnMut(&'a T) -> B, B: Ord,
// reviewer_notes: Executable find-like search assume_specification uses shared FnMut key and Ord observation bridges with conditional insertion relation; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T, B: core::cmp::Ord, F: core::ops::FnMut(&'a T) -> B>[ <[T]>::binary_search_by_key::<B, F> ](slice: &'a [T], key: &B, f: F) -> (result: core::result::Result<usize, usize>) ensures slice_binary_search_by_key_result::<F, T, B>(slice@, *key, f, result);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunk_by
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1867
// signature: pub const fn chunk_by<F>(&self, pred: F) -> ChunkBy<'_, T, F> where F: FnMut(&T, &T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_adjacent_chunk_view fixes source/remaining, empty yielded_prefix/remainder, forward adjacent-predicate partition state, and adjacent predicate observations
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by/det_harness.rs
// target_binding_result: target core::slice::chunk_by bound from inventory declaration core:33749 at core/src/slice/mod.rs:1867
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T, &T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by::<F> ]( slice: &'a [T], pred: F, ) -> (iter: core::slice::ChunkBy<'a, T, F>) ensures slice_adjacent_chunk_view::<core::slice::ChunkBy<'a, T, F>, F, T>(iter, slice@, pred), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunk_by_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1909
// signature: pub const fn chunk_by_mut<F>(&mut self, pred: F) -> ChunkByMut<'_, T, F> where F: FnMut(&T, &T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_adjacent_chunk_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, forward adjacent-predicate partition state, adjacent predicate observations, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunk_by_mut/det_harness.rs
// target_binding_result: target core::slice::chunk_by_mut bound from inventory declaration core:33761 at core/src/slice/mod.rs:1909
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T, &T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T, &T) -> bool>[ <[T]>::chunk_by_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> (iter: core::slice::ChunkByMut<'a, T, F>) ensures slice_adjacent_chunk_view::<core::slice::ChunkByMut<'a, T, F>, F, T>( iter, old(slice)@, pred, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunks
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1158
// signature: pub const fn chunks(&self, chunk_size: usize) -> Chunks<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records self@ as source/remaining, empty yielded_prefix and remainder, chunk_size, and forward source order
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks/det_harness.rs
// target_binding_result: target core::slice::chunks bound from inventory declaration core:33631 at core/src/slice/mod.rs:1158
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::chunks ]( slice: &'a [T], chunk_size: usize, ) -> (iter: core::slice::Chunks<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).source == slice@, slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remaining == slice@, slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).chunk_size == chunk_size as int, !slice_iterator_view::<core::slice::Chunks<'a, T>, T>(iter).reverse, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunks_exact
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1245
// signature: pub const fn chunks_exact(&self, chunk_size: usize) -> ChunksExact<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records self@, empty yielded_prefix, forward exact chunk partition, and a suffix remainder shorter than chunk_size
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact/det_harness.rs
// target_binding_result: target core::slice::chunks_exact bound from inventory declaration core:33657 at core/src/slice/mod.rs:1245
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::chunks_exact ]( slice: &'a [T], chunk_size: usize, ) -> (iter: core::slice::ChunksExact<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).source == slice@, slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int, !slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter).reverse, slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExact<'a, T>, T>(iter)), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunks_exact_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1293
// signature: pub const fn chunks_exact_mut(&mut self, chunk_size: usize) -> ChunksExactMut<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records old(self)@, empty yielded_prefix, forward exact chunk partition, suffix remainder, and an unchanged constructor frame
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_exact_mut/det_harness.rs
// target_binding_result: target core::slice::chunks_exact_mut bound from inventory declaration core:33673 at core/src/slice/mod.rs:1293
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::chunks_exact_mut ]( slice: &'a mut [T], chunk_size: usize, ) -> (iter: core::slice::ChunksExactMut<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).source == old(slice)@, slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int, !slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter).reverse, slice_chunk_partition::<T>(slice_iterator_view::<core::slice::ChunksExactMut<'a, T>, T>(iter)), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::chunks_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1202
// signature: pub const fn chunks_mut(&mut self, chunk_size: usize) -> ChunksMut<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records old(self)@ as source/remaining, empty yielded_prefix and remainder, chunk_size, forward source order, and an unchanged constructor frame
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__chunks_mut/det_harness.rs
// target_binding_result: target core::slice::chunks_mut bound from inventory declaration core:33644 at core/src/slice/mod.rs:1202
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::chunks_mut ]( slice: &'a mut [T], chunk_size: usize, ) -> (iter: core::slice::ChunksMut<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).source == old(slice)@, slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remaining == old(slice)@, slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int, !slice_iterator_view::<core::slice::ChunksMut<'a, T>, T>(iter).reverse, final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::clone_from_slice
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:4260
// signature: pub const fn clone_from_slice(&mut self, src: &[T]) where T: [const] Clone + [const] Destruct,
// requires: old(dst)@.len() == src@.len()
// ensures: slice_cloned_from(src@, final(dst)@)
// shared_helpers: slice_cloned_from relation using vstd cloned<T> plus old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=clone-or-callback-effect-boundary; unknown_review_reason=Clone/FnMut effects are modeled by source-order observation relations, so the contract preserves effect nondeterminism instead of choosing outputs; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__clone_from_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__clone_from_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__clone_from_slice/det_harness.rs
// target_binding_result: target core::slice::clone_from_slice bound from inventory declaration core:10943 at core/src/slice/mod.rs:4260
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: [const] Clone + [const] Destruct,
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::clone::Clone>[ <[T]>::clone_from_slice ](dst: &mut [T], src: &[T]) requires old(dst)@.len() == src@.len() ensures slice_cloned_from(src@, final(dst)@);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::contains
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2594
// signature: pub fn contains(&self, x: &T) -> bool where T: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: b <==> slice_contains_value(slice@, *x)
// shared_helpers: partial_eq_observed bridge plus Seq membership/prefix/suffix helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__contains/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__contains/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__contains/det_harness.rs
// target_binding_result: target core::slice::contains bound from inventory declaration core:61098 at core/src/slice/mod.rs:2594
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: PartialEq,
// reviewer_notes: Executable observation assume_specification now uses the shared partial_eq_observed bridge; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::contains ](slice: &[T], x: &T) -> (b: bool) ensures b <==> slice_contains_value(slice@, *x);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::element_offset
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:5267
// signature: pub fn element_offset(&self, element: &T) -> Option<usize>
// requires: T is not zero-sized, matching the documented panic condition
// ensures: result.is_some() ==> result.unwrap() < self@.len() and element pointer equals as_ptr(self)+result.unwrap(); result.is_none() ==> element pointer is not aligned to an element start inside the slice allocation
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__element_offset/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__element_offset/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__element_offset/det_harness.rs
// target_binding_result: target core::slice::element_offset bound from inventory declaration core:61143 at core/src/slice/mod.rs:5267
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::element_offset ]( slice: &[T], element: &T, ) -> (ret: Option<usize>) ensures ret.is_some() ==> ret.unwrap() < slice@.len() && slice_element_offset_result(slice@, element, ret.unwrap()), ret.is_none() ==> !slice_element_in_domain(slice@, element), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::ends_with
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2655
// signature: pub fn ends_with(&self, needle: &[T]) -> bool where T: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: b <==> slice_is_suffix(slice@, needle@)
// shared_helpers: partial_eq_observed bridge plus Seq membership/prefix/suffix helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ends_with/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ends_with/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__ends_with/det_harness.rs
// target_binding_result: target core::slice::ends_with bound from inventory declaration core:61100 at core/src/slice/mod.rs:2655
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: PartialEq,
// reviewer_notes: Executable observation assume_specification now uses the shared partial_eq_observed bridge for pairwise suffix matching; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::ends_with ](slice: &[T], needle: &[T]) -> (b: bool) ensures b <==> slice_is_suffix(slice@, needle@);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::eq_ignore_ascii_case
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:60
// signature: pub const fn eq_ignore_ascii_case(&self, other: &[u8]) -> bool
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result <==> self@.len() == other@.len() && forall i in range, ascii_lower_byte(self@[i]) == ascii_lower_byte(other@[i])
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__eq_ignore_ascii_case/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__eq_ignore_ascii_case/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__eq_ignore_ascii_case/det_harness.rs
// target_binding_result: target core::slice::eq_ignore_ascii_case bound from inventory declaration core:61046 at core/src/slice/ascii.rs:60
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::eq_ignore_ascii_case ]( slice: &[u8], other: &[u8], ) -> (ret: bool) ensures ret <==> ascii_eq_ignore_case(slice@, other@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::escape_ascii
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:218
// signature: pub fn escape_ascii(&self) -> EscapeAscii<'_>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_iterator_view(result).source == self@; flatten(result) == ascii_escape_seq(self@)
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__escape_ascii/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__escape_ascii/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__escape_ascii/det_harness.rs
// target_binding_result: target core::slice::escape_ascii bound from inventory declaration core:33425 at core/src/slice/ascii.rs:218
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a>[ <[u8]>::escape_ascii ]( slice: &'a [u8], ) -> (iter: core::slice::EscapeAscii<'a>) ensures slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).source == slice@, slice_iterator_view::<core::slice::EscapeAscii<'a>, u8>(iter).remaining == ascii_escape_seq(slice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::fill
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:4172
// signature: pub fn fill(&mut self, value: T) where T: Clone,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_filled_with_clone(old(slice)@, value, final(slice)@)
// shared_helpers: slice_filled_with_clone relation using vstd cloned<T> plus old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=clone-or-callback-effect-boundary; unknown_review_reason=Clone/FnMut effects are modeled by source-order observation relations, so the contract preserves effect nondeterminism instead of choosing outputs; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill/det_harness.rs
// target_binding_result: target core::slice::fill bound from inventory declaration core:61030 at core/src/slice/mod.rs:4172
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Clone,
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::clone::Clone>[ <[T]>::fill ](slice: &mut [T], value: T) ensures slice_filled_with_clone(old(slice)@, value, final(slice)@);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::fill_with
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:4196
// signature: pub fn fill_with<F>(&mut self, mut f: F) where F: FnMut() -> T,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(slice)@ == zero_arg_fnmut_outputs(f, old(slice)@.len()) and zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len()).len() == old(slice)@.len()
// shared_helpers: zero_arg_fnmut_outputs closure-observation sequence plus old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill_with/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill_with/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__fill_with/det_harness.rs
// target_binding_result: target core::slice::fill_with bound from inventory declaration core:61127 at core/src/slice/mod.rs:4196
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut() -> T,
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, F: core::ops::FnMut() -> T>[ <[T]>::fill_with::<F> ](slice: &mut [T], f: F) ensures final(slice)@ == zero_arg_fnmut_outputs(f, old(slice)@.len()), zero_arg_fnmut_outputs::<F, T>(f, old(slice)@.len()).len() == old(slice)@.len();
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::first_chunk
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:327
// signature: pub const fn first_chunk<const N: usize>(&self) -> Option<&[T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some(chunk), array_view(chunk) is the exact prefix subrange of old(self)@ of length N
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk/det_harness.rs
// target_binding_result: target core::slice::first_chunk bound from inventory declaration core:61064 at core/src/slice/mod.rs:327
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::first_chunk::<N> ]( slice: &[T], ) -> (ret: Option<&[T; N]>) ensures (N as int) <= slice@.len() ==> ret.is_some() && array_ref_view(ret.unwrap()) == slice_fixed_prefix::<T, N>(slice@), (N as int) > slice@.len() ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::first_chunk_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:357
// signature: pub const fn first_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some(chunk), array_view(chunk) is the exact prefix subrange of old(self)@ of length N; final(self)@ is old(self)@ with the returned chunk subrange replaced by array_view(final(chunk)) and all other indices unchanged
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__first_chunk_mut/det_harness.rs
// target_binding_result: target core::slice::first_chunk_mut bound from inventory declaration core:61065 at core/src/slice/mod.rs:357
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::first_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: Option<&mut [T; N]>) ensures (N as int) <= old(slice)@.len() ==> ret.is_some() && array_mut_ref_view(ret.unwrap()) == slice_fixed_prefix::<T, N>(old(slice)@) && final(slice)@ == array_value_view(*final(ret.unwrap())) + old(slice)@.subrange(N as int, old(slice)@.len() as int), (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::from_mut
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/raw.rs:211
// signature: pub const fn from_mut<T>(s: &mut T) -> &mut [T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@.len() == 1; result@[0] == *s; final(s) equals the sole element of final(result) and final(result)@ == seq![*final(s)]
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_mut/det_harness.rs
// target_binding_result: target core::slice::from_mut bound from inventory declaration core:33772 at core/src/slice/raw.rs:211
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <T>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ core::slice::from_mut::<T> ]( value: &'a mut T, ) -> (ret: &'a mut [T]) ensures ret@ == seq![*old(value)], final(ret)@ == seq![*final(value)], ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::from_raw_parts
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/raw.rs:124
// signature: pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T]
// requires: slice_raw_domain(data, len, shared) holds: data is non-null/aligned, one-allocation, initialized for len elements, no wrap, and aliasing obeys Rust shared reference rules
// ensures: result@.len() == len; result.as_ptr() == data and result@ is the Seq view of the initialized memory range described by slice_raw_domain(data, len, ...)
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts/det_harness.rs
// target_binding_result: target core::slice::from_raw_parts bound from inventory declaration core:9483 at core/src/slice/raw.rs:124
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, T>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ core::slice::from_raw_parts::<T> ]( data: *const T, len: usize, ) -> (ret: &'a [T]) requires slice_raw_domain_valid(slice_raw_domain(data, len, SliceRawMutability::Immutable)), ensures slice_from_raw_parts_result(data, len, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::from_raw_parts_mut
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/raw.rs:179
// signature: pub const unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> &'a mut [T]
// requires: slice_raw_domain(data, len, mutable) holds: data is non-null/aligned, one-allocation, initialized for len elements, no wrap, and aliasing obeys Rust mutable reference rules
// ensures: result@.len() == len; result.as_ptr() == data and result@ is the Seq view of the initialized memory range described by slice_raw_domain(data, len, ...); mutations through result update exactly the raw-domain memory range represented by result@
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_raw_parts_mut/det_harness.rs
// target_binding_result: target core::slice::from_raw_parts_mut bound from inventory declaration core:9596 at core/src/slice/raw.rs:179
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, T>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ core::slice::from_raw_parts_mut::<T> ]( data: *mut T, len: usize, ) -> (ret: &'a mut [T]) requires slice_raw_domain_valid(slice_raw_mut_domain(data, len, SliceRawMutability::Mutable)), ensures slice_from_raw_parts_mut_result(data, len, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::from_ref
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/raw.rs:203
// signature: pub const fn from_ref<T>(s: &T) -> &[T]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@.len() == 1; result@[0] == *s
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_ref/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_ref/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__from_ref/det_harness.rs
// target_binding_result: target core::slice::from_ref bound from inventory declaration core:33771 at core/src/slice/raw.rs:203
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <T>
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ core::slice::from_ref::<T> ]( value: &'a T, ) -> (ret: &'a [T]) ensures ret@ == seq![*value], ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get_disjoint_mut
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:5216
// signature: pub fn get_disjoint_mut<I, const N: usize>( &mut self, indices: [I; N], ) -> Result<[&mut I::Output; N], GetDisjointMutError> where I: GetDisjointMutIndex + SliceIndex<Self>,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result and/or final state is related to old(self)@ by the shared Seq/View model and preserves source-observable length/frame facts
// shared_helpers: old/final Seq update, frame, permutation, and disjointness helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=disjoint-mutable-alias-boundary; unknown_review_reason=disjoint mutable-reference arrays preserve source aliasing and post-state relations, but reference identity is not uniquely fixed by the contract; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_mut/det_harness.rs
// target_binding_result: target core::slice::get_disjoint_mut bound from inventory declaration core:33825 at core/src/slice/mod.rs:5216
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I, const N: usize> I: GetDisjointMutIndex + SliceIndex<Self>,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification<T, I, const N: usize>[ <[T]>::get_disjoint_mut::<I, N> ]( slice: &mut [T], indices: [I; N], ) -> (ret: core::result::Result< [&mut <I as core::slice::SliceIndex<[T]>>::Output; N], core::slice::GetDisjointMutError, >) where I: core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]> ensures ret.is_ok() ==> slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices) && final(slice)@.len() == old(slice)@.len(), ret.is_err() ==> !slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices) && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get_disjoint_unchecked_mut
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:5149
// signature: pub unsafe fn get_disjoint_unchecked_mut<I, const N: usize>( &mut self, indices: [I; N], ) -> [&mut I::Output; N] where I: GetDisjointMutIndex + SliceIndex<Self>,
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes
// ensures: result and/or final state is related to old(self)@ by the shared Seq/View model and preserves source-observable length/frame facts
// shared_helpers: old/final Seq update, frame, permutation, and disjointness helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=disjoint-mutable-alias-boundary; unknown_review_reason=disjoint mutable-reference arrays preserve source aliasing and post-state relations, but reference identity is not uniquely fixed by the contract; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_unchecked_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_unchecked_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_disjoint_unchecked_mut/det_harness.rs
// target_binding_result: target core::slice::get_disjoint_unchecked_mut bound from inventory declaration core:61142 at core/src/slice/mod.rs:5149
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I, const N: usize> I: GetDisjointMutIndex + SliceIndex<Self>,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification<T, I, const N: usize>[ <[T]>::get_disjoint_unchecked_mut::<I, N> ]( slice: &mut [T], indices: [I; N], ) -> (ret: [&mut <I as core::slice::SliceIndex<[T]>>::Output; N]) where I: core::slice::GetDisjointMutIndex + core::slice::SliceIndex<[T]> requires slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices), ensures final(slice)@.len() == old(slice)@.len(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get_mut
// status: generated-new-real-relation-spec
// family: basic-observation-and-conversion
// source: core/src/slice/mod.rs:600
// signature: pub const fn get_mut<I>(&mut self, index: I) -> Option<&mut I::Output> where I: [const] SliceIndex<Self>,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: if result is None then the index is outside slice@.len(); if result is Some(p) then index is in range and *p == old(slice)@[index]; final(slice)@ == old(slice)@.update(index, *final(result.unwrap())) when Some; otherwise final(slice)@ == old(slice)@
// shared_helpers: shared [T]@ -> Seq<T> View model and length/subrange helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=mutable-reference-view-boundary; unknown_review_reason=contract fixes the Seq view and old/final frame, but mutable reference identity and alias/lifetime state are not uniquely determined by that view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_mut/det_harness.rs
// target_binding_result: target core::slice::get_mut bound from inventory declaration core:61073 at core/src/slice/mod.rs:600
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I> I: [const] SliceIndex<Self>,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification<T, I>[ <[T]>::get_mut::<I> ]( slice: &mut [T], index: I, ) -> (ret: Option<&mut <I as core::slice::SliceIndex<[T]>>::Output>) where I: core::slice::SliceIndex<[T]> ensures ret.is_some() ==> slice_index_in_range(old(slice)@, index) && slice_index_mut_frame(old(slice)@, index, final(slice)@), ret.is_none() ==> !slice_index_in_range(old(slice)@, index) && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get_unchecked
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:640
// signature: pub const unsafe fn get_unchecked<I>(&self, index: I) -> &I::Output where I: [const] SliceIndex<Self>,
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes
// ensures: result pointer/range/provenance is derived from the input slice or raw domain and preserves length/alignment facts
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked/det_harness.rs
// target_binding_result: target core::slice::get_unchecked bound from inventory declaration core:33468 at core/src/slice/mod.rs:640
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I> I: [const] SliceIndex<Self>,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification<T, I>[ <[T]>::get_unchecked::<I> ]( slice: &[T], index: I, ) -> (ret: &<I as core::slice::SliceIndex<[T]>>::Output) where I: core::slice::SliceIndex<[T]> requires slice_index_in_range(slice@, index), ensures slice_index_result(slice@, index, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::get_unchecked_mut
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:686
// signature: pub const unsafe fn get_unchecked_mut<I>(&mut self, index: I) -> &mut I::Output where I: [const] SliceIndex<Self>,
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes
// ensures: result pointer/range/provenance is derived from the input slice or raw domain and preserves length/alignment facts; final(self)@ == old(self)@ at function return unless later mutation occurs through a returned mutable reference explicitly modeled above
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__get_unchecked_mut/det_harness.rs
// target_binding_result: target core::slice::get_unchecked_mut bound from inventory declaration core:33469 at core/src/slice/mod.rs:686
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <I> I: [const] SliceIndex<Self>,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification<T, I>[ <[T]>::get_unchecked_mut::<I> ]( slice: &mut [T], index: I, ) -> (ret: &mut <I as core::slice::SliceIndex<[T]>>::Output) where I: core::slice::SliceIndex<[T]> requires slice_index_in_range(old(slice)@, index), ensures slice_index_mut_frame(old(slice)@, index, final(slice)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::is_ascii
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:18
// signature: pub const fn is_ascii(&self) -> bool
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result <==> forall i in range, self@[i] <= 0x7f
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_ascii/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_ascii/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_ascii/det_harness.rs
// target_binding_result: target core::slice::is_ascii bound from inventory declaration core:61043 at core/src/slice/ascii.rs:18
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::is_ascii ]( slice: &[u8], ) -> (ret: bool) ensures ret <==> ascii_all(slice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::is_sorted
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:4735
// signature: pub fn is_sorted(&self) -> bool where T: PartialOrd,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result <==> self@ satisfies the shared PartialOrd sortedness observation relation
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and predicate observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted/det_harness.rs
// target_binding_result: target core::slice::is_sorted bound from inventory declaration core:61133 at core/src/slice/mod.rs:4735
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: PartialOrd,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::PartialOrd>[ <[T]>::is_sorted ]( slice: &[T], ) -> (ret: bool) ensures ret <==> slice_sorted_by_partial_ord(slice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::is_sorted_by
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:4778
// signature: pub fn is_sorted_by<'a, F>(&'a self, mut compare: F) -> bool where F: FnMut(&'a T, &'a T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result follows the source adjacent-pair FnMut call trace over self@; true iff all observed adjacent comparator calls succeed
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and source-adjacent FnMut observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by/det_harness.rs
// target_binding_result: target core::slice::is_sorted_by bound from inventory declaration core:61134 at core/src/slice/mod.rs:4778
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, F> F: FnMut(&'a T, &'a T) -> bool,
// reviewer_notes: Executable remaining-family assume_specification now models source-order adjacent `array_windows().all` comparator observations rather than all-pairs callback extensionality; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&'a T, &'a T) -> bool>[ <[T]>::is_sorted_by::<F> ]( slice: &'a [T], compare: F, ) -> (ret: bool) ensures slice_sorted_by_bool_compare_result(slice@, compare, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::is_sorted_by_key
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:4802
// signature: pub fn is_sorted_by_key<'a, F, K>(&'a self, f: F) -> bool where F: FnMut(&'a T) -> K, K: PartialOrd,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result follows the source key-extraction call trace over self@; true iff the observed adjacent keys are sorted
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and source-adjacent FnMut key observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by_key/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by_key/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__is_sorted_by_key/det_harness.rs
// target_binding_result: target core::slice::is_sorted_by_key bound from inventory declaration core:61135 at core/src/slice/mod.rs:4802
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, F, K> F: FnMut(&'a T) -> K, K: PartialOrd,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&'a T) -> K, K: core::cmp::PartialOrd>[ <[T]>::is_sorted_by_key::<F, K> ]( slice: &'a [T], f: F, ) -> (ret: bool) ensures slice_sorted_by_partial_key_result::<F, T, K>(slice@, f, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::iter_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1063
// signature: pub const fn iter_mut(&mut self) -> IterMut<'_, T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_iterator_view(result).remaining == old(self)@.as_ref(); IteratorSpec::initial_value_relation(result, result); final(self)@ is determined by updates through yielded mutable references and preserves iteration order
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__iter_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__iter_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__iter_mut/det_harness.rs
// target_binding_result: target core::slice::iter_mut bound from inventory declaration core:33492 at core/src/slice/mod.rs:1063
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::iter_mut ]( slice: &'a mut [T], ) -> (iter: core::slice::IterMut<'a, T>) ensures slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).source == old(slice)@, slice_iterator_view::<core::slice::IterMut<'a, T>, T>(iter).remaining == old(slice)@, final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::last_chunk
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:509
// signature: pub const fn last_chunk<const N: usize>(&self) -> Option<&[T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some(chunk), array_view(chunk) is the exact suffix subrange of old(self)@ of length N
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk/det_harness.rs
// target_binding_result: target core::slice::last_chunk bound from inventory declaration core:61070 at core/src/slice/mod.rs:509
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::last_chunk::<N> ]( slice: &[T], ) -> (ret: Option<&[T; N]>) ensures (N as int) <= slice@.len() ==> ret.is_some() && array_ref_view(ret.unwrap()) == slice_fixed_suffix::<T, N>(slice@), (N as int) > slice@.len() ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::last_chunk_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:539
// signature: pub const fn last_chunk_mut<const N: usize>(&mut self) -> Option<&mut [T; N]>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some(chunk), array_view(chunk) is the exact suffix subrange of old(self)@ of length N; final(self)@ is old(self)@ with the returned chunk subrange replaced by array_view(final(chunk)) and all other indices unchanged
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__last_chunk_mut/det_harness.rs
// target_binding_result: target core::slice::last_chunk_mut bound from inventory declaration core:61071 at core/src/slice/mod.rs:539
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::last_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: Option<&mut [T; N]>) ensures (N as int) <= old(slice)@.len() ==> ret.is_some() && array_mut_ref_view(ret.unwrap()) == slice_fixed_suffix::<T, N>(old(slice)@) && final(slice)@ == old(slice)@.subrange(0, (old(slice)@.len() - N) as int) + array_value_view(*final(ret.unwrap())), (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::make_ascii_lowercase
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:195
// signature: pub const fn make_ascii_lowercase(&mut self)
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(self)@ == Seq::new(old(self)@.len(), |i| ascii_lower_byte(old(self)@[i]))
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_lowercase/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_lowercase/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_lowercase/det_harness.rs
// target_binding_result: target core::slice::make_ascii_lowercase bound from inventory declaration core:61048 at core/src/slice/ascii.rs:195
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::make_ascii_lowercase ]( slice: &mut [u8], ) ensures final(slice)@ == ascii_lower_seq(old(slice)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::make_ascii_uppercase
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:173
// signature: pub const fn make_ascii_uppercase(&mut self)
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(self)@ == Seq::new(old(self)@.len(), |i| ascii_upper_byte(old(self)@[i]))
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_uppercase/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_uppercase/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__make_ascii_uppercase/det_harness.rs
// target_binding_result: target core::slice::make_ascii_uppercase bound from inventory declaration core:61047 at core/src/slice/ascii.rs:173
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::make_ascii_uppercase ]( slice: &mut [u8], ) ensures final(slice)@ == ascii_upper_seq(old(slice)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::partition_point
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:4861
// signature: pub fn partition_point<P>(&self, mut pred: P) -> usize where P: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_partition_point_result(slice@, pred, index)
// shared_helpers: ord_cmp_observed, FnMut ordering/key observation, predicate observation, sortedness, and partition helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=duplicate-or-callback-search-boundary; unknown_review_reason=search result is source-backed but relational: duplicate matches, insertion points, or callback/predicate observations do not force a unique return; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__partition_point/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__partition_point/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__partition_point/det_harness.rs
// target_binding_result: target core::slice::partition_point bound from inventory declaration core:61108 at core/src/slice/mod.rs:4861
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <P> P: FnMut(&T) -> bool,
// reviewer_notes: Executable find-like search assume_specification uses shared FnMut predicate observation bridge and conditional partition-point relation; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, P: core::ops::FnMut(&T) -> bool>[ <[T]>::partition_point::<P> ](slice: &[T], pred: P) -> (index: usize) ensures slice_partition_point_result(slice@, pred, index);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rchunks
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1689
// signature: pub const fn rchunks(&self, chunk_size: usize) -> RChunks<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records self@ as source/remaining, empty yielded_prefix and remainder, chunk_size, and reverse source order
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks/det_harness.rs
// target_binding_result: target core::slice::rchunks bound from inventory declaration core:33696 at core/src/slice/mod.rs:1689
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::rchunks ]( slice: &'a [T], chunk_size: usize, ) -> (iter: core::slice::RChunks<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).source == slice@, slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remaining == slice@, slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).chunk_size == chunk_size as int, slice_iterator_view::<core::slice::RChunks<'a, T>, T>(iter).reverse, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rchunks_exact
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1778
// signature: pub const fn rchunks_exact(&self, chunk_size: usize) -> RChunksExact<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records self@, empty yielded_prefix, reverse exact chunk partition, and a prefix remainder shorter than chunk_size
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact/det_harness.rs
// target_binding_result: target core::slice::rchunks_exact bound from inventory declaration core:33722 at core/src/slice/mod.rs:1778
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::rchunks_exact ]( slice: &'a [T], chunk_size: usize, ) -> (iter: core::slice::RChunksExact<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).source == slice@, slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).chunk_size == chunk_size as int, slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter).reverse, slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExact<'a, T>, T>(iter)), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rchunks_exact_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1827
// signature: pub const fn rchunks_exact_mut(&mut self, chunk_size: usize) -> RChunksExactMut<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records old(self)@, empty yielded_prefix, reverse exact chunk partition, prefix remainder, and an unchanged constructor frame
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_exact_mut/det_harness.rs
// target_binding_result: target core::slice::rchunks_exact_mut bound from inventory declaration core:33737 at core/src/slice/mod.rs:1827
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::rchunks_exact_mut ]( slice: &'a mut [T], chunk_size: usize, ) -> (iter: core::slice::RChunksExactMut<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).source == old(slice)@, slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).chunk_size == chunk_size as int, slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter).reverse, slice_chunk_partition::<T>(slice_iterator_view::<core::slice::RChunksExactMut<'a, T>, T>(iter)), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rchunks_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1733
// signature: pub const fn rchunks_mut(&mut self, chunk_size: usize) -> RChunksMut<'_, T>
// requires: chunk_size != 0
// ensures: slice_iterator_view(result) records old(self)@ as source/remaining, empty yielded_prefix and remainder, chunk_size, reverse source order, and an unchanged constructor frame
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rchunks_mut/det_harness.rs
// target_binding_result: target core::slice::rchunks_mut bound from inventory declaration core:33709 at core/src/slice/mod.rs:1733
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::rchunks_mut ]( slice: &'a mut [T], chunk_size: usize, ) -> (iter: core::slice::RChunksMut<'a, T>) requires chunk_size != 0, ensures slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).source == old(slice)@, slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remaining == old(slice)@, slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).chunk_size == chunk_size as int, slice_iterator_view::<core::slice::RChunksMut<'a, T>, T>(iter).reverse, final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::reverse
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:981
// signature: pub const fn reverse(&mut self)
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(slice)@ == slice_reversed(old(slice)@)
// shared_helpers: slice_reversed Seq transformer over old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__reverse/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__reverse/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__reverse/det_harness.rs
// target_binding_result: target core::slice::reverse bound from inventory declaration core:61080 at core/src/slice/mod.rs:981
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::reverse ](slice: &mut [T]) ensures final(slice)@ == slice_reversed(old(slice)@);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rotate_left
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:3890
// signature: pub const fn rotate_left(&mut self, mid: usize)
// requires: mid <= old(slice)@.len()
// ensures: final(slice)@ == slice_rotated_left(old(slice)@, mid as int)
// shared_helpers: slice_rotated_left subrange-concatenation transformer over old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_left/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_left/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_left/det_harness.rs
// target_binding_result: target core::slice::rotate_left bound from inventory declaration core:61123 at core/src/slice/mod.rs:3890
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::rotate_left ](slice: &mut [T], mid: usize) requires mid <= old(slice)@.len() ensures final(slice)@ == slice_rotated_left(old(slice)@, mid as int);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rotate_right
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:3936
// signature: pub const fn rotate_right(&mut self, k: usize)
// requires: k <= old(slice)@.len()
// ensures: final(slice)@ == slice_rotated_right(old(slice)@, k as int)
// shared_helpers: slice_rotated_right subrange-concatenation transformer over old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_right/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_right/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rotate_right/det_harness.rs
// target_binding_result: target core::slice::rotate_right bound from inventory declaration core:61124 at core/src/slice/mod.rs:3936
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::rotate_right ](slice: &mut [T], k: usize) requires k <= old(slice)@.len() ensures final(slice)@ == slice_rotated_right(old(slice)@, k as int);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rsplit
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2365
// signature: pub fn rsplit<F>(&self, pred: F) -> RSplit<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes source/remaining, empty yielded_prefix/remainder, reverse predicate partition state, and predicate observations
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit/det_harness.rs
// target_binding_result: target core::slice::rsplit bound from inventory declaration core:33558 at core/src/slice/mod.rs:2365
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit::<F> ]( slice: &'a [T], pred: F, ) -> (iter: core::slice::RSplit<'a, T, F>) ensures slice_predicate_split_view::<core::slice::RSplit<'a, T, F>, F, T>( iter, slice@, pred, false, true, 0, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rsplit_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2391
// signature: pub fn rsplit_mut<F>(&mut self, pred: F) -> RSplitMut<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, reverse predicate partition state, predicate observations, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplit_mut/det_harness.rs
// target_binding_result: target core::slice::rsplit_mut bound from inventory declaration core:33569 at core/src/slice/mod.rs:2391
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplit_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> (iter: core::slice::RSplitMut<'a, T, F>) ensures slice_predicate_split_view::<core::slice::RSplitMut<'a, T, F>, F, T>( iter, old(slice)@, pred, false, true, 0, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rsplitn
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2474
// signature: pub fn rsplitn<F>(&self, n: usize, pred: F) -> RSplitN<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes source/remaining, empty yielded_prefix/remainder, reverse predicate partition state, and n as the split limit
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn/det_harness.rs
// target_binding_result: target core::slice::rsplitn bound from inventory declaration core:33589 at core/src/slice/mod.rs:2474
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn::<F> ]( slice: &'a [T], n: usize, pred: F, ) -> (iter: core::slice::RSplitN<'a, T, F>) ensures slice_predicate_split_view::<core::slice::RSplitN<'a, T, F>, F, T>( iter, slice@, pred, false, true, n as int, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::rsplitn_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2501
// signature: pub fn rsplitn_mut<F>(&mut self, n: usize, pred: F) -> RSplitNMut<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, reverse predicate partition state, n as the split limit, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__rsplitn_mut/det_harness.rs
// target_binding_result: target core::slice::rsplitn_mut bound from inventory declaration core:33609 at core/src/slice/mod.rs:2501
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::rsplitn_mut::<F> ]( slice: &'a mut [T], n: usize, pred: F, ) -> (iter: core::slice::RSplitNMut<'a, T, F>) ensures slice_predicate_split_view::<core::slice::RSplitNMut<'a, T, F>, F, T>( iter, old(slice)@, pred, false, true, n as int, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::select_nth_unstable
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3522
// signature: pub fn select_nth_unstable(&mut self, index: usize) -> (&mut [T], &mut T, &mut [T]) where T: Ord,
// requires: index < old(self)@.len()
// ensures: final(self)@ is a permutation of old(self)@; ret.0@.len() == index and ret.1 is the element at final(self)@[index] and ret.2@.len() == old(self)@.len() - index - 1; all elements in ret.0 are <= pivot and all elements in ret.2 are >= pivot under the Ord/key or observed comparator Ordering relation
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable/det_harness.rs
// target_binding_result: target core::slice::select_nth_unstable bound from inventory declaration core:61117 at core/src/slice/mod.rs:3522
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Ord,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::Ord>[ <[T]>::select_nth_unstable ]( slice: &mut [T], index: usize, ) -> (ret: (&mut [T], &mut T, &mut [T])) requires index < old(slice)@.len(), ensures final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@, final(ret.0)@.len() == index, slice_permutation(old(slice)@, final(slice)@), slice_select_partition_ord(final(ret.0)@, *final(ret.1), final(ret.2)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::select_nth_unstable_by
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3587
// signature: pub fn select_nth_unstable_by<F>( &mut self, index: usize, mut compare: F, ) -> (&mut [T], &mut T, &mut [T]) where F: FnMut(&T, &T) -> Ordering,
// requires: index < old(self)@.len()
// ensures: final(self)@ is a permutation of old(self)@; ret.0@.len() == index and ret.1 is the element at final(self)@[index] and ret.2@.len() == old(self)@.len() - index - 1; all elements in ret.0 are <= pivot and all elements in ret.2 are >= pivot under the Ord/key or observed comparator Ordering relation
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by/det_harness.rs
// target_binding_result: target core::slice::select_nth_unstable_by bound from inventory declaration core:61118 at core/src/slice/mod.rs:3587
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T, &T) -> Ordering,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> core::cmp::Ordering>[ <[T]>::select_nth_unstable_by::<F> ]( slice: &mut [T], index: usize, compare: F, ) -> (ret: (&mut [T], &mut T, &mut [T])) requires index < old(slice)@.len(), ensures final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@, final(ret.0)@.len() == index, slice_permutation(old(slice)@, final(slice)@), slice_select_partition_cmp( final(ret.0)@, *final(ret.1), final(ret.2)@, comparator_observation(compare, old(slice)@), ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::select_nth_unstable_by_key
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3654
// signature: pub fn select_nth_unstable_by_key<K, F>( &mut self, index: usize, mut f: F, ) -> (&mut [T], &mut T, &mut [T]) where F: FnMut(&T) -> K, K: Ord,
// requires: index < old(self)@.len()
// ensures: final(self)@ is a permutation of old(self)@; ret.0@.len() == index and ret.1 is the element at final(self)@[index] and ret.2@.len() == old(self)@.len() - index - 1; all elements in ret.0 are <= pivot and all elements in ret.2 are >= pivot under the Ord/key or observed comparator Ordering relation
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by_key/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by_key/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__select_nth_unstable_by_key/det_harness.rs
// target_binding_result: target core::slice::select_nth_unstable_by_key bound from inventory declaration core:61119 at core/src/slice/mod.rs:3654
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <K, F> F: FnMut(&T) -> K, K: Ord,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, K: core::cmp::Ord, F: core::ops::FnMut(&T) -> K>[ <[T]>::select_nth_unstable_by_key::<K, F> ]( slice: &mut [T], index: usize, f: F, ) -> (ret: (&mut [T], &mut T, &mut [T])) requires index < old(slice)@.len(), ensures final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@, final(ret.0)@.len() == index, slice_permutation(old(slice)@, final(slice)@), slice_select_partition_key::<F, T, K>(final(ret.0)@, *final(ret.1), final(ret.2)@, f), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::sort_unstable
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3139
// signature: pub fn sort_unstable(&mut self) where T: Ord,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(self)@ is a permutation of old(self)@; final(self)@ is sorted by the Ord/key or observed comparator Ordering relation when that relation is a total order; equal-element relative order is not specified
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable/det_harness.rs
// target_binding_result: target core::slice::sort_unstable bound from inventory declaration core:61111 at core/src/slice/mod.rs:3139
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Ord,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::Ord>[ <[T]>::sort_unstable ]( slice: &mut [T], ) ensures slice_permutation(old(slice)@, final(slice)@), slice_sorted_by_ord(final(slice)@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::sort_unstable_by
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3194
// signature: pub fn sort_unstable_by<F>(&mut self, mut compare: F) where F: FnMut(&T, &T) -> Ordering,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(self)@ is a permutation of old(self)@; final(self)@ is sorted by the Ord/key or observed comparator Ordering relation when that relation is a total order; equal-element relative order is not specified
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by/det_harness.rs
// target_binding_result: target core::slice::sort_unstable_by bound from inventory declaration core:61112 at core/src/slice/mod.rs:3194
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T, &T) -> Ordering,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, F: core::ops::FnMut(&T, &T) -> core::cmp::Ordering>[ <[T]>::sort_unstable_by::<F> ]( slice: &mut [T], compare: F, ) ensures slice_permutation(old(slice)@, final(slice)@), slice_sorted_by_cmp(final(slice)@, comparator_observation(compare, old(slice)@)), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::sort_unstable_by_key
// status: generated-new-real-relation-spec
// family: sorting-and-selection
// source: core/src/slice/mod.rs:3246
// signature: pub fn sort_unstable_by_key<K, F>(&mut self, mut f: F) where F: FnMut(&T) -> K, K: Ord,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: final(self)@ is a permutation of old(self)@; final(self)@ is sorted by the Ord/key or observed comparator Ordering relation when that relation is a total order; equal-element relative order is not specified
// shared_helpers: Seq permutation, sortedness/order, partition, and comparator Ordering-observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=unstable-sort-or-selection-boundary; unknown_review_reason=unstable sort/select APIs guarantee ordering or partition plus permutation, not a unique permutation for equal keys or pivot-equivalent elements; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by_key/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by_key/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__sort_unstable_by_key/det_harness.rs
// target_binding_result: target core::slice::sort_unstable_by_key bound from inventory declaration core:61113 at core/src/slice/mod.rs:3246
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <K, F> F: FnMut(&T) -> K, K: Ord,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, K: core::cmp::Ord, F: core::ops::FnMut(&T) -> K>[ <[T]>::sort_unstable_by_key::<K, F> ]( slice: &mut [T], f: F, ) ensures slice_permutation(old(slice)@, final(slice)@), slice_sorted_by_key::<F, T, K>(final(slice)@, f), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2247
// signature: pub fn split<F>(&self, pred: F) -> Split<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes source/remaining, empty yielded_prefix/remainder, forward non-inclusive predicate partition state, and predicate observations
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split/det_harness.rs
// target_binding_result: target core::slice::split bound from inventory declaration core:33508 at core/src/slice/mod.rs:2247
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split::<F> ]( slice: &'a [T], pred: F, ) -> (iter: core::slice::Split<'a, T, F>) ensures slice_predicate_split_view::<core::slice::Split<'a, T, F>, F, T>( iter, slice@, pred, false, false, 0, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at_checked
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2156
// signature: pub const fn split_at_checked(&self, mid: usize) -> Option<(&[T], &[T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> mid <= old(self)@.len(); when Some((l,r)), l@ == old(self)@.subrange(0, mid) and r@ == old(self)@.subrange(mid, old(self)@.len())
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_checked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_checked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_checked/det_harness.rs
// target_binding_result: target core::slice::split_at_checked bound from inventory declaration core:61089 at core/src/slice/mod.rs:2156
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_at_checked ]( slice: &[T], mid: usize, ) -> (ret: Option<(&[T], &[T])>) ensures mid <= slice@.len() ==> ret.is_some() && ret.unwrap().0@ == slice@.subrange(0, mid as int) && ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int), mid > slice@.len() ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at_mut_checked
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2195
// signature: pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut [T], &mut [T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> mid <= old(self)@.len(); when Some((l,r)), l@ == old(self)@.subrange(0, mid) and r@ == old(self)@.subrange(mid, old(self)@.len()); final(self)@ == final(l)@ + final(r)@ when Some; final(self)@ == old(self)@ when None
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_checked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_checked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_checked/det_harness.rs
// target_binding_result: target core::slice::split_at_mut_checked bound from inventory declaration core:61091 at core/src/slice/mod.rs:2195
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_at_mut_checked ]( slice: &mut [T], mid: usize, ) -> (ret: Option<(&mut [T], &mut [T])>) ensures mid <= old(slice)@.len() ==> ret.is_some() && ret.unwrap().0@ == old(slice)@.subrange(0, mid as int) && ret.unwrap().1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int) && final(slice)@ == final(ret.unwrap().0)@ + final(ret.unwrap().1)@, mid > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at_mut_unchecked
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2095
// signature: pub const unsafe fn split_at_mut_unchecked(&mut self, mid: usize) -> (&mut [T], &mut [T])
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes; mid <= old(self)@.len()
// ensures: ret.0@ == old(self)@.subrange(0, mid); ret.1@ == old(self)@.subrange(mid, old(self)@.len()); final(self)@ == final(ret.0)@ + final(ret.1)@
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_unchecked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_unchecked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_mut_unchecked/det_harness.rs
// target_binding_result: target core::slice::split_at_mut_unchecked bound from inventory declaration core:61094 at core/src/slice/mod.rs:2095
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_at_mut_unchecked ]( slice: &mut [T], mid: usize, ) -> (ret: (&mut [T], &mut [T])) requires split_point_in_range(old(slice)@, mid), ensures ret.0@ == old(slice)@.subrange(0, mid as int), ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int), final(slice)@ == final(ret.0)@ + final(ret.1)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_at_unchecked
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2041
// signature: pub const unsafe fn split_at_unchecked(&self, mid: usize) -> (&[T], &[T])
// requires: documented unsafe precondition holds for all unchecked indices/ranges/chunk sizes; mid <= old(self)@.len()
// ensures: ret.0@ == old(self)@.subrange(0, mid); ret.1@ == old(self)@.subrange(mid, old(self)@.len())
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_unchecked/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_unchecked/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_at_unchecked/det_harness.rs
// target_binding_result: target core::slice::split_at_unchecked bound from inventory declaration core:61093 at core/src/slice/mod.rs:2041
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_at_unchecked ]( slice: &[T], mid: usize, ) -> (ret: (&[T], &[T])) requires split_point_in_range(slice@, mid), ensures ret.0@ == slice@.subrange(0, mid as int), ret.1@ == slice@.subrange(mid as int, slice@.len() as int), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_first
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:198
// signature: pub const fn split_first(&self) -> Option<(&T, &[T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_none() <==> old(self)@.len() == 0; when Some((head, tail)), *head == old(self)@[0] and tail@ == old(self)@.subrange(1, old(self)@.len())
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first/det_harness.rs
// target_binding_result: target core::slice::split_first bound from inventory declaration core:61058 at core/src/slice/mod.rs:198
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_first ]( slice: &[T], ) -> (ret: Option<(&T, &[T])>) ensures slice@.len() == 0 ==> ret.is_none(), slice@.len() != 0 ==> ret.is_some() && *ret.unwrap().0 == slice@[0] && ret.unwrap().1@ == slice@.subrange(1, slice@.len() as int), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_first_chunk
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:387
// signature: pub const fn split_first_chunk<const N: usize>(&self) -> Option<(&[T; N], &[T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some((chunk, rem)), array_view(chunk) is the exact prefix length-N subrange and rem@ is the complementary subrange
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk/det_harness.rs
// target_binding_result: target core::slice::split_first_chunk bound from inventory declaration core:61066 at core/src/slice/mod.rs:387
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::split_first_chunk::<N> ]( slice: &[T], ) -> (ret: Option<(&[T; N], &[T])>) ensures (N as int) <= slice@.len() ==> ret.is_some() && array_ref_view(ret.unwrap().0) == slice_fixed_prefix::<T, N>(slice@) && ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int), (N as int) > slice@.len() ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_first_chunk_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:417
// signature: pub const fn split_first_chunk_mut<const N: usize>( &mut self, ) -> Option<(&mut [T; N], &mut [T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some((chunk, rem)), array_view(chunk) is the exact prefix length-N subrange and rem@ is the complementary subrange; final(self)@ == final(chunk/rem pieces concatenated in source order)
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_chunk_mut/det_harness.rs
// target_binding_result: target core::slice::split_first_chunk_mut bound from inventory declaration core:61067 at core/src/slice/mod.rs:417
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::split_first_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: Option<(&mut [T; N], &mut [T])>) ensures (N as int) <= old(slice)@.len() ==> ret.is_some() && array_mut_ref_view(ret.unwrap().0) == slice_fixed_prefix::<T, N>(old(slice)@) && ret.unwrap().1@ == old(slice)@.subrange(N as int, old(slice)@.len() as int) && final(slice)@ == array_value_view(*final(ret.unwrap().0)) + final(ret.unwrap().1)@, (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_first_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:220
// signature: pub const fn split_first_mut(&mut self) -> Option<(&mut T, &mut [T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_none() <==> old(self)@.len() == 0; when Some((head, tail)), *head == old(self)@[0] and tail@ == old(self)@.subrange(1, old(self)@.len()); final(self)@ == seq![*final(head)] + final(tail)@
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_first_mut/det_harness.rs
// target_binding_result: target core::slice::split_first_mut bound from inventory declaration core:61059 at core/src/slice/mod.rs:220
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_first_mut ]( slice: &mut [T], ) -> (ret: Option<(&mut T, &mut [T])>) ensures old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@, old(slice)@.len() != 0 ==> ret.is_some() && *ret.unwrap().0 == old(slice)@[0] && ret.unwrap().1@ == old(slice)@.subrange(1, old(slice)@.len() as int) && final(slice)@ == seq![*final(ret.unwrap().0)] + final(ret.unwrap().1)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_inclusive
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2305
// signature: pub fn split_inclusive<F>(&self, pred: F) -> SplitInclusive<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes source/remaining, empty yielded_prefix/remainder, forward inclusive predicate partition state, and predicate observations
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive/det_harness.rs
// target_binding_result: target core::slice::split_inclusive bound from inventory declaration core:33523 at core/src/slice/mod.rs:2305
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_inclusive::<F> ]( slice: &'a [T], pred: F, ) -> (iter: core::slice::SplitInclusive<'a, T, F>) ensures slice_predicate_split_view::<core::slice::SplitInclusive<'a, T, F>, F, T>( iter, slice@, pred, true, false, 0, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_inclusive_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2329
// signature: pub fn split_inclusive_mut<F>(&mut self, pred: F) -> SplitInclusiveMut<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, forward inclusive predicate partition state, predicate observations, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_inclusive_mut/det_harness.rs
// target_binding_result: target core::slice::split_inclusive_mut bound from inventory declaration core:33548 at core/src/slice/mod.rs:2329
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_inclusive_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> (iter: core::slice::SplitInclusiveMut<'a, T, F>) ensures slice_predicate_split_view::<core::slice::SplitInclusiveMut<'a, T, F>, F, T>( iter, old(slice)@, pred, true, false, 0, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_last
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:240
// signature: pub const fn split_last(&self) -> Option<(&T, &[T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_none() <==> old(self)@.len() == 0; when Some((last, init)), *last == old(self)@[old(self)@.len()-1] and init@ == old(self)@.subrange(0, old(self)@.len()-1)
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last/det_harness.rs
// target_binding_result: target core::slice::split_last bound from inventory declaration core:61060 at core/src/slice/mod.rs:240
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_last ]( slice: &[T], ) -> (ret: Option<(&T, &[T])>) ensures slice@.len() == 0 ==> ret.is_none(), slice@.len() != 0 ==> ret.is_some() && *ret.unwrap().0 == slice@[(slice@.len() - 1) as int] && ret.unwrap().1@ == slice@.subrange(0, (slice@.len() - 1) as int), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_last_chunk
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:447
// signature: pub const fn split_last_chunk<const N: usize>(&self) -> Option<(&[T], &[T; N])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some((chunk, rem)), array_view(chunk) is the exact suffix length-N subrange and rem@ is the complementary subrange
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk/det_harness.rs
// target_binding_result: target core::slice::split_last_chunk bound from inventory declaration core:61068 at core/src/slice/mod.rs:447
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::split_last_chunk::<N> ]( slice: &[T], ) -> (ret: Option<(&[T], &[T; N])>) ensures (N as int) <= slice@.len() ==> ret.is_some() && ret.unwrap().0@ == slice@.subrange(0, (slice@.len() - N) as int) && array_ref_view(ret.unwrap().1) == slice_fixed_suffix::<T, N>(slice@), (N as int) > slice@.len() ==> ret.is_none(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_last_chunk_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:478
// signature: pub const fn split_last_chunk_mut<const N: usize>( &mut self, ) -> Option<(&mut [T], &mut [T; N])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() <==> old(self)@.len() >= N; when Some((chunk, rem)), array_view(chunk) is the exact suffix length-N subrange and rem@ is the complementary subrange; final(self)@ == final(chunk/rem pieces concatenated in source order)
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_chunk_mut/det_harness.rs
// target_binding_result: target core::slice::split_last_chunk_mut bound from inventory declaration core:61069 at core/src/slice/mod.rs:478
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <const N: usize>
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T, const N: usize>[ <[T]>::split_last_chunk_mut::<N> ]( slice: &mut [T], ) -> (ret: Option<(&mut [T], &mut [T; N])>) ensures (N as int) <= old(slice)@.len() ==> ret.is_some() && ret.unwrap().0@ == old(slice)@.subrange(0, (old(slice)@.len() - N) as int) && array_mut_ref_view(ret.unwrap().1) == slice_fixed_suffix::<T, N>(old(slice)@) && final(slice)@ == final(ret.unwrap().0)@ + array_value_view(*final(ret.unwrap().1)), (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_last_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:262
// signature: pub const fn split_last_mut(&mut self) -> Option<(&mut T, &mut [T])>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_none() <==> old(self)@.len() == 0; when Some((last, init)), *last == old(self)@[old(self)@.len()-1] and init@ == old(self)@.subrange(0, old(self)@.len()-1); final(self)@ == final(init)@ + seq![*final(last)]
// shared_helpers: Seq subrange/chunk partition and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_last_mut/det_harness.rs
// target_binding_result: target core::slice::split_last_mut bound from inventory declaration core:61061 at core/src/slice/mod.rs:262
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::split_last_mut ]( slice: &mut [T], ) -> (ret: Option<(&mut T, &mut [T])>) ensures old(slice)@.len() == 0 ==> ret.is_none() && final(slice)@ == old(slice)@, old(slice)@.len() != 0 ==> ret.is_some() && *ret.unwrap().0 == old(slice)@[(old(slice)@.len() - 1) as int] && ret.unwrap().1@ == old(slice)@.subrange(0, (old(slice)@.len() - 1) as int) && final(slice)@ == final(ret.unwrap().1)@ + seq![*final(ret.unwrap().0)], ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2269
// signature: pub fn split_mut<F>(&mut self, pred: F) -> SplitMut<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, forward non-inclusive predicate partition state, predicate observations, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_mut/det_harness.rs
// target_binding_result: target core::slice::split_mut bound from inventory declaration core:33536 at core/src/slice/mod.rs:2269
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::split_mut::<F> ]( slice: &'a mut [T], pred: F, ) -> (iter: core::slice::SplitMut<'a, T, F>) ensures slice_predicate_split_view::<core::slice::SplitMut<'a, T, F>, F, T>( iter, old(slice)@, pred, false, false, 0, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:4913
// signature: pub fn split_off<'a, R: OneSidedRange<usize>>( self: &mut &'a Self, range: R, ) -> Option<&'a Self>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None leaves the slice reference unchanged; Some return and final slice reference form a prefix/suffix partition of old(*self)@
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off/det_harness.rs
// target_binding_result: target core::slice::split_off bound from inventory declaration core:61136 at core/src/slice/mod.rs:4913
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, R: OneSidedRange<usize>>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[ <[T]>::split_off::<R> ]( slice_ref: &mut &'a [T], range: R, ) -> (ret: Option<&'a [T]>) ensures ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@, ret.is_some() ==> slice_split_off_partition::<T>( (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off_first
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:5017
// signature: pub const fn split_off_first<'a>(self: &mut &'a Self) -> Option<&'a T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None iff old(*self)@ is empty; Some returns the old first element and final slice reference is the old tail
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first/det_harness.rs
// target_binding_result: target core::slice::split_off_first bound from inventory declaration core:61138 at core/src/slice/mod.rs:5017
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::split_off_first ]( slice_ref: &mut &'a [T], ) -> (ret: Option<&'a T>) ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && (*final(slice_ref))@ == (*old(slice_ref))@, (*old(slice_ref))@.len() != 0 ==> ret.is_some() && slice_split_off_first_result::<T>( (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(), ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off_first_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:5042
// signature: pub const fn split_off_first_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None iff old(*self)@ is empty; Some returns the old first element, final slice reference is the old tail, and final(return) composes with the tail length
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_first_mut/det_harness.rs
// target_binding_result: target core::slice::split_off_first_mut bound from inventory declaration core:61139 at core/src/slice/mod.rs:5042
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::split_off_first_mut ]( slice_ref: &mut &'a mut [T], ) -> (ret: Option<&'a mut T>) ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && (*final(slice_ref))@ == (*old(slice_ref))@, (*old(slice_ref))@.len() != 0 ==> ret.is_some() && slice_split_off_first_result::<T>( (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(), ) && (seq![*final(ret.unwrap())] + (*final(slice_ref))@).len() == (*old(slice_ref))@.len(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off_last
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:5067
// signature: pub const fn split_off_last<'a>(self: &mut &'a Self) -> Option<&'a T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None iff old(*self)@ is empty; Some returns the old last element and final slice reference is the old prefix
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last/det_harness.rs
// target_binding_result: target core::slice::split_off_last bound from inventory declaration core:61140 at core/src/slice/mod.rs:5067
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::split_off_last ]( slice_ref: &mut &'a [T], ) -> (ret: Option<&'a T>) ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && (*final(slice_ref))@ == (*old(slice_ref))@, (*old(slice_ref))@.len() != 0 ==> ret.is_some() && slice_split_off_last_result::<T>( (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(), ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off_last_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:5092
// signature: pub const fn split_off_last_mut<'a>(self: &mut &'a mut Self) -> Option<&'a mut T>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None iff old(*self)@ is empty; Some returns the old last element, final slice reference is the old prefix, and final(return) composes with the prefix length
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_last_mut/det_harness.rs
// target_binding_result: target core::slice::split_off_last_mut bound from inventory declaration core:61141 at core/src/slice/mod.rs:5092
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T>[ <[T]>::split_off_last_mut ]( slice_ref: &mut &'a mut [T], ) -> (ret: Option<&'a mut T>) ensures (*old(slice_ref))@.len() == 0 ==> ret.is_none() && (*final(slice_ref))@ == (*old(slice_ref))@, (*old(slice_ref))@.len() != 0 ==> ret.is_some() && slice_split_off_last_result::<T>( (*old(slice_ref))@, (*final(slice_ref))@, *ret.unwrap(), ) && ((*final(slice_ref))@ + seq![*final(ret.unwrap())]).len() == (*old(slice_ref))@.len(), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::split_off_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:4979
// signature: pub fn split_off_mut<'a, R: OneSidedRange<usize>>( self: &mut &'a mut Self, range: R, ) -> Option<&'a mut Self>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: None leaves the mutable slice reference unchanged; Some return/final(return) and final slice reference form prefix/suffix partitions of old(*self)@
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__split_off_mut/det_harness.rs
// target_binding_result: target core::slice::split_off_mut bound from inventory declaration core:61137 at core/src/slice/mod.rs:4979
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <'a, R: OneSidedRange<usize>>
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, R: core::ops::OneSidedRange<usize>>[ <[T]>::split_off_mut::<R> ]( slice_ref: &mut &'a mut [T], range: R, ) -> (ret: Option<&'a mut [T]>) ensures ret.is_none() ==> (*final(slice_ref))@ == (*old(slice_ref))@, ret.is_some() ==> slice_split_off_partition::<T>( (*old(slice_ref))@, (*final(slice_ref))@, ret.unwrap()@, ), ret.is_some() ==> slice_split_off_partition::<T>( (*old(slice_ref))@, (*final(slice_ref))@, final(ret.unwrap())@, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::splitn
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2419
// signature: pub fn splitn<F>(&self, n: usize, pred: F) -> SplitN<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes source/remaining, empty yielded_prefix/remainder, forward predicate partition state, and n as the split limit
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn/det_harness.rs
// target_binding_result: target core::slice::splitn bound from inventory declaration core:33579 at core/src/slice/mod.rs:2419
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn::<F> ]( slice: &'a [T], n: usize, pred: F, ) -> (iter: core::slice::SplitN<'a, T, F>) ensures slice_predicate_split_view::<core::slice::SplitN<'a, T, F>, F, T>( iter, slice@, pred, false, false, n as int, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::splitn_mut
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:2445
// signature: pub fn splitn_mut<F>(&mut self, n: usize, pred: F) -> SplitNMut<'_, T, F> where F: FnMut(&T) -> bool,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: slice_predicate_split_view fixes old(self)@ source/remaining, empty yielded_prefix/remainder, forward predicate partition state, n as the split limit, and final(self)@ == old(self)@
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn_mut/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn_mut/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__splitn_mut/det_harness.rs
// target_binding_result: target core::slice::splitn_mut bound from inventory declaration core:33599 at core/src/slice/mod.rs:2445
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <F> F: FnMut(&T) -> bool,
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a, T, F: core::ops::FnMut(&T) -> bool>[ <[T]>::splitn_mut::<F> ]( slice: &'a mut [T], n: usize, pred: F, ) -> (iter: core::slice::SplitNMut<'a, T, F>) ensures slice_predicate_split_view::<core::slice::SplitNMut<'a, T, F>, F, T>( iter, old(slice)@, pred, false, false, n as int, ), final(slice)@ == old(slice)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::starts_with
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2624
// signature: pub fn starts_with(&self, needle: &[T]) -> bool where T: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: b <==> slice_is_prefix(slice@, needle@)
// shared_helpers: partial_eq_observed bridge plus Seq membership/prefix/suffix helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__starts_with/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__starts_with/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__starts_with/det_harness.rs
// target_binding_result: target core::slice::starts_with bound from inventory declaration core:61099 at core/src/slice/mod.rs:2624
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: PartialEq,
// reviewer_notes: Executable observation assume_specification now uses the shared partial_eq_observed bridge for pairwise prefix matching; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T: core::cmp::PartialEq>[ <[T]>::starts_with ](slice: &[T], needle: &[T]) -> (b: bool) ensures b <==> slice_is_prefix(slice@, needle@);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::strip_circumfix
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2763
// signature: pub fn strip_circumfix<S, P>(&self, prefix: &P, suffix: &S) -> Option<&[T]> where T: PartialEq, S: SlicePattern<Item = T> + ?Sized, P: SlicePattern<Item = T> + ?Sized,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() iff the required prefix/suffix SlicePattern view matches self@; when Some(r), r@ is the exact remaining subrange after removing the matched prefix/suffix/circumfix; when None, no matching prefix/suffix/circumfix relation holds
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and predicate observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_circumfix/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_circumfix/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_circumfix/det_harness.rs
// target_binding_result: target core::slice::strip_circumfix bound from inventory declaration core:61103 at core/src/slice/mod.rs:2763
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <S, P> T: PartialEq, S: SlicePattern<Item = T> + ?Sized, P: SlicePattern<Item = T> + ?Sized,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification< 'a, 'p, 's, T: core::cmp::PartialEq, S: core::slice::SlicePattern<Item = T> + ?Sized, P: core::slice::SlicePattern<Item = T> + ?Sized, >[ <[T]>::strip_circumfix::<S, P> ]( slice: &'a [T], prefix: &'p P, suffix: &'s S, ) -> (ret: Option<&'a [T]>) ensures slice_strip_circumfix_result( slice@, slice_pattern_view::<P, T>(prefix), slice_pattern_view::<S, T>(suffix), ret, ), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::strip_prefix
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2687
// signature: pub fn strip_prefix<P: SlicePattern<Item = T> + ?Sized>(&self, prefix: &P) -> Option<&[T]> where T: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() iff the required prefix/suffix SlicePattern view matches self@; when Some(r), r@ is the exact remaining subrange after removing the matched prefix/suffix/circumfix; when None, no matching prefix/suffix/circumfix relation holds
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and predicate observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_prefix/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_prefix/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_prefix/det_harness.rs
// target_binding_result: target core::slice::strip_prefix bound from inventory declaration core:61101 at core/src/slice/mod.rs:2687
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <P: SlicePattern<Item = T> + ?Sized> T: PartialEq,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification< 'a, 'p, T: core::cmp::PartialEq, P: core::slice::SlicePattern<Item = T> + ?Sized, >[ <[T]>::strip_prefix::<P> ]( slice: &'a [T], prefix: &'p P, ) -> (ret: Option<&'a [T]>) ensures slice_strip_prefix_result(slice@, slice_pattern_view::<P, T>(prefix), ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::strip_suffix
// status: generated-new-real-relation-spec
// family: search-prefix-suffix-ordering
// source: core/src/slice/mod.rs:2723
// signature: pub fn strip_suffix<P: SlicePattern<Item = T> + ?Sized>(&self, suffix: &P) -> Option<&[T]> where T: PartialEq,
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result.is_some() iff the required prefix/suffix SlicePattern view matches self@; when Some(r), r@ is the exact remaining subrange after removing the matched prefix/suffix/circumfix; when None, no matching prefix/suffix/circumfix relation holds
// shared_helpers: Seq membership, prefix/suffix/subrange, sortedness, and predicate observation helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_suffix/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_suffix/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__strip_suffix/det_harness.rs
// target_binding_result: target core::slice::strip_suffix bound from inventory declaration core:61102 at core/src/slice/mod.rs:2723
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: <P: SlicePattern<Item = T> + ?Sized> T: PartialEq,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: #[verifier::allow(undeclared_external_trait)] pub assume_specification< 'a, 'p, T: core::cmp::PartialEq, P: core::slice::SlicePattern<Item = T> + ?Sized, >[ <[T]>::strip_suffix::<P> ]( slice: &'a [T], suffix: &'p P, ) -> (ret: Option<&'a [T]>) ensures slice_strip_suffix_result(slice@, slice_pattern_view::<P, T>(suffix), ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::subslice_range
// status: generated-new-real-relation-spec
// family: raw-pointer-and-provenance
// source: core/src/slice/mod.rs:5321
// signature: pub fn subslice_range(&self, subslice: &[T]) -> Option<core::range::Range<usize>>
// requires: T is not zero-sized, matching the documented panic condition
// ensures: result.is_some() ==> result.unwrap().start <= result.unwrap().end <= self@.len(); when Some(range), subslice@ == self@.subrange(range.start, range.end) and pointer provenance matches self allocation; None means no aligned in-allocation subrange relation is established
// shared_helpers: slice Seq/View plus pointer provenance, length, alignment, and unsafe-domain helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=raw-pointer-provenance-boundary; unknown_review_reason=pointer address, provenance, alignment, or layout state is source-observable but not uniquely recoverable from the pure slice Seq view; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__subslice_range/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__subslice_range/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__subslice_range/det_harness.rs
// target_binding_result: target core::slice::subslice_range bound from inventory declaration core:61144 at core/src/slice/mod.rs:5321
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::subslice_range ]( slice: &[T], subslice: &[T], ) -> (ret: Option<core::range::Range<usize>>) ensures ret.is_some() ==> slice_subslice_range_result(slice@, subslice@, ret.unwrap()), ret.is_none() ==> !slice_subslice_in_domain(slice@, subslice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::swap
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:908
// signature: pub const fn swap(&mut self, a: usize, b: usize)
// requires: a < old(slice)@.len() and b < old(slice)@.len()
// ensures: final(slice)@ == slice_swapped(old(slice)@, a as int, b as int)
// shared_helpers: slice_swapped Seq update transformer over old/final slice views
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap/det_harness.rs
// target_binding_result: target core::slice::swap bound from inventory declaration core:61078 at core/src/slice/mod.rs:908
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::swap ](slice: &mut [T], a: usize, b: usize) requires a < old(slice)@.len(), b < old(slice)@.len() ensures final(slice)@ == slice_swapped(old(slice)@, a as int, b as int);
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::swap_with_slice
// status: generated-new-real-relation-spec
// family: mutation-frame-and-permutation
// source: core/src/slice/mod.rs:4429
// signature: pub const fn swap_with_slice(&mut self, other: &mut [T])
// requires: old(slice)@.len() == old(other)@.len()
// ensures: final(slice)@ == old(other)@ and final(other)@ == old(slice)@
// shared_helpers: old/final paired-slice frame relation
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_observation_mutation_batch.rs --no-verify; harness=verification/harnesses/slice_observation_mutation_batch.rs; stdout=verification/evidence/slice_observation_mutation_batch.verus.stdout(empty); stderr=verification/evidence/slice_observation_mutation_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap_with_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap_with_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__swap_with_slice/det_harness.rs
// target_binding_result: target core::slice::swap_with_slice bound from inventory declaration core:61129 at core/src/slice/mod.rs:4429
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable mutation assume_specification wired through specs/slice_shared_vocabulary.rs; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<T>[ <[T]>::swap_with_slice ](slice: &mut [T], other: &mut [T]) requires old(slice)@.len() == old(other)@.len() ensures final(slice)@ == old(other)@, final(other)@ == old(slice)@;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::trim_ascii
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:308
// signature: pub const fn trim_ascii(&self) -> &[u8]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@ is a subrange of self@; removed prefix/suffix bytes are exactly ascii whitespace; boundary bytes of result, if any, are not ascii whitespace
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii/det_harness.rs
// target_binding_result: target core::slice::trim_ascii bound from inventory declaration core:61054 at core/src/slice/ascii.rs:308
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::trim_ascii ]( slice: &[u8], ) -> (ret: &[u8]) ensures ascii_trim_result(slice@, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::trim_ascii_end
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:274
// signature: pub const fn trim_ascii_end(&self) -> &[u8]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@ is a subrange of self@; removed prefix/suffix bytes are exactly ascii whitespace; boundary bytes of result, if any, are not ascii whitespace
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_end/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_end/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_end/det_harness.rs
// target_binding_result: target core::slice::trim_ascii_end bound from inventory declaration core:61053 at core/src/slice/ascii.rs:274
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::trim_ascii_end ]( slice: &[u8], ) -> (ret: &[u8]) ensures ascii_trim_end_result(slice@, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::trim_ascii_start
// status: generated-new-real-relation-spec
// family: ascii-byte-sequence
// source: core/src/slice/ascii.rs:241
// signature: pub const fn trim_ascii_start(&self) -> &[u8]
// requires: none beyond documented Rust panic/unsafe domains
// ensures: result@ is a subrange of self@; removed prefix/suffix bytes are exactly ascii whitespace; boundary bytes of result, if any, are not ascii whitespace
// shared_helpers: Source-backed Seq<u8> ASCII classification, case-map, and trim boundary/subrange helpers; EscapeAscii byte expansion remains an iterator-formatting boundary
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNSAT; r0_z3=unsat; classification=complete; verus_rc=0; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_start/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_start/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__trim_ascii_start/det_harness.rs
// target_binding_result: target core::slice::trim_ascii_start bound from inventory declaration core:61051 at core/src/slice/ascii.rs:241
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: ASCII case and trim contracts now use source-backed shared byte-range and whitespace-boundary vocabulary from core/src/slice/ascii.rs; escape_ascii preserves the remaining iterator-formatting boundary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification[ <[u8]>::trim_ascii_start ]( slice: &[u8], ) -> (ret: &[u8]) ensures ascii_trim_start_result(slice@, ret), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::utf8_chunks
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/str/lossy.rs:45
// signature: pub fn utf8_chunks(&self) -> Utf8Chunks<'_>
// requires: none beyond documented Rust panic/unsafe domains
// ensures: utf8_chunk_partition(result, self@) ties the Utf8Chunks iterator source and remaining bytes to self@
// shared_helpers: Seq subrange/chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator remaining-sequence helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__utf8_chunks/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__utf8_chunks/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__utf8_chunks/det_harness.rs
// target_binding_result: target core::slice::utf8_chunks bound from inventory declaration core:34438 at core/src/str/lossy.rs:45
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: medium: executable Verus typechecked; feedback-pipeline determinism result recorded in determinism_result
// contract_text: pub assume_specification<'a>[ <[u8]>::utf8_chunks ]( slice: &'a [u8], ) -> (iter: core::str::Utf8Chunks<'a>) ensures utf8_chunk_partition::<core::str::Utf8Chunks<'a>>(iter, slice@), ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::windows
// status: generated-new-real-relation-spec
// family: iterator-splitting-and-chunking
// source: core/src/slice/mod.rs:1118
// signature: pub const fn windows(&self, size: usize) -> Windows<'_, T>
// requires: size != 0
// ensures: slice_iterator_view(result) records self@ as source/remaining, empty yielded_prefix and remainder, window size, and forward overlapping-window state
// shared_helpers: Seq source/remaining/remainder/yielded-prefix state, exact chunk partition, predicate split, adjacent chunk_by, split_off, utf8 chunk, and iterator helpers
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_splitting_iterator_batch.rs --no-verify; harness=verification/harnesses/slice_splitting_iterator_batch.rs; stdout=verification/evidence/slice_splitting_iterator_batch.verus.stdout(empty); stderr=verification/evidence/slice_splitting_iterator_batch.verus.stderr(empty); static-contract-shape-check retained with executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=iterator-or-subslice-state-boundary; unknown_review_reason=contract fixes source/remaining/subrange state, but the Rust iterator, chunk, split, or borrowed subslice value retains opaque runtime/lifetime state; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__windows/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__windows/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__windows/det_harness.rs
// target_binding_result: target core::slice::windows bound from inventory declaration core:29161 at core/src/slice/mod.rs:1118
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: none
// reviewer_notes: Executable splitting/chunk/iterator assume_specification wired through shared split, array, chunk-partition, and iterator-view vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, T>[ <[T]>::windows ]( slice: &'a [T], size: usize, ) -> (iter: core::slice::Windows<'a, T>) requires size != 0, ensures slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).source == slice@, slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remaining == slice@, slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).yielded_prefix.len() == 0, slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).remainder.len() == 0, slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).chunk_size == size as int, !slice_iterator_view::<core::slice::Windows<'a, T>, T>(iter).reverse, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::write_clone_of_slice
// status: generated-new-real-relation-spec
// family: maybe-uninit-slice-storage
// source: core/src/mem/maybe_uninit.rs:1223
// signature: pub fn write_clone_of_slice(&mut self, src: &[T]) -> &mut [T] where T: Clone,
// requires: old(self)@.len() == src@.len()
// ensures: result@ == src@; final(self)@ is initialized at every index and maybe_uninit_written_from(final(self)@, src@) holds
// shared_helpers: MaybeUninit initialization/raw-storage view plus old/final write-frame helper
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=maybeuninit-storage-boundary; unknown_review_reason=MaybeUninit initialization/storage state is modeled relationally through a raw-storage view and cannot be collapsed to one unique concrete value; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_clone_of_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_clone_of_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_clone_of_slice/det_harness.rs
// target_binding_result: target core::slice::write_clone_of_slice bound from inventory declaration core:61027 at core/src/mem/maybe_uninit.rs:1223
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Clone,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, 'b, T: core::clone::Clone>[ <[core::mem::MaybeUninit<T>]>::write_clone_of_slice ]( slice: &'a mut [core::mem::MaybeUninit<T>], src: &'b [T], ) -> (ret: &'a mut [T]) requires old(slice)@.len() == src@.len(), ensures ret@ == src@, maybe_uninit_written_from( maybe_uninit_seq_relation(old(slice)@), maybe_uninit_seq_relation(final(slice)@), src@, ), maybe_uninit_seq_relation(final(slice)@).values == final(ret)@, ;
// END SLICE_SPEC
// BEGIN SLICE_SPEC target=core::slice::write_copy_of_slice
// status: generated-new-real-relation-spec
// family: maybe-uninit-slice-storage
// source: core/src/mem/maybe_uninit.rs:1163
// signature: pub const fn write_copy_of_slice(&mut self, src: &[T]) -> &mut [T] where T: Copy,
// requires: old(self)@.len() == src@.len()
// ensures: result@ == src@; final(self)@ is initialized at every index and maybe_uninit_written_from(final(self)@, src@) holds
// shared_helpers: MaybeUninit initialization/raw-storage view plus old/final write-frame helper
// typecheck_result: verus-typecheck: pass; rc=0; command=/home/chentianyu/nanvix-rust-std-spec-survey/verus/source/target-verus/release/verus verification/harnesses/slice_remaining_families_batch.rs --no-verify; harness=verification/harnesses/slice_remaining_families_batch.rs; stdout=verification/evidence/slice_remaining_families_batch.verus.stdout(empty); stderr=verification/evidence/slice_remaining_families_batch.verus.stderr(empty); executable declaration present
// determinism_result: feedback-pipeline determinism: status=ok; R0=UNKNOWN; r0_z3=unknown; classification=ok_inconclusive; unknown_reason=maybeuninit-storage-boundary; unknown_review_reason=MaybeUninit initialization/storage state is modeled relationally through a raw-storage view and cannot be collapsed to one unique concrete value; verus_rc=1; evidence=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_copy_of_slice/result.json; synthetic=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_copy_of_slice/synthetic_spec.rs; harness=verification/evidence/slice_feedback_determinism/all-20260811T1142Z-comparator-ordering-refresh/core__slice__write_copy_of_slice/det_harness.rs
// target_binding_result: target core::slice::write_copy_of_slice bound from inventory declaration core:61029 at core/src/mem/maybe_uninit.rs:1163
// signature_shape_result: signature mirrored from inventory row and source declaration
// generic_bounds_result: T: Copy,
// reviewer_notes: Executable remaining-family assume_specification wired through shared sorting/comparator, ASCII, raw pointer/provenance, SliceIndex, fixed-array flattening, and MaybeUninit vocabulary; feedback-pipeline determinism result recorded in determinism_result.
// contract_text: pub assume_specification<'a, 'b, T: core::marker::Copy>[ <[core::mem::MaybeUninit<T>]>::write_copy_of_slice ]( slice: &'a mut [core::mem::MaybeUninit<T>], src: &'b [T], ) -> (ret: &'a mut [T]) requires old(slice)@.len() == src@.len(), ensures ret@ == src@, maybe_uninit_written_from( maybe_uninit_seq_relation(old(slice)@), maybe_uninit_seq_relation(final(slice)@), src@, ), maybe_uninit_seq_relation(final(slice)@).values == final(ret)@, ;
// END SLICE_SPEC
