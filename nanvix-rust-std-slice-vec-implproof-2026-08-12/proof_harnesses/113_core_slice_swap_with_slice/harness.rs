#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::swap_with_slice
// Source: core/src/slice/mod.rs:4422-4430
// Source item sha256: 679e07be477f68c32a5245c6034d010fdf73eb5bc7b68fc3fbfdefb56cdb515a
// Dependency manifest: proof_manifests/113_core_slice_swap_with_slice/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

macro_rules! assert {
    ($cond:expr) => {
        rust_1_96_assert($cond)
    };
    ($cond:expr, $($arg:tt)+) => {
        rust_1_96_assert($cond)
    };
}

verus! {

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

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_swap_nonoverlapping<T>(dst: *mut T, src: *mut T, count: usize) {
    core::ptr::swap_nonoverlapping(dst, src, count);
}

#[verifier::external_body]
pub fn rust_1_96_swap_with_slice_final_frame_bridge<T>(
    slice: &mut [T],
    other: &mut [T],
    Ghost(source): Ghost<Seq<T>>,
    Ghost(other_source): Ghost<Seq<T>>,
    slice_ptr: *mut T,
    other_ptr: *mut T,
    count: usize,
)
    requires
        old(slice)@ == source,
        old(other)@ == other_source,
        source.len() == other_source.len(),
        count == source.len(),
        slice_start_mut_ptr(source, slice_ptr),
        slice_start_mut_ptr(other_source, other_ptr),
    ensures
        final(slice)@ == other_source,
        final(other)@ == source,
{
}

pub fn swap_with_slice<T>(slice: &mut [T], other: &mut [T])
    requires
        old(slice)@.len() == old(other)@.len(),
    ensures
        final(slice)@ == old(other)@,
        final(other)@ == old(slice)@,
{
    let ghost source = slice@;
    let ghost other_source = other@;
    assert!(slice.len() == other.len(), "destination and source slices have different lengths");

    let slice_ptr = as_mut_ptr(slice);
    let other_ptr = as_mut_ptr(other);
    let count = slice.len();
    proof {
        assert(source.len() == other_source.len());
        assert(count == source.len());
    }

    unsafe {
        rust_1_96_ptr_swap_nonoverlapping(slice_ptr, other_ptr, count);
    }
    rust_1_96_swap_with_slice_final_frame_bridge(
        slice,
        other,
        Ghost(source),
        Ghost(other_source),
        slice_ptr,
        other_ptr,
        count,
    );
}

}
