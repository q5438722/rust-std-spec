#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::is_empty
// Source: alloc/src/vec/mod.rs:3047-3049
// Source item sha256: 8fda893dc10ecf45122b1aa88aca5cbcdb5e38a8c9abd6ecdeb3f947ac651047
// Dependency manifest: proof_manifests/164_alloc_vec_Vec_is_empty/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.len() == 0`, with only the receiver made explicit by the local Vec model.

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
    fn len(&self) -> (len: usize)
        ensures
            len == self@.len(),
    {
        self.len
    }

    pub fn is_empty(&self) -> (res: bool)
        ensures
            res <==> self@.len() == 0,
    {
        self.len() == 0
    }
}

}
