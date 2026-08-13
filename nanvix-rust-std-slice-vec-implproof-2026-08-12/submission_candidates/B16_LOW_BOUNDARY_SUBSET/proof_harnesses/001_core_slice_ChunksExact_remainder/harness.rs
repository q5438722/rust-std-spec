#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::ChunksExact::remainder
// Source: core/src/slice/iter.rs:1843-1880
// Source item sha256: 52c87daecc8119b00040a9a13d3d339571ba252c96f64bb463cfe834699e7bd0
// Dependency manifest: proof_manifests/001_core_slice_ChunksExact_remainder/dependency_assumption_manifest.json

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

pub struct ChunksExact<'a, T: 'a> {
    v: &'a [T],
    rem: &'a [T],
    chunk_size: usize,
}

pub closed spec fn slice_iterator_view<'a, T>(iter: &ChunksExact<'a, T>) -> SliceIteratorView<T> {
    SliceIteratorView {
        source: iter.v@ + iter.rem@,
        yielded_prefix: Seq::empty(),
        remaining: iter.v@,
        remainder: iter.rem@,
        chunk_size: iter.chunk_size as int,
        reverse: false,
    }
}

impl<'a, T> ChunksExact<'a, T> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        (self.rem@.len() as int) < self.chunk_size as int
    }

    pub fn remainder(&self) -> (ret: &'a [T])
        ensures
            ret@ == slice_iterator_view(self).remainder,
            ret@.len() < slice_iterator_view(self).chunk_size,
    {
        proof {
            reveal(slice_iterator_view);
            use_type_invariant(self);
        }
        self.rem
    }
}

}
