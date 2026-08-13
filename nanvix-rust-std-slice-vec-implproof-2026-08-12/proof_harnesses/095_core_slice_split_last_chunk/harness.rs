#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::split_last_chunk
// Source: core/src/slice/mod.rs:447-454
// Source item sha256: 19393965046770f1853ca8e1332251de5bfed4426ce1baac25f52dd4a3feaf58
// Dependency manifest: proof_manifests/095_core_slice_split_last_chunk/dependency_assumption_manifest.json

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
pub unsafe fn rust_1_96_split_last_chunk_array_ref<'a, T, const N: usize>(
    last: &'a [T],
) -> (ret: &'a [T; N])
    requires
        last@.len() == N,
    ensures
        array_ref_view::<T, N>(ret) == last@,
{
    unsafe { &*(last.as_ptr().cast_array()) }
}

pub fn split_last_chunk<'a, T, const N: usize>(
    slice: &'a [T],
) -> (ret: Option<(&'a [T], &'a [T; N])>)
    ensures
        (N as int) <= slice@.len() ==> ret.is_some()
            && ret.unwrap().0@ == slice@.subrange(0, (slice@.len() - N) as int)
            && array_ref_view::<T, N>(ret.unwrap().1) == slice_fixed_suffix::<T, N>(slice@),
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
    let (init, last) = slice.split_at(index);
    proof {
        slice@.lemma_split_at(index as int);
        assert(init@ =~= slice@.subrange(0, index as int));
        assert(last@ =~= slice@.subrange(index as int, slice@.len() as int));
        assert(init@ + last@ == slice@);
        assert(init@ =~= slice@.subrange(0, (slice@.len() - N) as int));
        assert(last@ =~= slice_fixed_suffix::<T, N>(slice@));
        assert(last@.len() == N);
    }
    let chunk = unsafe { rust_1_96_split_last_chunk_array_ref::<T, N>(last) };
    proof {
        assert(array_ref_view::<T, N>(chunk) == slice_fixed_suffix::<T, N>(slice@));
    }
    Some((init, chunk))
}

}
