#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Drain::as_slice
// Source: alloc/src/vec/drain.rs:21-33 and alloc/src/vec/drain.rs:56-58
// Source item sha256: 499a0275b9e12deee5d729b3178413319b23ffd95be4e479468c2b244c9fb8d9
// Dependency manifest: proof_manifests/121_alloc_vec_Drain_as_slice/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub trait Allocator {
}

pub struct Vec<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

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

pub mod slice {
    use super::*;

    pub struct Iter<'a, T: 'a> {
        ptr: NonNull<T>,
        end_or_len: *const T,
        _marker: PhantomData<&'a T>,
    }

    pub uninterp spec fn slice_iterator_view<'a, T>(iter: &Iter<'a, T>) -> SliceIteratorView<T>;

    impl<'a, T> Iter<'a, T> {
        #[verifier::external_body]
        pub fn as_slice<'b>(&'b self) -> (ret: &'b [T])
            ensures
                ret@ == slice_iterator_view(self).remaining,
        {
            &[]
        }
    }
}

pub struct Drain<'a, T: 'a, A: Allocator> {
    tail_start: usize,
    tail_len: usize,
    iter: slice::Iter<'a, T>,
    vec: NonNull<Vec<T, A>>,
}

pub closed spec fn vec_drain_remaining<'a, T, A: Allocator>(drain: &Drain<'a, T, A>) -> Seq<T> {
    slice::slice_iterator_view(&drain.iter).remaining
}

impl<'a, T, A: Allocator> Drain<'a, T, A> {
    pub fn as_slice<'b>(&'b self) -> (ret: &'b [T])
        ensures
            ret@ == vec_drain_remaining::<T, A>(self),
    {
        let ret = self.iter.as_slice();
        proof {
            reveal(vec_drain_remaining);
        }
        ret
    }
}

}
