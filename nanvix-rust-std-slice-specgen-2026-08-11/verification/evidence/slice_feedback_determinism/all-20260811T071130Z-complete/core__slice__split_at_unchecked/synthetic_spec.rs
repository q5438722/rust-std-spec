#![allow(unused_imports)]
#![feature(slice_pattern)]
#![feature(strip_circumfix)]
#![feature(substr_range)]
extern crate alloc;
use vstd::prelude::*;
use vstd::seq::*;
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

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> nat;

pub open spec fn slice_permutation<T>(left: Seq<T>, right: Seq<T>) -> bool {
    left.len() == right.len() && forall|value: T|
        slice_multiplicity(left, value) == slice_multiplicity(right, value)
}

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(
    left: T,
    right: T,
) -> core::cmp::Ordering;

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

pub open spec fn slice_sorted_by_ord<T: core::cmp::Ord>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len() ==> ord_leq_observed(seq[i], seq[j])
}

pub uninterp spec fn partial_ord_leq_observed<T: core::cmp::PartialOrd>(left: T, right: T) -> bool;

pub open spec fn slice_sorted_by_partial_ord<T: core::cmp::PartialOrd>(seq: Seq<T>) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len() ==> partial_ord_leq_observed(seq[i], seq[j])
}

pub open spec fn slice_sorted_by_bool_compare<F, T>(seq: Seq<T>, compare: F) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> fnmut_adjacent_predicate_observed(compare, seq[i], seq[j])
}

pub open spec fn slice_sorted_by_partial_key<F, T, K: core::cmp::PartialOrd>(
    seq: Seq<T>,
    f: F,
) -> bool {
    forall|i: int, j: int| 0 <= i <= j < seq.len()
        ==> partial_ord_leq_observed(
            fnmut_key_observed::<F, T, K>(f, seq[i]),
            fnmut_key_observed::<F, T, K>(f, seq[j]),
        )
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
}

pub uninterp spec fn comparator_leq_observed<T>(
    observation: ComparatorObservation<T>,
    left: T,
    right: T,
) -> bool;

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

pub open spec fn slice_chunk_partition<T>(view: SliceIteratorView<T>) -> bool {
    view.chunk_size > 0
        && (view.remainder.len() as int) < view.chunk_size
        && view.yielded_prefix + view.remaining == view.source
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
    view.source == source
        && view.remaining == source
        && view.reverse == reverse
        && view.chunk_size == limit
        && limit >= 0
        && (inclusive || !inclusive)
        && forall|i: int| 0 <= i < source.len()
            ==> (#[trigger] fnmut_predicate_observed(pred, source[i])
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
    view.source == source
        && view.remaining == source
        && forall|i: int| 0 <= i + 1 < source.len()
            ==> (#[trigger] fnmut_adjacent_predicate_observed(pred, source[i], source[i + 1])
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
    view.source == source && view.remaining == source
}

pub uninterp spec fn array_ref_view<T, const N: usize>(array: &[T; N]) -> Seq<T>;

pub uninterp spec fn array_mut_ref_view<T, const N: usize>(array: &mut [T; N]) -> Seq<T>;

pub uninterp spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T>;

pub open spec fn split_point_in_range<T>(seq: Seq<T>, mid: usize) -> bool {
    mid <= seq.len()
}

pub open spec fn slice_fixed_prefix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange(0, N as int)
}

pub open spec fn slice_fixed_suffix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange((seq.len() - N) as int, seq.len() as int)
}

pub uninterp spec fn flatten_array_chunks<T, const N: usize>(chunks: Seq<[T; N]>) -> Seq<T>;

pub uninterp spec fn unflatten_array_chunks<T, const N: usize>(seq: Seq<T>) -> Seq<[T; N]>;

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

pub uninterp spec fn maybe_uninit_storage_relation<T>(
    storage: &[core::mem::MaybeUninit<T>],
) -> MaybeUninitSliceRelation<T>;

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

pub uninterp spec fn maybe_uninit_from_initialized<T>(values: Seq<T>) -> Seq<core::mem::MaybeUninit<T>>;

pub uninterp spec fn ascii_lower_byte(byte: u8) -> u8;

pub uninterp spec fn ascii_upper_byte(byte: u8) -> u8;

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

pub uninterp spec fn ascii_trim_start_index(seq: Seq<u8>) -> int;

pub uninterp spec fn ascii_trim_end_index(seq: Seq<u8>) -> int;

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

pub exec fn __rust_std_candidate<T>(
    slice: &[T],
    mid: usize,
) -> (ret: (&[T], &[T]))
    requires
        split_point_in_range(slice@, mid),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
    { loop { } }
}
