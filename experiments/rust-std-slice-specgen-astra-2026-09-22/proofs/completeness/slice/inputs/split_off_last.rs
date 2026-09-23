use vstd::prelude::*;
#[path = "../../../../specs/slice/split_off_post.rs"]
mod contracts;

mod source {
    pub const fn split_off_last<'a, T>(slice: &mut &'a [T]) -> Option<&'a T> {
        let Some((last, rem)) = slice.split_last() else { return None };
        *slice = rem;
        Some(last)
    }
}

verus! {
// Analysis only; source proofs do not import this declaration.
pub assume_specification<'a, T>[source::split_off_last::<T>](
    slice: &mut &'a [T],
) -> (result: Option<&'a T>)
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
;
}
