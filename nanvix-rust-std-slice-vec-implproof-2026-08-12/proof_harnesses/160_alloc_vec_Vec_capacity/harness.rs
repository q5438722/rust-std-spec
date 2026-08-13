#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::capacity
// Source: alloc/src/vec/mod.rs:1446-1448
// Source item sha256: 58ac14c0f858280736502c5a5d6c947cdad8fbe3958d7f65816af5f03b0a325d
// Dependency manifest: proof_manifests/160_alloc_vec_Vec_capacity/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.capacity()`. The only trusted boundary is the source-backed RawVec
// allocator-capacity observation.

use core::marker::PhantomData;
use vstd::prelude::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    cap: usize,
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub closed spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat {
    buf.cap as nat
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn capacity(&self) -> (result: usize)
        ensures
            result as nat == self.spec_capacity(),
    {
        self.buf.capacity()
    }
}

}
