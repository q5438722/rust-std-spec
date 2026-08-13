#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::select_nth_unstable_by
// Source: core/src/slice/mod.rs:3581-3590 and core/src/slice/sort/select.rs:17-59
// Source item sha256: e747f8a086cd882588cd5afe9b1800c1ec90130423301aef03089f05e5623fca
// Dependency manifest: proof_manifests/078_core_slice_select_nth_unstable_by/dependency_assumption_manifest.json

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

pub open spec fn slice_select_partition_cmp<T>(
    left: Seq<T>,
    pivot: T,
    right: Seq<T>,
    observation: ComparatorObservation<T>,
) -> bool {
    (forall|i: int| #![trigger comparator_leq_observed(observation, left[i], pivot)]
        0 <= i < left.len() ==> comparator_leq_observed(observation, left[i], pivot))
        && (forall|i: int| #![trigger comparator_leq_observed(observation, pivot, right[i])]
            0 <= i < right.len() ==> comparator_leq_observed(observation, pivot, right[i]))
}

pub mod sort {
    pub mod select {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{ComparatorObservation, slice_permutation, slice_select_partition_cmp};

        #[verifier::external_body]
        pub fn partition_at_index_by_compare<'a, T, F>(
            slice: &'a mut [T],
            index: usize,
            Ghost(observation): Ghost<ComparatorObservation<T>>,
            compare: &mut F,
        ) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
            where
                F: FnMut(&T, &T) -> core::cmp::Ordering,
            requires
                index < old(slice)@.len(),
                observation.domain == old(slice)@,
            ensures
                final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
                final(ret.0)@.len() == index,
                *final(ret.1) == final(slice)@[index as int],
                final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
                slice_permutation(old(slice)@, final(slice)@),
                slice_select_partition_cmp(final(ret.0)@, *final(ret.1), final(ret.2)@, observation),
        {
            let (left, right) = slice.split_at_mut(index);
            let (pivot, right) = right.split_at_mut(1);
            let pivot = &mut pivot[0];
            (left, pivot, right)
        }
    }
}

pub fn select_nth_unstable_by<'a, T, F>(
    slice: &'a mut [T],
    index: usize,
    mut compare: F,
) -> (ret: (&'a mut [T], &'a mut T, &'a mut [T]))
    where
        F: FnMut(&T, &T) -> core::cmp::Ordering,
    requires
        index < old(slice)@.len(),
    ensures
        final(slice)@ == final(ret.0)@ + seq![*final(ret.1)] + final(ret.2)@,
        final(ret.0)@.len() == index,
        *final(ret.1) == final(slice)@[index as int],
        final(ret.2)@.len() == old(slice)@.len() - (index as int) - 1,
        slice_permutation(old(slice)@, final(slice)@),
        slice_select_partition_cmp(
            final(ret.0)@,
            *final(ret.1),
            final(ret.2)@,
            comparator_observation(compare, old(slice)@),
        ),
{
    broadcast use axiom_comparator_observation_domain;
    assert(comparator_observation(compare, old(slice)@).domain == old(slice)@);
    sort::select::partition_at_index_by_compare(
        slice,
        index,
        Ghost(comparator_observation(compare, old(slice)@)),
        &mut compare,
    )
}

}
