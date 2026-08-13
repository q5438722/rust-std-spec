#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::spare_capacity_mut
// Source: alloc/src/vec/mod.rs:3221-3231
// Source item sha256: 4afbe28230aa6dd0b41e9c23a5090e23f337024acf96d26bd4eef42b0e497d46
// Dependency manifest: proof_manifests/144_alloc_vec_Vec_spare_capacity_mut/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// `self.as_mut_ptr().add(self.len)`, `self.buf.capacity() - self.len`,
// and `slice::from_raw_parts_mut` over `MaybeUninit<T>` spare storage. Trusted
// boundaries are limited to reviewed Vec::as_mut_ptr, source-backed RawVec
// capacity, raw-pointer add/cast provenance, Vec len<=capacity, and mutable
// MaybeUninit raw-parts reconstruction.

use core::marker::PhantomData;
use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
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

pub struct RawVec<T, A: Allocator> {
    ptr: MutPtr<T>,
    cap: usize,
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

pub uninterp spec fn vec_start_mut_ptr<T>(seq: Seq<T>, capacity: nat, ptr: MutPtr<T>) -> bool;

pub uninterp spec fn raw_spare_mut_slice_domain<T>(
    source: Seq<T>,
    capacity: nat,
    data: MutPtr<MaybeUninit<T>>,
    len: usize,
) -> bool;

pub uninterp spec fn raw_spare_mut_slice_view<T>(
    source: Seq<T>,
    capacity: nat,
    data: MutPtr<MaybeUninit<T>>,
    len: usize,
) -> Seq<MaybeUninit<T>>;

pub uninterp spec fn vec_spare_capacity_relation<T>(
    source: Seq<T>,
    capacity: nat,
    spare: Seq<MaybeUninit<T>>,
) -> bool;

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

impl<T> MutPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: MutPtr<T>)
    {
        self
    }

    #[verifier::external_body]
    pub fn cast_maybe_uninit(self) -> (ptr: MutPtr<MaybeUninit<T>>)
    {
        MutPtr { raw: self.raw as *mut MaybeUninit<T>, _marker_t: PhantomData }
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    pub fn capacity(&self) -> (cap: usize)
        ensures
            cap as nat == raw_vec_capacity(self),
    {
        self.cap
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub fn spare_capacity_mut(&mut self) -> (ret: &mut [MaybeUninit<T>])
        ensures
            ret@.len() + old(self)@.len() == old(self).spec_capacity(),
            vec_spare_capacity_relation(old(self)@, old(self).spec_capacity(), ret@),
            final(self)@ == old(self)@,
    {
        let ghost source = self@;
        let ghost source_capacity = self.spec_capacity();
        let len = self.len;
        let cap = self.buf.capacity();
        proof {
            assert(len as nat == source.len());
            assert(cap as nat == source_capacity);
            rust_1_96_spare_capacity_len_capacity_boundary::<T, A>(source, source_capacity, len, cap);
            assert(self.len <= cap);
        }

        unsafe {
            let data = self.as_mut_ptr().add(self.len).cast_maybe_uninit();
            proof {
                assert(self.len == len);
                assert(self.len <= cap);
            }
            let spare_len = cap - self.len;
            proof {
                assert(spare_len == cap - len);
                rust_1_96_spare_capacity_raw_parts_boundary::<T, A>(
                    source,
                    source_capacity,
                    len,
                    cap,
                    spare_len,
                    data,
                );
            }
            slice::from_raw_parts_mut(Ghost(source), Ghost(source_capacity), data, spare_len)
        }
    }

    #[verifier::external_body]
    fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            vec_start_mut_ptr(old(self)@, old(self).spec_capacity(), ptr),
            final(self)@ == old(self)@,
            final(self).spec_capacity() == old(self).spec_capacity(),
            final(self).len == old(self).len,
    {
        self.buf.ptr
    }
}

#[verifier::external_body]
proof fn rust_1_96_spare_capacity_len_capacity_boundary<T, A: Allocator>(
    source: Seq<T>,
    capacity: nat,
    len: usize,
    cap: usize,
)
    requires
        len as nat == source.len(),
        cap as nat == capacity,
    ensures
        len <= cap,
{
}

#[verifier::external_body]
proof fn rust_1_96_spare_capacity_raw_parts_boundary<T, A: Allocator>(
    source: Seq<T>,
    capacity: nat,
    len: usize,
    cap: usize,
    spare_len: usize,
    data: MutPtr<MaybeUninit<T>>,
)
    requires
        len as nat == source.len(),
        cap as nat == capacity,
        len <= cap,
        spare_len == cap - len,
    ensures
        spare_len as nat + source.len() == capacity,
        raw_spare_mut_slice_domain(source, capacity, data, spare_len),
        raw_spare_mut_slice_view(source, capacity, data, spare_len).len() == spare_len as nat,
        vec_spare_capacity_relation(
            source,
            capacity,
            raw_spare_mut_slice_view(source, capacity, data, spare_len),
        ),
{
}

pub mod slice {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn from_raw_parts_mut<'a, T>(
        Ghost(source): Ghost<Seq<T>>,
        Ghost(capacity): Ghost<nat>,
        data: MutPtr<MaybeUninit<T>>,
        len: usize,
    ) -> (ret: &'a mut [MaybeUninit<T>])
        requires
            raw_spare_mut_slice_domain(source, capacity, data, len),
        ensures
            ret@ == raw_spare_mut_slice_view(source, capacity, data, len),
            ret@.len() == len as nat,
            final(ret)@.len() == len as nat,
    {
        unsafe { &mut *core::ptr::slice_from_raw_parts_mut(data.raw, len) }
    }
}

}
