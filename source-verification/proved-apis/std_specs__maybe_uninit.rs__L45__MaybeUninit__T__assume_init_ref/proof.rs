#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use core::mem::MaybeUninit;
use vstd::prelude::*;
use vstd::raw_ptr::{ptr_ref, MemContents, PointsTo};
use vstd::std_specs::maybe_uninit::*;

verus! {

pub uninterp spec fn is_maybe_uninit_data_ptr<T>(
    m: &MaybeUninit<T>,
    ptr: *const T,
) -> bool;

pub assume_specification<T>[ core::intrinsics::assert_inhabited::<T> ]()
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ MaybeUninit::<T>::as_ptr ](
    m: &MaybeUninit<T>,
) -> (ptr: *const T)
    ensures
        is_maybe_uninit_data_ptr(m, ptr),
    opens_invariants none
    no_unwind
;

axiom fn axiom_maybe_uninit_points_to<'a, T>(
    m: &'a MaybeUninit<T>,
    ptr: *const T,
) -> (tracked pt: &'a PointsTo<T>)
    requires
        is_maybe_uninit_data_ptr(m, ptr),
    ensures
        pt.ptr() == ptr,
        pt.opt_value() == m.mem_contents(),
;

unsafe fn source_maybe_uninit_assume_init_ref<'a, T>(
    m: &'a MaybeUninit<T>,
) -> (ret: &'a T)
    requires
        m.mem_contents().is_init(),
    ensures
        ret == m.mem_contents().value(),
    opens_invariants none
    no_unwind
{
    unsafe {
        core::intrinsics::assert_inhabited::<T>();
        let ptr = m.as_ptr();
        let tracked pt = axiom_maybe_uninit_points_to(m, ptr);
        ptr_ref(ptr, Tracked(pt))
    }
}

}

fn main() {}