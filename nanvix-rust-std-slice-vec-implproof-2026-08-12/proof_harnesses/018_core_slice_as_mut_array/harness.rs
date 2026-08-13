#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_mut_array
// Source: core/src/slice/mod.rs:869-879
// Source item sha256: d2208668f0b01536cedf4b43a19beca6d879c2dca9e7fb2ba16b10a8110d0529
// Dependency manifest: proof_manifests/018_core_slice_as_mut_array/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn array_mut_ref_view<T, const N: usize>(array: &mut [T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub uninterp spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool;

pub uninterp spec fn slice_mut_array_ptr<T, const N: usize>(
    seq: Seq<T>,
    ptr: *mut [T; N],
) -> bool;

#[verifier::external_body]
pub fn rust_1_96_slice_as_mut_ptr_cast<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    slice as *mut [T] as *mut T
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
        slice_mut_array_ptr::<T, N>(old(slice)@, array_ptr),
        final(slice)@ == old(slice)@,
{
    ptr.cast_array()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_as_mut_array_ref<'a, T, const N: usize>(
    slice: &'a mut [T],
    ptr: *mut [T; N],
) -> (ret: &'a mut [T; N])
    requires
        old(slice)@.len() == N,
        slice_mut_array_ptr::<T, N>(old(slice)@, ptr),
    ensures
        array_mut_ref_view::<T, N>(ret) == old(slice)@,
        final(slice)@ == array_value_view::<T, N>(*final(ret)),
{
    unsafe { &mut *ptr }
}

pub fn as_mut_array<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: Option<&'a mut [T; N]>)
    ensures
        old(slice)@.len() == N ==> ret.is_some()
            && array_mut_ref_view::<T, N>(ret.unwrap()) == old(slice)@
            && final(slice)@ == array_value_view::<T, N>(*final(ret.unwrap())),
        old(slice)@.len() != N ==> ret.is_none() && final(slice)@ == old(slice)@,
{
    let ghost source = slice@;
    if slice.len() == N {
        proof {
            assert(source.len() == N);
        }
        let raw = as_mut_ptr(slice);
        let ptr = rust_1_96_mut_ptr_cast_array::<T, N>(slice, raw);
        let me = unsafe { rust_1_96_as_mut_array_ref::<T, N>(slice, ptr) };
        Some(me)
    } else {
        proof {
            assert(source.len() != N);
        }
        None
    }
}

}
