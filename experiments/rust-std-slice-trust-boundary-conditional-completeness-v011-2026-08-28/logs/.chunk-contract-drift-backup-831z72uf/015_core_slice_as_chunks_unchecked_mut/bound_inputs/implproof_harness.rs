#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_chunks_unchecked_mut
// Source: core/src/slice/mod.rs:1498-1509
// Source item sha256: 010fedd7bf7435cf32f970fa8b916ebc3c94e0d0770c06b6c4361ce21c5ba4e4
// Dependency manifest: proof_manifests/015_core_slice_as_chunks_unchecked_mut/dependency_assumption_manifest.json

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
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

pub uninterp spec fn array_chunk_mut_source<T, const N: usize>(
    ptr: *mut [T; N],
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

pub unsafe fn exact_div(len: usize, divisor: usize) -> (ret: usize)
    requires
        divisor != 0,
        (len as nat) % (divisor as nat) == 0,
    ensures
        ret as nat == (len as nat) / (divisor as nat),
        (ret as nat) * (divisor as nat) == len as nat,
{
    let ret = len / divisor;
    proof {
        let n = len as int;
        let d = divisor as int;
        let q = n / d;
        assert(d > 0);
        assert(n % d == 0);
        lemma_fundamental_div_mod(n, d);
        assert(n == d * q + n % d);
        assert(d * q + n % d == d * q);
        assert(n == d * q);
        assert(d * q == n);
        lemma_mul_is_commutative(d, q);
        assert(q * d == n);
        assert(ret as int == q);
        assert((ret as int) * d == n);
    }
    ret
}

pub fn rust_1_96_slice_as_mut_ptr_cast<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    let len = slice.len();
    let ptr = core::ptr::null_mut::<T>().with_addr(len);
    proof {
        assert(old(slice)@.len() == len as nat);
    }
    ptr
}

pub fn as_mut_ptr<T>(slice: &mut [T]) -> (ptr: *mut T)
    ensures
        slice_start_mut_ptr(old(slice)@, ptr),
        final(slice)@ == old(slice)@,
{
    rust_1_96_slice_as_mut_ptr_cast(slice)
}

#[verifier::external_body]
pub fn rust_1_96_mut_ptr_cast_array_chunks<T, const N: usize>(
    slice: &mut [T],
    ptr: *mut T,
    new_len: usize,
) -> (array_ptr: *mut [T; N])
    requires
        N != 0,
        slice_start_mut_ptr(old(slice)@, ptr),
        (new_len as nat) * (N as nat) == old(slice)@.len(),
    ensures
        array_chunk_mut_source::<T, N>(array_ptr, new_len) == old(slice)@,
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(array_ptr, new_len, SliceRawMutability::Mutable),
            new_len,
            SliceRawMutability::Mutable,
        ),
        final(slice)@ == old(slice)@,
{
    ptr.cast()
}

#[verifier::external_body]
pub unsafe fn rust_1_96_from_raw_parts_mut_array_chunks<'a, T, const N: usize>(
    slice: &'a mut [T],
    data: *mut [T; N],
    len: usize,
) -> (ret: &'a mut [[T; N]])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        array_chunk_mut_source::<T, N>(data, len) == old(slice)@,
    ensures
        ret@.len() == len,
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

pub unsafe fn from_raw_parts_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
    data: *mut [T; N],
    len: usize,
) -> (ret: &'a mut [[T; N]])
    requires
        slice_raw_domain_valid_for(
            slice_raw_mut_domain(data, len, SliceRawMutability::Mutable),
            len,
            SliceRawMutability::Mutable,
        ),
        array_chunk_mut_source::<T, N>(data, len) == old(slice)@,
    ensures
        ret@.len() == len,
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
{
    unsafe { rust_1_96_from_raw_parts_mut_array_chunks(slice, data, len) }
}

pub unsafe fn as_chunks_unchecked_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: &'a mut [[T; N]])
    requires
        N != 0,
        old(slice)@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as nat == source.len());
        assert((len as nat) % (N as nat) == 0);
    }
    ub_checks::assert_unsafe_precondition(N, len);

    let new_len = unsafe { exact_div(len, N) };
    proof {
        assert((new_len as nat) * (N as nat) == len as nat);
        assert((new_len as nat) * (N as nat) == source.len());
    }
    let ptr = as_mut_ptr(slice);
    let cast = rust_1_96_mut_ptr_cast_array_chunks::<T, N>(slice, ptr, new_len);
    unsafe { from_raw_parts_mut::<T, N>(slice, cast, new_len) }
}

}
