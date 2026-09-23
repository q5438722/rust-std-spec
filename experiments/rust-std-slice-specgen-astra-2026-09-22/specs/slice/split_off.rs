use vstd::prelude::*;

#[path = "split_off_post.rs"]
pub mod post;

verus! {

// Rust 1.96 slice/mod.rs:4993-5015; const use requires const_split_off_first_last.
pub assume_specification<'a, T>[ <[T]>::split_off_first ](
    slice: &mut &'a [T],
) -> (result: Option<&'a T>)
    ensures
        post::split_off_first_post(
            (*old(slice))@,
            (
                match result {
                    None => None,
                    Some(value) => Some(*value),
                },
                (*final(slice))@,
            ),
        ),
    no_unwind
;

// Rust 1.96 slice/mod.rs:5043-5065; const use requires const_split_off_first_last.
pub assume_specification<'a, T>[ <[T]>::split_off_last ](
    slice: &mut &'a [T],
) -> (result: Option<&'a T>)
    ensures
        post::split_off_last_post(
            (*old(slice))@,
            (
                match result {
                    None => None,
                    Some(value) => Some(*value),
                },
                (*final(slice))@,
            ),
        ),
    no_unwind
;

}
