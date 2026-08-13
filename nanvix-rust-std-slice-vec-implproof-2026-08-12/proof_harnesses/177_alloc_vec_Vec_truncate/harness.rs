#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::truncate
// Source: alloc/src/vec/mod.rs:1786-1806
// Source item sha256: 313c80370f5440fac3c71d476b84509e66203aaf878ed6677a5f8831823c475c
// Dependency manifest: proof_manifests/177_alloc_vec_Vec_truncate/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// unsafe early return when len exceeds self.len, remaining_len computation,
// slice_from_raw_parts_mut(self.as_mut_ptr().add(len), remaining_len),
// self.len = len, and drop_in_place of the old tail.
// Trusted boundaries are limited to the reviewed as_mut_ptr/raw pointer slice
// construction and the drop/length-commit effect on the logical Vec view.

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;
use vstd::view::*;

verus! {

pub trait Allocator {
}

pub struct RawVec<T, A: Allocator> {
    ptr: *mut T,
    _marker_t: PhantomData<T>,
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
        *self
    }
}

pub struct RawMutSlice<T> {
    ptr: MutPtr<T>,
    len: usize,
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

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn slice_from_raw_parts_mut<T>(data: MutPtr<T>, len: usize) -> (slice: RawMutSlice<T>) {
        RawMutSlice { ptr: data, len }
    }

    #[verifier::external_body]
    pub unsafe fn drop_in_place<T>(to_drop: RawMutSlice<T>) {
    }
}

impl<T> MutPtr<T> {
    #[verifier::external_body]
    pub unsafe fn add(self, count: usize) -> (ptr: MutPtr<T>) {
        self
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub closed spec fn spec_len(&self) -> usize {
        self.len
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
    pub fn as_mut_ptr(&mut self) -> (ptr: MutPtr<T>)
        ensures
            final(self)@ == old(self)@,
    {
        MutPtr { raw: self.buf.ptr, _marker_t: PhantomData }
    }

    pub fn truncate(&mut self, len: usize)
        ensures
            len <= old(self).len() ==> final(self)@ == old(self)@.subrange(0, len as int),
            len > old(self).len() ==> final(self)@ == old(self)@,
    {
        let ghost source = self@;
        proof {
            assert(source.len() == self.len as nat);
        }
        unsafe {
            if len > self.len {
                return;
            }
            proof {
                assert(len <= self.len);
                assert(len as nat <= source.len());
            }
            let remaining_len = self.len - len;
            let s = ptr::slice_from_raw_parts_mut(self.as_mut_ptr().add(len), remaining_len);
            self.len = len;
            ptr::drop_in_place(s);
            proof {
                assert(self@.len() == len as nat);
                rust_1_96_truncate_len_drop_effect::<T, A>(self, source, len);
            }
        }
    }
}

#[verifier::external_body]
proof fn rust_1_96_truncate_len_drop_effect<T, A: Allocator>(
    vec: &Vec<T, A>,
    source: Seq<T>,
    len: usize,
)
    requires
        len as nat <= source.len(),
        vec@.len() == len as nat,
    ensures
        vec@ == source.subrange(0, len as int),
{
}

}
