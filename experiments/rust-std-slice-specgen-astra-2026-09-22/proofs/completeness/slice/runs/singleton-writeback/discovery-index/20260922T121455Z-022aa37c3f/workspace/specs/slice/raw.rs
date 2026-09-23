use vstd::prelude::*;

#[path = "raw_post.rs"]
pub mod post;

verus! {

// Rust 1.96 slice/raw.rs:198-205.
pub assume_specification<T>[ core::slice::from_ref ](s: &T) -> (result: &[T])
    ensures
        post::singleton_post(*s, result@),
;

// Rust 1.96 slice/raw.rs:207-213; the two clauses describe different states.
pub assume_specification<T>[ core::slice::from_mut ](s: &mut T) -> (result: &mut [T])
    ensures
        post::singleton_post(*old(s), result@),
        post::singleton_post(*final(s), final(result)@),
;

}
