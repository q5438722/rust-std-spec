#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::shrink_to
// Source: alloc/src/vec/mod.rs:1633-1637
// Source item sha256: ccf6385c3871762eb1ba633ea239b2b1084d3089f98b07e71532ce323220cb45
// Dependency manifest: proof_manifests/173_alloc_vec_Vec_shrink_to/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 branch and
// RawVec shrink call, adapted only by naming the `cmp::max(self.len, min_capacity)`
// result before passing it to `self.buf.shrink_to_fit`.
// Trusted boundaries are limited to the source-backed Vec capacity/length
// invariant and RawVec shrink allocator-capacity operation preserving the
// initialized prefix represented by the Vec view.

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

pub mod cmp {
    use super::*;

    #[verifier::external_body]
    pub fn max(a: usize, b: usize) -> (result: usize)
        ensures
            result >= a,
            result >= b,
            result == a || result == b,
    {
        if a >= b {
            a
        } else {
            b
        }
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }

    #[verifier::external_body]
    fn shrink_to_fit(&mut self, cap: usize)
        requires
            cap as nat <= raw_vec_capacity(old(self)),
        ensures
            raw_vec_capacity(final(self)) >= cap as nat,
            raw_vec_capacity(final(self)) <= raw_vec_capacity(old(self)),
            forall|prefix_len: usize| prefix_len <= cap ==>
                raw_vec_initialized_seq(final(self), prefix_len) ==
                    raw_vec_initialized_seq(old(self), prefix_len),
    {
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    proof fn vec_len_capacity_invariant(&self)
        ensures
            self.len as nat <= self.spec_capacity(),
    {
    }

    #[verifier::external_body]
    fn capacity(&self) -> (capacity: usize)
        ensures
            capacity as nat == self.spec_capacity(),
            self.len as nat <= self.spec_capacity(),
    {
        let capacity = self.buf.capacity();
        proof {
            self.vec_len_capacity_invariant();
        }
        capacity
    }

    pub fn shrink_to(&mut self, min_capacity: usize)
        ensures
            final(self)@ == old(self)@,
            final(self).spec_capacity() >= old(self)@.len(),
            final(self).spec_capacity() <= old(self).spec_capacity(),
    {
        let ghost source = self@;
        let ghost source_len = self.len;
        let ghost source_capacity = self.spec_capacity();
        proof {
            self.vec_len_capacity_invariant();
            assert(source.len() == source_len as nat);
            assert(source_len as nat <= source_capacity);
        }
        if self.capacity() > min_capacity {
            let shrink_capacity = cmp::max(self.len, min_capacity);
            proof {
                assert(self.len == source_len);
                assert(self.spec_capacity() == source_capacity);
                assert(source_len <= shrink_capacity);
                assert(min_capacity <= shrink_capacity);
                assert(shrink_capacity as nat <= source_capacity);
            }
            self.buf.shrink_to_fit(shrink_capacity);
            proof {
                assert(self.len == source_len);
                assert(source_len <= shrink_capacity);
                assert(raw_vec_initialized_seq(&self.buf, source_len) == source);
                assert(self@ == source);
                assert(self.spec_capacity() >= source_len as nat);
                assert(self.spec_capacity() <= source_capacity);
            }
        } else {
            proof {
                assert(self@ == source);
                assert(self.spec_capacity() == source_capacity);
                assert(self.spec_capacity() >= source_len as nat);
            }
        }
    }
}

}
