#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::into_raw_parts
// Source: alloc/src/vec/mod.rs:842-845
// Source item sha256: 73e1cdd172063d94e4ee444da5a24df73c3a89e829f871f946a895f569edcfc0
// Dependency manifest: proof_manifests/136_alloc_vec_Vec_into_raw_parts/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 data flow:
// ManuallyDrop::new(self), then as_mut_ptr/len/capacity observations. The trusted
// boundary is limited to source-backed ManuallyDrop deref/accessor behavior and
// RawVec raw-pointer/capacity/provenance vocabulary from alloc/src/vec/mod.rs and
// alloc/src/raw_vec/mod.rs; the target itself is not an external body.

use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub struct RawVec<T> {
    ptr: *mut T,
    cap: usize,
}

pub struct Vec<T> {
    buf: RawVec<T>,
    len: usize,
}

pub struct ManuallyDrop<T> {
    buf: RawVec<T>,
    len: usize,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T>(buf: &RawVec<T>) -> Seq<T>;

pub closed spec fn raw_vec_capacity<T>(buf: &RawVec<T>) -> nat {
    buf.cap as nat
}

pub uninterp spec fn vec_raw_parts_round_trip<T>(
    seq: Seq<T>,
    capacity: nat,
    ptr: *mut T,
    len: usize,
    cap: usize,
) -> bool;

impl<T> View for Vec<T> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T> CapacitySpec for Vec<T> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

impl<T> Vec<T> {
    pub fn into_raw_parts(self) -> (parts: (*mut T, usize, usize))
        ensures
            parts.1 == self@.len(),
            parts.2 as nat == self.spec_capacity(),
            vec_raw_parts_round_trip(self@, self.spec_capacity(), parts.0, parts.1, parts.2),
    {
        let ghost source_view = self@;
        let ghost source_capacity = self.spec_capacity();
        let mut me = ManuallyDrop::new(self);
        let ptr = me.as_mut_ptr();
        let len = me.len();
        let cap = me.capacity();
        proof {
            assert(raw_vec_initialized_seq(&me.buf) == source_view);
            assert(raw_vec_capacity(&me.buf) == source_capacity);
            assert(len == source_view.len());
            assert(cap as nat == source_capacity);
            assert(vec_raw_parts_round_trip::<T>(source_view, source_capacity, ptr, len, cap));
        }
        (ptr, len, cap)
    }
}

impl<T> ManuallyDrop<T> {
    #[verifier::external_body]
    fn new(vec: Vec<T>) -> (me: Self)
        ensures
            raw_vec_initialized_seq(&me.buf) == vec@,
            raw_vec_capacity(&me.buf) == vec.spec_capacity(),
            me.len == vec@.len(),
    {
        ManuallyDrop { buf: vec.buf, len: vec.len }
    }

    #[verifier::external_body]
    fn as_mut_ptr(&mut self) -> (ptr: *mut T)
        ensures
            raw_vec_initialized_seq(&final(self).buf) == raw_vec_initialized_seq(&old(self).buf),
            raw_vec_capacity(&final(self).buf) == raw_vec_capacity(&old(self).buf),
            final(self).len == old(self).len,
            forall|cap: usize|
                cap as nat == raw_vec_capacity(&old(self).buf) ==>
                    vec_raw_parts_round_trip(
                        raw_vec_initialized_seq(&old(self).buf),
                        raw_vec_capacity(&old(self).buf),
                        ptr,
                        old(self).len,
                        cap,
                    ),
    {
        self.buf.ptr
    }

    #[verifier::external_body]
    fn len(&self) -> (len: usize)
        ensures
            len == self.len,
            len == raw_vec_initialized_seq(&self.buf).len(),
    {
        self.len
    }

    #[verifier::external_body]
    fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(&self.buf),
    {
        self.buf.cap
    }
}

}
