#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::try_reserve
// Source: alloc/src/vec/mod.rs:1537-1539
// Source item sha256: 6d996eef72e836e7886a8ec8e33f75b79fc971b0e8e5cbae9eeb593ce895ca3b
// Dependency manifest: proof_manifests/178_alloc_vec_Vec_try_reserve/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.try_reserve(self.len, additional)`. RawVec try_reserve now uses the
// same Ghost initialized-prefix model as Vec::reserve and preserves the
// initialized Vec view without a whole RawVec external body.

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
    model: Ghost<Seq<T>>,
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct Vec<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub uninterp spec fn raw_vec_value<T, A: Allocator>(buf: &RawVec<T, A>, i: int) -> T;

pub closed spec fn raw_vec_initialized_seq<T, A: Allocator>(
    buf: &RawVec<T, A>,
    len: usize,
) -> Seq<T> {
    Seq::new(len as nat, |i: int|
        if 0 <= i < buf.model@.len() {
            buf.model@[i]
        } else {
            raw_vec_value(buf, i)
        })
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf, self.len)
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    fn try_reserve(
        &mut self,
        len: usize,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        requires
            len as nat <= old(self).model@.len(),
        ensures
            final(self).model@ == old(self).model@,
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
        no_unwind
    {
        proof {
            assert(self.model@ == old(self).model@);
            assert(raw_vec_initialized_seq(self, len).len() == raw_vec_initialized_seq(old(self), len).len());
            assert forall|i: int|
                0 <= i < raw_vec_initialized_seq(self, len).len()
                implies raw_vec_initialized_seq(self, len)[i] == raw_vec_initialized_seq(old(self), len)[i]
            by {
                assert(i < len as nat);
                assert(i < old(self).model@.len());
            }
            assert(raw_vec_initialized_seq(self, len) =~= raw_vec_initialized_seq(old(self), len));
        }
        core::result::Result::Ok(())
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        self.len as nat <= self.buf.model@.len()
    }

    pub fn try_reserve(
        &mut self,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        ensures
            final(self)@ == old(self)@,
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        proof {
            use_type_invariant(&*self);
        }
        let result = self.buf.try_reserve(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self.len as nat <= self.buf.model@.len());
            assert(self@ == source);
        }
        result
    }
}

}
