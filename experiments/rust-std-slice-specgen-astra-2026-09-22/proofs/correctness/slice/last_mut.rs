use vstd::prelude::*;
#[path = "../../../specs/slice/mutable_endpoints.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:285-306; body:304-306.
pub const fn last_mut<T>(slice: &mut [T]) -> (result: Option<&mut T>)
    ensures
        contracts::last_mut_post(
            old(slice)@,
            match result { None => None, Some(value) => Some(*final(value)) },
            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),
        ),
{
    if slice.len() == 0 {
        None
    } else {
        let i = slice.len() - 1;
        Some(&mut slice[i])
    }
}
}
