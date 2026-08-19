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
// The raw tail slice constructor and drop call remain executable after the
// length commit, and the prefix relation is proved in this harness.

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

    pub unsafe fn slice_from_raw_parts_mut<T>(data: MutPtr<T>, len: usize) -> (slice: RawMutSlice<T>) {
        RawMutSlice { ptr: data, len }
    }

    pub unsafe fn drop_in_place<T>(to_drop: RawMutSlice<T>) {
    }
}

impl<T> MutPtr<T> {
    pub unsafe fn add(self, count: usize) -> (ptr: MutPtr<T>) {
        self
    }
}

impl<T, A: Allocator> Vec<T, A> {
    pub closed spec fn spec_len(&self) -> usize {
        self.len
    }

    #[verifier::when_used_as_spec(spec_len)]
    pub fn len(&self) -> (len: usize)
        ensures
            len == self.spec_len(),
            len as nat == self@.len(),
    {
        self.len
    }

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
            proof {
                assert(self@ == source);
                rust_1_96_truncate_len_drop_effect::<T, A>(&self.buf, source, self.len, len);
                assert(raw_vec_initialized_seq(&self.buf, len) == source.subrange(0, len as int));
            }
            self.len = len;
            ptr::drop_in_place(s);
            proof {
                assert(self@.len() == len as nat);
                assert(raw_vec_initialized_seq(&self.buf, len) == source.subrange(0, len as int));
            }
        }
    }
}

proof fn rust_1_96_truncate_len_drop_effect<T, A: Allocator>(
    buf: &RawVec<T, A>,
    source: Seq<T>,
    old_len: usize,
    len: usize,
)
    requires
        len <= old_len,
        source == raw_vec_initialized_seq(buf, old_len),
    ensures
        raw_vec_initialized_seq(buf, len) == source.subrange(0, len as int),
{
    assert(raw_vec_initialized_seq::<T, A>(buf, len)
        =~= raw_vec_initialized_seq::<T, A>(buf, old_len).subrange(0, len as int));
}

}
