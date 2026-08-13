#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at
// Source: core/src/slice/mod.rs:1952-1957
// Source item sha256: 1737ca6053f4c97c0746a0ced8b32dd3b29c871561f987454033fa98c4b2e9ef
// Dependency manifest: proof_manifests/155_core_slice_split_at/dependency_assumption_manifest.json
//
// Rust 1.96 body:
// match self.split_at_checked(mid) { Some(pair) => pair, None => panic!("mid > len") }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

#[verifier::external_body]
pub fn split_at_checked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: Option<(&'a [T], &'a [T])>)
    ensures
        (mid as int) <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, mid as int)
            && ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
        (mid as int) > slice@.len() ==> ret.is_none(),
{
    slice.split_at_checked(mid)
}

#[verifier::external_body]
pub fn rust_1_96_split_at_mid_panic<'a, T>() -> (ret: (&'a [T], &'a [T]))
    ensures
        false,
{
    panic!("mid > len")
}

pub fn split_at<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        (mid as int) <= slice@.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    match split_at_checked(slice, mid) {
        Some(pair) => pair,
        None => {
            proof {
                assert(false);
            }
            rust_1_96_split_at_mid_panic()
        },
    }
}

}
