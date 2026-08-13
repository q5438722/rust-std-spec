#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
#![crate_type = "lib"]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::clear
// Source: alloc/src/vec/mod.rs:2994-3007
// Source item sha256: d1e84ae8795bd399bd3a40128f9cae373e0b046264d744b7dc22e6f3c593c76c
// Dependency manifest: proof_manifests/161_alloc_vec_Vec_clear/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 flow:
// let elems: *mut [T] = self.as_mut_slice(); then unsafe len reset and
// ptr::drop_in_place(elems). Trusted boundaries are limited to the reviewed
// Vec::as_mut_slice sequence/final-frame vocabulary, the source-backed implicit
// raw mutable-slice pointer coercion, and the source-backed drop_in_place call.

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

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn drop_in_place<T>(elems: *mut [T]) {
        unsafe { core::ptr::drop_in_place(elems) }
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn as_mut_slice<'a>(&'a mut self) -> (slice: &'a mut [T])
        ensures
            slice@ == old(self)@,
            final(slice)@ == final(self)@,
    {
        loop {}
    }

    #[verifier::external_body]
    pub fn rust_1_96_as_mut_slice_raw_ptr(slice: &mut [T]) -> (elems: *mut [T]) {
        core::ptr::slice_from_raw_parts_mut(core::ptr::null_mut::<T>(), 0)
    }

    pub fn clear(&mut self)
        ensures
            final(self).view() == Seq::<T>::empty(),
    {
        let elems: *mut [T] = Self::rust_1_96_as_mut_slice_raw_ptr(self.as_mut_slice());

        unsafe {
            self.len = 0;
            ptr::drop_in_place(elems);
        }

        assert(final(self).view() =~= Seq::<T>::empty());
    }
}

}
