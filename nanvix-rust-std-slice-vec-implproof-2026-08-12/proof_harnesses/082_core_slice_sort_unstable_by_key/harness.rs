#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::sort_unstable_by_key
// Source: core/src/slice/mod.rs:3240-3246 and core/src/slice/sort/unstable/mod.rs
// Source item sha256: a1709e9e61a25c52c3235a85bf2c15daf80785ec749e7f9bed299596413c074e
// Dependency manifest: proof_manifests/082_core_slice_sort_unstable_by_key/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct KeyObservation<T> {
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

pub uninterp spec fn ord_cmp_observed<K: core::cmp::Ord>(
    left: K,
    right: K,
) -> core::cmp::Ordering;

pub open spec fn ord_leq_observed<K: core::cmp::Ord>(left: K, right: K) -> bool {
    ordering_rank(ord_cmp_observed(left, right)) <= 0
}

pub uninterp spec fn key_observation<F, T, K>(
    f: F,
    domain: Seq<T>,
) -> KeyObservation<T>;

pub uninterp spec fn key_observed<T, K: core::cmp::Ord>(
    observation: KeyObservation<T>,
    value: T,
) -> K;

pub uninterp spec fn fnmut_key_observed<F, T, K>(f: F, value: T) -> K;

pub uninterp spec fn slice_multiplicity<T>(seq: Seq<T>, value: T) -> int;

pub uninterp spec fn slice_permutation<T>(before: Seq<T>, after: Seq<T>) -> bool;

pub uninterp spec fn slice_sorted_by_key<F, T, K: core::cmp::Ord>(
    seq: Seq<T>,
    f: F,
) -> bool;

pub open spec fn slice_sorted_by_key_observed<T, K: core::cmp::Ord>(
    seq: Seq<T>,
    observation: KeyObservation<T>,
) -> bool {
    forall|i: int, j: int| #![trigger ord_leq_observed(
            key_observed::<T, K>(observation, seq[i]),
            key_observed::<T, K>(observation, seq[j]),
        )]
        0 <= i && i <= j && j < seq.len()
            ==> ord_leq_observed(
                key_observed::<T, K>(observation, seq[i]),
                key_observed::<T, K>(observation, seq[j]),
            )
}

pub broadcast axiom fn axiom_key_observation_domain<F, T, K>(f: F, domain: Seq<T>)
    ensures
        #[trigger] key_observation::<F, T, K>(f, domain).domain == domain,
;

pub broadcast axiom fn axiom_key_observation_sorted_bridge<F, T, K: core::cmp::Ord>(
    f: F,
    domain: Seq<T>,
    seq: Seq<T>,
)
    ensures
        #[trigger] slice_sorted_by_key_observed::<T, K>(
            seq,
            key_observation::<F, T, K>(f, domain),
        ) ==> slice_sorted_by_key::<F, T, K>(seq, f),
;

pub mod sort {
    pub mod unstable {
        use vstd::prelude::*;
        use vstd::seq::*;
        use super::super::{
            KeyObservation, slice_permutation, slice_sorted_by_key_observed,
        };

        #[verifier::external_body]
        pub fn sort<T, K, F>(
            slice: &mut [T],
            Ghost(observation): Ghost<KeyObservation<T>>,
            f: &mut F,
        )
            where
                F: FnMut(&T) -> K,
                K: core::cmp::Ord,
            requires
                observation.domain == old(slice)@,
            ensures
                slice_permutation(old(slice)@, final(slice)@),
                slice_sorted_by_key_observed::<T, K>(final(slice)@, observation),
        {
        }
    }
}

pub fn sort_unstable_by_key<T, K, F>(slice: &mut [T], mut f: F)
    where
        F: FnMut(&T) -> K,
        K: core::cmp::Ord,
    ensures
        slice_permutation(old(slice)@, final(slice)@),
        slice_sorted_by_key::<F, T, K>(final(slice)@, f),
{
    broadcast use axiom_key_observation_domain;
    broadcast use axiom_key_observation_sorted_bridge;
    let ghost observation = key_observation::<F, T, K>(f, old(slice)@);
    assert(observation.domain == old(slice)@);
    sort::unstable::sort(slice, Ghost(observation), &mut f);
    assert(slice_sorted_by_key_observed::<T, K>(final(slice)@, observation));
}

}
