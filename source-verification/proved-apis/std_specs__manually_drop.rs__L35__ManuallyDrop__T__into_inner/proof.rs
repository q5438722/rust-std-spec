#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::std_specs::manually_drop::*;

verus! {

pub uninterp spec fn spec_ptr_from_ref<V: core::marker::PointeeSized>(
    value: &V,
) -> *const V;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::from_ref::<V> ](
    value: &V,
) -> (ptr: *const V)
    ensures
        ptr == spec_ptr_from_ref(value),
    opens_invariants none
    no_unwind
;

pub assume_specification<V>[ core::ptr::read::<V> ](
    ptr: *const V,
) -> (value: V)
    ensures
        forall|source: &V|
            ptr == spec_ptr_from_ref(source) ==> value == *source,
    opens_invariants none
    no_unwind
;

fn source_manually_drop_into_inner<T>(slot: ManuallyDrop<T>) -> (value: T)
    ensures
        value == slot@,
{
    // Verus does not support `&raw const`; Deref and from_ref form the
    // equivalent pointer to the transparent wrapper's payload.
    let inner: &T = core::ops::Deref::deref(&slot);
    let ptr = core::ptr::from_ref(inner);
    // SAFETY: `inner` points to a valid `T`, and `slot` will not drop it.
    unsafe { core::ptr::read(ptr) }
}

} // verus!

fn main() {}