use vstd::prelude::*;
#[path = "../../../../specs/slice/mod.rs"]
mod contracts;

verus! {
// Isolated V-SLICE-PATTERN proposal; not an adopted source proof.
// Rust 1.96 core/src/slice/mod.rs:140-157; original body:155-157.
pub const fn first<T>(slice: &[T]) -> (result: Option<&T>)
    ensures
        contracts::first_post(slice, result),
{
    if slice.len() == 0 { None } else { Some(&slice[0]) }
}
}
