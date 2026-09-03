#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::first_chunk_mut
// Source: core/src/slice/mod.rs:357-366
// Source item sha256: 2170d94c79e1f26619cef13c46a6700a5a217819967b3a26a6ec3dc9fc9e703d
// Dependency manifest: proof_manifests/046_core_slice_first_chunk_mut/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn array_mut_ref_view<T, const N: usize>(array: &mut [T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub open spec fn slice_fixed_prefix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange(0, N as int)
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub uninterp spec fn slice_mut_prefix_array_ptr<T, const N: usize>(
    seq: Seq<T>,
    ptr: *mut [T; N],
) -> bool;

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
pub fn rust_1_96_mut_ptr_cast_array<T, const N: usize>(
    slice: &mut [T],
    ptr: *mut T,
) -> (array_ptr: *mut [T; N])
    requires
        slice_start_mut_ptr(old(slice)@, ptr),
    ensures
        slice_mut_prefix_array_ptr::<T, N>(old(slice)@, array_ptr),
        final(slice)@ == old(slice)@,
{
    ptr.cast_array()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_first_chunk_mut_array_ref<'a, T, const N: usize>(
    slice: &'a mut [T],
    ptr: *mut [T; N],
) -> (ret: &'a mut [T; N])
    requires
        (N as int) <= old(slice)@.len(),
        slice_mut_prefix_array_ptr::<T, N>(old(slice)@, ptr),
    ensures
        array_mut_ref_view::<T, N>(ret) == slice_fixed_prefix::<T, N>(old(slice)@),
        final(slice)@ == array_value_view::<T, N>(*final(ret))
            + old(slice)@.subrange(N as int, old(slice)@.len() as int),
{
    unsafe { &mut *ptr }
}

pub fn first_chunk_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: Option<&'a mut [T; N]>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && array_mut_ref_view::<T, N>(ret.unwrap()) == slice_fixed_prefix::<T, N>(old(slice)@)
            && final(slice)@ == array_value_view::<T, N>(*final(ret.unwrap()))
                + old(slice)@.subrange(N as int, old(slice)@.len() as int),
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
{
    let ghost source = slice@;
    if slice.len() < N {
        proof {
            assert((N as int) > source.len());
        }
        None
    } else {
        proof {
            assert((N as int) <= source.len());
        }
        let raw = as_mut_ptr(slice);
        let ptr = rust_1_96_mut_ptr_cast_array::<T, N>(slice, raw);
        let chunk = unsafe { rust_1_96_first_chunk_mut_array_ref::<T, N>(slice, ptr) };
        Some(chunk)
    }
}

}
