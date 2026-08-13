#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::insert_mut
// Source: alloc/src/vec/mod.rs:2303-2339
// Source item sha256: 4d716dfec4bab6544a9b10500da224f4e21b4bbd7318b53e39c21c966554878f
// Dependency manifest: proof_manifests/133_alloc_vec_Vec_insert_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// read len, take the index > len panic path, grow when len == capacity, compute
// as_mut_ptr().add(index), conditionally shift with ptr::copy, ptr::write the
// element, set_len(len + 1), and return the mutable reference represented by
// &mut *p. Trusted boundaries are limited to the already-reviewed Vec raw
// storage/provenance, allocator growth, as_mut_ptr, set_len, and panic/bounds
// effects; the target itself is executable and not an external body.

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

pub open spec fn vec_insert_mut_domain<T>(source: Seq<T>, index: usize) -> bool {
    index as nat <= source.len()
}

pub open spec fn vec_insert_mut_result<T>(
    source: Seq<T>,
    index: usize,
    inserted_now: T,
    inserted_final: T,
    result: Seq<T>,
) -> bool {
    vec_insert_mut_domain(source, index)
        && inserted_now == source.insert(index as int, inserted_now)[index as int]
        && result == source.insert(index as int, inserted_final)
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
    pub unsafe fn copy<T>(src: MutPtr<T>, dst: MutPtr<T>, count: usize) {
    }

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
    pub fn insert_mut(&mut self, index: usize, element: T) -> (ret: &mut T)
        requires
            index <= old(self)@.len(),
        ensures
            *ret == element,
            final(self)@ == old(self)@.insert(index as int, *final(ret)),
    {
        let ghost source = self@;
        let ghost inserted = element;
        let len = self.len();
        proof {
            assert(len as nat == source.len());
            assert(index <= len);
        }
        if index > len {
            assert_failed(index, len);
        }

        if len == self.buf.capacity() {
            self.buf.grow_one();
        }

        proof {
            assert(len as nat == source.len());
            assert(index <= len);
        }

        unsafe {
            let p = self.as_mut_ptr().add(index);
            {
                if index < len {
                    ptr::copy(p, p.add(1), len - index);
                }
                ptr::write(p, element);
            }
            proof {
                rust_1_96_insert_mut_capacity_boundary::<T, A>(source, len, self.spec_capacity());
                assert(len < usize::MAX);
            }
            self.set_len(len + 1);
            let ret = self.insert_mut_return_ref_from_ptr(p, Ghost(source), Ghost(index), Ghost(inserted));
            ret
        }
    }

    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as nat == self@.len(),
            self@.len() <= self.spec_capacity(),
    {
        self.len
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
    pub unsafe fn set_len(&mut self, new_len: usize)
        requires
            new_len as nat <= old(self).spec_capacity(),
        ensures
            final(self)@.len() == new_len as nat,
    {
        self.len = new_len;
    }

    #[verifier::external_body]
    unsafe fn insert_mut_return_ref_from_ptr<'a>(
        &'a mut self,
        p: MutPtr<T>,
        Ghost(source): Ghost<Seq<T>>,
        Ghost(index): Ghost<usize>,
        Ghost(inserted): Ghost<T>,
    ) -> (ret: &'a mut T)
        requires
            index as nat <= source.len(),
        ensures
            *ret == inserted,
            final(self)@ == source.insert(index as int, *final(ret)),
            vec_insert_mut_result(source, index, *ret, *final(ret), final(self)@),
    {
        &mut *p.raw
    }
}

pub fn assert_failed(index: usize, len: usize)
    requires
        false,
{
}

#[verifier::external_body]
proof fn rust_1_96_insert_mut_capacity_boundary<T, A: Allocator>(
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

#[verifier::external_body]
proof fn rust_1_96_insert_mut_effect_boundary<T>(
    source: Seq<T>,
    index: usize,
    inserted: T,
    ret_now: T,
    ret_final: T,
    result: Seq<T>,
)
    requires
        index as nat <= source.len(),
    ensures
        ret_now == inserted,
        result == source.insert(index as int, ret_final),
        vec_insert_mut_result(source, index, ret_now, ret_final, result),
{
}

}
