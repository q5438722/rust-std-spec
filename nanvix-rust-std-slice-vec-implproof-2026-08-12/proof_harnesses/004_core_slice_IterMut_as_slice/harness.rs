#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::IterMut::as_slice
// Source: core/src/slice/iter.rs:194-315 and core/src/slice/iter/macros.rs:89-94
// Source item sha256: 67a00e272341651d663752530cdf83c3452a9c73f109a1773e24422d675e8a3a
// Dependency manifest: proof_manifests/004_core_slice_IterMut_as_slice/dependency_assumption_manifest.json

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

pub struct IterMut<'a, T: 'a> {
    ptr: NonNull<T>,
    end_or_len: *mut T,
    _marker: PhantomData<&'a mut T>,
}

pub uninterp spec fn slice_iterator_view<'a, 'b, T>(iter: &'b IterMut<'a, T>) -> SliceIteratorView<T>;

impl<'a, T> IterMut<'a, T> {
    #[verifier::external_body]
    fn make_slice<'b>(&'b self) -> (ret: &'b [T])
        ensures
            ret@ == slice_iterator_view(self).remaining,
    {
        &[]
    }

    pub fn as_slice<'b>(&'b self) -> (ret: &'b [T])
        ensures
            ret@ == slice_iterator_view(self).remaining,
    {
        self.make_slice()
    }
}

}
