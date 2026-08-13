#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::leak
// Source: alloc/src/vec/mod.rs:3183-3189
// Source item sha256: e4456338d71998a9f4d2e2e27b060fc4f5aab3eecfe3725c08f35a351798e117
// Dependency manifest: proof_manifests/137_alloc_vec_Vec_leak/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 data flow:
// ManuallyDrop::new(self), then slice::from_raw_parts_mut(me.as_mut_ptr(), me.len).
// The trusted boundary is limited to source-backed ManuallyDrop no-drop/accessor
// behavior, Vec/RawVec raw-pointer provenance, and the unsafe mutable-slice view.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub struct ManuallyDrop<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn raw_mut_slice_view<T>(ptr: *mut T, len: usize) -> Seq<T>;

pub uninterp spec fn raw_mut_slice_domain<T>(ptr: *mut T, len: usize) -> bool;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn leak<'a>(self) -> (ret: &'a mut [T])
        ensures
            ret@ == self@,
            final(ret)@.len() == self@.len(),
    {
        let ghost source_view = self@;
        let mut me = ManuallyDrop::new(self);
        let ptr = me.as_mut_ptr();
        let len = me.len;
        proof {
            assert(raw_vec_initialized_seq(&me.buf) == source_view);
            assert(len == source_view.len());
            assert(raw_mut_slice_domain(ptr, len));
            assert(raw_mut_slice_view(ptr, len) == source_view);
        }
        unsafe { slice::from_raw_parts_mut(ptr, len) }
    }
}

impl<T, A: Allocator> ManuallyDrop<T, A> {
    #[verifier::external_body]
    fn new(vec: Vec<T, A>) -> (me: Self)
        ensures
            raw_vec_initialized_seq(&me.buf) == vec@,
            me.len == vec@.len(),
    {
        ManuallyDrop { buf: vec.buf, len: vec.len }
    }

    #[verifier::external_body]
    fn as_mut_ptr(&mut self) -> (ptr: *mut T)
        ensures
            raw_vec_initialized_seq(&final(self).buf) == raw_vec_initialized_seq(&old(self).buf),
            final(self).len == old(self).len,
            raw_mut_slice_domain(ptr, final(self).len),
            raw_mut_slice_view(ptr, final(self).len) == raw_vec_initialized_seq(&final(self).buf),
    {
        self.buf.ptr
    }
}

pub mod slice {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
        requires
            raw_mut_slice_domain(data, len),
        ensures
            ret@ == raw_mut_slice_view(data, len),
            final(ret)@.len() == len,
    {
        unsafe { &mut *core::ptr::slice_from_raw_parts_mut(data, len) }
    }
}

}
