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
