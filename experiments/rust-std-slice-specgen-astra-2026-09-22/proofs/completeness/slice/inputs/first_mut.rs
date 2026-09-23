use vstd::prelude::*;
#[path = "../mutable_endpoints_state.rs"]
mod state;

verus! {

// Value-state analysis only; the public mutable signature is unchanged.
pub fn first_mut_observation<T>(
    input_initial: Ghost<Seq<T>>,
    caller_final: Ghost<Option<T>>,
) -> (result: Ghost<(Option<T>, Seq<T>)>)
    requires
        caller_final@.is_none() <==> input_initial@.len() == 0,
    ensures
        state::post::first_mut_post(input_initial@, caller_final@, result@),
{
    proof {
        state::all_caller_writes(input_initial@, caller_final@);
    }
    Ghost(match caller_final@ {
        None => (None, seq![]),
        Some(written) => (Some(input_initial@[0]), input_initial@.update(0, written)),
    })
}

}
