#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub fn source_core_ptr_cast_mut<T: core::marker::PointeeSized>(
    ptr: *const T,
) -> (result: *mut T)
    ensures
        result == ptr as *mut T,
{
    ptr as _
}

} // verus!

fn main() {}