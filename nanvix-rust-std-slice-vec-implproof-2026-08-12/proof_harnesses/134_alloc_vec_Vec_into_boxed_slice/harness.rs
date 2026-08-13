#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::Vec::into_boxed_slice
// Source: alloc/src/vec/mod.rs:1733-1741
// Source item sha256: 9e01645b7eb77565f8c9119a9d5c258092a94b937fe775ec0227e0be20e18f44
// Dependency manifest: proof_manifests/134_alloc_vec_Vec_into_boxed_slice/dependency_assumption_manifest.json
//
// The public target body below is executable and keeps the Rust 1.96 control/data
// flow. The trusted boundary is limited to source-backed allocator/raw-pointer/
// provenance/MaybeUninit operations below: Vec::shrink_to_fit
// (alloc/src/vec/mod.rs:1604-1611 plus RawVec::shrink_to_fit at
// alloc/src/raw_vec/mod.rs:745-749), ManuallyDrop::new/Deref
// (core/src/mem/manually_drop.rs:184-185,273-278), ptr::read
// (core/src/ptr/mod.rs:1682-1698), RawVec::into_box
// (alloc/src/raw_vec/mod.rs:238-249), and Box<[MaybeUninit<T>]>::assume_init
// (alloc/src/boxed.rs:1229-1259).

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

pub struct ManuallyDrop<T, A: Allocator> {
    buf: RawVec<T, A>,
    len: usize,
}

pub struct BoxedMaybeUninitSlice<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub struct BoxedSlice<T, A: Allocator> {
    _marker_t: PhantomData<T>,
    _marker_a: PhantomData<A>,
}

pub trait CapacitySpec {
    spec fn spec_capacity(&self) -> nat;
}

pub uninterp spec fn raw_vec_initialized_seq<T, A: Allocator>(buf: &RawVec<T, A>) -> Seq<T>;

pub uninterp spec fn raw_vec_capacity<T, A: Allocator>(buf: &RawVec<T, A>) -> nat;

pub uninterp spec fn maybe_uninit_box_view<T, A: Allocator>(boxed: &BoxedMaybeUninitSlice<T, A>) -> Seq<T>;

pub uninterp spec fn maybe_uninit_box_capacity<T, A: Allocator>(boxed: &BoxedMaybeUninitSlice<T, A>) -> nat;

pub uninterp spec fn boxed_slice_view<T, A: Allocator>(boxed: BoxedSlice<T, A>) -> Seq<T>;

pub uninterp spec fn boxed_slice_capacity<T, A: Allocator>(boxed: BoxedSlice<T, A>) -> nat;

impl<T, A: Allocator> View for Vec<T, A> {
    type V = Seq<T>;

    closed spec fn view(&self) -> Seq<T> {
        raw_vec_initialized_seq(&self.buf)
    }
}

impl<T, A: Allocator> CapacitySpec for Vec<T, A> {
    closed spec fn spec_capacity(&self) -> nat {
        raw_vec_capacity(&self.buf)
    }
}

impl<T, A: Allocator> Vec<T, A> {
    #[verifier::external_body]
    pub fn shrink_to_fit(&mut self)
        ensures
            final(self)@ == old(self)@,
            final(self).spec_capacity() >= old(self)@.len(),
            final(self).spec_capacity() <= old(self).spec_capacity(),
    {
    }

    pub fn into_boxed_slice(self) -> (ret: BoxedSlice<T, A>)
        ensures
            boxed_slice_view::<T, A>(ret) == self@,
            boxed_slice_capacity::<T, A>(ret) == self@.len(),
    {
        let mut this = self;
        unsafe {
            this.shrink_to_fit();
            let me = ManuallyDrop::new(this);
            let buf = ptr::read(&me.buf);
            let len = me.len();
            buf.into_box(len).assume_init()
        }
    }
}

impl<T, A: Allocator> ManuallyDrop<T, A> {
    #[verifier::external_body]
    fn new(vec: Vec<T, A>) -> (me: Self)
        ensures
            raw_vec_initialized_seq(&me.buf) == vec@,
            raw_vec_capacity(&me.buf) == vec.spec_capacity(),
            me.len as nat == vec@.len(),
    {
        ManuallyDrop { buf: vec.buf, len: vec.len }
    }

    #[verifier::external_body]
    fn len(&self) -> (len: usize)
        ensures
            len as nat == raw_vec_initialized_seq(&self.buf).len(),
    {
        self.len
    }
}

pub mod ptr {
    use super::*;

    #[verifier::external_body]
    pub unsafe fn read<T, A: Allocator>(src: &RawVec<T, A>) -> (buf: RawVec<T, A>)
        ensures
            raw_vec_initialized_seq(&buf) == raw_vec_initialized_seq(src),
            raw_vec_capacity(&buf) == raw_vec_capacity(src),
    {
        RawVec { _marker_t: PhantomData, _marker_a: PhantomData }
    }
}

impl<T, A: Allocator> RawVec<T, A> {
    #[verifier::external_body]
    pub unsafe fn into_box(self, len: usize) -> (boxed: BoxedMaybeUninitSlice<T, A>)
        requires
            len as nat == raw_vec_initialized_seq(&self).len(),
        ensures
            maybe_uninit_box_view(&boxed) == raw_vec_initialized_seq(&self),
            maybe_uninit_box_capacity(&boxed) == len as nat,
    {
        BoxedMaybeUninitSlice { _marker_t: PhantomData, _marker_a: PhantomData }
    }
}

impl<T, A: Allocator> BoxedMaybeUninitSlice<T, A> {
    #[verifier::external_body]
    pub unsafe fn assume_init(self) -> (boxed: BoxedSlice<T, A>)
        ensures
            boxed_slice_view::<T, A>(boxed) == maybe_uninit_box_view(&self),
            boxed_slice_capacity::<T, A>(boxed) == maybe_uninit_box_capacity(&self),
    {
        BoxedSlice { _marker_t: PhantomData, _marker_a: PhantomData }
    }
}

}
