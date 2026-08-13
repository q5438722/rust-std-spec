#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::select_nth_unstable_by_key
// Source: core/src/slice/mod.rs:3648-3658 and core/src/slice/sort/select.rs:17-59
// Source item sha256: eaf3bba68e8eb20e76011297d8822b6b064bb15d044d8e495442c3c759ffb061
// Dependency manifest: proof_manifests/079_core_slice_select_nth_unstable_by_key/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
}

pub uninterp spec fn ord_cmp_observed<K: core::cmp::Ord>(
    left: K,
    right: K,
) -> core::cmp::Ordering;

pub uninterp spec fn ord_leq_observed<K: core::cmp::Ord>(left: K, right: K) -> bool;

pub uninterp spec fn fnmut_key_observed<F, T, K>(f: F, value: T) -> K;

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> int;

pub uninterp spec fn slice_permutation<T>(before: Seq<T>, after: Seq<T>) -> bool;

pub open spec fn slice_select_partition_key<F, T, K: core::cmp::Ord>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    f: F,
) -> bool {
    (forall|i: int| #![trigger ord_leq_observed(
            fnmut_key_observed::<F, T, K>(f, left[i]),
            fnmut_key_observed::<F, T, K>(f, pivot),
        )]
        0 <= i < left.len()
            ==> ord_leq_observed(
                fnmut_key_observed::<F, T, K>(f, left[i]),
                fnmut_key_observed::<F, T, K>(f, pivot),
            ))
        && (forall|i: int| #![trigger ord_leq_observed(
                fnmut_key_observed::<F, T, K>(f, pivot),
                fnmut_key_observed::<F, T, K>(f, right[i]),
            )]
            0 <= i < right.len()
                ==> ord_leq_observed(
                    fnmut_key_observed::<F, T, K>(f, pivot),
                    fnmut_key_observed::<F, T, K>(f, right[i]),
                ))
}

pub mod sort {
    pub mod select {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{slice_permutation, slice_select_partition_key};

        #[verifier::external_body]
        pub fn partition_at_index_by_key<'a, T, K, F>(
            slice: &'a mut [T],
            index: usize,
            key_fn: F,
        ) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
            where
                F: FnMut(&T) -> K,
                K: core::cmp::Ord,
            requires
                index < old(slice)@.len(),
            ensures
                final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
                final(ret.0)@.len() == index,
                *final(ret.1) == final(slice)@[index as int],
                final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
                slice_permutation(old(slice)@, final(slice)@),
                slice_select_partition_key::<F, T, K>(
                    final(ret.0)@,
                    *final(ret.1),
                    final(ret.2)@,
                    key_fn,
                ),
        {
            let (left, right) = slice.split_at_mut(index);
            let (pivot, right) = right.split_at_mut(1);
            let pivot = &mut pivot[0];
            (left, pivot, right)
        }
    }
}

pub fn select_nth_unstable_by_key<'a, T, K, F>(
    slice: &'a mut [T],
    index: usize,
    mut f: F,
) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
    where
        F: FnMut(&T) -> K,
        K: core::cmp::Ord,
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        *final(ret.1) == final(slice)@[index as int],
        final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_key::<F, T, K>(
            final(ret.0)@,
            *final(ret.1),
            final(ret.2)@,
            f,
        ),
{
    sort::select::partition_at_index_by_key(slice, index, f)
}

}
