#![allow(dead_code, unused_imports, unused_variables)]
// Experiment-local source constructor model for core::slice::splitn_mut.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIdentity {
    pub source: Seq<int>,
    pub start: int,
    pub allocation: int,
    pub borrow: int,
}

pub ghost struct PredicateSnapshot {
    pub identity: int,
    pub state: int,
}

pub ghost struct SplitMut {
    pub v: SliceIdentity,
    pub pred: PredicateSnapshot,
    pub finished: bool,
    pub callback_calls: nat,
}

pub ghost struct GenericSplitN {
    pub iter: SplitMut,
    pub count: nat,
}

pub ghost struct SplitNMut {
    pub inner: GenericSplitN,
}

pub ghost struct SliceIteratorView {
    pub source: Seq<int>,
    pub remaining: Seq<int>,
    pub yielded_prefix: Seq<int>,
    pub remainder: Seq<int>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub ghost struct FinalState {
    pub slice: SliceIdentity,
    pub predicate_identity: int,
    pub predicate_state: int,
    pub callback_calls: nat,
}

pub uninterp spec fn fnmut_predicate_observed(
    predicate_identity: int,
    value: int,
) -> bool;

pub open spec fn same_slice_identity(left: SliceIdentity, right: SliceIdentity) -> bool {
    left.source == right.source
        && left.start == right.start
        && left.allocation == right.allocation
        && left.borrow == right.borrow
}

pub open spec fn same_predicate(
    left: PredicateSnapshot,
    right: PredicateSnapshot,
) -> bool {
    left.identity == right.identity && left.state == right.state
}

impl SplitMut {
    pub proof fn new(
        slice: SliceIdentity,
        pred: PredicateSnapshot,
    ) -> (ret: SplitMut)
        ensures
            same_slice_identity(ret.v, slice),
            same_predicate(ret.pred, pred),
            !ret.finished,
            ret.callback_calls == 0,
    {
        SplitMut {
            v: slice,
            pred,
            finished: false,
            callback_calls: 0,
        }
    }
}

impl SplitNMut {
    pub proof fn new(s: SplitMut, n: nat) -> (ret: SplitNMut)
        ensures
            same_slice_identity(ret.inner.iter.v, s.v),
            same_predicate(ret.inner.iter.pred, s.pred),
            ret.inner.iter.finished == s.finished,
            ret.inner.iter.callback_calls == s.callback_calls,
            ret.inner.count == n,
    {
        SplitNMut {
            inner: GenericSplitN { iter: s, count: n },
        }
    }
}

pub proof fn split_mut(
    slice: SliceIdentity,
    pred: PredicateSnapshot,
) -> (ret: SplitMut)
    ensures
        same_slice_identity(ret.v, slice),
        same_predicate(ret.pred, pred),
        !ret.finished,
        ret.callback_calls == 0,
{
    SplitMut::new(slice, pred)
}

pub open spec fn slice_iterator_view(iter: SplitNMut) -> SliceIteratorView {
    SliceIteratorView {
        source: iter.inner.iter.v.source,
        remaining: iter.inner.iter.v.source,
        yielded_prefix: Seq::empty(),
        remainder: Seq::empty(),
        chunk_size: iter.inner.count as int,
        reverse: false,
    }
}

pub open spec fn slice_iterator_well_formed(view: SliceIteratorView) -> bool {
    0 <= view.chunk_size && view.remainder.len() <= view.source.len()
}

pub open spec fn slice_predicate_split_view(
    iter: SplitNMut,
    source: Seq<int>,
    pred: PredicateSnapshot,
    inclusive: bool,
    reverse: bool,
    limit: int,
) -> bool {
    let view = slice_iterator_view(iter);
    slice_iterator_well_formed(view)
        && view.source == source
        && view.remaining == source
        && view.yielded_prefix == Seq::empty()
        && view.remainder == Seq::empty()
        && view.reverse == reverse
        && view.chunk_size == limit
        && limit >= 0
        && !inclusive
        && same_predicate(iter.inner.iter.pred, pred)
        && !iter.inner.iter.finished
        && iter.inner.iter.callback_calls == 0
        && (if reverse {
            view.remaining + view.yielded_prefix == source
        } else {
            view.yielded_prefix + view.remaining == source
        })
        && forall|i: int| #![trigger fnmut_predicate_observed(pred.identity, source[i])]
            0 <= i < source.len()
            ==> (fnmut_predicate_observed(pred.identity, source[i])
                || !fnmut_predicate_observed(pred.identity, source[i]))
}

pub proof fn splitn_mut(
    slice: SliceIdentity,
    n: nat,
    pred: PredicateSnapshot,
) -> (ret: SplitNMut)
    ensures
        same_slice_identity(ret.inner.iter.v, slice),
        same_predicate(ret.inner.iter.pred, pred),
        !ret.inner.iter.finished,
        ret.inner.iter.callback_calls == 0,
        ret.inner.count == n,
        slice_predicate_split_view(ret, slice.source, pred, false, false, n as int),
{
    let split = split_mut(slice, pred);
    let ret = SplitNMut::new(split, n);
    reveal(slice_iterator_view);
    reveal(slice_predicate_split_view);
    reveal(slice_iterator_well_formed);
    assert(Seq::<int>::empty() + slice.source == slice.source);
    assert forall|i: int|
        #![trigger fnmut_predicate_observed(pred.identity, slice.source[i])]
        0 <= i < slice.source.len() implies
        (fnmut_predicate_observed(pred.identity, slice.source[i])
            || !fnmut_predicate_observed(pred.identity, slice.source[i])) by {}
    ret
}

pub open spec fn constructor_transition(
    slice: SliceIdentity,
    pred: PredicateSnapshot,
    n: nat,
    iter: SplitNMut,
    final_state: FinalState,
) -> bool {
    same_slice_identity(iter.inner.iter.v, slice)
        && same_predicate(iter.inner.iter.pred, pred)
        && !iter.inner.iter.finished
        && iter.inner.iter.callback_calls == 0
        && iter.inner.count == n
        && slice_predicate_split_view(iter, slice.source, pred, false, false, n as int)
        && same_slice_identity(final_state.slice, slice)
        && final_state.predicate_identity == pred.identity
        && final_state.predicate_state == pred.state
        && final_state.callback_calls == 0
}

pub open spec fn exact_equivalent(
    left: SplitNMut,
    left_state: FinalState,
    right: SplitNMut,
    right_state: FinalState,
) -> bool {
    same_slice_identity(left.inner.iter.v, right.inner.iter.v)
        && same_predicate(left.inner.iter.pred, right.inner.iter.pred)
        && left.inner.iter.finished == right.inner.iter.finished
        && left.inner.iter.callback_calls == right.inner.iter.callback_calls
        && left.inner.count == right.inner.count
        && slice_iterator_view(left).source == slice_iterator_view(right).source
        && slice_iterator_view(left).remaining == slice_iterator_view(right).remaining
        && slice_iterator_view(left).yielded_prefix
            == slice_iterator_view(right).yielded_prefix
        && slice_iterator_view(left).remainder == slice_iterator_view(right).remainder
        && slice_iterator_view(left).chunk_size == slice_iterator_view(right).chunk_size
        && slice_iterator_view(left).reverse == slice_iterator_view(right).reverse
        && same_slice_identity(left_state.slice, right_state.slice)
        && left_state.predicate_identity == right_state.predicate_identity
        && left_state.predicate_state == right_state.predicate_state
        && left_state.callback_calls == right_state.callback_calls
}

pub proof fn conditional_completeness(
    slice: SliceIdentity,
    pred: PredicateSnapshot,
    n: nat,
    iter1: SplitNMut,
    state1: FinalState,
    iter2: SplitNMut,
    state2: FinalState,
)
    requires
        constructor_transition(slice, pred, n, iter1, state1),
        constructor_transition(slice, pred, n, iter2, state2),
    ensures
        exact_equivalent(iter1, state1, iter2, state2),
{
    reveal(constructor_transition);
    reveal(exact_equivalent);
    reveal(slice_iterator_view);
}

}
