#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::reserve
// Source: alloc/src/vec/mod.rs:1470-1472
// Source item sha256: 4ded02663952e67a346806815cfb0e4793baf644311bac182337299ffa407f49
// Dependency manifest: proof_manifests/170_alloc_vec_Vec_reserve/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.reserve(self.len, additional);`. RawVec reserve is now executable in
// the harness: capacity is updated separately from a Ghost initialized-prefix
// model guarded by the target-local Vec len/capacity type invariant.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
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

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
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
    fn reserve(&mut self, len: usize, additional: usize)
        requires
            len as nat <= old(self).model@.len(),
        ensures
            final(self).model@ == old(self).model@,
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
            raw_vec_capacity(final(self)) >= raw_vec_capacity(old(self)),
        no_unwind
    {
        if additional <= usize::MAX - len {
            let needed = len + additional;
            if self.cap < needed {
                self.cap = needed;
            }
        }
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
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        self.len as nat <= self.buf.model@.len() && self.len as nat <= raw_vec_capacity(&self.buf)
    }

    pub fn reserve(&mut self, additional: usize)
        ensures
            final(self)@ == old(self)@,
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        proof {
            use_type_invariant(&*self);
        }
        self.buf.reserve(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self.len as nat <= self.buf.model@.len());
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
            assert(self@ == source);
        }
    }
}

}
