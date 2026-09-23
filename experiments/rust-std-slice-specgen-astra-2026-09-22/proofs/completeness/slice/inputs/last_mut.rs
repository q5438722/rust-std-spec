use vstd::prelude::*;
#[path = "../mutable_endpoints_state.rs"]
mod state;

verus! {

// Value-state analysis only; the public mutable signature is unchanged.
pub fn last_mut_observation<T>(
    input_initial: Ghost<Seq<T>>,
    caller_final: Ghost<Option<T>>,
) -> (result: Ghost<(Option<T>, Seq<T>)>)
    requires
        caller_final@.is_none() <==> input_initial@.len() == 0,
    ensures
        state::post::last_mut_post(input_initial@, caller_final@, result@),
{
    proof {
        state::all_caller_writes(input_initial@, caller_final@);
    }
    Ghost(match caller_final@ {
        None => (None, seq![]),
        Some(written) => (
            Some(input_initial@[input_initial@.len() - 1]),
            input_initial@.update(input_initial@.len() - 1, written),
        ),
    })
}

}
