use vstd::prelude::*;

#[path = "../from_mut_state.rs"]
mod state;

verus! {

// Completeness only: the public API and its two state relations are unchanged.
pub fn from_mut_observation<T>(
    Ghost(input_initial): Ghost<T>,
    Ghost(caller_final): Ghost<Seq<T>>,
) -> (result: Ghost<(Seq<T>, T)>)
    requires
        caller_final.len() == 1,
    ensures
        state::from_mut_post(input_initial, caller_final, result@),
{
    proof {
        state::all_caller_writes(input_initial, caller_final);
    }
    Ghost((seq![input_initial], caller_final[0]))
}

}
