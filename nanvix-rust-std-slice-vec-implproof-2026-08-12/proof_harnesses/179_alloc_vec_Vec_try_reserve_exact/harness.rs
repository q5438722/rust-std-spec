#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::try_reserve_exact
// Source: alloc/src/vec/mod.rs:1580-1582
// Source item sha256: 18865e667a6be1d4d3359dd42aa80f4000fae28d8fe1db41be021871a65ab075
// Dependency manifest: proof_manifests/179_alloc_vec_Vec_try_reserve_exact/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.try_reserve_exact(self.len, additional)`. The trusted boundary is
// limited to RawVec try_reserve_exact's allocator/result-capacity operation
// preserving the initialized prefix represented by the Vec view.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct TryReserveError {
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
    fn try_reserve_exact(
        &mut self,
        len: usize,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        ensures
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
            result is Ok ==> raw_vec_capacity(final(self)) >= len as nat + additional as nat,
    {
        core::result::Result::Ok(())
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn try_reserve_exact(
        &mut self,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        ensures
            final(self)@ == old(self)@,
            result is Ok ==> final(self).spec_capacity() >= old(self)@.len() + additional as nat,
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        assert(source.len() == source_len as nat);
        let result = self.buf.try_reserve_exact(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self@ == source);
            if result is Ok {
                assert(self.spec_capacity() >= source_len as nat + additional as nat);
                assert(self.spec_capacity() >= source.len() + additional as nat);
            }
        }
        result
    }
}

}
