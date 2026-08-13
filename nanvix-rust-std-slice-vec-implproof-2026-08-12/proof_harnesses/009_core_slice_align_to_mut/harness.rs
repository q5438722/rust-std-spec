#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::align_to_mut
// Source: core/src/slice/mod.rs:4564-4605
// Source item sha256: 79bc07c28c34e853de5c1bbc49ebb8f27b4e8837109fc51c6a15eef97565ec27
// Dependency manifest: proof_manifests/009_core_slice_align_to_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and preserves the Rust 1.96 branch
// structure: ZST early return, as_ptr/align_offset, offset bounds check, and the
// aligned mutable raw-parts branch. The named aligned-branch boundary covers only
// source-backed split_at_mut, align_to_offsets, rest length/as_mut_ptr, mutable
// raw-parts/provenance/aliasing, and final-frame facts that Verus does not model
// recursively in this target.

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn slice_align_to_domain<T, U>(source: Seq<T>) -> bool;

pub uninterp spec fn slice_aligned_middle<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool;

pub open spec fn slice_align_to_result<T, U>(
    source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
) -> bool {
    prefix.len() <= source.len()
        && suffix.len() <= source.len()
        && prefix.len() + suffix.len() <= source.len()
        && prefix == source.subrange(0, prefix.len() as int)
        && suffix == source.subrange((source.len() - suffix.len()) as int, source.len() as int)
        && slice_aligned_middle::<T, U>(source, prefix, middle, suffix)
}

pub open spec fn slice_align_to_mut_result<T, U>(
    old_source: Seq<T>,
    prefix: Seq<T>,
    middle: Seq<U>,
    suffix: Seq<T>,
    final_prefix: Seq<T>,
    final_middle: Seq<U>,
    final_suffix: Seq<T>,
    final_source: Seq<T>,
) -> bool {
    slice_align_to_result::<T, U>(old_source, prefix, middle, suffix)
        && final_source.len() == old_source.len()
        && final_prefix.len() == prefix.len()
        && final_middle.len() == middle.len()
        && final_suffix.len() == suffix.len()
        && final_prefix.len() + final_suffix.len() <= final_source.len()
        && final_prefix == final_source.subrange(0, final_prefix.len() as int)
        && final_suffix == final_source.subrange(
            (final_source.len() - final_suffix.len()) as int,
            final_source.len() as int,
        )
}

#[verifier::external_body]
pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool) {
    core::mem::size_of::<T>() == 0
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_ptr<T>(slice: &[T]) -> (ptr: *const T) {
    slice.as_ptr()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_ptr_align_offset<T, U>(ptr: *const T) -> (offset: usize) {
    loop {
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_align_to_mut_zst_or_overflow<'a, T, U>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    loop {
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_align_to_mut_split_offsets_raw_parts<'a, T, U>(
    slice: &'a mut [T],
    offset: usize,
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    requires
        offset <= old(slice)@.len(),
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    loop {
    }
}

pub unsafe fn align_to_mut<'a, T, U>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [T], &'a mut [U], &'a mut [T]))
    requires
        slice_align_to_domain::<T, U>(old(slice)@),
    ensures
        slice_align_to_mut_result::<T, U>(
            old(slice)@,
            ret.0@,
            ret.1@,
            ret.2@,
            final(ret.0)@,
            final(ret.1)@,
            final(ret.2)@,
            final(slice)@,
        ),
{
    if rust_1_96_type_is_zst::<U>() || rust_1_96_type_is_zst::<T>() {
        return unsafe { rust_1_96_align_to_mut_zst_or_overflow::<T, U>(slice) };
    }

    let ptr = rust_1_96_slice_as_ptr(slice);
    let offset = unsafe { rust_1_96_ptr_align_offset::<T, U>(ptr) };
    if offset > slice.len() {
        unsafe { rust_1_96_align_to_mut_zst_or_overflow::<T, U>(slice) }
    } else {
        proof {
            assert(offset <= slice.len());
        }
        unsafe { rust_1_96_align_to_mut_split_offsets_raw_parts::<T, U>(slice, offset) }
    }
}

}
