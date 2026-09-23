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
        state::post::singleton_post(input_initial, result@.0),
        result@.1 == caller_final[0],
{
    proof {
        state::all_caller_writes(input_initial, caller_final);
        state::observation_correspondence(
            input_initial, caller_final, (seq![input_initial], caller_final[0]),
        );
    }
    Ghost((seq![input_initial], caller_final[0]))
}

}
