#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::last_chunk
// Source: core/src/slice/mod.rs:509-517
// Source item sha256: 1cd96ff4fc6dafb14815b1b402d6844b2f87c5740529e5e5e85db47e433ad811
// Dependency manifest: proof_manifests/061_core_slice_last_chunk/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn array_ref_view<T, const N: usize>(array: &[T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn slice_fixed_suffix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange((seq.len() - N) as int, seq.len() as int)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_last_chunk_array_ref<'a, T, const N: usize>(
    last: &'a [T],
) -> (ret: &'a [T; N])
    requires
        last@.len() == N,
    ensures
        array_ref_view::<T, N>(ret) == last@,
{
    unsafe { &*(last.as_ptr().cast_array()) }
}

pub fn last_chunk<'a, T, const N: usize>(slice: &'a [T]) -> (ret: Option<&'a [T; N]>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && array_ref_view::<T, N>(ret.unwrap()) == slice_fixed_suffix::<T, N>(slice@),
        (N as int) > slice@.len() ==> ret.is_none(),
{
    let Some(index) = slice.len().checked_sub(N) else {
        return None;
    };
    proof {
        assert((N as int) <= slice@.len());
        assert(index == slice.len() - N);
        assert(index as int == slice@.len() - N as int);
        assert(index <= slice.len());
    }
    let (_, last) = slice.split_at(index);
    proof {
        slice@.lemma_split_at(index as int);
        assert(last@ =~= slice@.subrange(index as int, slice@.len() as int));
        assert(last@ =~= slice_fixed_suffix::<T, N>(slice@));
        assert(last@.len() == N);
    }
    Some(unsafe { rust_1_96_last_chunk_array_ref::<T, N>(last) })
}

}
