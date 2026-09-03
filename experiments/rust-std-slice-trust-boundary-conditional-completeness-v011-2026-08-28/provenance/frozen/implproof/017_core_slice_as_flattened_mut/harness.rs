#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_flattened_mut
// Source: core/src/slice/mod.rs:5487-5497
// Source item sha256: d3fdd4bf0c5162b4000f8b7d767f7802944c5834053070e69dd3469f640dc5a2
// Dependency manifest: proof_manifests/017_core_slice_as_flattened_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 control/data
// flow. The checked_mul normal-return path is executable; the trusted boundary
// is limited to source-backed intrinsic/panic/raw-pointer/provenance operations
// below: the checked_mul overflow panic edge, unchecked_mul for the non-ZST
// address-space arithmetic, the proof relation for the source-shaped
// *mut [T; N] to *mut T cast, and slice::from_raw_parts_mut final-frame reconstruction.

use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;

verus! {

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub open spec fn flatten_array_chunks<T, const N: usize>(chunks: Seq<[T; N]>) -> Seq<T> {
    if N == 0 {
        Seq::empty()
    } else {
        Seq::new(chunks.len() * (N as nat), |i: int|
            array_value_view::<T, N>(chunks[i / (N as int)])[i % (N as int)])
    }
}

pub ghost enum SliceRawMutability {
    Immutable,
    Mutable,
}

pub ghost struct SliceRawDomain {
    pub len: int,
    pub non_null: bool,
    pub aligned: bool,
    pub one_allocation: bool,
    pub initialized: bool,
    pub aliasing_ok: bool,
    pub within_isize: bool,
    pub mutability: SliceRawMutability,
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub uninterp spec fn slice_raw_mut_domain<T>(
    ptr: *mut T,
    len: usize,
    mutability: SliceRawMutability,
) -> SliceRawDomain;

pub open spec fn slice_raw_domain_valid(domain: SliceRawDomain) -> bool {
    0 <= domain.len
        && domain.non_null
        && domain.aligned
        && domain.one_allocation
        && domain.initialized
        && domain.aliasing_ok
        && domain.within_isize
}

pub open spec fn slice_raw_domain_valid_for(
    domain: SliceRawDomain,
    len: usize,
    mutability: SliceRawMutability,
) -> bool {
    slice_raw_domain_valid(domain) && domain.len == len as int && domain.mutability == mutability
}

pub uninterp spec fn flat_slice_mut_source<T>(ptr: *mut T, len: usize) -> Seq<T>;

pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool) {
    core::mem::size_of::<T>() == 0
}

pub fn rust_1_96_checked_mul_expect(lhs: usize, rhs: usize) -> (ret: usize)
    ensures
        ret as nat == lhs as nat * rhs as nat,
{
    match lhs.checked_mul(rhs) {
        Some(value) => value,
        None => rust_1_96_slice_len_overflow_panic(),
    }
}

#[verifier::external_body]
pub fn rust_1_96_slice_len_overflow_panic() -> ! {
    panic!("slice len overflow")
}

#[verifier::external_body]
pub unsafe fn rust_1_96_unchecked_mul(lhs: usize, rhs: usize) -> (ret: usize)
    ensures
        ret as nat == lhs as nat * rhs as nat,
{
    unsafe { lhs.unchecked_mul(rhs) }
}

pub fn rust_1_96_slice_as_mut_ptr_cast<U>(slice: &mut [U]) -> (ptr: *mut U)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    let len = slice.len();
    let ptr = core::ptr::null_mut::<U>().with_addr(len);
    proof {
        assert(old(slice)@.len() == len as nat);
    }
    ptr
}

pub fn as_mut_ptr<U>(slice: &mut [U]) -> (ptr: *mut U)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    rust_1_96_slice_as_mut_ptr_cast(slice)
}

#[verifier::external_body]
proof fn rust_1_96_array_mut_ptr_cast_relation<T, const N: usize>(
    slice: &mut [[T; N]],
    flat: *mut T,
    len: usize,
)
    requires
        len as nat == old(slice)@.len() * N,
    ensures
        flat_slice_mut_source::<T>(flat, len) == flatten_array_chunks::<T, N>(old(slice)@),
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(flat, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        final(slice)@ == old(slice)@,
{
}

pub fn rust_1_96_array_mut_ptr_cast<T, const N: usize>(
    slice: &mut [[T; N]],
    ptr: *mut [T; N],
    len: usize,
) -> (flat: *mut T)
    requires
        slice_start_mut_ptr(old(slice)@, ptr),
        len as nat == old(slice)@.len() * N,
    ensures
        flat_slice_mut_source::<T>(flat, len) == flatten_array_chunks::<T, N>(old(slice)@),
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(flat, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        final(slice)@ == old(slice)@,
{
    let flat = ptr as *mut T;
    proof {
        rust_1_96_array_mut_ptr_cast_relation::<T, N>(slice, flat, len);
    }
    flat
}

#[verifier::external_body]
pub unsafe fn rust_1_96_from_raw_parts_mut_flat<'a, T, const N: usize>(
    slice: &'a mut [[T; N]],
    data: *mut T,
    len: usize,
) -> (ret: &'a mut [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        flat_slice_mut_source::<T>(data, len) == flatten_array_chunks::<T, N>(old(slice)@),
    ensures
        ret@ == flatten_array_chunks::<T, N>(old(slice)@),
        ret@.len() == len,
        flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@,
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

pub unsafe fn from_raw_parts_mut<'a, T, const N: usize>(
    slice: &'a mut [[T; N]],
    data: *mut T,
    len: usize,
) -> (ret: &'a mut [T])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        flat_slice_mut_source::<T>(data, len) == flatten_array_chunks::<T, N>(old(slice)@),
    ensures
        ret@ == flatten_array_chunks::<T, N>(old(slice)@),
        ret@.len() == len,
        flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@,
{
    unsafe { rust_1_96_from_raw_parts_mut_flat::<T, N>(slice, data, len) }
}

pub fn as_flattened_mut<'a, T, const N: usize>(slice: &'a mut [[T; N]]) -> (ret: &'a mut [T])
    ensures
        ret@ == flatten_array_chunks::<T, N>(old(slice)@),
        flatten_array_chunks::<T, N>(final(slice)@) == final(ret)@,
{
    let ghost source = slice@;
    let chunk_len = slice.len();
    proof {
        assert(chunk_len as nat == source.len());
    }
    let len = if rust_1_96_type_is_zst::<T>() {
        rust_1_96_checked_mul_expect(chunk_len, N)
    } else {
        unsafe { rust_1_96_unchecked_mul(chunk_len, N) }
    };
    proof {
        assert(len as nat == source.len() * N);
    }
    let ptr = as_mut_ptr::<[T; N]>(slice);
    let flat_ptr = rust_1_96_array_mut_ptr_cast::<T, N>(slice, ptr, len);
    unsafe { from_raw_parts_mut::<T, N>(slice, flat_ptr, len) }
}

}
