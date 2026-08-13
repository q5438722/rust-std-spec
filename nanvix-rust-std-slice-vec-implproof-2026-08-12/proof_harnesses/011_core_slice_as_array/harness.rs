#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_array
// Source: core/src/slice/mod.rs:850-860
// Source item sha256: efbfcb6441f004405e90bfcd0530b077ad2ce4f32d957ddff3107b2a9b669545
// Dependency manifest: proof_manifests/011_core_slice_as_array/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn array_ref_view<T, const N: usize>(array: &[T; N]) -> Seq<T> {
    (*array)@
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
pub unsafe fn rust_1_96_as_array_ref<'a, T, const N: usize>(
    slice: &'a [T],
    ptr: *const [T; N],
) -> (ret: &'a [T; N])
    requires
        slice@.len() == N,
        slice_array_ptr::<T, N>(slice@, ptr),
    ensures
        array_ref_view::<T, N>(ret) == slice@,
{
    unsafe { &*ptr }
}

pub fn as_array<'a, T, const N: usize>(slice: &'a [T]) -> (ret: Option<&'a [T; N]>)
    ensures
        slice@.len() == N ==> ret.is_some() && array_ref_view::<T, N>(ret.unwrap()) == slice@,
        slice@.len() != N ==> ret.is_none(),
{
    if slice.len() == N {
        proof {
            assert(slice@.len() == N);
        }
        let raw = as_ptr(slice);
        let ptr = rust_1_96_ptr_cast_array::<T, N>(slice, raw);
        let me = unsafe { rust_1_96_as_array_ref::<T, N>(slice, ptr) };
        Some(me)
    } else {
        proof {
            assert(slice@.len() != N);
        }
        None
    }
}

}
