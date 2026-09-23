use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:182-200; body:198-200.
pub const fn split_first<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_first_post(slice, result),
{
    if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }
}
}
