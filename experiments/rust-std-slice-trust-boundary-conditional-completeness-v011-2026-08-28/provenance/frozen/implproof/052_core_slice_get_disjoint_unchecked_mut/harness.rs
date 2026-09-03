#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::get_disjoint_unchecked_mut
// Source: core/src/slice/mod.rs:5142-5166
// Source item sha256: fadb1cf499d963bdf8603a8901d68a9dc03c5ce7ebf3f084ce0fe58348b65be2
// Dependency manifest: proof_manifests/052_core_slice_get_disjoint_unchecked_mut/dependency_assumption_manifest.json

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
    // NB: This implementation is written as it is because any variation of
    // `indices.map(|i| self.get_unchecked_mut(i))` would make miri unhappy,
    // or generate worse code otherwise. This is also why we need to go
    // through a raw pointer here.
    let ghost source = slice@;
    let slice_raw = rust_1_96_slice_receiver_to_raw(slice);
    assert(slice@ == source);
    let mut arr = rust_1_96_maybe_uninit_array_uninit::<T, I>();
    let arr_ptr = rust_1_96_maybe_uninit_array_as_mut_ptr(&mut arr);

    // SAFETY: We expect `indices` to contain disjunct values that are
    // in bounds of `self`.
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

}
