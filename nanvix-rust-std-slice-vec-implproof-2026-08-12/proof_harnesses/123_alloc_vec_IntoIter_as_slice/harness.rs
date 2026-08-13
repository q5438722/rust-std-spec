#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::IntoIter::as_slice
// Source: alloc/src/vec/into_iter.rs:45-60 and alloc/src/vec/into_iter.rs:88-90
// Source item sha256: 67c76644a8b9172e9112aa9eb6e3000069c672ec3095d86f5b8762ed410fa67b
// Dependency manifest: proof_manifests/123_alloc_vec_IntoIter_as_slice/dependency_assumption_manifest.json

use core::marker::PhantomData;
use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::seq::*;

verus! {

pub trait Allocator {
}

pub struct NonNull<T> {
    _marker: PhantomData<T>,
}

impl<T> NonNull<T> {
    #[verifier::external_body]
    pub fn as_ptr(&self) -> (ptr: *mut T) {
        core::ptr::null_mut()
    }
}

pub struct IntoIter<T, A: Allocator> {
    buf: NonNull<T>,
    phantom: PhantomData<T>,
    cap: usize,
    alloc: ManuallyDrop<A>,
    ptr: NonNull<T>,
    end: *const T,
}

pub uninterp spec fn vec_into_iter_remaining<T, A: Allocator>(iter: &IntoIter<T, A>) -> Seq<T>;

impl<T, A: Allocator> IntoIter<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as int == vec_into_iter_remaining::<T, A>(self).len(),
    {
        0
    }

    #[verifier::external_body]
    unsafe fn rust_1_96_slice_from_raw_parts_remaining<'a>(
        iter: &'a Self,
        data: *mut T,
        len: usize,
    ) -> (ret: &'a [T])
        ensures
            ret@ == vec_into_iter_remaining::<T, A>(iter),
    {
        unsafe { &*core::ptr::slice_from_raw_parts(data, len) }
    }

    pub fn as_slice<'a>(&'a self) -> (ret: &'a [T])
        ensures
            ret@ == vec_into_iter_remaining::<T, A>(self),
    {
        unsafe { Self::rust_1_96_slice_from_raw_parts_remaining(self, self.ptr.as_ptr(), self.len()) }
    }
}

}
