#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::sort_unstable_by
// Source: core/src/slice/mod.rs:3188-3193 and core/src/slice/sort/unstable/mod.rs
// Source item sha256: 92008bd2d8e9d1bb3d95e3585474f6c372dc276528c919693bdfcfd21f8863ed
// Dependency manifest: proof_manifests/081_core_slice_sort_unstable_by/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct ComparatorObservation<T> {
    pub domain: Seq<T>,
    pub trace_id: int,
}

pub open spec fn ordering_rank(ordering: core::cmp::Ordering) -> int {
    match ordering {
        core::cmp::Ordering::Less => -1,
        core::cmp::Ordering::Equal => 0,
        core::cmp::Ordering::Greater => 1,
    }
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

pub uninterp spec fn comparator_observation<F, T>(
    compare: F,
    domain: Seq<T>,
) -> ComparatorObservation<T>;

pub broadcast axiom fn axiom_comparator_observation_domain<F, T>(compare: F, domain: Seq<T>)
    ensures
        #[trigger] comparator_observation::<F, T>(compare, domain).domain == domain,
;

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> int;

pub uninterp spec fn slice_permutation<T>(before: Seq<T>, after: Seq<T>) -> bool;

pub uninterp spec fn slice_sorted_by_cmp<T>(
    seq: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool;

pub mod sort {
    pub mod unstable {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{ComparatorObservation, slice_permutation, slice_sorted_by_cmp};

        #[verifier::external_body]
        pub fn sort<T, F>(
            slice: &mut [T],
            Ghost(observation): Ghost<ComparatorObservation<T>>,
            compare: &mut F,
        )
            where
                F: FnMut(&T, &T) -> core::cmp::Ordering,
            requires
                observation.domain == old(slice)@,
            ensures
                slice_permutation(old(slice)@, final(slice)@),
                slice_sorted_by_cmp(final(slice)@, observation),
        {
        }
    }
}

pub fn sort_unstable_by<T, F>(slice: &mut [T], mut compare: F)
    where
        F: FnMut(&T, &T) -> core::cmp::Ordering,
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_cmp(final(slice)@, comparator_observation(compare, old(slice)@)),
{
    broadcast use axiom_comparator_observation_domain;
    assert(comparator_observation(compare, old(slice)@).domain == old(slice)@);
    sort::unstable::sort(
        slice,
        Ghost(comparator_observation(compare, old(slice)@)),
        &mut compare,
    );
}

}
