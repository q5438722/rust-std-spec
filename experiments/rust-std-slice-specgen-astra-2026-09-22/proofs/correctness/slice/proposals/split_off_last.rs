use vstd::prelude::*;
#[path = "../../../../specs/slice/split_off_post.rs"]
mod contracts;
#[path = "../split_last.rs"]
mod split_dependency;

verus! {
// Isolated proposal for Rust 1.96 slice/mod.rs:5043-5065; not adopted.
pub const fn split_off_last<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)
    ensures
        contracts::split_off_last_post(
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
    let Some((last, rem)) = split_dependency::split_last(*slice) else { return None };
    *slice = rem;
    Some(last)
}
}
