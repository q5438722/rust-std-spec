#![feature(core_intrinsics)]
#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::std_specs::maybe_uninit::*;

verus! {

pub assume_specification<T>[ core::intrinsics::assert_inhabited::<T> ]()
    opens_invariants none
    no_unwind
;

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

unsafe fn source_maybe_uninit_assume_init<T>(
    m: MaybeUninit<T>,
) -> (value: T)
    requires
        m.mem_contents().is_init(),
    ensures
        value == m.mem_contents().value(),
    opens_invariants none
    no_unwind
{
    unsafe {
        core::intrinsics::assert_inhabited::<T>();
        // The private `value` field and `&raw const` are unavailable downstream;
        // `assume_init_ref` exposes the same initialized payload pointer.
        let initialized: &T = m.assume_init_ref();
        let ptr = core::ptr::from_ref(initialized);
        core::ptr::read(ptr)
    }
}

} // verus!

fn main() {}