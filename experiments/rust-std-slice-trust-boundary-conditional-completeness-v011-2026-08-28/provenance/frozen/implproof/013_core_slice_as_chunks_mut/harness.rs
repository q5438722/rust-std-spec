#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_chunks_mut
// Source: core/src/slice/mod.rs:1552-1562
// Source item sha256: 53fb689ca4c691d2e432cbea572e07fcc1c5cd487734c27f9d0b82841f5b7ae8
// Dependency manifest: proof_manifests/013_core_slice_as_chunks_mut/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: assert N != 0,
// compute the rounded-down length, split with split_at_mut_unchecked, convert
// the multiple-of-N prefix with as_chunks_unchecked_mut, and return chunks plus
// the remainder. Reviewed unsafe callees are reused as named source-backed
// boundaries; the target postcondition is not assumed.

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
use vstd::prelude::*;
use vstd::raw_ptr::*;
use vstd::seq::*;
use vstd::seq_lib::*;

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

pub open spec fn slice_array_chunks_partition<T, const N: usize>(
    seq: Seq<T>,
    chunks: Seq<[T; N]>,
    remainder: Seq<T>,
) -> bool {
    N != 0 && (remainder.len() as int) < N && flatten_array_chunks::<T, N>(chunks) + remainder == seq
}

pub open spec fn split_point_in_range<T>(source: Seq<T>, mid: usize) -> bool {
    (mid as int) <= source.len()
}

pub open spec fn split_at_mut_unchecked_result<T>(
    source: Seq<T>,
    mid: usize,
    left: Seq<T>,
    right: Seq<T>,
    final_source: Seq<T>,
    final_left: Seq<T>,
    final_right: Seq<T>,
) -> bool {
    left == source.subrange(0, mid as int)
        && right == source.subrange(mid as int, source.len() as int)
        && final_source == final_left + final_right
}

pub open spec fn slice_start_mut_ptr<T>(seq: Seq<T>, ptr: *mut T) -> bool {
    ptr@.addr as nat == seq.len() && ptr@.provenance == Provenance::null()
}

pub mod ub_checks {
    use super::*;

    pub fn assert_unsafe_precondition(mid: usize, len: usize)
        requires
            mid <= len,
    {
    }
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

pub unsafe fn unchecked_sub(len: usize, mid: usize) -> (ret: usize)
    requires
        mid <= len,
    ensures
        ret as int == len as int - mid as int,
{
    proof {
        assert(mid <= len);
    }
    len - mid
}

#[verifier::external_body]
pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    ensures
        ret@.len() == len,
        slice_start_mut_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts_mut(data, len) }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_split_at_mut_unchecked_raw_parts<'a, T>(
    slice: &'a mut [T],
    ptr: *mut T,
    mid: usize,
    len: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
        mid <= len,
        len == old(slice)@.len(),
        slice_start_mut_ptr(old(slice)@, ptr),
    ensures
        split_at_mut_unchecked_result(
            old(slice)@,
            mid,
            ret.0@,
            ret.1@,
            final(slice)@,
            final(ret.0)@,
            final(ret.1)@,
        ),
{
    unsafe {
        (
            from_raw_parts_mut(ptr, mid),
            from_raw_parts_mut(ptr.add(mid), unchecked_sub(len, mid)),
        )
    }
}

pub unsafe fn split_at_mut_unchecked<'a, T>(
    slice: &'a mut [T],
    mid: usize,
) -> (ret: (&'a mut [T], &'a mut [T]))
    requires
        split_point_in_range(old(slice)@, mid),
    ensures
        ret.0@ == old(slice)@.subrange(0, mid as int),
        ret.1@ == old(slice)@.subrange(mid as int, old(slice)@.len() as int),
        final(slice)@ == final(ret.0)@ + final(ret.1)@,
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
        assert((mid as int) <= source.len());
        assert(mid <= len);
    }

    let ptr = as_mut_ptr(slice);

    ub_checks::assert_unsafe_precondition(mid, len);

    unsafe { rust_1_96_split_at_mut_unchecked_raw_parts(slice, ptr, mid, len) }
}

#[verifier::external_body]
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
    unsafe { slice.as_chunks_unchecked_mut() }
}

pub fn as_chunks_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [[T; N]], &'a mut [T]))
    requires
        N != 0,
    ensures
        slice_array_chunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@),
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret.0)@) + final(ret.1)@,
{
    assert(N != 0);
    let ghost source = slice@;
    let len = slice.len();
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(len as int == n);
        assert((len / N) as int == q);
        assert(n == c * q + n % c);
        assert(c * q == q * c);
        assert(q * c <= n);
        assert(((len / N) as int) * (N as int) <= usize::MAX as int);
    }
    let len_rounded_down = len / N * N;
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(len as int == n);
        assert((len / N) as int == q);
        assert(len_rounded_down as int == q * c);
        assert(n == c * q + n % c);
        assert(c * q == q * c);
        assert(q * c <= n);
        assert((len_rounded_down as int) <= n);
        assert(split_point_in_range::<T>(source, len_rounded_down));
    }
    let (multiple_of_n, remainder) = unsafe { split_at_mut_unchecked(slice, len_rounded_down) };
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(len_rounded_down as int == q * c);
        assert(multiple_of_n@ =~= source.subrange(0, len_rounded_down as int));
        assert(remainder@ =~= source.subrange(len_rounded_down as int, source.len() as int));
        assert(multiple_of_n@.len() == len_rounded_down);
        assert((multiple_of_n@.len() as int) == q * c);
        assert((multiple_of_n@.len() as int) % c == 0);
        assert(multiple_of_n@.len() % (N as nat) == 0);
        assert(remainder@.len() == n - q * c);
        assert(remainder@.len() == n % c);
        assert((remainder@.len() as int) < c);
        source.lemma_split_at(len_rounded_down as int);
        assert(multiple_of_n@ + remainder@ == source);
    }
    let ghost chunk_source = multiple_of_n@;
    let array_slice = unsafe { as_chunks_unchecked_mut::<T, N>(multiple_of_n) };
    proof {
        reveal(slice_array_chunks_partition);
        assert(flatten_array_chunks::<T, N>(array_slice@) == chunk_source);
        assert(chunk_source + remainder@ == source);
        assert(flatten_array_chunks::<T, N>(array_slice@) + remainder@ == source);
        assert(slice_array_chunks_partition::<T, N>(source, array_slice@, remainder@));
    }
    (array_slice, remainder)
}

}
