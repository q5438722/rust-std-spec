#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::first_chunk
// Source: core/src/slice/mod.rs:327-335
// Source item sha256: 2d6510def24ad43c531530168886eac87c775205f9dedcf10983714e4f8cc122
// Dependency manifest: proof_manifests/045_core_slice_first_chunk/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn array_ref_view<T, const N: usize>(array: &[T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn slice_fixed_prefix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange(0, N as int)
}

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub uninterp spec fn slice_array_ptr<T, const N: usize>(seq: Seq<T>, ptr: *const [T; N]) -> bool;

#[verifier::external_body]
pub fn rust_1_96_slice_as_ptr_cast<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    slice.as_ptr()
}

pub fn as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    rust_1_96_slice_as_ptr_cast(slice)
}

#[verifier::external_body]
pub fn rust_1_96_ptr_cast_array<T, const N: usize>(
    slice: &[T],
    ptr: *const T,
) -> (array_ptr: *const [T; N])
    requires
        slice_start_ptr(slice@, ptr),
    ensures
        slice_array_ptr::<T, N>(slice@, array_ptr),
{
    ptr.cast_array()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_first_chunk_array_ref<'a, T, const N: usize>(
    slice: &'a [T],
    ptr: *const [T; N],
) -> (ret: &'a [T; N])
    requires
        (N as int) <= slice@.len(),
        slice_array_ptr::<T, N>(slice@, ptr),
    ensures
        array_ref_view::<T, N>(ret) == slice_fixed_prefix::<T, N>(slice@),
{
    unsafe { &*ptr }
}

pub fn first_chunk<'a, T, const N: usize>(slice: &'a [T]) -> (ret: Option<&'a [T; N]>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view::<T, N>(ret.unwrap()) == slice_fixed_prefix::<T, N>(slice@),
        (N as int) > slice@.len() ==> ret.is_none(),
{
    if slice.len() < N {
        proof {
            assert((N as int) > slice@.len());
        }
        None
    } else {
        proof {
            assert((N as int) <= slice@.len());
        }
        let raw = as_ptr(slice);
        let ptr = rust_1_96_ptr_cast_array::<T, N>(slice, raw);
        let chunk = unsafe { rust_1_96_first_chunk_array_ref::<T, N>(slice, ptr) };
        Some(chunk)
    }
}

}
