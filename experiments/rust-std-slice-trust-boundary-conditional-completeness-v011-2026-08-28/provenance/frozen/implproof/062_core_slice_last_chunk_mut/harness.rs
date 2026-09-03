#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![feature(ptr_cast_array)]
// Target-specific Verus implementation harness.
// Target: core::slice::last_chunk_mut
// Source: core/src/slice/mod.rs:539-548
// Source item sha256: cc48aeefd7888744bec1500626ba5bc1a4dc8e47df42e3d7e458d293f366ebd4
// Dependency manifest: proof_manifests/062_core_slice_last_chunk_mut/dependency_assumption_manifest.json

use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub open spec fn array_mut_ref_view<T, const N: usize>(array: &mut [T; N]) -> Seq<T> {
    (*array)@
}

pub open spec fn array_value_view<T, const N: usize>(array: [T; N]) -> Seq<T> {
    array@
}

pub open spec fn slice_fixed_suffix<T, const N: usize>(seq: Seq<T>) -> Seq<T> {
    seq.subrange((seq.len() - N) as int, seq.len() as int)
}

#[verifier::external_body]
pub unsafe fn rust_1_96_last_chunk_mut_array_ref<'a, T, const N: usize>(
    last: &'a mut [T],
) -> (ret: &'a mut [T; N])
    requires
        old(last)@.len() == N,
    ensures
        array_mut_ref_view::<T, N>(ret) == old(last)@,
        final(last)@ == array_value_view::<T, N>(*final(ret)),
{
    unsafe { &mut *(last.as_mut_ptr().cast_array()) }
}

pub fn last_chunk_mut<'a, T, const N: usize>(
    slice: &'a mut [T],
) -> (ret: Option<&'a mut [T; N]>)
    ensures
        (N as int) <= old(slice)@.len() ==> ret.is_some()
            && array_mut_ref_view::<T, N>(ret.unwrap()) == slice_fixed_suffix::<T, N>(old(slice)@)
            && final(slice)@ == old(slice)@.subrange(0, (old(slice)@.len() - N) as int)
                + array_value_view::<T, N>(*final(ret.unwrap())),
        (N as int) > old(slice)@.len() ==> ret.is_none() && final(slice)@ == old(slice)@,
{
    let ghost source = slice@;
    let Some(index) = slice.len().checked_sub(N) else {
        return None;
    };
    proof {
        assert((N as int) <= source.len());
        assert(index == slice.len() - N);
        assert(index as int == source.len() - N as int);
        assert(index <= slice.len());
    }
    let (init, last) = slice.split_at_mut(index);
    proof {
        source.lemma_split_at(index as int);
        assert(init@ =~= source.subrange(0, index as int));
        assert(last@ =~= source.subrange(index as int, source.len() as int));
        assert(init@ + last@ == source);
        assert(last@ =~= slice_fixed_suffix::<T, N>(source));
        assert(last@.len() == N);
    }
    let chunk = unsafe { rust_1_96_last_chunk_mut_array_ref::<T, N>(last) };
    proof {
        assert(array_mut_ref_view::<T, N>(chunk) == slice_fixed_suffix::<T, N>(source));
    }
    Some(chunk)
}

}
