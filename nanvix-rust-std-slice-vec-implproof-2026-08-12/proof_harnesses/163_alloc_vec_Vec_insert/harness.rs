#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::insert
// Source: alloc/src/vec/mod.rs:2272-2274
// Source item sha256: cb8c65f2290ea70aeb94f6133ccc3eb3c07fb11219e3bf58907b6691c0fcceb9
// Dependency manifest: proof_manifests/163_alloc_vec_Vec_insert/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// flow `let _ = self.insert_mut(index, element);`, adapted only to the exact
// existing-vstd parameter name `i`. The trusted boundary is the already-reviewed
// `Vec::insert_mut` implementation proof.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub closed spec fn len(&self) -> usize {
        self.len
    }

    #[verifier::external_body]
    pub fn insert_mut(&mut self, index: usize, element: T) -> (ret: &mut T)
        requires
            index <= old(self).len(),
        ensures
            *ret == element,
            final(self)@ == old(self)@.insert(index as int, *final(ret)),
    {
        unsafe { &mut *self.buf.ptr }
    }

    pub fn insert(&mut self, i: usize, element: T)
        requires
            i <= old(self).len(),
        ensures
            final(self)@ == old(self)@.insert(i as int, element),
    {
        let _ = self.insert_mut(i, element);
    }
}

}
