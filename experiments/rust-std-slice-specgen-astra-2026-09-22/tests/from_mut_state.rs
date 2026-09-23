use vstd::prelude::*;

#[path = "../proofs/completeness/slice/from_mut_state.rs"]
mod state;

verus! {

pub proof fn changed_caller_value()
    ensures
        state::from_mut_post(5u8, seq![9u8], (seq![5u8], 9u8)),
{
    state::all_caller_writes(5u8, seq![9u8]);
}

pub struct Borrowed<'a> {
    pub value: &'a u8,
}

pub proof fn non_copy_non_static<'a>(initial: Borrowed<'a>, written: Borrowed<'a>)
    ensures
        state::from_mut_post(initial, seq![written], (seq![initial], written)),
{
    state::all_caller_writes(initial, seq![written]);
}

pub struct ZeroSized;

pub proof fn zero_sized(initial: ZeroSized, written: ZeroSized)
    ensures
        state::from_mut_post(initial, seq![written], (seq![initial], written)),
{
    state::all_caller_writes(initial, seq![written]);
}

pub proof fn initial_constraint_is_independent()
    ensures
        state::post::singleton_post(9u8, seq![9u8]),
        !state::from_mut_post(5u8, seq![9u8], (seq![6u8], 9u8)),
        !state::from_mut_post(5u8, seq![9u8], (seq![5u8, 6u8], 9u8)),
{
    assert(seq![6u8][0] != seq![5u8][0]);
}

pub proof fn return_constraint_is_independent()
    ensures
        state::post::singleton_post(5u8, seq![5u8]),
        !state::from_mut_post(5u8, seq![9u8], (seq![5u8], 8u8)),
{
    assert(seq![9u8][0] != seq![8u8][0]);
}

}
