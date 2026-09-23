use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Isolated V-SLICE-PATTERN proposal; not an adopted source proof.
// Rust 1.96 core/src/slice/mod.rs:182-200; original body:198-200.
pub const fn split_first<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)
    ensures
        contracts::split_first_post(slice, result),
{
    if slice.len() == 0 {
        None
    } else {
        Some((&slice[0], slice.split_at(1).1))
    }
}
}
