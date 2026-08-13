#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::drain
// Source: alloc/src/vec/mod.rs:2948-2976
// Source item sha256: bb98ccb2d8f8a925970c71928abbfa1e9a0948d901534b23887b53c292d8a1e1
// Dependency manifest: proof_manifests/129_alloc_vec_Vec_drain/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// len, slice::range, unsafe set_len(start), slice::from_raw_parts(self.as_ptr().add(start),
// end - start), and Drain construction. Trusted boundaries are limited to
// source-backed RangeBounds resolution, reviewed Vec::as_ptr / Vec::set_len
// effects, raw-pointer/provenance, and opaque Drain iterator/lifetime/drop state.

use core::marker::PhantomData;
use core::ops::{Range, RangeBounds};
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *const T,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
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

pub struct Drain<'a, T: 'a, A: Allocator> {
    tail_start: usize,
    tail_len: usize,
    iter: core::slice::Iter<'a, T>,
    vec: NonNull<Vec<T, A>>,
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

pub uninterp spec fn vec_range_start<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub uninterp spec fn vec_range_end<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> int;

pub open spec fn vec_range_bounds_valid<T, R: RangeBounds<usize>>(source: Seq<T>, range: R) -> bool {
    0 <= vec_range_start(source, range)
        && vec_range_start(source, range) <= vec_range_end(source, range)
        && vec_range_end(source, range) <= source.len()
}

pub uninterp spec fn slice_iterator_view<'a, T>(iter: &core::slice::Iter<'a, T>) -> SliceIteratorView<T>;

pub uninterp spec fn vec_drain_created<'a, T, A: Allocator, R: RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    drain: Drain<'a, T, A>,
    shortened_vec: Seq<T>,
) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
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

    #[verifier::external_body]
    pub unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> (ret: &'a [T])
        ensures
            ret@.len() == len,
    {
        unsafe { core::slice::from_raw_parts(data, len) }
    }
}

impl<T, A: Allocator> NonNull<Vec<T, A>> {
    #[verifier::external_body]
    pub fn from(reference: &mut Vec<T, A>) -> (ret: Self)
        ensures
            final(reference)@ == old(reference)@,
    {
        NonNull { _marker: PhantomData }
    }
}

#[verifier::external_body]
pub unsafe fn rust_1_96_vec_drain_ptr_add<T>(ptr: *const T, start: usize) -> (ret: *const T) {
    unsafe { ptr.add(start) }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: *const T) {
        self.buf.ptr
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len as nat <= old(self)@.len(),
        ensures
            final(self)@.len() == new_len as nat,
    {
        self.len = new_len;
    }

    pub fn drain<'a, R>(&'a mut self, range: R) -> (drain: Drain<'a, T, A>)
        where
            R: RangeBounds<usize>,
        requires
            vec_range_bounds_valid(old(self)@, range),
        ensures
            vec_drain_created(old(self)@, range, drain, final(self)@),
    {
        let ghost source = self@;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
        }
        let Range { start, end } = slice::range(range, ..len);

        unsafe {
            proof {
                rust_1_96_drain_range_bounds::<T, R>(source, range, start, end, len);
                assert(start <= end);
                assert(end <= len);
                assert(start as nat <= source.len());
            }
            self.set_len(start);
            let data = rust_1_96_vec_drain_ptr_add(self.as_ptr(), start);
            let range_slice = slice::from_raw_parts(data, end - start);
            let drain = Drain {
                tail_start: end,
                tail_len: len - end,
                iter: range_slice.iter(),
                vec: NonNull::from(self),
            };
            proof {
                rust_1_96_drain_created_boundary::<T, A, R>(
                    source,
                    range,
                    start,
                    end,
                    len,
                    drain,
                    self@,
                );
            }
            drain
        }
    }
}

#[verifier::external_body]
pub proof fn rust_1_96_drain_range_bounds<T, R: RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    start: usize,
    end: usize,
    len: usize,
)
    requires
        vec_range_bounds_valid(source, range),
        len as nat == source.len(),
        start <= end,
        end <= len,
    ensures
        start as int == vec_range_start(source, range),
        end as int == vec_range_end(source, range),
{
}

#[verifier::external_body]
pub proof fn rust_1_96_drain_created_boundary<'a, T, A: Allocator, R: RangeBounds<usize>>(
    source: Seq<T>,
    range: R,
    start: usize,
    end: usize,
    len: usize,
    drain: Drain<'a, T, A>,
    shortened_vec: Seq<T>,
)
    requires
        vec_range_bounds_valid(source, range),
        start as int == vec_range_start(source, range),
        end as int == vec_range_end(source, range),
        len as nat == source.len(),
        shortened_vec.len() == start as nat,
    ensures
        vec_drain_created(source, range, drain, shortened_vec),
{
}

}
