#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::as_rchunks_mut
// Source: core/src/slice/mod.rs:1605-1613
// Source item sha256: 2de629d24e9c7a21c57f1857ac9cf123c54ecf397268228a1cc0a5acbd0988d4
// Dependency manifest: proof_manifests/024_core_slice_as_rchunks_mut/dependency_assumption_manifest.json

use vstd::arithmetic::div_mod::*;
use vstd::arithmetic::mul::*;
use vstd::prelude::*;
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

pub open spec fn slice_array_rchunks_partition<T, const N: usize>(
    seq: Seq<T>,
    remainder: Seq<T>,
    chunks: Seq<[T; N]>,
) -> bool {
    N != 0 && (remainder.len() as int) < N && remainder + flatten_array_chunks::<T, N>(chunks) == seq
}

#[verifier::external_body]
pub unsafe fn rust_1_96_as_chunks_unchecked_mut_view<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: &'a mut [[T; N]])
    requires
        N != 0,
        (old(slice)@.len() as int) % (N as int) == 0,
    ensures
        flatten_array_chunks::<T, N>(ret@) == old(slice)@,
        final(slice)@ == flatten_array_chunks::<T, N>(final(ret)@),
{
    unsafe { slice.as_chunks_unchecked_mut() }
}

pub fn as_rchunks_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: (&'a mut [T], &'a mut [[T; N]]))
    requires
        N != 0,
    ensures
        slice_array_rchunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@),
        final(slice)@ == final(ret.0)@ + flatten_array_chunks::<T, N>(final(ret.1)@),
{
    assert(N != 0);
    let ghost source = slice@;
    let len = slice.len() / N;
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(slice.len() == source.len());
        assert(len as int == q);
        assert(0 <= n % c);
        assert(n == c * q + n % c);
        assert(c * q == q * c);
        assert(q * c <= n);
        assert((len as int) * (N as int) <= slice.len() as int);
        assert((len as int) * (N as int) <= usize::MAX as int);
    }
    let len_multiple = len * N;
    let split_index = slice.len() - len_multiple;
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(slice.len() == source.len());
        assert(len as int == q);
        assert(len_multiple as int == q * c);
        assert(c * q == q * c);
        assert(n == c * q + n % c);
        assert(split_index as int == n - q * c);
        assert(split_index as int == n % c);
        assert((split_index as int) < c);
        assert(split_index <= slice.len());
    }
    let (remainder, multiple_of_n) = slice.split_at_mut(split_index);
    proof {
        let n = source.len() as int;
        let c = N as int;
        let q = n / c;
        source.lemma_split_at(split_index as int);
        lemma_fundamental_div_mod(n, c);
        lemma_mod_division_less_than_divisor(n, c);
        lemma_mod_multiples_basic(q, c);
        lemma_mul_is_commutative(c, q);
        assert(remainder@ =~= source.subrange(0, split_index as int));
        assert(multiple_of_n@ =~= source.subrange(split_index as int, source.len() as int));
        assert(remainder@ + multiple_of_n@ == source);
        assert(remainder@.len() == split_index);
        assert((remainder@.len() as int) < c);
        assert(len as int == q);
        assert(len_multiple as int == q * c);
        assert(multiple_of_n@.len() == len_multiple);
        assert((multiple_of_n@.len() as int) == q * c);
        assert((multiple_of_n@.len() as int) % c == 0);
    }
    let ghost chunk_source = multiple_of_n@;
    let array_slice = unsafe { rust_1_96_as_chunks_unchecked_mut_view::<T, N>(multiple_of_n) };
    proof {
        reveal(slice_array_rchunks_partition);
        assert(remainder@ + chunk_source == source);
        assert(flatten_array_chunks::<T, N>(array_slice@) == chunk_source);
        assert(remainder@ + flatten_array_chunks::<T, N>(array_slice@) == source);
        assert(slice_array_rchunks_partition::<T, N>(source, remainder@, array_slice@));
    }
    (remainder, array_slice)
}

}
