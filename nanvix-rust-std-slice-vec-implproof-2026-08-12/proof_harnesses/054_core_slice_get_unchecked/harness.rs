#![allow(dead_code, unused_imports, unused_variables, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::get_unchecked
// Source: core/src/slice/mod.rs:639-647
// Source item sha256: 52a8f107029603a78f11de9d849732deb57d722ee78dbe2ce36072a67108c3d5
// Dependency manifest: proof_manifests/054_core_slice_get_unchecked/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub trait SliceIndex<T> {
    type Output;
}

pub uninterp spec fn slice_index_in_range<T, I>(seq: Seq<T>, index: I) -> bool;

pub uninterp spec fn slice_index_result<T, I>(
    seq: Seq<T>,
    index: I,
    ret: &<I as SliceIndex<T>>::Output,
) -> bool
    where
        I: SliceIndex<T>;

#[verifier::external_body]
pub unsafe fn rust_1_96_sliceindex_get_unchecked_ref<'a, T, I>(
    slice: &'a [T],
    index: I,
) -> (ret: &'a <I as SliceIndex<T>>::Output)
    where
        I: SliceIndex<T>,
    requires
        slice_index_in_range::<T, I>(slice@, index),
    ensures
        slice_index_result::<T, I>(slice@, index, ret),
{
    loop {
    }
}

pub unsafe fn get_unchecked<'a, T, I>(
    slice: &'a [T],
    index: I,
) -> (ret: &'a <I as SliceIndex<T>>::Output)
    where
        I: SliceIndex<T>,
    requires
        slice_index_in_range::<T, I>(slice@, index),
    ensures
        slice_index_result::<T, I>(slice@, index, ret),
{
    // SAFETY: the caller upholds the generated in-range SliceIndex domain.
    // The source-backed trait boundary covers the raw pointer result and deref.
    unsafe { rust_1_96_sliceindex_get_unchecked_ref(slice, index) }
}

}
