#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::extract_if
// Source: alloc/src/vec/mod.rs:4174-4180 and alloc/src/vec/extract_if.rs:21-50
// Source item sha256: 5595a6134c0c7591aa806ba37cad0fa913be6fddb6f9baf51ff5ca8db32025b0
// Dependency manifest: proof_manifests/131_alloc_vec_Vec_extract_if/dependency_assumption_manifest.json

use core::marker::PhantomData;
use core::ops::{Range, RangeBounds};
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

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn vec_range_start<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub uninterp spec fn vec_range_end<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub open spec fn vec_range_bounds_valid<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> bool {
    0 <= vec_range_start(source, range)
        && vec_range_start(source, range) <= vec_range_end(source, range)
        && vec_range_end(source, range) <= source.len()
}

pub uninterp spec fn vec_extract_if_created<
    'a,
    T,
    A: Allocator,
    F: FnMut(&mut T) -> bool,
    R: RangeBounds<usize>,
>(
    source: Seq<T>,
    range: R,
    filter: F,
    iter: ExtractIf<'a, T, F, A>,
    shortened_vec: Seq<T>,
) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

pub mod slice {
    use super::*;

    #[verifier::external_body]
    pub fn range<R: RangeBounds<usize>>(src: R, bounds: core::ops::RangeTo<usize>) -> (ret: Range<usize>)
        ensures
            ret.start <= ret.end,
            ret.end <= bounds.end,
    {
        0..bounds.end
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as int == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len == 0,
        ensures
            final(self)@.len() == 0,
    {
        self.len = new_len;
    }

    pub fn extract_if<'a, F, R>(&'a mut self, range: R, filter: F) -> (iter: ExtractIf<'a, T, F, A>)
        where
            F: FnMut(&mut T) -> bool,
            R: RangeBounds<usize>,
        requires
            vec_range_bounds_valid(old(self)@, range),
        ensures
            vec_extract_if_created(old(self)@, range, filter, iter, final(self)@),
    {
        ExtractIf::new(self, filter, range)
    }
}

pub struct ExtractIf<'a, T, F, A: Allocator>
    where
        F: FnMut(&mut T) -> bool,
{
    vec: &'a mut Vec<T, A>,
    idx: usize,
    end: usize,
    del: usize,
    old_len: usize,
    pred: F,
}

impl<'a, T, F, A: Allocator> ExtractIf<'a, T, F, A>
    where
        F: FnMut(&mut T) -> bool,
{
    #[verifier::external_body]
    pub fn new<R: RangeBounds<usize>>(vec: &'a mut Vec<T, A>, pred: F, range: R) -> (ret: Self)
        requires
            vec_range_bounds_valid(old(vec)@, range),
        ensures
            vec_extract_if_created(old(vec)@, range, pred, ret, final(vec)@),
    {
        let old_len = vec.len();
        let Range { start, end } = slice::range(range, ..old_len);

        // Guard against the vec getting leaked (leak amplification).
        unsafe {
            vec.set_len(0);
        }
        ExtractIf { vec, idx: start, del: 0, end, old_len, pred }
    }
}

}
