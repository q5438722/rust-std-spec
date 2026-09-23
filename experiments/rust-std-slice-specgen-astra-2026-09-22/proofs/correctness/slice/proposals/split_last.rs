use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Isolated V-SLICE-PATTERN proposal; not an adopted source proof.
// Rust 1.96 core/src/slice/mod.rs:224-242; original body:240-242.
pub const fn split_last<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_last_post(slice, result),
{
    if slice.len() == 0 {
        None
    } else {
        let i = slice.len() - 1;
        Some((&slice[i], slice.split_at(i).0))
    }
}
}
