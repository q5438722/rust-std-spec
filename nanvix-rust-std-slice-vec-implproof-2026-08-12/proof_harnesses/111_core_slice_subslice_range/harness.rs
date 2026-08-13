#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::subslice_range
// Source: core/src/slice/mod.rs:5315-5337
// Source item sha256: a7deec2b313078cd2025212553c60d1578ed93aac7baa15a11c2749f97fd5421
// Dependency manifest: proof_manifests/111_core_slice_subslice_range/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 control/data
// flow. The trusted boundary is limited to source-backed layout panic handling,
// immutable as_ptr, pointer-address observation, wrapping address subtraction,
// alignment/division over size_of::<T>(), wrapping end construction, and the
// pure pointer-domain bridge needed because the generated contract's Seq view
// does not model addresses or provenance.

use core::ops::Range;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub uninterp spec fn rust_type_is_zst<T>() -> bool;

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub uninterp spec fn slice_subslice_range_result<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    range: Range<usize>,
) -> bool;

pub uninterp spec fn slice_subslice_in_domain<T>(seq: Seq<T>, subslice: Seq<T>) -> bool;

pub open spec fn slice_subslice_range_option_result<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    ret: Option<Range<usize>>,
) -> bool {
    (ret.is_some() ==> slice_subslice_range_result(seq, subslice, ret.unwrap())
        && subslice.len() <= seq.len())
        && (ret.is_none() ==> !slice_subslice_in_domain(seq, subslice))
}

#[verifier::external_body]
pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool)
    ensures
        is_zst == rust_type_is_zst::<T>(),
{
    core::mem::size_of::<T>() == 0
}

#[verifier::external_body]
pub fn rust_1_96_subslice_range_zst_panic<T>()
    ensures
        false,
{
    panic!("elements are zero-sized");
}

#[verifier::external_body]
pub fn rust_1_96_size_of<T>() -> (size: usize)
    ensures
        rust_type_is_zst::<T>() <==> size == 0,
        !rust_type_is_zst::<T>() ==> size > 0,
{
    core::mem::size_of::<T>()
}

#[verifier::external_body]
pub fn rust_1_96_slice_as_ptr_cast<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    slice as *const [T] as *const T
}

pub fn as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    rust_1_96_slice_as_ptr_cast(slice)
}

#[verifier::external_body]
pub fn rust_1_96_ptr_addr<T>(ptr: *const T) -> (addr: usize) {
    ptr.addr()
}

#[verifier::external_body]
pub fn rust_1_96_wrapping_sub(lhs: usize, rhs: usize) -> (ret: usize) {
    lhs.wrapping_sub(rhs)
}

#[verifier::external_body]
pub fn rust_1_96_is_multiple_of(value: usize, divisor: usize) -> (ret: bool)
    requires
        divisor > 0,
{
    value.is_multiple_of(divisor)
}

#[verifier::external_body]
pub fn rust_1_96_divide_byte_offset(byte_offset: usize, size: usize) -> (offset: usize)
    requires
        size > 0,
{
    byte_offset / size
}

#[verifier::external_body]
pub fn rust_1_96_wrapping_add(lhs: usize, rhs: usize) -> (ret: usize) {
    lhs.wrapping_add(rhs)
}

#[verifier::external_body]
pub proof fn rust_1_96_subslice_range_unaligned_bridge<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    self_ptr: *const T,
    subslice_ptr: *const T,
    self_start: usize,
    subslice_start: usize,
    byte_start: usize,
    size: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        slice_start_ptr(subslice, subslice_ptr),
        size > 0,
    ensures
        slice_subslice_range_option_result(seq, subslice, None),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_subslice_range_oob_bridge<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    self_ptr: *const T,
    subslice_ptr: *const T,
    self_start: usize,
    subslice_start: usize,
    byte_start: usize,
    size: usize,
    start: usize,
    end: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        slice_start_ptr(subslice, subslice_ptr),
        size > 0,
        !(start <= seq.len() && end <= seq.len()),
    ensures
        slice_subslice_range_option_result(seq, subslice, None),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_subslice_range_some_bridge<T>(
    seq: Seq<T>,
    subslice: Seq<T>,
    self_ptr: *const T,
    subslice_ptr: *const T,
    self_start: usize,
    subslice_start: usize,
    byte_start: usize,
    size: usize,
    start: usize,
    end: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        slice_start_ptr(subslice, subslice_ptr),
        size > 0,
        start <= seq.len(),
        end <= seq.len(),
    ensures
        slice_subslice_range_option_result(seq, subslice, Some(Range { start, end })),
{
}

pub fn subslice_range<T>(slice: &[T], subslice: &[T]) -> (ret: Option<Range<usize>>)
    ensures
        slice_subslice_range_option_result(slice@, subslice@, ret),
{
    let ghost source = slice@;
    let ghost sub = subslice@;
    let is_zst = rust_1_96_type_is_zst::<T>();
    if is_zst {
        rust_1_96_subslice_range_zst_panic::<T>();
    }

    let self_ptr = as_ptr(slice);
    let self_start = rust_1_96_ptr_addr(self_ptr);
    let subslice_ptr = as_ptr(subslice);
    let subslice_start = rust_1_96_ptr_addr(subslice_ptr);

    let byte_start = rust_1_96_wrapping_sub(subslice_start, self_start);
    let size = rust_1_96_size_of::<T>();
    proof {
        assert(!rust_type_is_zst::<T>());
        assert(size > 0);
    }

    if !rust_1_96_is_multiple_of(byte_start, size) {
        proof {
            rust_1_96_subslice_range_unaligned_bridge(
                source,
                sub,
                self_ptr,
                subslice_ptr,
                self_start,
                subslice_start,
                byte_start,
                size,
            );
        }
        return None;
    }

    let start = rust_1_96_divide_byte_offset(byte_start, size);
    let end = rust_1_96_wrapping_add(start, subslice.len());

    if start <= slice.len() && end <= slice.len() {
        let range = Range { start, end };
        proof {
            rust_1_96_subslice_range_some_bridge(
                source,
                sub,
                self_ptr,
                subslice_ptr,
                self_start,
                subslice_start,
                byte_start,
                size,
                start,
                end,
            );
        }
        Some(range)
    } else {
        proof {
            assert(!(start <= source.len() && end <= source.len()));
            rust_1_96_subslice_range_oob_bridge(
                source,
                sub,
                self_ptr,
                subslice_ptr,
                self_start,
                subslice_start,
                byte_start,
                size,
                start,
                end,
            );
        }
        None
    }
}

}
