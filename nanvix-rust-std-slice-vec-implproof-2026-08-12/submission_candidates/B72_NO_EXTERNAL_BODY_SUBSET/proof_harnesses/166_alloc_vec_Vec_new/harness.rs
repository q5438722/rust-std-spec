#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::new
// Source: alloc/src/vec/mod.rs:463-465
// Source item sha256: 68ca2b0c9bd7cda598fb7cfd7ecf49aa22aa4c194ddcf3d572842920a7092bc2
// Dependency manifest: proof_manifests/166_alloc_vec_Vec_new/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `Vec { buf: RawVec::new(), len: 0 }`; the local RawVec constructor is the
// minimal allocator-storage model needed to prove the exact existing-vstd
// postcondition `v@ == Seq::<T>::empty()`.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub struct RawVec<T> {
    _marker_t: PhantomData<T>,
}

pub struct Vec<T> {
    buf: RawVec<T>,
    len: usize,
}

pub uninterp spec fn raw_vec_value<T>(buf: &RawVec<T>, i: int) -> T;

pub open spec fn raw_vec_initialized_seq<T>(buf: &RawVec<T>, len: usize) -> Seq<T> {
    Seq::new(len as nat, |i: int| raw_vec_value(buf, i))
}

impl<T> View for Vec<T> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T> RawVec<T> {
    fn new() -> (buf: RawVec<T>) {
        RawVec { _marker_t: PhantomData }
    }
}

impl<T> Vec<T> {
    pub fn new() -> (v: Vec<T>)
        ensures
            v@ == Seq::<T>::empty(),
    {
        Vec { buf: RawVec::new(), len: 0 }
    }
}

}
