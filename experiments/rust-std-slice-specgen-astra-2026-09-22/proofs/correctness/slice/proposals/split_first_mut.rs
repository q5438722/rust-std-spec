use vstd::prelude::*;
#[path = "../../../../specs/slice/mutable_splits_post.rs"]
mod contracts;

verus! {
// Isolated proposal; permission is required in issues/V-SLICE-PATTERN.md.
pub const fn split_first_mut<T>(slice: &mut [T]) -> (result: Option<(&mut T, &mut [T])>)
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
{
    if slice.len() == 0 {
        None
    } else {
        let (head, tail) = slice.split_at_mut(1);
        proof {
            vstd::slice::mut_ref_slice_len_eq(&tail);
        }
        Some((&mut head[0], tail))
    }
}
}
