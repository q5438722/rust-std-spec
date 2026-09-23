use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:120-138; body:136-138.
pub const fn is_empty<T>(slice: &[T]) -> (result: bool)
    ensures
        contracts::is_empty_post(slice, result),
{
    slice.len() == 0
}
}
