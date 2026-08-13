#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::extend_from_slice
// Source: alloc/src/vec/mod.rs:3525-3527
// Source item sha256: aac946f78f45041c7f02c37ffee06b8701714905b4a0f34bbe80e0e0a98c2e4c
// Dependency manifest: proof_manifests/162_alloc_vec_Vec_extend_from_slice/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96
// `self.spec_extend(other.iter())` data flow. Trusted boundaries are limited to
// the source-backed slice iterator view and private SpecExtend/clone semantics
// needed to connect that body to the exact existing-vstd cloned extension
// contract.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub struct SliceReceiver<'a, T: 'a> {
    pub slice: &'a [T],
}

pub struct SliceIter<'a, T: 'a> {
    pub slice: &'a [T],
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

pub open spec fn slice_receiver_source<'a, T>(receiver: SliceReceiver<'a, T>) -> Seq<T> {
    receiver.slice@
}

pub open spec fn slice_iter_source<'a, T>(iter: SliceIter<'a, T>) -> Seq<T> {
    iter.slice@
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<'a, T> SliceReceiver<'a, T> {
    #[verifier::external_body]
    pub fn iter(self) -> (iter: SliceIter<'a, T>)
        ensures
            slice_iter_source(iter) == slice_receiver_source(self),
    {
        SliceIter { slice: self.slice }
    }
}

impl<T: core::clone::Clone, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    fn spec_extend<'a>(&mut self, iter: SliceIter<'a, T>)
        ensures
            final(self)@.len() == old(self)@.len() + slice_iter_source(iter).len(),
            forall|i: int|
                #![trigger final(self)@[i]]
                0 <= i < final(self)@.len() ==> if i < old(self)@.len() {
                    final(self)@[i] == old(self)@[i]
                } else {
                    cloned::<T>(slice_iter_source(iter)[i - old(self)@.len()], final(self)@[i])
                },
    {
    }

    pub fn extend_from_slice<'a>(&mut self, other: &'a [T])
        ensures
            final(self)@.len() == old(self)@.len() + other@.len(),
            forall|i: int|
                #![trigger final(self)@[i]]
                0 <= i < final(self)@.len() ==> if i < old(self)@.len() {
                    final(self)@[i] == old(self)@[i]
                } else {
                    cloned::<T>(other@[i - old(self)@.len()], final(self)@[i])
                },
    {
        let other = SliceReceiver { slice: other };
        self.spec_extend(other.iter())
    }
}

}
