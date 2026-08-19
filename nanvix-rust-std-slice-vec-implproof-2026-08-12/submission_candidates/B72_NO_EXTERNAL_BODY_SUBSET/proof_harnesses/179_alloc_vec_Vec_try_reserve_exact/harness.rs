#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::try_reserve_exact
// Source: alloc/src/vec/mod.rs:1580-1582
// Source item sha256: 18865e667a6be1d4d3359dd42aa80f4000fae28d8fe1db41be021871a65ab075
// Dependency manifest: proof_manifests/179_alloc_vec_Vec_try_reserve_exact/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 body
// `self.buf.try_reserve_exact(self.len, additional)`. RawVec try_reserve_exact
// now uses the same Ghost initialized-prefix/type-invariant model as
// Vec::reserve and returns Err on the source-shaped capacity-overflow path.

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
    fn try_reserve_exact(
        &mut self,
        len: usize,
        additional: usize,
    ) -> (result: core::result::Result<(), TryReserveError>)
        requires
            len as nat <= old(self).model@.len(),
        ensures
            final(self).model@ == old(self).model@,
            raw_vec_initialized_seq(final(self), len) == raw_vec_initialized_seq(old(self), len),
            raw_vec_capacity(final(self)) >= raw_vec_capacity(old(self)),
            result is Ok ==> raw_vec_capacity(final(self)) >= len as nat + additional as nat,
        no_unwind
    {
        let result = if additional <= usize::MAX - len {
            proof {
                assert(len as nat + additional as nat <= usize::MAX as nat);
            }
            let needed = len + additional;
            if self.cap < needed {
                self.cap = needed;
            }
            proof {
                assert(needed as nat == len as nat + additional as nat);
                assert(self.cap >= needed);
                assert(raw_vec_capacity(self) >= raw_vec_capacity(old(self)));
            }
            core::result::Result::Ok(())
        } else {
            core::result::Result::Err(TryReserveError {})
        };
        proof {
            assert(self.model@ == old(self).model@);
            assert(raw_vec_capacity(self) >= raw_vec_capacity(old(self)));
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
        result
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::type_invariant]
    spec fn invariant(&self) -> bool {
        self.len as nat <= self.buf.model@.len() && self.len as nat <= raw_vec_capacity(&self.buf)
    }

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
        proof {
            use_type_invariant(&*self);
        }
        let result = self.buf.try_reserve_exact(self.len, additional);
        proof {
            assert(self.len == source_len);
            assert(self.len as nat <= self.buf.model@.len());
            assert(self.len as nat <= raw_vec_capacity(&self.buf));
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
