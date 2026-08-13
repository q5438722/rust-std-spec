#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::as_slice
// Source: alloc/src/vec/mod.rs:1823-1842
// Source item sha256: f88b7f2076ec783fa661d350464cb623d1fa17242d1c3ca10b55a12fbfd66b61
// Dependency manifest: proof_manifests/159_alloc_vec_Vec_as_slice/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 data flow:
// self.as_ptr(), self.len, then the unsafe aggregate_raw_ptr shared-slice
// construction. Trusted boundaries are limited to the reviewed Vec::as_ptr
// raw-pointer vocabulary and the source-backed intrinsic/raw shared slice
// dereference boundary.

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

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T>;

pub uninterp spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat;

pub uninterp spec fn vec_start_ptr<T>(seq: Seq<T>, capacity: nat, ptr: *const T) -> bool;

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
    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: *const T)
        ensures
            vec_start_ptr(self@, self.spec_capacity(), ptr),
    {
        core::ptr::null()
    }

    #[verifier::external_body]
    unsafe fn rust_1_96_aggregate_raw_ptr_slice<'a>(
        vec: &'a Self,
        ptr: *const T,
        len: usize,
    ) -> (slice: &'a [T])
        requires
            vec_start_ptr(vec@, vec.spec_capacity(), ptr),
        ensures
            slice@ == vec@,
    {
        // Rust 1.96 source expression:
        // &*core::intrinsics::aggregate_raw_ptr::<*const [T], _, _>(ptr, len)
        unsafe { core::slice::from_raw_parts(ptr, len) }
    }

    pub fn as_slice<'a>(&'a self) -> (slice: &'a [T])
        ensures
            slice@ == self@,
    {
        let ptr = self.as_ptr();
        let len = self.len;
        unsafe { Self::rust_1_96_aggregate_raw_ptr_slice(self, ptr, len) }
    }
}

}
