use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:224-242; body:240-242.
pub const fn split_last<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_last_post(slice, result),
{
    if let [init @ .., last] = slice { Some((last, init)) } else { None }
}
}
