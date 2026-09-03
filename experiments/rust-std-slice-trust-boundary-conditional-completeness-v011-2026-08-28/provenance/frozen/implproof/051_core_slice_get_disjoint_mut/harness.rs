#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::get_disjoint_mut
// Source: core/src/slice/mod.rs:5209-5220
// Source item sha256: 292597fa2c1db3013b7e606fa810dbc0b309cbbe4f2f916c0cd4e02dd40bd59d
// Dependency manifest: proof_manifests/051_core_slice_get_disjoint_mut/dependency_assumption_manifest.json

use core::clone::Clone;
use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn slice_disjoint_indices_valid<T, I, const N: usize>(
    seq: Seq<T>,
    indices: [I; N],
) -> bool;

pub trait GetDisjointMutIndex: Clone {
}

pub trait SliceIndex<T> {
    type Output;
}

pub enum GetDisjointMutError {
    IndexOutOfBounds,
    OverlappingIndices,
}

pub struct RustSliceRawPtr<T> {
    _marker: PhantomData<T>,
}

pub struct RustMaybeUninitMutRefArray<'a, T: 'a, I> {
    _marker_slice: PhantomData<&'a mut T>,
    _marker_index: PhantomData<I>,
}

pub struct RustMutRefArrayPtr<'a, T: 'a, I> {
    _marker_slice: PhantomData<&'a mut T>,
    _marker_index: PhantomData<I>,
}

#[verifier::external_body]
pub fn get_disjoint_check_valid<I, const N: usize>(
    indices: &[I; N],
    len: usize,
    Ghost(valid): Ghost<bool>,
) -> (ret: core::result::Result<(), GetDisjointMutError>)
    ensures
        match ret {
            core::result::Result::Ok(()) => valid,
            core::result::Result::Err(_) => !valid,
        },
{
    core::result::Result::Ok(())
}

pub fn rust_1_96_slice_receiver_to_raw<T>(slice: &mut [T]) -> (ret: RustSliceRawPtr<T>)
    ensures
        final(slice)@ == old(slice)@,
{
    RustSliceRawPtr { _marker: PhantomData }
}

pub fn rust_1_96_maybe_uninit_array_uninit<'a, T, I>() -> (
    ret: RustMaybeUninitMutRefArray<'a, T, I>
) {
    RustMaybeUninitMutRefArray { _marker_slice: PhantomData, _marker_index: PhantomData }
}

pub fn rust_1_96_maybe_uninit_array_as_mut_ptr<'a, T, I>(
    arr: &mut RustMaybeUninitMutRefArray<'a, T, I>,
) -> (ret: RustMutRefArrayPtr<'a, T, I>) {
    RustMutRefArrayPtr { _marker_slice: PhantomData, _marker_index: PhantomData }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_fill_disjoint_mut_array_and_assume_init<'a, T, I, const N: usize>(
    slice: &'a mut [T],
    slice_raw: RustSliceRawPtr<T>,
    indices: [I; N],
    arr_ptr: RustMutRefArrayPtr<'a, T, I>,
    arr: &mut RustMaybeUninitMutRefArray<'a, T, I>,
) -> (ret: [&'a mut <I as SliceIndex<T>>::Output; N])
    where
        I: GetDisjointMutIndex + SliceIndex<T>,
    requires
        slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices),
    ensures
        final(slice)@.len() == old(slice)@.len(),
{
    unsafe {
        core::mem::MaybeUninit::<[&'a mut <I as SliceIndex<T>>::Output; N]>::uninit()
            .assume_init()
    }
}

pub unsafe fn get_disjoint_unchecked_mut<'a, T, I, const N: usize>(
    slice: &'a mut [T],
    indices: [I; N],
) -> (ret: [&'a mut <I as SliceIndex<T>>::Output; N])
    where
        I: GetDisjointMutIndex + SliceIndex<T>,
    requires
        slice_disjoint_indices_valid::<T, I, N>(old(slice)@, indices),
    ensures
        final(slice)@.len() == old(slice)@.len(),
{
    let ghost source = slice@;
    let slice_raw = rust_1_96_slice_receiver_to_raw(slice);
    assert(slice@ == source);
    let mut arr = rust_1_96_maybe_uninit_array_uninit::<T, I>();
    let arr_ptr = rust_1_96_maybe_uninit_array_as_mut_ptr(&mut arr);

    let ret = unsafe {
        rust_1_96_fill_disjoint_mut_array_and_assume_init::<T, I, N>(
            slice,
            slice_raw,
            indices,
            arr_ptr,
            &mut arr,
        )
    };
    ret
}

pub fn get_disjoint_mut<'a, T, I, const N: usize>(
    slice: &'a mut [T],
    indices: [I; N],
) -> (ret: core::result::Result<[&'a mut <I as SliceIndex<T>>::Output; N], GetDisjointMutError>)
    where
        I: GetDisjointMutIndex + SliceIndex<T>,
    ensures
        match ret {
            core::result::Result::Ok(_) => slice_disjoint_indices_valid::<T, I, N>(
                old(slice)@,
                indices,
            ) && final(slice)@.len() == old(slice)@.len(),
            core::result::Result::Err(_) => !slice_disjoint_indices_valid::<T, I, N>(
                old(slice)@,
                indices,
            ) && final(slice)@ == old(slice)@,
        },
{
    let ghost source = slice@;
    let ghost valid = slice_disjoint_indices_valid::<T, I, N>(source, indices);
    let check = get_disjoint_check_valid(&indices, slice.len(), Ghost(valid));
    match check {
        core::result::Result::Ok(()) => {
            let ret = unsafe { get_disjoint_unchecked_mut(slice, indices) };
            core::result::Result::Ok(ret)
        },
        core::result::Result::Err(error) => core::result::Result::Err(error),
    }
}

}
