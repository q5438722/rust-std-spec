#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::reserve_exact
// Source: alloc/src/vec/mod.rs:1500-1502
// Source item sha256: bc6abd6c66986fb488a7f7b477b31d6a37de280ac60a8400c0e3612b0b560da1
// Dependency manifest: proof_manifests/171_alloc_vec_Vec_reserve_exact/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.reserve_exact(self.len, additional);`. The trusted boundary is
// limited to RawVec reserve_exact's allocator/capacity operation preserving the
// initialized prefix represented by the Vec view while ensuring enough capacity
// for the initialized length plus the requested additional capacity.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

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
    len: usize,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
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

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    fn reserve_exact(&mut self, len: usize, additional: usize)
        ensures
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
            raw_vec_capacity(final(self)) >= len as nat + additional as nat,
    {
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn reserve_exact(&mut self, additional: usize)
        ensures
            final(self)@ == old(self)@,
            final(self).spec_capacity() >= old(self)@.len() + additional as nat,
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        assert(source.len() == source_len as nat);
        self.buf.reserve_exact(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self@ == source);
            assert(self.spec_capacity() >= source_len as nat + additional as nat);
            assert(self.spec_capacity() >= source.len() + additional as nat);
        }
    }
}

}
