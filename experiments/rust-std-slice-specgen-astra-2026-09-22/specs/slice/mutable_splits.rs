use vstd::prelude::*;

#[path = "mutable_splits_post.rs"]
pub mod post;

verus! {

// split_first_mut is already registered by the selected vstd.
// Rust 1.96 slice/mod.rs:244-264.
pub assume_specification<T>[ <[T]>::split_last_mut ](
    slice: &mut [T],
) -> (result: Option<(&mut T, &mut [T])>)
    ensures
        post::split_last_mut_post(
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
    no_unwind
;

}
