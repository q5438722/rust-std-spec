use vstd::prelude::*;
#[path = "../proofs/completeness/slice/mutable_splits_state.rs"]
mod state;
use state::post::{split_first_mut_post, split_last_mut_post};

verus! {

pub proof fn documented_two_region_changes()
    ensures
        split_first_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((0, seq![1, 2])), seq![3, 4, 5])),
        split_last_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((2, seq![0, 1])), seq![4, 5, 3])),
{
    assert(seq![0int, 1, 2].subrange(1, 3) =~= seq![1, 2]);
    assert(seq![0int, 1, 2].subrange(0, 2) =~= seq![0, 1]);
}

pub proof fn neither_region_can_be_frozen()
    ensures
        !split_first_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((0, seq![1, 2])), seq![0, 4, 5])),
        !split_first_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((0, seq![1, 2])), seq![3, 1, 2])),
        !split_last_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((2, seq![0, 1])), seq![4, 5, 2])),
        !split_last_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((2, seq![0, 1])), seq![0, 1, 3])),
{
}

pub proof fn initial_element_and_whole_remainder_are_independent()
    ensures
        !split_first_mut_post(seq![10int, 40, 30], Some((7, seq![8, 9])),
            (Some((30, seq![40, 30])), seq![7, 8, 9])),
        !split_first_mut_post(seq![10int, 40, 30], Some((7, seq![8, 9])),
            (Some((10, seq![30, 40])), seq![7, 8, 9])),
        !split_last_mut_post(seq![10int, 40, 30], Some((7, seq![8, 9])),
            (Some((10, seq![10, 40])), seq![8, 9, 7])),
        !split_last_mut_post(seq![10int, 40, 30], Some((7, seq![8, 9])),
            (Some((30, seq![40, 10])), seq![8, 9, 7])),
{
    assert(seq![10int, 40, 30].subrange(1, 3)[0] == 40);
    assert(seq![10int, 40, 30].subrange(0, 2)[0] == 10);
}

pub proof fn option_shape_is_not_a_caller_choice()
    ensures
        !split_first_mut_post(seq![0int], None, (None, seq![])),
        !split_last_mut_post(seq![0int], None, (None, seq![])),
        !split_first_mut_post(seq![0int], Some((5, seq![])), (None, seq![5])),
        !split_last_mut_post(seq![0int], Some((5, seq![])), (None, seq![5])),
        !split_first_mut_post(Seq::<int>::empty(), Some((5, seq![])), (None, seq![])),
        !split_last_mut_post(Seq::<int>::empty(), Some((5, seq![])), (None, seq![])),
{
}

pub proof fn caller_remainder_length_is_a_cross_state_constraint()
    ensures
        !split_first_mut_post(seq![0int, 1, 2], Some((3, seq![4])),
            (Some((0, seq![1, 2])), seq![3, 4])),
        !split_last_mut_post(seq![0int, 1, 2], Some((3, seq![4])),
            (Some((2, seq![0, 1])), seq![4, 3])),
{
}

pub proof fn tuple_position_does_not_reverse_writeback_order()
    ensures
        !split_first_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((0, seq![1, 2])), seq![4, 5, 3])),
        !split_last_mut_post(seq![0int, 1, 2], Some((3, seq![4, 5])),
            (Some((2, seq![0, 1])), seq![3, 4, 5])),
{
}

pub proof fn singleton_has_an_empty_remainder<T>(initial: T, written: T)
    ensures
        split_first_mut_post(seq![initial], Some((written, seq![])),
            (Some((initial, seq![])), seq![written])),
        split_last_mut_post(seq![initial], Some((written, seq![])),
            (Some((initial, seq![])), seq![written])),
{
    assert(seq![initial].subrange(1, 1) =~= seq![]);
    assert(seq![initial].subrange(0, 0) =~= seq![]);
}

pub struct NonCopy<'a> {
    pub borrowed: &'a u8,
}

pub proof fn non_copy_non_static_writes<'a>(
    initial: Seq<NonCopy<'a>>,
    element: NonCopy<'a>,
    remainder: Seq<NonCopy<'a>>,
)
    requires
        remainder.len() + 1 == initial.len(),
    ensures
        split_first_mut_post(initial, Some((element, remainder)),
            (Some((initial[0], initial.subrange(1, initial.len() as int))),
             seq![element] + remainder)),
        split_last_mut_post(initial, Some((element, remainder)),
            (Some((initial[initial.len() - 1], initial.subrange(0, initial.len() - 1))),
             remainder + seq![element])),
{
    state::all_caller_writes(initial, Some((element, remainder)));
}

pub struct ZeroSized;

pub proof fn zero_sized_element_extents()
    ensures
        split_first_mut_post(seq![ZeroSized, ZeroSized], Some((ZeroSized, seq![ZeroSized])),
            (Some((ZeroSized, seq![ZeroSized])), seq![ZeroSized, ZeroSized])),
        split_last_mut_post(seq![ZeroSized, ZeroSized], Some((ZeroSized, seq![ZeroSized])),
            (Some((ZeroSized, seq![ZeroSized])), seq![ZeroSized, ZeroSized])),
{
    assert(seq![ZeroSized, ZeroSized].subrange(1, 2) =~= seq![ZeroSized]);
    assert(seq![ZeroSized, ZeroSized].subrange(0, 1) =~= seq![ZeroSized]);
}

pub proof fn empty_without_an_element<T>()
    ensures
        split_first_mut_post(Seq::<T>::empty(), None, (None, seq![])),
        split_last_mut_post(Seq::<T>::empty(), None, (None, seq![])),
{
    state::all_caller_writes(Seq::<T>::empty(), None);
}

}
