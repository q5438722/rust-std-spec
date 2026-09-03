#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::sort_unstable
// Source: core/src/slice/mod.rs:3133-3138 and core/src/slice/sort/unstable/mod.rs
// Source item sha256: 5154b661dcc16f24263c4b635e0888ffc4be3015e2838c800eab883b6f352be6
// Dependency manifest: proof_manifests/080_core_slice_sort_unstable/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn ord_cmp_observed<T: core::cmp::Ord>(left: T, right: T) -> core::cmp::Ordering;

pub uninterp spec fn ord_leq_observed<T: core::cmp::Ord>(left: T, right: T) -> bool;

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> int;

pub uninterp spec fn slice_permutation<T>(before: Seq<T>, after: Seq<T>) -> bool;

pub uninterp spec fn slice_sorted_by_ord<T: core::cmp::Ord>(seq: Seq<T>) -> bool;

pub mod sort {
    pub mod unstable {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{slice_permutation, slice_sorted_by_ord};

        #[verifier::external_body]
        pub fn sort<T: core::cmp::Ord, F>(slice: &mut [T], is_less: &mut F)
            where
                F: FnMut(&T, &T) -> bool,
            ensures
                slice_permutation(old(slice)@, final(slice)@),
                slice_sorted_by_ord(final(slice)@),
        {
        }
    }
}

pub fn sort_unstable<T: core::cmp::Ord>(slice: &mut [T])
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_ord(final(slice)@),
{
    sort::unstable::sort(slice, &mut T::lt);
}

}
