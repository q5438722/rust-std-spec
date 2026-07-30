#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_unsafe)]
#![feature(core_intrinsics)]

use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::{PointsTo, ptr_mut_ref};
use vstd::std_specs::maybe_uninit::*;

verus! {

pub assume_specification<T>[ core::intrinsics::assert_inhabited::<T> ]()
    opens_invariants none
    no_unwind
;

pub uninterp spec fn spec_maybe_uninit_as_mut_ptr<T>(
    m: &MaybeUninit<T>,
) -> *mut T;

pub assume_specification<T>[ MaybeUninit::<T>::as_mut_ptr ](
    m: &mut MaybeUninit<T>,
) -> (ptr: *mut T)
    ensures
        ptr == spec_maybe_uninit_as_mut_ptr(old(m)),
        *final(m) === *old(m),
    opens_invariants none
    no_unwind
;

// vstd does not expose the permission projection for this transparent storage cast.
pub axiom fn axiom_maybe_uninit_as_mut_ptr_points_to<'a, T>(
    m: &'a mut MaybeUninit<T>,
    ptr: *mut T,
) -> (tracked points_to: &'a mut PointsTo<T>)
    requires
        ptr == spec_maybe_uninit_as_mut_ptr(m),
    ensures
        points_to.ptr() == ptr,
        points_to.opt_value() == old(m).mem_contents(),
        final(m).mem_contents() == final(points_to).opt_value(),
;

unsafe fn source_maybe_uninit_assume_init_mut<T>(
    m: &mut MaybeUninit<T>,
) -> (ret: &mut T)
    requires
        m.mem_contents().is_init(),
    ensures
        *ret == old(m).mem_contents().value(),
        final(m).mem_contents().is_init(),
        final(m).mem_contents().value() == *final(ret),
    opens_invariants none
    no_unwind
{
    unsafe {
        core::intrinsics::assert_inhabited::<T>();
        let ptr = m.as_mut_ptr();
        // Verus raw-pointer dereferences use an explicit permission.
        let tracked points_to = axiom_maybe_uninit_as_mut_ptr_points_to(m, ptr);
        assert(points_to.is_init());
        ptr_mut_ref(ptr, Tracked(points_to))
    }
}

} // verus!

fn main() {}