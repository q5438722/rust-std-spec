#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::is_sorted_by
// Source: core/src/slice/mod.rs:4771-4776
// Source item sha256: 1cb452749dadbe91c21b3c460fa9ef9e84b17ffef85eb59c88b3e350f63e8d14
// Dependency manifest: proof_manifests/058_core_slice_is_sorted_by/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

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

pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remaining: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub struct SliceReceiver<'a, T: 'a> {
    slice: &'a [T],
}

pub struct ArrayWindows<'a, T: 'a, const N: usize> {
    v: &'a [T],
}

pub closed spec fn slice_receiver_source<'a, T>(receiver: SliceReceiver<'a, T>) -> Seq<T> {
    receiver.slice@
}

pub closed spec fn slice_iterator_view<'a, T, const N: usize>(
    iter: ArrayWindows<'a, T, N>,
) -> SliceIteratorView<T> {
    SliceIteratorView {
        source: iter.v@,
        yielded_prefix: Seq::empty(),
        remaining: iter.v@,
        remainder: Seq::empty(),
        chunk_size: N as int,
        reverse: false,
    }
}

impl<'a, T, const N: usize> ArrayWindows<'a, T, N> {
    pub fn new(slice: &'a [T]) -> (ret: Self)
        requires
            N != 0,
        ensures
            slice_iterator_view(ret).source == slice@,
            slice_iterator_view(ret).remaining == slice@,
            slice_iterator_view(ret).yielded_prefix.len() == 0,
            slice_iterator_view(ret).remainder.len() == 0,
            slice_iterator_view(ret).chunk_size == N as int,
            !slice_iterator_view(ret).reverse,
    {
        let ret = Self { v: slice };
        proof {
            reveal(slice_iterator_view);
        }
        ret
    }

    #[verifier::external_body]
    pub fn all<F>(self, compare: F) -> (ret: bool)
        where
            F: FnMut(&'a T, &'a T) -> bool,
        requires
            N == 2,
            slice_iterator_view(self).source == slice_iterator_view(self).remaining,
            slice_iterator_view(self).yielded_prefix.len() == 0,
            slice_iterator_view(self).remainder.len() == 0,
            !slice_iterator_view(self).reverse,
        ensures
            slice_sorted_by_bool_compare_result::<F, T>(
                slice_iterator_view(self).source,
                compare,
                ret,
            ),
    {
        false
    }
}

impl<'a, T> SliceReceiver<'a, T> {
    pub fn array_windows<const N: usize>(self) -> (iter: ArrayWindows<'a, T, N>)
        requires
            N != 0,
        ensures
            slice_iterator_view(iter).source == slice_receiver_source(self),
            slice_iterator_view(iter).remaining == slice_receiver_source(self),
            slice_iterator_view(iter).yielded_prefix.len() == 0,
            slice_iterator_view(iter).remainder.len() == 0,
            slice_iterator_view(iter).chunk_size == N as int,
            !slice_iterator_view(iter).reverse,
    {
        assert(N != 0);
        let iter = ArrayWindows::new(self.slice);
        proof {
            reveal(slice_receiver_source);
            reveal(slice_iterator_view);
        }
        iter
    }
}

pub fn is_sorted_by<'a, T: 'a, F>(
    slice: &'a [T],
    compare: F,
) -> (ret: bool)
    where
        F: FnMut(&'a T, &'a T) -> bool,
    ensures
        slice_sorted_by_bool_compare_result::<F, T>(slice@, compare, ret),
{
    let self_slice = SliceReceiver { slice };
    let windows = self_slice.array_windows::<2>();
    proof {
        reveal(slice_receiver_source);
        reveal(slice_iterator_view);
    }
    windows.all(compare)
}

}
