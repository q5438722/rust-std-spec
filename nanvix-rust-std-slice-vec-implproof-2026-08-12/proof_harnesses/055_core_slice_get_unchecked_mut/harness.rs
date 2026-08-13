#![allow(dead_code, unused_imports, unused_variables, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::get_unchecked_mut
// Source: core/src/slice/mod.rs:684-692
// Source item sha256: feb16246768c2ac347ede8b95039570e3fddfb54257e2f8abadf710ff1c139e1
// Dependency manifest: proof_manifests/055_core_slice_get_unchecked_mut/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub trait SliceIndex<T> {
    type Output;
}

pub uninterp spec fn slice_index_in_range<T, I>(seq: Seq<T>, index: I) -> bool;

pub uninterp spec fn slice_index_mut_frame<T, I>(
    old_seq: Seq<T>,
    index: I,
    final_seq: Seq<T>,
) -> bool;

#[verifier::external_body]
pub unsafe fn rust_1_96_sliceindex_get_unchecked_mut_ref<'a, T, I>(
    slice: &'a mut [T],
    index: I,
) -> (ret: &'a mut <I as SliceIndex<T>>::Output)
    where
        I: SliceIndex<T>,
    requires
        slice_index_in_range::<T, I>(old(slice)@, index),
    ensures
        slice_index_mut_frame::<T, I>(old(slice)@, index, final(slice)@),
{
    loop {
    }
}

pub unsafe fn get_unchecked_mut<'a, T, I>(
    slice: &'a mut [T],
    index: I,
) -> (ret: &'a mut <I as SliceIndex<T>>::Output)
    where
        I: SliceIndex<T>,
    requires
        slice_index_in_range::<T, I>(old(slice)@, index),
    ensures
        slice_index_mut_frame::<T, I>(old(slice)@, index, final(slice)@),
{
    // SAFETY: the caller upholds the generated in-range SliceIndex domain.
    // The source-backed trait boundary covers the raw mutable pointer result and deref.
    unsafe { rust_1_96_sliceindex_get_unchecked_mut_ref(slice, index) }
}

}
