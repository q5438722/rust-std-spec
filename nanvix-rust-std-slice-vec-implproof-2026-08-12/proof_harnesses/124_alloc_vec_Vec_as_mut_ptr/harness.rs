#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::as_mut_ptr
// Source: alloc/src/vec/mod.rs:2022-2026 and alloc/raw_vec/mod.rs:73-75, 295-297, 608-610
// Source item sha256: 56c46d9ef725e15cd271f3f23002feff485277b74e9e73f1bf9b87663be0718b
// Dependency manifest: proof_manifests/124_alloc_vec_Vec_as_mut_ptr/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVecInner<A: Allocator> {
    _marker: PhantomData<A>,
}

pub struct RawVec<T, A: Allocator> {
    inner: RawVecInner<A>,
    _marker: PhantomData<T>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat;

pub uninterp spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: *mut T) -> bool;

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

impl<A: Allocator> RawVecInner<A> {
    #[verifier::external_body]
    fn ptr<T>(&self) -> (ptr: *mut T) {
        core::ptr::null_mut()
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    fn ptr(&self) -> (ptr: *mut T)
        ensures
            vec_start_mut_ptr(raw_vec_initialized_seq(self), raw_vec_capacity(self), ptr),
    {
        self.inner.ptr::<T>()
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn as_mut_ptr(&mut self) -> (ptr: *mut T)
        ensures
            vec_start_mut_ptr(old(self)@, old(self).spec_capacity(), ptr),
            final(self)@ == old(self)@,
    {
        // We shadow the slice method of the same name to avoid going through
        // `deref_mut`, which creates an intermediate reference.
        self.buf.ptr()
    }
}

}
