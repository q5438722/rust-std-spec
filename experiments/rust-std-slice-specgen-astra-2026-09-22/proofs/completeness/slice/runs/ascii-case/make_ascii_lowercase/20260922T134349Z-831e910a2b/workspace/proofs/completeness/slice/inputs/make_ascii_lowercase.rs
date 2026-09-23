use vstd::prelude::*;

#[path = "../ascii_state.rs"]
mod state;

verus! {

// Completeness only: the unit-returning public API remains unchanged.
pub fn make_ascii_lowercase_observation(initial: Ghost<Seq<u8>>) -> (result: Ghost<Seq<u8>>)
    ensures
        state::post::lowercase_post(initial@, result@),
{
    Ghost(initial@.map_values(|byte: u8| state::post::lowercase_byte(byte)))
}

}
