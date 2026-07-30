#![feature(core_intrinsics)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::intrinsics::align_of_val as intrinsic_align_of_val;
use vstd::layout::*;
use vstd::prelude::*;

verus! {

pub uninterp spec fn spec_align_of_val_raw<V: ?Sized>(ptr: *const V) -> nat;

pub uninterp spec fn spec_ptr_from_ref<V: core::marker::PointeeSized>(
    val: &V,
) -> *const V;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::from_ref::<V> ](
    val: &V,
) -> (ptr: *const V)
    ensures
        ptr == spec_ptr_from_ref::<V>(val),
    opens_invariants none
    no_unwind
;

pub assume_specification<V: ?Sized>[ core::intrinsics::align_of_val::<V> ](
    ptr: *const V,
) -> (u: usize)
    ensures
        u as nat == spec_align_of_val_raw::<V>(ptr),
    opens_invariants none
    no_unwind
;

pub axiom fn axiom_align_of_val_from_ref<V: ?Sized>(val: &V)
    ensures
        spec_align_of_val_raw::<V>(spec_ptr_from_ref::<V>(val))
            == spec_align_of_val::<V>(val),
;

fn source_core_mem_align_of_val<V: ?Sized>(val: &V) -> (u: usize)
    ensures
        u as nat == spec_align_of_val::<V>(val),
{
    let ptr = core::ptr::from_ref(val);
    let u = unsafe { intrinsic_align_of_val(ptr) };
    proof {
        axiom_align_of_val_from_ref(val);
    }
    u
}

}

fn main() {}