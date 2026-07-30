#![allow(dead_code)]
#![allow(unused_imports)]

use core::mem::ManuallyDrop;
use vstd::prelude::*;
use vstd::std_specs::core::*;

unsafe fn as_manually_drop_mut<T>(value: &mut T) -> &mut ManuallyDrop<T> {
    unsafe { &mut *(value as *mut T as *mut ManuallyDrop<T>) }
}

fn manually_drop_new<T>(value: T) -> ManuallyDrop<T> {
    ManuallyDrop::new(value)
}

verus! {

pub assume_specification<T>[ as_manually_drop_mut::<T> ](
    value: &mut T,
) -> (slot: &mut ManuallyDrop<T>)
    ensures
        slot@ == *old(value),
        final(slot)@ == *final(value),
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ ManuallyDrop::<T>::take ](
    slot: &mut ManuallyDrop<T>,
) -> (value: T)
    ensures
        value == old(slot)@,
        final(slot)@ == old(slot)@,
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ manually_drop_new::<T> ](
    value: T,
) -> (slot: ManuallyDrop<T>)
    ensures
        slot@ == value,
    opens_invariants none
    no_unwind
;

unsafe fn source_typed_swap_nonoverlapping<T>(x: &mut T, y: &mut T)
    ensures
        *final(x) == *old(y),
        *final(y) == *old(x),
    opens_invariants none
    no_unwind
{
    let x_slot = unsafe { as_manually_drop_mut(x) };
    let y_slot = unsafe { as_manually_drop_mut(y) };

    let temp = unsafe { ManuallyDrop::take(x_slot) };
    let other = unsafe { ManuallyDrop::take(y_slot) };
    *x_slot = manually_drop_new(other);
    *y_slot = manually_drop_new(temp);
}

fn source_core_mem_swap<T>(x: &mut T, y: &mut T)
    ensures
        *final(x) == *old(y),
        *final(y) == *old(x),
    opens_invariants none
    no_unwind
{
    // SAFETY: `&mut` guarantees these are typed readable and writable
    // as well as non-overlapping.
    unsafe { source_typed_swap_nonoverlapping(x, y) }
}

}

fn main() {}