#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::with_capacity
// Source: alloc/src/vec/mod.rs:523-525
// Source item sha256: 587d728a404473e7211bb213714f55c52999c7689ebcb4f68023d97f13a3d800
// Dependency manifest: proof_manifests/180_alloc_vec_Vec_with_capacity/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// body `Self::with_capacity_in(capacity, Global)`. The trusted boundary is
// limited to the source-backed RawVec/Global allocation path that constructs an
// empty Vec for the requested capacity.

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
    #[verifier::external_body]
    pub fn with_capacity_in(capacity: usize, alloc: A) -> (vec: Self)
        ensures
            vec@ == Seq::<T>::empty(),
    {
        Vec { buf: RawVec { _marker_t: PhantomData, _marker_a: PhantomData }, len: 0 }
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
