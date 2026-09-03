#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_mut_ptr_range
// Source: core/src/slice/mod.rs:836-841
// Source item sha256: 55220e2d82364704a997a82d83801dc9c3b9cd696b3bfa33155b979609448b31
// Dependency manifest: proof_manifests/020_core_slice_as_mut_ptr_range/dependency_assumption_manifest.json

use core::ops::Range;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub uninterp spec fn slice_mut_ptr_range_result<T>(seq: Seq<T>, range: Range<*mut T>) -> bool;

pub open spec fn slice_mut_ptr_range_starts_at_slice<T>(
    seq: Seq<T>,
    range: Range<*mut T>,
) -> bool {
    slice_mut_ptr_range_result(seq, range) && slice_start_mut_ptr(seq, range.start)
}

pub fn rust_1_96_slice_as_mut_ptr_cast<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    let len = slice.len();
    let ptr = core::ptr::null_mut::<T>().with_addr(len);
    proof {
        assert(old(slice)@.len() == len as nat);
    }
    ptr
}

pub fn as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    rust_1_96_slice_as_mut_ptr_cast(slice)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_mut_ptr_add_range_end<T>(
    slice: &mut [T],
    start: *mut T,
    len: usize,
) -> (end: *mut T)
    requires
        slice_start_mut_ptr(old(slice)@, start),
        len == old(slice)@.len(),
    ensures
        slice_mut_ptr_range_result(old(slice)@, start..end),
        final(slice)@ == old(slice)@,
{
    unsafe { start.add(len) }
}

pub fn as_mut_ptr_range<T>(slice: &mut [T]) -> (range: Range<*mut T>)
    ensures
        slice_mut_ptr_range_starts_at_slice(old(slice)@, range),
        final(slice)@ == old(slice)@,
{
    let start = as_mut_ptr(slice);
    let len = slice.len();
    let end = unsafe { rust_1_96_mut_ptr_add_range_end(slice, start, len) };
    start..end
}

}
