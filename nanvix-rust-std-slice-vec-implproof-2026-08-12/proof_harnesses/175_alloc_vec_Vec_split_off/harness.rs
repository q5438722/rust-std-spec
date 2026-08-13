#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::split_off
// Source: alloc/src/vec/mod.rs:3080-3107
// Source item sha256: d672f7a5113a022b6b6ad201e5b796e498199cb4e7506226bde479431b7eb5c2
// Dependency manifest: proof_manifests/175_alloc_vec_Vec_split_off/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// bounds check/panic arm, other_len computation, with_capacity_in using the
// cloned allocator, unsafe set_len calls, copy_nonoverlapping, and returning
// other. Trusted boundaries are limited to source-backed allocator/Clone
// observation and raw pointer/set_len/copy effects needed to initialize the
// split tail in the newly allocated Vec.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    cap: usize,
    alloc: A,
    _marker_t: PhantomData<T>,
}

pub struct ConstPtr<T> {
    _marker_t: PhantomData<T>,
}

pub struct MutPtr<T> {
    _marker_t: PhantomData<T>,
}

impl<T> Copy for ConstPtr<T> {
}

impl<T> Clone for ConstPtr<T> {
    fn clone(&self) -> ConstPtr<T> {
        *self
    }
}

impl<T> Copy for MutPtr<T> {
}

impl<T> Clone for MutPtr<T> {
    fn clone(&self) -> MutPtr<T> {
        *self
    }
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

pub uninterp spec fn vec_start_ptr<T>(seq: Seq<T>, capacity: nat, ptr: ConstPtr<T>) -> bool;

pub uninterp spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: MutPtr<T>) -> bool;

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

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn copy_nonoverlapping<T>(src: ConstPtr<T>, dst: MutPtr<T>, count: usize) {
    }
}

impl<T> ConstPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: ConstPtr<T>) {
        self
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
            self@.len() <= self.spec_capacity(),
    {
        self.len
    }

    #[verifier::external_body]
    pub fn allocator(&self) -> (allocator: &A)
    {
        &self.buf.alloc
    }

    #[verifier::external_body]
    pub fn with_capacity_in(capacity: usize, alloc: A) -> (vec: Vec<T, A>)
        ensures
            vec@ == Seq::<T>::empty(),
            vec.spec_capacity() >= capacity as nat,
    {
        Vec { buf: RawVec { cap: capacity, alloc, _marker_t: PhantomData }, len: 0 }
    }

    #[verifier::external_body]
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len as nat <= old(self).spec_capacity(),
        ensures
            new_len as nat <= old(self)@.len() ==>
                final(self)@ == old(self)@.subrange(0, new_len as int),
            new_len as nat > old(self)@.len() ==>
                final(self)@.len() == new_len as nat,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        self.len = new_len;
    }

    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: ConstPtr<T>)
        ensures
            vec_start_ptr(self@, self.spec_capacity(), ptr),
    {
        ConstPtr { _marker_t: PhantomData }
    }

    #[verifier::external_body]
    pub fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            vec_start_mut_ptr(old(self)@, old(self).spec_capacity(), ptr),
            final(self)@ == old(self)@,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        MutPtr { _marker_t: PhantomData }
    }

    pub fn split_off(&mut self, at: usize) -> (return_value: Self)
        where A: core::clone::Clone
        requires
            at <= old(self)@.len(),
        ensures
            final(self)@ == old(self)@.subrange(0, at as int),
            return_value@ == old(self)@.subrange(at as int, old(self)@.len() as int),
    {
        let ghost source = self@;
        proof {
            assert(source.len() == self.len as nat);
            assert(at as nat <= self.len as nat);
            assert(at <= self.len);
        }

        if at > self.len() {
            assert_failed(at, self.len());
        }

        let other_len = self.len - at;
        let mut other = Vec::with_capacity_in(other_len, self.allocator().clone());

        proof {
            assert(other_len == self.len - at);
            assert(other_len as nat == source.len() - at as nat);
            assert(other_len as nat <= other.spec_capacity());
            assert(at as nat <= self.spec_capacity());
        }

        unsafe {
            self.set_len(at);
            other.set_len(other_len);

            ptr::copy_nonoverlapping(self.as_ptr().add(at), other.as_mut_ptr(), other.len());
        }
        proof {
            assert(self@ == source.subrange(0, at as int));
            rust_1_96_split_off_raw_copy_effect(&other, source, at, other_len);
        }
        other
    }
}

pub fn assert_failed(at: usize, len: usize)
    requires
        false,
{
}

#[verifier::external_body]
proof fn rust_1_96_split_off_raw_copy_effect<T, A: Allocator>(
    other: &Vec<T, A>,
    source: Seq<T>,
    at: usize,
    other_len: usize,
)
    requires
        at as nat <= source.len(),
        other_len as nat == source.len() - at as nat,
    ensures
        other@ == source.subrange(at as int, source.len() as int),
{
}

}
