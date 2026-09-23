use vstd::prelude::*;
#[path = "../../../specs/slice/split_off_post.rs"]
mod contracts;
#[path = "split_last.rs"]
mod split_dependency;

verus! {
// Rust 1.96 core/src/slice/mod.rs:5043-5065; body:5061-5064.
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
