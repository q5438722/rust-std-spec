#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at_mut
// Source: core/src/slice/mod.rs:1986-1991
// Source item sha256: cc3d855f0e5ce32308dd0a29e83847998a6522a0156384d0343be27028e6a8bd
// Dependency manifest: proof_manifests/156_core_slice_split_at_mut/dependency_assumption_manifest.json
//
// Rust 1.96 body:
// match self.split_at_mut_checked(mid) { Some(pair) => pair, None => panic!("mid > len") }

use vstd::prelude::*;
use vstd::seq::*;

verus! {

#[verifier::external_body]
pub fn split_at_mut_checked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: Option<(&'a mut [T], &'a mut [T])>)
    ensures
        (mid as int) <= old(slice)@.len() ==> ret.is_some()
            && ret.unwrap().0@ == old(slice)@.subrange(0, mid as int)
            && ret.unwrap().1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int)
            && final(slice)@ == final(ret.unwrap().0)@ + final(ret.unwrap().1)@,
        (mid as int) > old(slice)@.len() ==> ret.is_none()
            && final(slice)@ == old(slice)@,
{
    slice.split_at_mut_checked(mid)
}

#[verifier::external_body]
pub fn rust_1_96_split_at_mut_mid_panic<'a, T>() -> (ret: (&'a mut [T], &'a mut [T]))
    ensures
        false,
{
    panic!("mid > len")
}

pub fn split_at_mut<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        (mid as int) <= old(slice)@.len(),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
{
    match split_at_mut_checked(slice, mid) {
        Some(pair) => pair,
        None => {
            proof {
                assert(false);
            }
            rust_1_96_split_at_mut_mid_panic()
        },
    }
}

}
