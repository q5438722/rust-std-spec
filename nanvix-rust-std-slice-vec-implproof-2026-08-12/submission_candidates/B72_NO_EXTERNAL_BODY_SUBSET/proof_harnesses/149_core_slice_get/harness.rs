#![allow(dead_code, unused_imports, unused_variables)]
// Target-specific Verus implementation harness.
// Target: core::slice::get
// Source: core/src/slice/mod.rs:572-577
// Source item sha256: f9e71a7d0218566f3b21467e4f552e762ce8d7d4a49e2d879423cbc99b4604fe
// Dependency manifest: proof_manifests/149_core_slice_get/dependency_assumption_manifest.json
//
// Rust 1.96 body: index.get(self)

use vstd::prelude::*;

verus! {

pub trait SliceIndex<T: ?Sized> {
    type Output: ?Sized;

    spec fn spec_get(self, slice: &T) -> Option<&Self::Output>;

    fn get<'a>(self, slice: &'a T) -> (ret: Option<&'a Self::Output>)
        ensures
            ret == self.spec_get(slice),
    ;
}

pub open spec fn spec_slice_get<T: ?Sized, I: SliceIndex<T>>(
    val: &T,
    idx: I,
) -> Option<&<I as SliceIndex<T>>::Output> {
    idx.spec_get(val)
}

pub broadcast axiom fn axiom_slice_get_usize<T>(v: &[T], i: usize)
    ensures
        i < v.len() ==> #[trigger] spec_slice_get(v, i) == Some(&v[i as int]),
        i >= v.len() ==> spec_slice_get(v, i).is_none(),
;

impl<T> SliceIndex<[T]> for usize {
    type Output = T;

    open spec fn spec_get(self, slice: &[T]) -> Option<&T> {
        if self < slice.len() {
            Some(&slice[self as int])
        } else {
            None
        }
    }

    fn get<'a>(self, slice: &'a [T]) -> (ret: Option<&'a T>)
        ensures
            ret == self.spec_get(slice),
    {
        if self < slice.len() {
            Some(&slice[self])
        } else {
            None
        }
    }
}

pub fn get<'a, T, I>(slice: &'a [T], index: I) -> (ret: Option<&'a <I as SliceIndex<[T]>>::Output>)
    where
        I: SliceIndex<[T]>,
    ensures
        ret == spec_slice_get(slice, index),
{
    index.get(slice)
}

}
