use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:140-157; body:155-157.
pub const fn first<T>(slice: &[T]) -> (result: Option<&T>)
    ensures
        contracts::first_post(slice, result),
{
    if let [first, ..] = slice { Some(first) } else { None }
}
}
