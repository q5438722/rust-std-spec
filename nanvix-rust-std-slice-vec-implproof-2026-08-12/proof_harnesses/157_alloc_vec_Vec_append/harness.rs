#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::append
// Source: alloc/src/vec/mod.rs:2893-2898
// Source item sha256: 3cd88920bbbd623e427470b16a820597755c2441f892a764a8dc642920a4ea8f
// Dependency manifest: proof_manifests/157_alloc_vec_Vec_append/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// unsafe { self.append_elements(other.as_slice() as _); other.set_len(0); }.
// Trusted boundaries are limited to the source-backed raw slice view exposed by
// as_slice, the private append_elements raw-pointer copy, and the unsafe
// set_len(0) length commit on the drained Vec.

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

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T>;

pub uninterp spec fn vec_const_raw_slice_view<T>(raw: *const [T]) -> Seq<T>;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn as_slice(&self) -> (raw: *const [T])
        ensures
            vec_const_raw_slice_view(raw) == self@,
    {
        core::ptr::slice_from_raw_parts(core::ptr::null::<T>(), 0)
    }

    #[verifier::external_body]
    unsafe fn append_elements(&mut self, other: *const [T])
        ensures
            final(self)@ == old(self)@ + vec_const_raw_slice_view(other),
    {
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len == 0,
        ensures
            final(self)@ == Seq::<T>::empty(),
    {
        self.len = new_len;
    }

    pub fn append(&mut self, other: &mut Self)
        ensures
            final(self)@ == old(self)@ + old(other)@,
            final(other)@ == Seq::<T>::empty(),
    {
        unsafe {
            self.append_elements(other.as_slice() as _);
            other.set_len(0);
        }
    }
}

}
