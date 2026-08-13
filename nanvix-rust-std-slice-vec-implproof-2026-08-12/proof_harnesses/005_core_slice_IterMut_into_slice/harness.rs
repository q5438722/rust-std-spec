#![allow(dead_code, unused_imports, unused_variables, unused_mut, unused_unsafe)]
// Target-specific Verus implementation harness.
// Target: core::slice::IterMut::into_slice
// Source: core/src/slice/iter.rs:194-205, 276-281 and core/src/slice/iter/macros.rs:49-60
// Source item sha256: 6b6f3d1c44a66191d56542d38615b12d4e540e8e4de042f6c176a22d715de7ca
// Dependency manifest: proof_manifests/005_core_slice_IterMut_into_slice/dependency_assumption_manifest.json

use core::marker::PhantomData;
use vstd::prelude::*;
use vstd::seq::*;

macro_rules! len {
    ($self:expr) => {{
        len_bang(&$self)
    }};
}

verus! {

pub struct NonNull<T> {
    ptr: *mut T,
    _marker: PhantomData<T>,
}

impl<T> NonNull<T> {
    fn as_ptr(&self) -> (ret: *mut T)
        ensures
            ret == self.ptr,
    {
        self.ptr
    }
}

pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remaining: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub uninterp spec fn raw_parts_mut_view<T>(data: *mut T, len: nat) -> Seq<T>;

pub uninterp spec fn len_macro_view<'a, T>(iter: IterMut<'a, T>) -> nat;

pub struct IterMut<'a, T: 'a> {
    ptr: NonNull<T>,
    end_or_len: *mut T,
    _marker: PhantomData<&'a mut T>,
}

pub closed spec fn slice_iterator_view<'a, T>(iter: IterMut<'a, T>) -> SliceIteratorView<T> {
    SliceIteratorView {
        source: raw_parts_mut_view(iter.ptr.ptr, len_macro_view(iter)),
        yielded_prefix: Seq::empty(),
        remaining: raw_parts_mut_view(iter.ptr.ptr, len_macro_view(iter)),
        remainder: Seq::empty(),
        chunk_size: 0,
        reverse: false,
    }
}

#[verifier::external_body]
pub fn len_bang<'a, T>(iter: &IterMut<'a, T>) -> (ret: usize)
    ensures
        ret as nat == len_macro_view(*iter),
{
    0
}

#[verifier::external_body]
pub fn from_raw_parts_mut<'a, T>(data: *mut T, len: usize) -> (ret: &'a mut [T])
    ensures
        ret@ == raw_parts_mut_view(data, len as nat),
{
    &mut []
}

impl<'a, T> IterMut<'a, T> {
    pub fn into_slice(self) -> (ret: &'a mut [T])
        ensures
            ret@ == slice_iterator_view(self).remaining,
    {
        // SAFETY: the iterator was created from a mutable slice with pointer
        // `self.ptr` and length `len!(self)`. This guarantees that all the prerequisites
        // for `from_raw_parts_mut` are fulfilled.
        let ret = unsafe { from_raw_parts_mut(self.ptr.as_ptr(), len!(self)) };
        proof {
            reveal(slice_iterator_view);
        }
        ret
    }
}

}
