#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at_unchecked
// Source: core/src/slice/mod.rs:2038-2054
// Source item sha256: 33646e1f7899e0cc5529360a61d81cc1939dbeb9053ecf983a01bbcda4bca4b0
// Dependency manifest: proof_manifests/087_core_slice_split_at_unchecked/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: len, as_ptr,
// unsafe-precondition check, and the unsafe raw-parts split expression. The raw
// pointer/provenance, unchecked subtraction, and raw-parts construction facts
// stay behind named source-backed boundaries.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub mod ub_checks {
    use super::*;

    pub fn assert_unsafe_precondition(mid: usize, len: usize)
        requires
            mid <= len,
    {
    }
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_ptr_cast<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    slice as *const [T] as *const T
}

pub fn as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    rust_1_96_slice_as_ptr_cast(slice)
}

#[verifier::external_body]
pub unsafe fn unchecked_sub(len: usize, mid: usize) -> (ret: usize)
    requires
        mid <= len,
    ensures
        ret as int == len as int - mid as int,
{
    len - mid
}

#[verifier::external_body]
pub unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> (ret: &'a [T])
    ensures
        ret@.len() == len,
        slice_start_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts(data, len) }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_split_at_unchecked_raw_parts<'a, T>(
    slice: &'a [T],
    ptr: *const T,
    mid: usize,
    len: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        split_point_in_range(slice@, mid),
        mid <= len,
        len == slice@.len(),
        slice_start_ptr(slice@, ptr),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    unsafe { (from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))) }
}

pub unsafe fn split_at_unchecked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        split_point_in_range(slice@, mid),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
        assert((mid as int) <= source.len());
        assert(mid <= len);
    }

    let ptr = as_ptr(slice);

    ub_checks::assert_unsafe_precondition(mid, len);

    unsafe { rust_1_96_split_at_unchecked_raw_parts(slice, ptr, mid, len) }
}

}
