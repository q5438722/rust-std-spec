use vstd::prelude::*;

#[path = "default_post.rs"]
pub mod post;

verus! {

// Rust 1.96 slice/mod.rs:5631-5638; only the non-const call is stable.
pub assume_specification<'a, T>[ <&'a [T] as core::default::Default>::default ]()
    -> (result: &'a [T])
    ensures
        post::default_post(result),
;

// Rust 1.96 slice/mod.rs:5640-5647; only the non-const call is stable.
pub assume_specification<'a, T>[ <&'a mut [T] as core::default::Default>::default ]()
    -> (result: &'a mut [T])
    ensures
        post::default_post(result),
;

}
