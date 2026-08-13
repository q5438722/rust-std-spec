#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::try_reserve
// Source: alloc/src/vec/mod.rs:1537-1539
// Source item sha256: 6d996eef72e836e7886a8ec8e33f75b79fc971b0e8e5cbae9eeb593ce895ca3b
// Dependency manifest: proof_manifests/178_alloc_vec_Vec_try_reserve/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.try_reserve(self.len, additional)`. The trusted boundary is
// limited to RawVec try_reserve's allocator/result operation preserving the
// initialized prefix represented by the Vec view.

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

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    fn try_reserve(
        &mut self,
        len: usize,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        ensures
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
    {
        core::result::Result::Ok(())
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn try_reserve(
        &mut self,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        ensures
            final(self)@ == old(self)@,
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        let result = self.buf.try_reserve(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self@ == source);
        }
        result
    }
}

}
