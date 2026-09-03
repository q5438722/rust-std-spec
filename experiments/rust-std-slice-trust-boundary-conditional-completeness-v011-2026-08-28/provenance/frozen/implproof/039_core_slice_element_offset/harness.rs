#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: core::slice::element_offset
// Source: core/src/slice/mod.rs:5260-5277
// Source item sha256: 2e1c40be6fe7b5b51032b7132000aa531f27957039e0545dee3811b6d36ad61a
// Dependency manifest: proof_manifests/039_core_slice_element_offset/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 control/data
// flow. The wrapping subtraction, alignment check, byte-offset division, and
// pointer-address observation, and concrete size queries are now executable
// verified helpers. The remaining trusted boundary is limited to source-backed
// ZST panic handling, immutable as_ptr, ptr::from_ref, and the pure
// pointer-domain bridge needed because the generated contract's Seq view does
// not model addresses or provenance.

use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub uninterp spec fn slice_element_offset_result<T>(seq: Seq<T>, element: &T, index: usize) -> bool;

pub uninterp spec fn slice_element_in_domain<T>(seq: Seq<T>, element: &T) -> bool;

pub open spec fn slice_element_offset_option_result<T>(
    seq: Seq<T>,
    element: &T,
    ret: Option<usize>,
) -> bool {
    (ret.is_some() ==> ret.unwrap() < seq.len()
        && slice_element_in_domain(seq, element)
        && slice_element_offset_result(seq, element, ret.unwrap()))
        && (ret.is_none() ==> !slice_element_in_domain(seq, element))
}

pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool)
    ensures
        is_zst == (core::mem::size_of::<T>() == 0),
{
    core::mem::size_of::<T>() == 0
}

#[verifier::external_body]
pub fn rust_1_96_element_offset_zst_panic<T>()
    ensures
        false,
{
    panic!("elements are zero-sized");
}

pub fn rust_1_96_size_of<T>() -> (size: usize)
    ensures
        size == core::mem::size_of::<T>(),
{
    core::mem::size_of::<T>()
}

pub fn rust_1_96_slice_as_ptr_cast<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    let len = slice.len();
    let ptr = core::ptr::null::<T>().with_addr(len);
    proof {
        assert(slice@.len() == len as nat);
    }
    ptr
}

pub fn as_ptr<T>(slice: &[T]) -> (ptr: *const T)
    ensures
        slice_start_ptr(slice@, ptr),
{
    rust_1_96_slice_as_ptr_cast(slice)
}

pub fn rust_1_96_ptr_addr<T>(ptr: *const T) -> (addr: usize) {
    ptr.addr()
}

#[verifier::external_body]
pub fn rust_1_96_ptr_from_ref<T>(element: &T) -> (ptr: *const T) {
    core::ptr::from_ref(element)
}

pub fn rust_1_96_wrapping_sub(lhs: usize, rhs: usize) -> (ret: usize) {
    lhs.wrapping_sub(rhs)
}

pub fn rust_1_96_is_multiple_of(value: usize, divisor: usize) -> (ret: bool)
    requires
        divisor > 0,
{
    value.is_multiple_of(divisor)
}

pub fn rust_1_96_divide_byte_offset(byte_offset: usize, size: usize) -> (offset: usize)
    requires
        size > 0,
{
    byte_offset / size
}

#[verifier::external_body]
pub proof fn rust_1_96_element_offset_unaligned_bridge<T>(
    seq: Seq<T>,
    element: &T,
    self_ptr: *const T,
    elem_ptr: *const T,
    self_start: usize,
    elem_start: usize,
    byte_offset: usize,
    size: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        size > 0,
    ensures
        slice_element_offset_option_result(seq, element, None),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_element_offset_oob_bridge<T>(
    seq: Seq<T>,
    element: &T,
    self_ptr: *const T,
    elem_ptr: *const T,
    self_start: usize,
    elem_start: usize,
    byte_offset: usize,
    size: usize,
    offset: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        size > 0,
        offset >= seq.len(),
    ensures
        slice_element_offset_option_result(seq, element, None),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_element_offset_some_bridge<T>(
    seq: Seq<T>,
    element: &T,
    self_ptr: *const T,
    elem_ptr: *const T,
    self_start: usize,
    elem_start: usize,
    byte_offset: usize,
    size: usize,
    offset: usize,
)
    requires
        slice_start_ptr(seq, self_ptr),
        size > 0,
        offset < seq.len(),
    ensures
        slice_element_offset_option_result(seq, element, Some(offset)),
{
}

pub fn element_offset<T>(slice: &[T], element: &T) -> (ret: Option<usize>)
    ensures
        slice_element_offset_option_result(slice@, element, ret),
{
    let ghost source = slice@;
    let is_zst = rust_1_96_type_is_zst::<T>();
    if is_zst {
        rust_1_96_element_offset_zst_panic::<T>();
    }

    let self_ptr = as_ptr(slice);
    let self_start = rust_1_96_ptr_addr(self_ptr);
    let elem_ptr = rust_1_96_ptr_from_ref(element);
    let elem_start = rust_1_96_ptr_addr(elem_ptr);

    let byte_offset = rust_1_96_wrapping_sub(elem_start, self_start);
    let size = rust_1_96_size_of::<T>();
    proof {
        assert(core::mem::size_of::<T>() != 0);
        assert(size > 0);
    }

    if !rust_1_96_is_multiple_of(byte_offset, size) {
        proof {
            rust_1_96_element_offset_unaligned_bridge(
                source,
                element,
                self_ptr,
                elem_ptr,
                self_start,
                elem_start,
                byte_offset,
                size,
            );
        }
        return None;
    }

    let offset = rust_1_96_divide_byte_offset(byte_offset, size);

    if offset < slice.len() {
        proof {
            rust_1_96_element_offset_some_bridge(
                source,
                element,
                self_ptr,
                elem_ptr,
                self_start,
                elem_start,
                byte_offset,
                size,
                offset,
            );
        }
        Some(offset)
    } else {
        proof {
            rust_1_96_element_offset_oob_bridge(
                source,
                element,
                self_ptr,
                elem_ptr,
                self_start,
                elem_start,
                byte_offset,
                size,
                offset,
            );
        }
        None
    }
}

}
