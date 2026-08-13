#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::push
// Source: alloc/src/vec/mod.rs:1003-1005
// Source item sha256: 006e192586e2af8b1c62b55f5cd21ef8b6462082a0638c7c87664df02a81d5de
// Dependency manifest: proof_manifests/168_alloc_vec_Vec_push/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 wrapper
// flow `let _ = self.push_mut(value);`. The trusted boundary is the
// already-reviewed `Vec::push_mut` implementation proof.

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
    #[verifier::external_body]
    pub fn push_mut(&mut self, value: T) -> (ret: &mut T)
        ensures
            *ret == value,
            final(self)@ == old(self)@.push(*final(ret)),
    {
        unsafe { &mut *self.buf.ptr }
    }

    pub fn push(&mut self, value: T)
        ensures
            final(self)@ == old(self)@.push(value),
    {
        let _ = self.push_mut(value);
    }
}

}
