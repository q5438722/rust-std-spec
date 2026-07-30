#![allow(dead_code)]
#![allow(unused_imports)]

use core::ptr::dangling_mut as ptr_dangling_mut;
use vstd::prelude::*;

verus! {

pub assume_specification<T>[ core::ptr::dangling_mut::<T> ]() -> (result: *mut T)
    ensures
        result@.addr != 0,
        result@.addr as nat % vstd::layout::align_of::<T>() == 0,
    opens_invariants none
    no_unwind
;

pub fn source_core_ptr_dangling<T>() -> (result: *const T)
    ensures
        result@.addr != 0,
        result@.addr as nat % vstd::layout::align_of::<T>() == 0,
    opens_invariants none
    no_unwind
{
    ptr_dangling_mut()
}

} // verus!

fn main() {}