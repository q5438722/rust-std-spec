#![feature(core_intrinsics)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::intrinsics::size_of_val as intrinsic_size_of_val;
use vstd::layout::*;
use vstd::prelude::*;

verus! {

pub uninterp spec fn spec_ptr_from_ref<V: core::marker::PointeeSized>(
    val: &V,
) -> *const V;

pub assume_specification<V: ?Sized>[ core::intrinsics::size_of_val::<V> ](
    ptr: *const V,
) -> (u: usize)
    ensures
        forall|val: &V|
            ptr == spec_ptr_from_ref::<V>(val) ==>
                u as nat == spec_size_of_val::<V>(val),
    opens_invariants none
    no_unwind
;

pub assume_specification<V: core::marker::PointeeSized>[ core::ptr::from_ref::<V> ](
    val: &V,
) -> (ptr: *const V)
    ensures
        ptr == spec_ptr_from_ref::<V>(val),
    opens_invariants none
    no_unwind
;

fn source_core_mem_size_of_val<V: ?Sized>(val: &V) -> (u: usize)
    ensures
        u as nat == spec_size_of_val::<V>(val),
{
    let ptr = core::ptr::from_ref(val);
    unsafe { intrinsic_size_of_val(ptr) }
}

}

fn main() {}