use vstd::prelude::*;
#[path = "../../../specs/slice/mutable_splits_post.rs"]
mod contracts;

verus! {
// Rust 1.96 core/src/slice/mod.rs:244-264; body:262-264.
pub const fn split_last_mut<T>(slice: &mut [T]) -> (result: Option<(&mut T, &mut [T])>)
    ensures
        contracts::split_last_mut_post(
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
        let i = slice.len() - 1;
        let (init, last) = slice.split_at_mut(i);
        proof {
            vstd::slice::mut_ref_slice_len_eq(&init);
        }
        Some((&mut last[0], init))
    }
}
}
