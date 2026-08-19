#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::with_capacity
// Source: alloc/src/vec/mod.rs:523-525
// Source item sha256: 587d728a404473e7211bb213714f55c52999c7689ebcb4f68023d97f13a3d800
// Dependency manifest: proof_manifests/180_alloc_vec_Vec_with_capacity/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// body `Self::with_capacity_in(capacity, Global)`. The RawVec/Global empty
// constructor is modeled as source-shaped field initialization, matching the
// already-reviewed split_off constructor reduction.

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
    cap: usize,
    alloc: A,
    _marker_t: PhantomData<T>,
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

pub closed spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat {
    buf.cap as nat
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn with_capacity_in(capacity: usize, alloc: A) -> (vec: Self)
        ensures
            vec@ == Seq::<T>::empty(),
            vec.spec_capacity() >= capacity as nat,
    {
        Vec { buf: RawVec { cap: capacity, alloc, _marker_t: PhantomData }, len: 0 }
    }
}

impl<T> Vec<T, Global> {
    pub fn with_capacity(capacity: usize) -> (v: Self)
        ensures
            v@ == Seq::<T>::empty(),
    {
        Self::with_capacity_in(capacity, Global)
    }
}

}
