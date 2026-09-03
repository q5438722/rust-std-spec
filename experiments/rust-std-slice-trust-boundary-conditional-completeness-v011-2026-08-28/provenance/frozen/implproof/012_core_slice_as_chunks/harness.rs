#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_chunks
// Source: core/src/slice/mod.rs:1396-1406
// Source item sha256: 9c4af13742dd8487899f401b86e30b861c36502191a1600057eb26d1ef9e7234
// Dependency manifest: proof_manifests/012_core_slice_as_chunks/dependency_assumption_manifest.json
//
// The public target body below preserves the Rust 1.96 flow: assert N != 0,
// compute the rounded-down length, split with split_at_unchecked, convert the
// multiple-of-N prefix with as_chunks_unchecked, and return chunks plus the
// remainder. Reviewed unsafe callees are reused as named source-backed
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

pub open spec fn slice_start_ptr<T>(seq: Seq<T>, ptr: *const T) -> bool {
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
pub unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> (ret: &'a [T])
    ensures
        ret@.len() == len,
        slice_start_ptr(ret@, data),
{
    unsafe { core::slice::from_raw_parts(data, len) }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_split_at_unchecked_raw_parts<'a, T>(
    slice: &'a [T],
    ptr: *const T,
    mid: usize,
    len: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        split_point_in_range(slice@, mid),
        mid <= len,
        len == slice@.len(),
        slice_start_ptr(slice@, ptr),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    unsafe { (from_raw_parts(ptr, mid), from_raw_parts(ptr.add(mid), unchecked_sub(len, mid))) }
}

pub unsafe fn split_at_unchecked<'a, T>(
    slice: &'a [T],
    mid: usize,
) -> (ret: (&'a [T], &'a [T]))
    requires
        split_point_in_range(slice@, mid),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
{
    let ghost source = slice@;
    let len = slice.len();
    proof {
        assert(len as int == source.len());
        assert((mid as int) <= source.len());
        assert(mid <= len);
    }

    let ptr = as_ptr(slice);

    ub_checks::assert_unsafe_precondition(mid, len);

    unsafe { rust_1_96_split_at_unchecked_raw_parts(slice, ptr, mid, len) }
}

#[verifier::external_body]
pub unsafe fn as_chunks_unchecked<'a, T, const N: usize>(
    slice: &'a [T],
) -> (ret: &'a [[T; N]])
    requires
        N != 0,
        slice@.len() % (N as nat) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == slice@,
{
    unsafe { slice.as_chunks_unchecked() }
}

pub fn as_chunks<'a, T, const N: usize>(
    slice: &'a [T],
) -> (ret: (&'a [[T; N]], &'a [T]))
    requires
        N != 0,
    ensures
        slice_array_chunks_partition::<T, N>(slice@, ret.0@, ret.1@),
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
    let (multiple_of_n, remainder) = unsafe { split_at_unchecked(slice, len_rounded_down) };
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
    let array_slice = unsafe { as_chunks_unchecked::<T, N>(multiple_of_n) };
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
