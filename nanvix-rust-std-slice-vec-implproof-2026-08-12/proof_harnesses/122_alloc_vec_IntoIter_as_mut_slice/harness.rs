#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: alloc::vec::IntoIter::as_mut_slice
// Source: alloc/src/vec/into_iter.rs:45-60 and alloc/src/vec/into_iter.rs:106-119
// Source item sha256: d37c9626fa2c73748fd0635410768e7139bfd271e847da808eea70504debe146
// Dependency manifest: proof_manifests/122_alloc_vec_IntoIter_as_mut_slice/dependency_assumption_manifest.json

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

pub uninterp spec fn vec_into_iter_remaining_mut<T, A: Allocator>(iter: IntoIter<T, A>) -> Seq<T>;

pub uninterp spec fn into_iter_raw_mut_slice_view<T>(raw: *mut [T]) -> Seq<T>;

impl<T, A: Allocator> IntoIter<T, A> {
    #[verifier::external_body]
    pub fn len(&self) -> (len: usize)
        ensures
            len as int == vec_into_iter_remaining_mut::<T, A>(*self).len(),
    {
        0
    }

    #[verifier::external_body]
    fn as_raw_mut_slice(&mut self) -> (raw: *mut [T])
        ensures
            into_iter_raw_mut_slice_view(raw) == vec_into_iter_remaining_mut::<T, A>(*old(self)),
            vec_into_iter_remaining_mut::<T, A>(*final(self))
                == vec_into_iter_remaining_mut::<T, A>(*old(self)),
    {
        core::ptr::slice_from_raw_parts_mut(self.ptr.as_ptr(), self.len())
    }

    #[verifier::external_body]
    unsafe fn rust_1_96_raw_mut_slice_deref<'a>(raw: *mut [T]) -> (ret: &'a mut [T])
        ensures
            ret@ == into_iter_raw_mut_slice_view(raw),
            final(ret)@ == into_iter_raw_mut_slice_view(raw),
    {
        unsafe { &mut *raw }
    }

    pub fn as_mut_slice<'a>(&'a mut self) -> (ret: &'a mut [T])
        ensures
            ret@ == vec_into_iter_remaining_mut::<T, A>(*old(self)),
            vec_into_iter_remaining_mut::<T, A>(*final(self)) == final(ret)@,
    {
        let raw = self.as_raw_mut_slice();
        unsafe { Self::rust_1_96_raw_mut_slice_deref(raw) }
    }
}

}
