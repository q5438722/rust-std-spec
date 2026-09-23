use vstd::prelude::*;

#[path = "ascii_post.rs"]
pub mod post;

verus! {

// Rust 1.96 slice/ascii.rs:161-181.
pub assume_specification[ <[u8]>::make_ascii_uppercase ](slice: &mut [u8])
    ensures
        post::uppercase_post(old(slice)@, final(slice)@),
;

// Rust 1.96 slice/ascii.rs:183-203.
pub assume_specification[ <[u8]>::make_ascii_lowercase ](slice: &mut [u8])
    ensures
        post::lowercase_post(old(slice)@, final(slice)@),
;

}
