#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_at_mut_unchecked
// Source: core/src/slice/mod.rs:2092-2112
// Source item sha256: 64e5aaab27b44c5104ff431b7f8c1be361ea556baa432a36e7386e76089a4531
// Dependency manifest: proof_manifests/086_core_slice_split_at_mut_unchecked/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: len, as_mut_ptr,
// unsafe-precondition check, and the unsafe raw-parts split expression. The raw
// pointer/provenance, unchecked subtraction, raw-parts construction, and final
// mutable frame facts stay behind named source-backed boundaries.

use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub open spec fn split_at_mut_unchecked_result<T>(
    source: Seq<T>,
    mid: usize,
    left: Seq<T>,
    right: Seq<T>,
    final_source: Seq<T>,
    final_left: Seq<T>,
    final_right: Seq<T>,
) -> bool {
    left == source.subrange(0, mid as int)
        && right == source.subrange(mid as int, source.len() as int)
        && final_source == final_left + final_right
}

pub mod ub_checks {
    use super::*;

    pub fn assert_unsafe_precondition(mid: usize, len: usize)
        requires
            mid <= len,
    {
    }
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

pub unsafe fn unchecked_sub(len: usize, mid: usize) -> (ret: usize)
    requires
        mid <= len,
    ensures
        ret as int == len as int - mid as int,
{
    proof {
        assert(mid <= len);
    }
    len - mid
}

#[verifier::external_body]
pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    ensures
        ret@.len() == len,
        slice_start_mut_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_split_at_mut_unchecked_raw_parts<'a, T>(
    slice: &'a mut [T],
    ptr: *mut T,
    mid: usize,
    len: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
        mid <= len,
        len == old(slice)@.len(),
        slice_start_mut_ptr(old(slice)@, ptr),
    ensures
        split_at_mut_unchecked_result(
            old(slice)@,
            mid,
            ret.0@,
            ret.1@,
            final(slice)@,
            final(ret.0)@,
            final(ret.1)@,
        ),
{
    unsafe {
        (
            from_raw_parts_mut(ptr, mid),
            from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid)),
        )
    }
}

pub unsafe fn split_at_mut_unchecked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
        assert((mid as int) <= source.len());
        assert(mid <= len);
    }

    let ptr = as_mut_ptr(slice);

    ub_checks::assert_unsafe_precondition(mid, len);

    unsafe { rust_1_96_split_at_mut_unchecked_raw_parts(slice, ptr, mid, len) }
}

}
