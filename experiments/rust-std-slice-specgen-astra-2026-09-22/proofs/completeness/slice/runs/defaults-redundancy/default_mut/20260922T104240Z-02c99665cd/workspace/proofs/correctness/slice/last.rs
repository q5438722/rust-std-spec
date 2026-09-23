use vstd::prelude::*;
#[path = "../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:266-283; body:281-283.
pub const fn last<T>(slice: &[T]) -> (result: Option<&T>)
    ensures
        contracts::last_post(slice, result),
{
    if let [.., last] = slice { Some(last) } else { None }
}
}
