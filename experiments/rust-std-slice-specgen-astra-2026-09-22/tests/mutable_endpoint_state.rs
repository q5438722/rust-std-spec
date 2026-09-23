use vstd::prelude::*;
#[path = "../proofs/completeness/slice/mutable_endpoints_state.rs"]
mod state;
use state::post::{first_mut_post, last_mut_post};

verus! {

pub proof fn documented_changes_are_legal()
    ensures
        first_mut_post(seq![0int, 1, 2], Some(5), (Some(0), seq![5, 1, 2])),
        last_mut_post(seq![0int, 1, 2], Some(10), (Some(2), seq![0, 1, 10])),
{
    assert(seq![0int, 1, 2].update(0, 5) =~= seq![5, 1, 2]);
    assert(seq![0int, 1, 2].update(2, 10) =~= seq![0, 1, 10]);
}

pub proof fn variants_cannot_be_changed()
    ensures
        !first_mut_post(seq![0int, 1], Some(5), (None, seq![5, 1])),
        !last_mut_post(seq![0int, 1], Some(5), (None, seq![0, 5])),
        !first_mut_post(Seq::<int>::empty(), None, (Some(0), seq![])),
        !last_mut_post(Seq::<int>::empty(), None, (Some(0), seq![])),
        !first_mut_post(Seq::<int>::empty(), Some(5), (None, seq![])),
        !last_mut_post(Seq::<int>::empty(), Some(5), (None, seq![])),
{
}

pub proof fn initial_elements_cannot_be_changed()
    ensures
        !first_mut_post(seq![10int, 40, 30], Some(7), (Some(30), seq![7, 40, 30])),
        !last_mut_post(seq![10int, 40, 30], Some(7), (Some(10), seq![10, 40, 7])),
{
}

pub proof fn unborrowed_elements_and_length_cannot_be_changed()
    ensures
        !first_mut_post(seq![0int, 1, 2], Some(5), (Some(0), seq![5, 9, 2])),
        !last_mut_post(seq![0int, 1, 2], Some(5), (Some(2), seq![9, 1, 5])),
        !first_mut_post(seq![0int, 1, 2], Some(5), (Some(0), seq![5])),
        !last_mut_post(seq![0int, 1, 2], Some(5), (Some(2), seq![5])),
{
    assert(seq![0int, 1, 2].update(0, 5)[1] == 1);
    assert(seq![0int, 1, 2].update(2, 5)[0] == 0);
    assert(seq![0int, 1, 2].update(0, 5).len() == 3);
    assert(seq![0int, 1, 2].update(2, 5).len() == 3);
}

pub proof fn caller_writes_cannot_be_frozen()
    ensures
        first_mut_post(seq![false, false], Some(true), (Some(false), seq![true, false])),
        last_mut_post(seq![false, false], Some(true), (Some(false), seq![false, true])),
        !first_mut_post(seq![false, false], Some(true), (Some(false), seq![false, false])),
        !last_mut_post(seq![false, false], Some(true), (Some(false), seq![false, false])),
{
    assert(seq![false, false].update(0, true) =~= seq![true, false]);
    assert(seq![false, false].update(1, true) =~= seq![false, true]);
}

pub struct NonCopy<'a> {
    pub borrowed: &'a u8,
}

pub proof fn non_copy_non_static_values<'a>(initial: NonCopy<'a>, written: NonCopy<'a>)
    ensures
        first_mut_post(seq![initial], Some(written), (Some(initial), seq![written])),
        last_mut_post(seq![initial], Some(written), (Some(initial), seq![written])),
{
    assert(seq![initial].update(0, written) =~= seq![written]);
}

pub struct ZeroSized;

pub proof fn zero_sized_positions()
    ensures
        first_mut_post(seq![ZeroSized, ZeroSized], Some(ZeroSized),
            (Some(ZeroSized), seq![ZeroSized, ZeroSized])),
        last_mut_post(seq![ZeroSized, ZeroSized], Some(ZeroSized),
            (Some(ZeroSized), seq![ZeroSized, ZeroSized])),
{
    assert(seq![ZeroSized, ZeroSized].update(0, ZeroSized) =~= seq![ZeroSized, ZeroSized]);
    assert(seq![ZeroSized, ZeroSized].update(1, ZeroSized) =~= seq![ZeroSized, ZeroSized]);
}

pub proof fn empty_without_an_element<T>()
    ensures
        first_mut_post(Seq::<T>::empty(), None, (None, seq![])),
        last_mut_post(Seq::<T>::empty(), None, (None, seq![])),
{
    state::all_caller_writes(Seq::<T>::empty(), None);
}

}
