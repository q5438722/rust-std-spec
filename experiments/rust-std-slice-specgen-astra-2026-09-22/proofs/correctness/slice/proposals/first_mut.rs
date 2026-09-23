use vstd::prelude::*;
#[path = "../../../../specs/slice/mutable_endpoints.rs"]
mod contracts;

verus! {
// Isolated proposal for Rust 1.96 slice/mod.rs:178-180; not adopted.
pub const fn first_mut<T>(slice: &mut [T]) -> (result: Option<&mut T>)
    ensures
        contracts::first_mut_post(
            old(slice)@,
            match result { None => None, Some(value) => Some(*final(value)) },
            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),
        ),
{
    if slice.len() == 0 { None } else { Some(&mut slice[0]) }
}
}
