#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::iter_mut
// Source: core/src/slice/mod.rs:1060-1062 and core/src/slice/iter.rs:194-246
// Source item sha256: 4e6646d30b8a5a57aa136cc9ea393ce812936e6e5c2eb9fd4afc034eb8d5242c
// Dependency manifest: proof_manifests/060_core_slice_iter_mut/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remaining: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub struct IterMut<'a, T: 'a> {
    _marker: PhantomData<&'a mut T>,
}

pub uninterp spec fn slice_iterator_view<'a, T>(iter: IterMut<'a, T>) -> SliceIteratorView<T>;

impl<'a, T> IterMut<'a, T> {
    #[verifier::external_body]
    pub fn new(slice: &'a mut [T]) -> (ret: Self)
        ensures
            slice_iterator_view(ret).source == old(slice)@,
            slice_iterator_view(ret).remaining == old(slice)@,
            slice_iterator_view(ret).yielded_prefix.len() == 0,
            slice_iterator_view(ret).remainder.len() == 0,
            !slice_iterator_view(ret).reverse,
            final(slice)@ == old(slice)@,
    {
        IterMut { _marker: PhantomData }
    }
}

pub fn iter_mut<'a, T>(slice: &'a mut [T]) -> (iter: IterMut<'a, T>)
    ensures
        slice_iterator_view(iter).source == old(slice)@,
        slice_iterator_view(iter).remaining == old(slice)@,
        slice_iterator_view(iter).yielded_prefix.len() == 0,
        slice_iterator_view(iter).remainder.len() == 0,
        !slice_iterator_view(iter).reverse,
        final(slice)@ == old(slice)@,
{
    IterMut::new(slice)
}

}
