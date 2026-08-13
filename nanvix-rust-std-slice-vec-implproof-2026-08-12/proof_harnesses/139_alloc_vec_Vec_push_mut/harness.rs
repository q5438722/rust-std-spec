#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::push_mut
// Source: alloc/src/vec/mod.rs:1035-1050
// Source item sha256: 6c8b36eab73f66482884d759b69b9fb660766ce4792acb7119f5947841e104ab
// Dependency manifest: proof_manifests/139_alloc_vec_Vec_push_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// read len, grow when len == capacity, compute as_mut_ptr().add(len),
// ptr::write the new element, assign self.len = len + 1, and return the
// mutable reference represented by &mut *end. Trusted boundaries are limited to
// reviewed/source-backed RawVec allocation capacity/growth, Vec::as_mut_ptr,
// raw-pointer add/write/provenance, the overflow/unsafe domain, and returned
// mutable-reference reconstruction.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    cap: usize,
    _marker_a: PhantomData<A>,
}

pub struct MutPtr<T> {
    raw: *mut T,
    _marker_t: PhantomData<T>,
}

impl<T> Copy for MutPtr<T> {
}

impl<T> Clone for MutPtr<T> {
    fn clone(&self) -> MutPtr<T> {
        MutPtr { raw: self.raw, _marker_t: PhantomData }
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

pub uninterp spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: MutPtr<T>) -> bool;

pub open spec fn vec_push_mut_result<T>(
    source: Seq<T>,
    pushed_now: T,
    pushed_final: T,
    result: Seq<T>,
) -> bool {
    pushed_now == pushed_now && result == source.push(pushed_final)
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

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn write<T>(dst: MutPtr<T>, value: T) {
    }
}

impl<T> MutPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: MutPtr<T>)
    {
        self
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }

    #[verifier::external_body]
    pub fn grow_one(&mut self)
        ensures
            raw_vec_capacity(final(self)) > raw_vec_capacity(old(self)),
    {
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn push_mut(&mut self, value: T) -> (ret: &mut T)
        ensures
            *ret == value,
            final(self)@ == old(self)@.push(*final(ret)),
            vec_push_mut_result(old(self)@, *ret, *final(ret), final(self)@),
    {
        let ghost source = self@;
        let ghost inserted = value;
        let len = self.len;
        proof {
            assert(len as nat == source.len());
        }

        if len == self.buf.capacity() {
            self.buf.grow_one();
        }

        unsafe {
            let end = self.as_mut_ptr().add(len);
            ptr::write(end, value);
            proof {
                rust_1_96_push_mut_capacity_boundary::<T, A>(source, len, self.spec_capacity());
                assert(len < usize::MAX);
            }
            self.len = len + 1;
            let ret = self.push_mut_return_ref_from_ptr(end, Ghost(source), Ghost(inserted));
            ret
        }
    }

    #[verifier::external_body]
    pub fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            vec_start_mut_ptr(old(self)@, old(self).spec_capacity(), ptr),
            final(self)@ == old(self)@,
            final(self).spec_capacity() == old(self).spec_capacity(),
    {
        MutPtr { raw: self.buf.ptr, _marker_t: PhantomData }
    }

    #[verifier::external_body]
    unsafe fn push_mut_return_ref_from_ptr<'a>(
        &'a mut self,
        end: MutPtr<T>,
        Ghost(source): Ghost<Seq<T>>,
        Ghost(inserted): Ghost<T>,
    ) -> (ret: &'a mut T)
        requires
            source.len() < usize::MAX,
        ensures
            *ret == inserted,
            final(self)@ == source.push(*final(ret)),
            vec_push_mut_result(source, *ret, *final(ret), final(self)@),
    {
        &mut *end.raw
    }
}

#[verifier::external_body]
proof fn rust_1_96_push_mut_capacity_boundary<T, A: Allocator>(
    source: Seq<T>,
    len: usize,
    capacity: nat,
)
    requires
        len as nat == source.len(),
    ensures
        len < usize::MAX,
        (len + 1) as nat <= capacity,
{
}

}
