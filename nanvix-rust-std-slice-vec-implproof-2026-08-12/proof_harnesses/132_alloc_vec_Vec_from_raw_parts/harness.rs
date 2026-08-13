#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::from_raw_parts
// Source: alloc/src/vec/mod.rs:644-646 and alloc/src/vec/mod.rs:1193-1204
// Source item sha256: 15a23750e7d631a39f08207076518c32dfb6ba427fafbc12f8e99e853f68b6de
// Dependency manifest: proof_manifests/132_alloc_vec_Vec_from_raw_parts/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct Global;

impl Allocator for Global {
}

pub struct RawVec<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
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

pub uninterp spec fn vec_raw_parts_domain<T>(ptr: *mut T, length: usize, capacity: usize) -> bool;

pub uninterp spec fn vec_raw_parts_initialized_seq<T>(ptr: *mut T, length: usize) -> Seq<T>;

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

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    pub unsafe fn from_raw_parts_in(ptr: *mut T, capacity: usize, alloc: A) -> (buf: Self)
        ensures
            raw_vec_capacity(&buf) == capacity as nat,
    {
        RawVec { _marker_t: PhantomData, _marker_a: PhantomData }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub unsafe fn from_raw_parts_in(
        ptr: *mut T,
        length: usize,
        capacity: usize,
        alloc: A,
    ) -> (vec: Self)
        requires
            vec_raw_parts_domain::<T>(ptr, length, capacity),
        ensures
            vec@ == vec_raw_parts_initialized_seq::<T>(ptr, length),
            vec.spec_capacity() == capacity as nat,
    {
        unsafe { Vec { buf: RawVec::from_raw_parts_in(ptr, capacity, alloc), len: length } }
    }
}

impl<T> Vec<T, Global> {
    pub unsafe fn from_raw_parts(ptr: *mut T, length: usize, capacity: usize) -> (vec: Self)
        requires
            vec_raw_parts_domain::<T>(ptr, length, capacity),
        ensures
            vec@ == vec_raw_parts_initialized_seq::<T>(ptr, length),
            vec.spec_capacity() == capacity as nat,
    {
        unsafe { Self::from_raw_parts_in(ptr, length, capacity, Global) }
    }
}

}
