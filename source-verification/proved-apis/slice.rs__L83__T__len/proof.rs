#![feature(ptr_metadata)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::slice::*;

verus! {

pub uninterp spec fn spec_ptr_from_ref<V: core::marker::PointeeSized>(
    value: &V,
) -> *const V;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::from_ref::<V> ](
    value: &V,
) -> (ptr: *const V)
    ensures
        ptr == spec_ptr_from_ref::<V>(value),
    opens_invariants none
    no_unwind
;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::metadata::<V> ](
    ptr: *const V,
) -> (metadata: <V as core::ptr::Pointee>::Metadata)
    ensures
        metadata == ptr@.metadata,
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_slice_metadata_from_ref<T>(slice: &[T])
    ensures
        spec_ptr_from_ref::<[T]>(slice)@.metadata == slice@.len(),
;

fn source_slice_len<T>(slice: &[T]) -> (len: usize)
    ensures
        len == spec_slice_len(slice),
{
    let ptr = core::ptr::from_ref(slice);
    let len = core::ptr::metadata(ptr);
    proof {
        axiom_slice_metadata_from_ref(slice);
        axiom_spec_len(slice);
    }
    len
}

}

fn main() {}