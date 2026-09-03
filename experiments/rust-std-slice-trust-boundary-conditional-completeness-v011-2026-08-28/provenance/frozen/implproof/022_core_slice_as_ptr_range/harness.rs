#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_ptr_range
// Source: core/src/slice/mod.rs:793-814
// Source item sha256: b42ea830188debee4c9145f4e52e8a270861f5c3845a4f1c4a50e006987ed5d7
// Dependency manifest: proof_manifests/022_core_slice_as_ptr_range/dependency_assumption_manifest.json

use core::ops::Range;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub uninterp spec fn slice_ptr_range_result<T>(seq: Seq<T>, range: Range<*const T>) -> bool;

pub open spec fn slice_ptr_range_starts_at_slice<T>(
    seq: Seq<T>,
    range: Range<*const T>,
) -> bool {
    slice_ptr_range_result(seq, range) && slice_start_ptr(seq, range.start)
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

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_add_range_end<T>(
    slice: &[T],
    start: *const T,
    len: usize,
) -> (end: *const T)
    requires
        slice_start_ptr(slice@, start),
        len == slice@.len(),
    ensures
        slice_ptr_range_result(slice@, start..end),
{
    unsafe { start.add(len) }
}

pub fn as_ptr_range<T>(slice: &[T]) -> (range: Range<*const T>)
    ensures
        slice_ptr_range_starts_at_slice(slice@, range),
{
    let start = as_ptr(slice);
    let len = slice.len();
    let end = unsafe { rust_1_96_ptr_add_range_end(slice, start, len) };
    start..end
}

}
