use vstd::prelude::*;

#[path = "../../../specs/slice/default_post.rs"]
mod contracts;

verus! {

// Rust 1.96 slice/mod.rs:5643-5646; Self = &'a mut [T].
pub fn default_mut<'a, T>() -> (result: &'a mut [T])
    ensures
        contracts::default_post(result),
{
    &mut []
}

}
