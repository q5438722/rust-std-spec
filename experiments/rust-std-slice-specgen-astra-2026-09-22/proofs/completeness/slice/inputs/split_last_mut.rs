use vstd::prelude::*;
#[path = "../mutable_splits_state.rs"]
mod state;

verus! {

pub fn split_last_mut_observation<T>(
    input_initial: Ghost<Seq<T>>,
    caller_final: Ghost<Option<(T, Seq<T>)>>,
) -> (result: Ghost<(Option<(T, Seq<T>)>, Seq<T>)>)
    requires
        match caller_final@ {
            None => input_initial@.len() == 0,
            Some((_, written_remainder)) =>
                written_remainder.len() + 1 == input_initial@.len(),
        },
    ensures
        state::post::split_last_mut_post(input_initial@, caller_final@, result@),
{
    proof {
        state::all_caller_writes(input_initial@, caller_final@);
    }
    Ghost(match caller_final@ {
        None => (None, seq![]),
        Some((written, written_remainder)) => (
            Some((
                input_initial@[input_initial@.len() - 1],
                input_initial@.subrange(0, input_initial@.len() - 1),
            )),
            written_remainder + seq![written],
        ),
    })
}

}
