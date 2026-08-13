#![allow(dead_code, unused_imports, unused_variables)]
#![feature(ptr_metadata)]
// Target-specific Verus implementation harness.
// Target: core::slice::len
// Source: core/src/slice/mod.rs:116-118
// Source item sha256: f020cc6bc61b6583630cc4eece93c8a4baf5c3a74c08569d270a0ca28a9a81b1
// Dependency manifest: proof_manifests/154_core_slice_len/dependency_assumption_manifest.json
//
// Rust 1.96 body: ptr::metadata(self)

use vstd::prelude::*;

verus! {

pub uninterp spec fn spec_slice_len<T>(slice: &[T]) -> usize;

pub broadcast axiom fn axiom_spec_len<T>(slice: &[T])
    ensures
        #[trigger] spec_slice_len(slice) == slice@.len(),
;

#[verifier::external_body]
pub fn rust_1_96_ptr_metadata<T>(slice: &[T]) -> (len: usize)
    ensures
        len == spec_slice_len(slice),
{
    core::ptr::metadata(slice)
}

pub fn len<T>(slice: &[T]) -> (len: usize)
    ensures
        len == spec_slice_len(slice),
{
    rust_1_96_ptr_metadata(slice)
}

}
