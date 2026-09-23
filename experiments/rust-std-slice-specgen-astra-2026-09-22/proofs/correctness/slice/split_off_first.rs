use vstd::prelude::*;
#[path = "../../../specs/slice/split_off_post.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:4993-5015; body:5011-5014.
pub const fn split_off_first<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)
    ensures
        contracts::split_off_first_post(
            (*old(slice))@,
            (
                match result {
                    None => None,
                    Some(value) => Some(*value),
                },
                (*final(slice))@,
            ),
        ),
{
    // FIXME(const-hack): Use `?` when available in const instead of `let-else`.
    let Some((first, rem)) = slice.split_first() else { return None };
    *slice = rem;
    Some(first)
}
}
