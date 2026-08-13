#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::clone_from_slice
// Source: core/src/slice/mod.rs:4254-4259 and private CloneFromSpec impls at 5588-5628
// Source item sha256: 0dfc2e8b8b0a5319d883279e62986e9055b56d6ac6ba773cc4f6b9887423819b
// Dependency manifest: proof_manifests/037_core_slice_clone_from_slice/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_cloned_from<T>(src: Seq<T>, dst: Seq<T>) -> bool {
    dst == src
}

#[verifier::external_body]
pub fn spec_clone_from<T: Clone>(dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        slice_cloned_from(src@, final(dst)@),
{
}

pub fn clone_from_slice<T: Clone>(dst: &mut [T], src: &[T])
    requires
        old(dst)@.len() == src@.len(),
    ensures
        slice_cloned_from(src@, final(dst)@),
{
    spec_clone_from(dst, src);
}

}
