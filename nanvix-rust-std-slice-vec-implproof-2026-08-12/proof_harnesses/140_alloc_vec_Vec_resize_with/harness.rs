#![allow(dead_code, unused_imports, unused_variables, unused_mut)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::resize_with
// Source: alloc/src/vec/mod.rs:3141-3151
// Source item sha256: 7da0ce9c77eee1999e5df23636944c2bb9f79d4aa5f95743aa968431af1e6672
// Dependency manifest: proof_manifests/140_alloc_vec_Vec_resize_with/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// read len, extend with repeat_with(f).take(new_len - len) when growing, and
// otherwise delegate to truncate. Trusted boundaries are limited to source-backed
// Vec len/truncate/extend_trusted effects, the repeat_with/take iterator wrapper,
// and the zero-argument FnMut output trace observed by extend_trusted.

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

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn zero_arg_fnmut_outputs<F, T>(f: F, len: nat) -> Seq<T>;

pub broadcast axiom fn axiom_zero_arg_fnmut_outputs_len<F, T>(f: F, len: nat)
    ensures
        #[trigger] zero_arg_fnmut_outputs::<F, T>(f, len).len() == len,
;

pub open spec fn vec_resize_with_result<T, F: FnMut() -> T>(
    source: Seq<T>,
    new_len: usize,
    f: F,
    result: Seq<T>,
) -> bool {
    &&& source.len() <= new_len as nat
    &&& result == source + zero_arg_fnmut_outputs::<F, T>(
        f,
        (new_len as int - source.len() as int) as nat,
    )
}

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

pub mod iter {
    use super::*;

    pub struct RepeatWith<F> {
        pub f: F,
    }

    pub struct Take<I> {
        pub iter: I,
        pub n: usize,
    }

    pub fn repeat_with<F>(f: F) -> (ret: RepeatWith<F>)
        ensures
            ret.f == f,
    {
        RepeatWith { f }
    }

    impl<F> RepeatWith<F> {
        pub fn take(self, n: usize) -> (ret: Take<Self>)
            ensures
                ret.iter == self,
                ret.n == n,
        {
            Take { iter: self, n }
        }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn resize_with<F>(&mut self, new_len: usize, f: F)
        where
            F: FnMut() -> T,
        ensures
            new_len <= old(self)@.len() ==> final(self)@ == old(self)@.subrange(0, new_len as int),
            new_len > old(self)@.len() ==> vec_resize_with_result(old(self)@, new_len, f, final(self)@),
    {
        let ghost source = self@;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
        }
        if new_len > len {
            let additional = new_len - len;
            let trusted_iter = iter::repeat_with(f).take(additional);
            proof {
                assert(additional as int == new_len as int - len as int);
                assert(new_len as int == source.len() + additional as int);
            }
            self.extend_trusted(trusted_iter);
        } else {
            self.truncate(new_len);
        }
    }

    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
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
    pub fn extend_trusted<F>(&mut self, iter: iter::Take<iter::RepeatWith<F>>)
        where
            F: FnMut() -> T,
        ensures
            forall|target_len: usize|
                target_len as int == old(self)@.len() + iter.n as int ==> #[trigger]
                    vec_resize_with_result::<T, F>(
                        old(self)@,
                        target_len,
                        iter.iter.f,
                        final(self)@,
                    ),
    {
    }
}

}
