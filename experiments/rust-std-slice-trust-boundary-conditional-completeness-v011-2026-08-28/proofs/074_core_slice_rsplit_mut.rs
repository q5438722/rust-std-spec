#![allow(dead_code, unused_imports, unused_variables)]
// Generated source-backed constructor model for core::slice::rsplit_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub address: int,
    pub allocation: int,
    pub provenance: int,
    pub borrow: int,
    pub element_size: nat,
}

pub open spec fn same_slice(left: SliceIdentity, right: SliceIdentity) -> bool {
    left.source == right.source
        && left.start == right.start
        && left.address == right.address
        && left.allocation == right.allocation
        && left.provenance == right.provenance
        && left.borrow == right.borrow
        && left.element_size == right.element_size
}

// Target proof prefix: rsplit_mut
pub ghost struct PredicateSnapshot {
    pub identity: int,
    pub state: int,
}

pub uninterp spec fn predicate_observed(
    predicate_identity: int,
    value: int,
) -> bool;

pub ghost struct Input {
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
}

pub ghost struct MutableIterator {
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
    pub source: Seq<int>,
    pub remaining: Seq<int>,
    pub yielded_prefix: Seq<int>,
    pub remainder: Seq<int>,
    pub limit: nat,
    pub reverse: bool,
    pub finished: bool,
    pub inclusive: bool,
    pub callback_calls: nat,
}

pub ghost struct FinalState {
    pub slice: SliceIdentity,
    pub predicate_identity: int,
    pub predicate_state: int,
    pub callback_calls: nat,
}

pub open spec fn same_predicate(
    left: PredicateSnapshot,
    right: PredicateSnapshot,
) -> bool {
    left.identity == right.identity && left.state == right.state
}

pub open spec fn output_transition(input: Input, iter: MutableIterator) -> bool {
    same_slice(iter.slice, input.slice)
        && same_predicate(iter.predicate, input.predicate)
        && iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.limit == 0
        && iter.reverse == true
        && iter.finished == false
        && iter.inclusive == false
        && iter.callback_calls == 0
}

pub ghost struct SplitMutStorage {
    pub slice: SliceIdentity,
    pub predicate: PredicateSnapshot,
    pub finished: bool,
}

pub ghost struct RSplitMutStorage {
    pub inner: SplitMutStorage,
}

pub open spec fn split_mut_new(input: Input) -> SplitMutStorage {
    SplitMutStorage {
        slice: input.slice,
        predicate: input.predicate,
        finished: false,
    }
}

pub open spec fn rsplit_mut_new(input: Input) -> RSplitMutStorage {
    RSplitMutStorage {
        inner: split_mut_new(input),
    }
}

pub open spec fn project_rsplit_mut(
    storage: RSplitMutStorage,
) -> MutableIterator {
    MutableIterator {
        slice: storage.inner.slice,
        predicate: storage.inner.predicate,
        source: storage.inner.slice.source,
        remaining: storage.inner.slice.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        limit: 0,
        reverse: true,
        finished: storage.inner.finished,
        inclusive: false,
        callback_calls: 0,
    }
}

pub proof fn rsplit_mut_flat_projection(input: Input)
    ensures
        output_transition(
            input,
            project_rsplit_mut(rsplit_mut_new(input)),
        ),
{
    reveal(output_transition);
    reveal(same_slice);
    reveal(same_predicate);
}

pub open spec fn active_contract(input: Input, iter: MutableIterator) -> bool {
    iter.source == input.slice.source
        && iter.remaining == input.slice.source
        && iter.yielded_prefix == Seq::<int>::empty()
        && iter.remainder == Seq::<int>::empty()
        && iter.limit == 0
        && iter.reverse == true
        && iter.yielded_prefix + iter.remaining == input.slice.source
        && forall|i: int|
            #![trigger predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )]
            0 <= i < input.slice.source.len()
            ==> (predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                )
                || !predicate_observed(
                    input.predicate.identity,
                    input.slice.source[i],
                ))
}

pub open spec fn final_state_transition(
    input: Input,
    state: FinalState,
) -> bool {
    same_slice(state.slice, input.slice)
        && state.predicate_identity == input.predicate.identity
        && state.predicate_state == input.predicate.state
        && state.callback_calls == 0
}

pub open spec fn target_transition(
    input: Input,
    iter: MutableIterator,
    state: FinalState,
) -> bool {
    output_transition(input, iter)
        && active_contract(input, iter)
        && final_state_transition(input, state)
}

pub proof fn rsplit_mut_constructor(
    input: Input,
) -> (ret: MutableIterator)
    ensures
        output_transition(input, ret),
        active_contract(input, ret),
{
    rsplit_mut_flat_projection(input);
    let ret = project_rsplit_mut(rsplit_mut_new(input));
    reveal(active_contract);
    assert(Seq::<int>::empty() + input.slice.source == input.slice.source);
    assert forall|i: int|
        #![trigger predicate_observed(
            input.predicate.identity,
            input.slice.source[i],
        )]
        0 <= i < input.slice.source.len() implies
        (predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )
            || !predicate_observed(
                input.predicate.identity,
                input.slice.source[i],
            )) by {{}}

    ret
}

pub open spec fn exact_equivalent(
    left: MutableIterator,
    left_state: FinalState,
    right: MutableIterator,
    right_state: FinalState,
) -> bool {
    same_slice(left.slice, right.slice)
        && same_predicate(left.predicate, right.predicate)
        && left.source == right.source
        && left.remaining == right.remaining
        && left.yielded_prefix == right.yielded_prefix
        && left.remainder == right.remainder
        && left.limit == right.limit
        && left.reverse == right.reverse
        && left.finished == right.finished
        && left.inclusive == right.inclusive
        && left.callback_calls == right.callback_calls
        && same_slice(left_state.slice, right_state.slice)
        && left_state.predicate_identity == right_state.predicate_identity
        && left_state.predicate_state == right_state.predicate_state
        && left_state.callback_calls == right_state.callback_calls
}

pub proof fn conditional_complete_rsplit_mut(
    input: Input,
    iter1: MutableIterator,
    state1: FinalState,
    iter2: MutableIterator,
    state2: FinalState,
)
    requires
        target_transition(input, iter1, state1),
        target_transition(input, iter2, state2),
    ensures
        exact_equivalent(iter1, state1, iter2, state2),
{
    reveal(target_transition);
    reveal(output_transition);
    reveal(final_state_transition);
    reveal(exact_equivalent);
}

} // verus!
