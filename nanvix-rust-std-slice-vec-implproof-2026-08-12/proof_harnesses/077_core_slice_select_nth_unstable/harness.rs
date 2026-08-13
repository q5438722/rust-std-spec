#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::select_nth_unstable
// Source: core/src/slice/mod.rs:3516-3521 and core/src/slice/sort/select.rs:17-59
// Source item sha256: dd55bbb0ec8084c8e81b3000133de113a2249b5c57d6ffa845cb5c5348909cd2
// Dependency manifest: proof_manifests/077_core_slice_select_nth_unstable/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(left: T, right: T) -> core::cmp::Ordering;

pub uninterp spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool;

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> int;

pub uninterp spec fn slice_permutation<T>(before: Seq<T>, after: Seq<T>) -> bool;

pub uninterp spec fn slice_select_partition_ord<T: core::cmp::Ord>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
) -> bool;

pub mod sort {
    pub mod select {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{slice_permutation, slice_select_partition_ord};

        #[verifier::external_body]
        pub fn partition_at_index<'a, T: core::cmp::Ord, F>(
            slice: &'a mut [T],
            index: usize,
            is_less: F,
        ) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
            where
                F: FnMut(&T, &T) -> bool,
            requires
                index < old(slice)@.len(),
            ensures
                final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
                final(ret.0)@.len() == index,
                *final(ret.1) == final(slice)@[index as int],
                final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
                slice_permutation(old(slice)@, final(slice)@),
                slice_select_partition_ord(final(ret.0)@, *final(ret.1), final(ret.2)@),
        {
            let (left, right) = slice.split_at_mut(index);
            let (pivot, right) = right.split_at_mut(1);
            let pivot = &mut pivot[0];
            (left, pivot, right)
        }
    }
}

pub fn select_nth_unstable<'a, T: core::cmp::Ord>(
    slice: &'a mut [T],
    index: usize,
) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        *final(ret.1) == final(slice)@[index as int],
        final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_ord(final(ret.0)@, *final(ret.1), final(ret.2)@),
{
    sort::select::partition_at_index(slice, index, T::lt)
}

}
