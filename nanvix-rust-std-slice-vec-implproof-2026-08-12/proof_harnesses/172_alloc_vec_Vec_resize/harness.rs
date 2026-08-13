#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::resize
// Source: alloc/src/vec/mod.rs:3491-3499
// Source item sha256: a3210d36b66d7e2b3fcd63b8034af51d1f9255427f09a0345208d1608a125618
// Dependency manifest: proof_manifests/172_alloc_vec_Vec_resize/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow
// `let len = self.len(); if new_len > len { self.extend_with(new_len - len, value) } else { self.truncate(new_len); }`.
// Trusted boundaries are limited to the source-backed Vec length observation,
// truncate prefix effect, and private extend_with clone/write effect.

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

impl<T: core::clone::Clone, A: Allocator> Vec<T, A> {
    pub closed spec fn spec_len(&self) -> usize {
        self.len
    }

    pub fn resize(&mut self, new_len: usize, value: T)
        ensures
            new_len <= old(self).len() ==> final(self)@ == old(self)@.subrange(0, new_len as int),
            new_len > old(self).len() ==> {
                &&& final(self)@.len() == new_len
                &&& final(self)@.subrange(0, old(self).len() as int) == old(self)@
                &&& forall|i: int| #![all_triggers]
                    old(self).len() <= i < new_len ==> cloned::<T>(value, final(self)@[i])
            },
    {
        let ghost source = self@;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
        }

        if new_len > len {
            let additional = new_len - len;
            proof {
                assert(additional as int == new_len as int - len as int);
                assert(new_len as int == source.len() + additional as int);
            }
            self.extend_with(additional, value)
        } else {
            self.truncate(new_len);
        }
    }

    #[verifier::external_body]
    #[verifier::when_used_as_spec(spec_len)]
    pub fn len(&self) -> (len: usize)
        ensures
            len == self.spec_len(),
            len as nat == self@.len(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn truncate(&mut self, len: usize)
        ensures
            len <= old(self)@.len() ==> final(self)@ == old(self)@.subrange(0, len as int),
            len > old(self)@.len() ==> final(self)@ == old(self)@,
    {
    }

    #[verifier::external_body]
    fn extend_with(&mut self, n: usize, value: T)
        ensures
            final(self)@.len() == old(self)@.len() + n as nat,
            final(self)@.subrange(0, old(self)@.len() as int) == old(self)@,
            forall|i: int| #![trigger final(self)@[i]]
                old(self)@.len() <= i < final(self)@.len() ==> cloned::<T>(value, final(self)@[i]),
    {
    }
}

}
