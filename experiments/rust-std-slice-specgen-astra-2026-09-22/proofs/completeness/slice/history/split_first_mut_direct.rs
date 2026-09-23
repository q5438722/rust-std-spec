use vstd::prelude::*;
#[path = "../../../../specs/slice/mutable_splits_post.rs"]
mod contracts;

mod source {
    pub const fn split_first_mut<T>(slice: &mut [T]) -> Option<(&mut T, &mut [T])> {
        if let [first, tail @ ..] = slice { Some((first, tail)) } else { None }
    }
}

verus! {
// Analysis only; source proofs do not import this declaration.
pub assume_specification<T>[source::split_first_mut::<T>](
    slice: &mut [T],
) -> (result: Option<(&mut T, &mut [T])>)
    ensures
        contracts::split_first_mut_post(
            old(slice)@,
            match result {
                None => None,
                Some((value, remainder)) => Some((*final(value), final(remainder)@)),
            },
            (
                match result {
                    None => None,
                    Some((value, remainder)) => Some((*value, remainder@)),
                },
                final(slice)@,
            ),
        ),
;
}
