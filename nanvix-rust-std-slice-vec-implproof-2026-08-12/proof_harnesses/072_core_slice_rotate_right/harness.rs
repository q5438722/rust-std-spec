#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::rotate_right
// Source: core/src/slice/mod.rs:3930-3940
// Source item sha256: d3996c05273d83acdb957fc526a9fdd3d1245ac6c2f43a452b323380fad3500d
// Dependency manifest: proof_manifests/072_core_slice_rotate_right/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

macro_rules! assert {
    ($cond:expr) => {
        rust_1_96_assert($cond)
    };
}

verus! {

pub open spec fn slice_rotated_right<T>(seq: Seq<T>, k: int) -> Seq<T> {
    if 0 <= k && k <= seq.len() {
        seq.subrange(seq.len() - k, seq.len() as int).add(seq.subrange(0, seq.len() - k))
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
pub unsafe fn rust_1_96_rotate_right_ptr_rotate<T>(mid: usize, p: *mut T, k: usize) {
    rotate::ptr_rotate(mid, p.add(mid), k);
}

#[verifier::external_body]
pub fn rust_1_96_rotate_right_final_frame_bridge<T>(
    slice: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    mid: usize,
    k: usize,
    p: *mut T,
)
    requires
        old(slice)@ == source,
        k <= source.len(),
        mid as int == source.len() - k as int,
        slice_start_mut_ptr(source, p),
    ensures
        final(slice)@ == slice_rotated_right(source, k as int),
{
}

pub fn rotate_right<T>(slice: &mut [T], k: usize)
    requires
        k <= old(slice)@.len(),
    ensures
        final(slice)@ == slice_rotated_right(old(slice)@, k as int),
{
    let ghost source = slice@;
    assert!(k <= slice.len());
    let mid = slice.len() - k;
    assert(mid as int == source.len() - k as int);
    let p = as_mut_ptr(slice);

    unsafe {
        rust_1_96_rotate_right_ptr_rotate(mid, p, k);
    }
    rust_1_96_rotate_right_final_frame_bridge(slice, Ghost(source), mid, k, p);
}

}
