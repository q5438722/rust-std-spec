#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::extend_from_within
// Source: alloc/src/vec/mod.rs:3556-3568 and alloc/src/vec/mod.rs:3693-3742
// Source item sha256: 0c19911f3d3d8d69a9eafd73ca4cf5377b9a677d19acc9f3697486a60de509cc
// Dependency manifest: proof_manifests/130_alloc_vec_Vec_extend_from_within/dependency_assumption_manifest.json

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

pub struct SourceRange<R> {
    pub start: usize,
    pub end: usize,
    pub source: R,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat;

pub uninterp spec fn vec_range_start<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub uninterp spec fn vec_range_end<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub open spec fn vec_range_bounds_valid<T, R: core::ops::RangeBounds<usize>>(source: Seq<T>, range: R) -> bool {
    0 <= vec_range_start(source, range)
        && vec_range_start(source, range) <= vec_range_end(source, range)
        && vec_range_end(source, range) <= source.len()
}

pub open spec fn vec_extend_from_within_result<T: core::clone::Clone, R: core::ops::RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    result: Seq<T>,
) -> bool {
    let start = vec_range_start(source, range);
    let end = vec_range_end(source, range);
    &&& vec_range_bounds_valid(source, range)
    &&& result.len() == source.len() + (end - start)
    &&& result.subrange(0, source.len() as int) == source
    &&& forall|i: int| #![trigger result[i]]
        source.len() <= i < result.len()
        ==> cloned::<T>(source[start + i - source.len()], result[i])
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

impl<R> SourceRange<R> {
    #[verifier::external_body]
    pub fn len(&self) -> (n: usize)
        requires
            self.start <= self.end,
        ensures
            n as int == self.end as int - self.start as int,
    {
        self.end - self.start
    }
}

pub mod slice {
    use super::*;

    #[verifier::external_body]
    pub fn range<R: core::ops::RangeBounds<usize>>(src: R, bounds: core::ops::RangeTo<usize>) -> (ret: SourceRange<R>)
        ensures
            ret.source == src,
            ret.start <= ret.end,
    {
        SourceRange { start: 0, end: bounds.end, source: src }
    }
}

impl<T: core::clone::Clone, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as int == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn reserve(&mut self, additional: usize)
        ensures
            final(self)@ == old(self)@,
            final(self).spec_capacity() >= old(self).spec_capacity(),
    {
    }

    #[verifier::external_body]
    pub unsafe fn spec_extend_from_within<R: core::ops::RangeBounds<usize>>(&mut self, src: SourceRange<R>)
        requires
            vec_range_bounds_valid(old(self)@, src.source),
        ensures
            vec_extend_from_within_result(old(self)@, src.source, final(self)@),
    {
    }

    pub fn extend_from_within<R>(&mut self, src: R)
    where
        R: core::ops::RangeBounds<usize>,
        requires
            vec_range_bounds_valid(old(self)@, src),
        ensures
            vec_extend_from_within_result(old(self)@, src, final(self)@),
    {
        let range = slice::range(src, ..self.len());
        self.reserve(range.len());

        // SAFETY:
        // - `slice::range` guarantees that the given range is valid for indexing self
        unsafe {
            self.spec_extend_from_within(range);
        }
    }
}

}
