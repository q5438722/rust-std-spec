use vstd::prelude::*;

#[path = "../../../specs/slice/default_post.rs"]
mod contracts;

verus! {

// Rust 1.96 slice/mod.rs:5634-5637; Self = &'a [T].
pub fn default_shared<'a, T>() -> (result: &'a [T])
    ensures
        contracts::default_post(result),
{
    &[]
}

}
