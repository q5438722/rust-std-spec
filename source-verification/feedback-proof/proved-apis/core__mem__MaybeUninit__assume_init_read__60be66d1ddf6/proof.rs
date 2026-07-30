#![feature(core_intrinsics)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use core::{intrinsics, mem::MaybeUninit};
use vstd::prelude::*;
use vstd::raw_ptr::MemContents;
use vstd::std_specs::maybe_uninit::*;

verus! {

pub uninterp spec fn ptr_mem_contents<T>(ptr: *const T) -> MemContents<T>;

pub assume_specification<T>[ intrinsics::assert_inhabited::<T> ]()
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ MaybeUninit::<T>::as_ptr ](
    m: &MaybeUninit<T>,
) -> (ptr: *const T)
    ensures
        ptr_mem_contents(ptr) == m.mem_contents(),
    opens_invariants none
    no_unwind
;

pub assume_specification<T>[ <*const T>::read ](
    ptr: *const T,
) -> (ret: T)
    requires
        ptr_mem_contents(ptr).is_init(),
    ensures
        ret == ptr_mem_contents(ptr).value(),
    opens_invariants none
    no_unwind
;

pub unsafe fn source_maybe_uninit_assume_init_read<T>(
    m: &MaybeUninit<T>,
) -> (ret: T)
    requires
        m.mem_contents().is_init(),
    ensures
        ret == m.mem_contents().value(),
    opens_invariants none
    no_unwind
{
    unsafe {
        intrinsics::assert_inhabited::<T>();
        m.as_ptr().read()
    }
}

}

fn main() {}