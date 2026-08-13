#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::Iter::as_slice
// Source: core/src/slice/iter.rs:69-139 and core/src/slice/iter/macros.rs:89-94
// Source item sha256: c7255b92712674fa8be5f0f442386dbdeade5271f71ed3d21356184c4dfa7d96
// Dependency manifest: proof_manifests/003_core_slice_Iter_as_slice/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub struct NonNull<T> {
    _marker: PhantomData<T>,
}


pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remaining: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub struct Iter<'a, T: 'a> {
    ptr: NonNull<T>,
    end_or_len: *const T,
    _marker: PhantomData<&'a T>,
}

pub uninterp spec fn slice_iterator_view<'a, T>(iter: &Iter<'a, T>) -> SliceIteratorView<T>;

impl<'a, T> Iter<'a, T> {
    #[verifier::external_body]
    fn make_slice(&self) -> (ret: &'a [T])
        ensures
            ret@ == slice_iterator_view(self).remaining,
    {
        &[]
    }

    pub fn as_slice(&self) -> (ret: &'a [T])
        ensures
            ret@ == slice_iterator_view(self).remaining,
    {
        self.make_slice()
    }
}

}
