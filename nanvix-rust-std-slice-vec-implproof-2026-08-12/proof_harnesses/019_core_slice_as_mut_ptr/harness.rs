#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_mut_ptr
// Source: core/src/slice/mod.rs:757-759
// Source item sha256: 99e25e7a86cc5c6b6b7557a4e100daf10a6be356072e931c8a093b6c6198dd9c
// Dependency manifest: proof_manifests/019_core_slice_as_mut_ptr/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

#[verifier::external_body]
pub fn rust_1_96_slice_as_mut_ptr_cast<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    slice as *mut [T] as *mut T
}

pub fn as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    rust_1_96_slice_as_mut_ptr_cast(slice)
}

}
