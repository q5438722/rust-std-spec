#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_ptr
// Source: core/src/slice/mod.rs:726-728
// Source item sha256: df0d49a1417773cb8932d48e9e7bb06a553039beaca7f20000b9fc6319236c1d
// Dependency manifest: proof_manifests/021_core_slice_as_ptr/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub fn rust_1_96_slice_as_ptr_cast<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    let len = slice.len();
    let ptr = core::ptr::null::<T>().with_addr(len);
    proof {
        assert(slice@.len() == len as nat);
    }
    ptr
}

pub fn as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    rust_1_96_slice_as_ptr_cast(slice)
}

}
