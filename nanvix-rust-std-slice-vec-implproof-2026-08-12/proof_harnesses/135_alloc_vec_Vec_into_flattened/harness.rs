#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::into_flattened
// Source: alloc/src/vec/mod.rs:3592-3611
// Source item sha256: 819497addbe0c00e81fdf0ed2bd3c5755a0e7b9be36f4fd8d11b50d72eef342b
// Dependency manifest: proof_manifests/135_alloc_vec_Vec_into_flattened/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 control/data
// flow. The trusted boundary is limited to source-backed allocator/intrinsic/
// panic/raw-pointer/provenance operations below: Vec::into_raw_parts_with_alloc
// (alloc/src/vec/mod.rs:1363-1370), T::IS_ZST / size_of (core intrinsic layout
// query), checked_mul().expect("vec len overflow") for the ZST panic edge,
// unchecked_mul for the non-ZST allocation-address-space arithmetic, raw pointer
// cast from *mut [T; N] to *mut T, and Vec::from_raw_parts_in
// (alloc/src/vec/mod.rs:1193-1204).

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    cap: usize,
    alloc: A,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn raw_flat_parts_view<T>(ptr: *mut T, length: usize) -> Seq<T>;

pub uninterp spec fn array_ptr_cast<T, const N: usize>(ptr: *mut [T; N]) -> *mut T;

pub uninterp spec fn array_value_view<T, const N: usize>(value: [T; N]) -> Seq<T>;

pub uninterp spec fn flatten_array_vec<T, const N: usize>(vec: Seq<[T; N]>) -> Seq<T>;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        self.buf.cap as nat
    }
}

#[verifier::external_body]
pub fn rust_1_96_type_is_zst<T>() -> (is_zst: bool) {
    core::mem::size_of::<T>() == 0
}

#[verifier::external_body]
pub fn rust_1_96_checked_mul_expect(lhs: usize, rhs: usize) -> (ret: usize)
    ensures
        ret as nat == lhs as nat * rhs as nat,
{
    lhs.checked_mul(rhs).expect("vec len overflow")
}

#[verifier::external_body]
pub unsafe fn rust_1_96_unchecked_mul(lhs: usize, rhs: usize) -> (ret: usize)
    ensures
        ret as nat == lhs as nat * rhs as nat,
{
    unsafe { lhs.unchecked_mul(rhs) }
}

#[verifier::external_body]
pub fn rust_1_96_array_ptr_cast<T, const N: usize>(ptr: *mut [T; N]) -> (flat: *mut T)
    ensures
        flat == array_ptr_cast::<T, N>(ptr),
{
    ptr as *mut T
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub unsafe fn from_raw_parts_in(
        ptr: *mut T,
        length: usize,
        capacity: usize,
        alloc: A,
    ) -> (vec: Self)
        ensures
            vec@ == raw_flat_parts_view::<T>(ptr, length),
            vec@.len() == length as nat,
            vec.spec_capacity() == capacity as nat,
    {
        Vec { buf: RawVec { ptr, cap: capacity, alloc }, len: length }
    }
}

impl<T, A: Allocator, const N: usize> Vec<[T; N], A> {
    #[verifier::external_body]
    pub fn into_raw_parts_with_alloc(self) -> (parts: (*mut [T; N], usize, usize, A))
        ensures
            parts.1 as nat == self@.len(),
            parts.2 as nat >= parts.1 as nat,
            forall|flat_len: usize|
                flat_len as nat == self@.len() * N ==>
                    raw_flat_parts_view::<T>(array_ptr_cast::<T, N>(parts.0), flat_len)
                        == flatten_array_vec::<T, N>(self@),
    {
        let len = self.len;
        let RawVec { ptr, cap, alloc } = self.buf;
        (ptr, len, cap, alloc)
    }

    pub fn into_flattened(self) -> (ret: Vec<T, A>)
        ensures
            ret@ == flatten_array_vec::<T, N>(self@),
            ret@.len() == self@.len() * N,
    {
        let ghost source = self@;
        let (ptr, len, cap, alloc) = self.into_raw_parts_with_alloc();
        let (new_len, new_cap) = if rust_1_96_type_is_zst::<T>() {
            (rust_1_96_checked_mul_expect(len, N), usize::MAX)
        } else {
            unsafe { (rust_1_96_unchecked_mul(len, N), rust_1_96_unchecked_mul(cap, N)) }
        };
        let flat_ptr = rust_1_96_array_ptr_cast::<T, N>(ptr);
        proof {
            assert(len as nat == source.len());
            assert(new_len as nat == source.len() * N);
            assert(raw_flat_parts_view::<T>(flat_ptr, new_len) == flatten_array_vec::<T, N>(source));
        }
        let ret = unsafe { Vec::<T, A>::from_raw_parts_in(flat_ptr, new_len, new_cap, alloc) };
        proof {
            assert(ret@ == flatten_array_vec::<T, N>(source));
            assert(ret@.len() == source.len() * N);
        }
        ret
    }
}

}
