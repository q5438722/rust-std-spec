#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_chunks_unchecked
// Source: core/src/slice/mod.rs:1338-1349
// Source item sha256: 1af5889426d173ab1e019f11a75a4697ca2a0e9e0a280108402b7b5ca699ddc3
// Dependency manifest: proof_manifests/014_core_slice_as_chunks_unchecked/dependency_assumption_manifest.json

use vstd::prelude::*;
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

pub uninterp spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool;

pub uninterp spec fn slice_raw_domain<T>(
    ptr: *const T,
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

pub uninterp spec fn array_chunk_source<T, const N: usize>(
    ptr: *const [T; N],
    len: usize,
) -> Seq<T>;

pub mod ub_checks {
    use super::*;

    pub fn assert_unsafe_precondition(n: usize, len: usize)
        requires
            n != 0,
            (len as nat) % (n as nat) == 0,
    {
    }
}

#[verifier::external_body]
pub unsafe fn exact_div(len: usize, divisor: usize) -> (ret: usize)
    requires
        divisor != 0,
        (len as nat) % (divisor as nat) == 0,
    ensures
        ret as nat == (len as nat) / (divisor as nat),
        (ret as nat) * (divisor as nat) == len as nat,
{
    len / divisor
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
pub fn rust_1_96_ptr_cast_array_chunks<T, const N: usize>(
    slice: &[T],
    ptr: *const T,
    new_len: usize,
) -> (array_ptr: *const [T; N])
    requires
        N != 0,
        slice_start_ptr(slice@, ptr),
        (new_len as nat) * (N as nat) == slice@.len(),
    ensures
        array_chunk_source::<T, N>(array_ptr, new_len) == slice@,
        slice_raw_domain_valid_for(
            slice_raw_domain(array_ptr, new_len, SliceRawMutability::Immutable),
            new_len,
            SliceRawMutability::Immutable,
        ),
{
    ptr.cast()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_from_raw_parts_array_chunks<'a, T, const N: usize>(
    data: *const [T; N],
    len: usize,
) -> (ret: &'a [[T; N]])
    requires
        slice_raw_domain_valid_for(
            slice_raw_domain(data, len, SliceRawMutability::Immutable),
            len,
            SliceRawMutability::Immutable,
        ),
    ensures
        ret@.len() == len,
        flatten_array_chunks::<T, N>(ret@) == array_chunk_source::<T, N>(data, len),
{
    unsafe { &*core::ptr::slice_from_raw_parts(data, len) }
}

pub unsafe fn from_raw_parts<'a, T, const N: usize>(
    data: *const [T; N],
    len: usize,
) -> (ret: &'a [[T; N]])
    requires
        slice_raw_domain_valid_for(
            slice_raw_domain(data, len, SliceRawMutability::Immutable),
            len,
            SliceRawMutability::Immutable,
        ),
    ensures
        ret@.len() == len,
        flatten_array_chunks::<T, N>(ret@) == array_chunk_source::<T, N>(data, len),
{
    unsafe { rust_1_96_from_raw_parts_array_chunks(data, len) }
}

pub unsafe fn as_chunks_unchecked<'a, T, const N: usize>(
    slice: &'a [T],
) -> (ret: &'a [[T; N]])
    requires
        N != 0,
        slice@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == slice@,
        ret@.len() == slice@.len() / (N as nat),
{
    let len = slice.len();
    proof {
        assert(len as nat == slice@.len());
        assert((len as nat) % (N as nat) == 0);
    }
    ub_checks::assert_unsafe_precondition(N, len);

    let new_len = unsafe { exact_div(len, N) };
    proof {
        assert((new_len as nat) * (N as nat) == len as nat);
        assert((new_len as nat) * (N as nat) == slice@.len());
        assert(new_len as nat == slice@.len() / (N as nat));
    }
    let ptr = as_ptr(slice);
    let cast = rust_1_96_ptr_cast_array_chunks::<T, N>(slice, ptr, new_len);
    unsafe { from_raw_parts::<T, N>(cast, new_len) }
}

}
