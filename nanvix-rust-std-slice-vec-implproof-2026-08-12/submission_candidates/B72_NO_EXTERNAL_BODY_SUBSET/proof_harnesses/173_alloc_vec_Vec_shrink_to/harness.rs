#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::shrink_to
// Source: alloc/src/vec/mod.rs:1633-1637
// Source item sha256: ccf6385c3871762eb1ba633ea239b2b1084d3089f98b07e71532ce323220cb45
// Dependency manifest: proof_manifests/173_alloc_vec_Vec_shrink_to/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 branch and
// RawVec shrink call, adapted only by naming the executable
// `cmp::max(self.len, min_capacity)` result before passing it to
// `self.buf.shrink_to_fit`. The Vec capacity/length fact is carried by a
// target-local type invariant; trusted boundaries are limited to the RawVec shrink allocator-capacity operation
// preserving the initialized prefix represented by the Vec view.

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

pub mod cmp {
    use super::*;

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
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }

    fn shrink_to_fit(&mut self, cap: usize)
        requires
            cap as nat <= raw_vec_capacity(old(self)),
            cap as nat <= old(self).model@.len(),
        ensures
            final(self).model@ == old(self).model@,
            raw_vec_capacity(final(self)) >= cap as nat,
            raw_vec_capacity(final(self)) <= raw_vec_capacity(old(self)),
            forall|prefix_len: usize| prefix_len <= cap ==>
                raw_vec_initialized_seq(final(self), prefix_len) ==
                    raw_vec_initialized_seq(old(self), prefix_len),
        no_unwind
    {
        let ghost old_cap = self.cap;
        if self.cap > cap {
            self.cap = cap;
        }
        proof {
            assert(self.model@ == old(self).model@);
            if old_cap > cap {
                assert(self.cap == cap);
            } else {
                assert(self.cap == old_cap);
                assert(cap <= old_cap);
            }
            assert(self.cap >= cap);
            assert(self.cap <= old_cap);
            assert(raw_vec_capacity(self) >= cap as nat);
            assert(raw_vec_capacity(self) <= raw_vec_capacity(old(self)));
            assert forall|prefix_len: usize| prefix_len <= cap implies
                raw_vec_initialized_seq(self, prefix_len) ==
                    raw_vec_initialized_seq(old(self), prefix_len)
            by {
                assert(raw_vec_initialized_seq(self, prefix_len).len() ==
                    raw_vec_initialized_seq(old(self), prefix_len).len());
                assert forall|i: int|
                    0 <= i < raw_vec_initialized_seq(self, prefix_len).len()
                    implies raw_vec_initialized_seq(self, prefix_len)[i] ==
                        raw_vec_initialized_seq(old(self), prefix_len)[i]
                by {
                    assert(i < prefix_len as nat);
                    assert(i < cap as nat);
                    assert(i < old(self).model@.len());
                }
                assert(raw_vec_initialized_seq(self, prefix_len) =~=
                    raw_vec_initialized_seq(old(self), prefix_len));
            }
        }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        self.len as nat <= raw_vec_capacity(&self.buf)
            && raw_vec_capacity(&self.buf) <= self.buf.model@.len()
    }

    fn capacity(&self) -> (capacity: usize)
        ensures
            capacity as nat == self.spec_capacity(),
            self.len as nat <= self.spec_capacity(),
    {
        let capacity = self.buf.capacity();
        proof {
            use_type_invariant(self);
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
            assert(self.spec_capacity() == raw_vec_capacity(&self.buf));
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
            use_type_invariant(&*self);
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
            assert(self.spec_capacity() == raw_vec_capacity(&self.buf));
            assert(raw_vec_capacity(&self.buf) <= self.buf.model@.len());
            assert(source.len() == source_len as nat);
            assert(source_len as nat <= source_capacity);
            assert(source_capacity <= self.buf.model@.len());
        }
        if self.capacity() > min_capacity {
            let shrink_capacity = cmp::max(self.len, min_capacity);
            proof {
                assert(self.len == source_len);
                assert(self.spec_capacity() == source_capacity);
                assert(source_len <= shrink_capacity);
                assert(min_capacity <= shrink_capacity);
                assert(shrink_capacity as nat <= source_capacity);
                assert(shrink_capacity as nat <= self.buf.model@.len());
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
