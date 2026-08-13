#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_first_chunk
// Source: core/src/slice/mod.rs:387-393
// Source item sha256: 76fb30ed3b07745c4987878944bf246f16b12ffb2debdd3ee01c7c86901b752e
// Dependency manifest: proof_manifests/089_core_slice_split_first_chunk/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: call
// split_at_checked(N), return None on out-of-range, and in the Some branch
// return the unsafe first.as_ptr().cast_array() array reference plus tail.

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
pub fn split_at_checked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: Option<(&'a [T], &'a [T])>)
    ensures
        (mid as int) <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, mid as int)
            && ret.unwrap().1@ == slice@.subrange(mid as int, slice@.len() as int),
        (mid as int) > slice@.len() ==> ret.is_none(),
{
    slice.split_at_checked(mid)
}

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
pub unsafe fn rust_1_96_split_first_chunk_array_ref<'a, T, const N: usize>(
    first: &'a [T],
    ptr: *const [T; N],
) -> (ret: &'a [T; N])
    requires
        first@.len() == N,
        slice_array_ptr::<T, N>(first@, ptr),
    ensures
        array_ref_view::<T, N>(ret) == first@,
{
    unsafe { &*ptr }
}

pub fn split_first_chunk<'a, T, const N: usize>(
    slice: &'a [T],
) -> (ret: Option<(&'a [T; N], &'a [T])>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view::<T, N>(ret.unwrap().0) == slice_fixed_prefix::<T, N>(slice@)
            && ret.unwrap().1@ == slice@.subrange(N as int, slice@.len() as int),
        (N as int) > slice@.len() ==> ret.is_none(),
{
    let Some((first, tail)) = split_at_checked(slice, N) else {
        proof {
            assert((N as int) > slice@.len());
        }
        return None;
    };

    proof {
        assert((N as int) <= slice@.len());
        assert(first@ == slice@.subrange(0, N as int));
        assert(tail@ == slice@.subrange(N as int, slice@.len() as int));
        assert(first@.len() == N);
        assert(first@ =~= slice_fixed_prefix::<T, N>(slice@));
    }

    let raw = as_ptr(first);
    let ptr = rust_1_96_ptr_cast_array::<T, N>(first, raw);
    let chunk = unsafe { rust_1_96_split_first_chunk_array_ref::<T, N>(first, ptr) };
    proof {
        assert(array_ref_view::<T, N>(chunk) == first@);
        assert(array_ref_view::<T, N>(chunk) == slice_fixed_prefix::<T, N>(slice@));
    }
    Some((chunk, tail))
}

}
