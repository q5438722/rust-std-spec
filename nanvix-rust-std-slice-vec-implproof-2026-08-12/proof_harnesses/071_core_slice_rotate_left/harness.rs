#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::rotate_left
// Source: core/src/slice/mod.rs:3884-3894
// Source item sha256: 401057f1307fb0b30a44fde8bff82a5b7aa6528f410e40b48a4ef1d09c01c418
// Dependency manifest: proof_manifests/071_core_slice_rotate_left/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

macro_rules! assert {
    ($cond:expr) => {
        rust_1_96_assert($cond)
    };
}

verus! {

pub open spec fn slice_rotated_left<T>(seq: Seq<T>, mid: int) -> Seq<T> {
    if 0 <= mid && mid <= seq.len() {
        seq.subrange(mid, seq.len() as int).add(seq.subrange(0, mid))
    } else {
        seq
    }
}

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub fn rust_1_96_assert(cond: bool)
    requires
        cond,
{
}

#[verifier::external_body]
pub fn as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    slice as *mut [T] as *mut T
}

pub mod rotate {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn ptr_rotate<T>(left: usize, mid: *mut T, right: usize) {
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_rotate_left_ptr_rotate<T>(mid: usize, p: *mut T, k: usize) {
    rotate::ptr_rotate(mid, p.add(mid), k);
}

#[verifier::external_body]
pub fn rust_1_96_rotate_left_final_frame_bridge<T>(
    slice: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    mid: usize,
    k: usize,
    p: *mut T,
)
    requires
        old(slice)@ == source,
        mid <= source.len(),
        k as int == source.len() - mid as int,
        slice_start_mut_ptr(source, p),
    ensures
        final(slice)@ == slice_rotated_left(source, mid as int),
{
}

pub fn rotate_left<T>(slice: &mut [T], mid: usize)
    requires
        mid <= old(slice)@.len(),
    ensures
        final(slice)@ == slice_rotated_left(old(slice)@, mid as int),
{
    let ghost source = slice@;
    assert!(mid <= slice.len());
    let k = slice.len() - mid;
    assert(k as int == source.len() - mid as int);
    let p = as_mut_ptr(slice);

    unsafe {
        rust_1_96_rotate_left_ptr_rotate(mid, p, k);
    }
    rust_1_96_rotate_left_final_frame_bridge(slice, Ghost(source), mid, k, p);
}

}
