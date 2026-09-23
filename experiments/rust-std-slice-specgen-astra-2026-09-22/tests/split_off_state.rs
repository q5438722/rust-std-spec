use vstd::prelude::*;
#[path = "../proofs/completeness/slice/split_off_state.rs"]
mod state;
use state::post::{split_off_first_post, split_off_last_post};

verus! {

pub proof fn empty_without_an_element<T>()
    ensures
        split_off_first_post(Seq::<T>::empty(), (None, seq![])),
        split_off_last_post(Seq::<T>::empty(), (None, seq![])),
{
    state::all_initial_states(Seq::<T>::empty());
}

pub proof fn singleton_consumes_exactly_one<T>(value: T)
    ensures
        split_off_first_post(seq![value], (Some(value), seq![])),
        split_off_last_post(seq![value], (Some(value), seq![])),
{
    assert(seq![value].subrange(1, 1) =~= seq![]);
    assert(seq![value].subrange(0, 0) =~= seq![]);
}

pub proof fn complete_values_and_order()
    ensures
        split_off_first_post(seq![10int, 40, 30], (Some(10), seq![40, 30])),
        split_off_last_post(seq![10int, 40, 30], (Some(30), seq![10, 40])),
        !split_off_first_post(seq![10int, 40, 30], (Some(30), seq![40, 30])),
        !split_off_first_post(seq![10int, 40, 30], (Some(10), seq![30, 40])),
        !split_off_last_post(seq![10int, 40, 30], (Some(10), seq![10, 40])),
        !split_off_last_post(seq![10int, 40, 30], (Some(30), seq![40, 10])),
{
    assert(seq![10int, 40, 30].subrange(1, 3) =~= seq![40, 30]);
    assert(seq![10int, 40, 30].subrange(0, 2) =~= seq![10, 40]);
}

pub proof fn remaining_is_not_presupplied_or_frozen()
    ensures
        !split_off_first_post(seq![10int, 20], (Some(10), seq![10, 20])),
        !split_off_last_post(seq![10int, 20], (Some(20), seq![10, 20])),
        !split_off_first_post(seq![10int, 20], (Some(10), seq![])),
        !split_off_last_post(seq![10int, 20], (Some(20), seq![])),
        !split_off_first_post(Seq::<int>::empty(), (None, seq![7])),
        !split_off_last_post(Seq::<int>::empty(), (None, seq![7])),
        !split_off_first_post(seq![10int], (None, seq![])),
        !split_off_last_post(seq![10int], (None, seq![])),
{
}

pub struct NonCopy<'a> {
    pub borrowed: &'a u8,
}

pub proof fn non_copy_non_static_totality<'a>(initial: Seq<NonCopy<'a>>)
    ensures
        exists|observations: (Option<NonCopy<'a>>, Seq<NonCopy<'a>>)|
            split_off_first_post(initial, observations),
        exists|observations: (Option<NonCopy<'a>>, Seq<NonCopy<'a>>)|
            split_off_last_post(initial, observations),
{
    state::all_initial_states(initial);
}

}
