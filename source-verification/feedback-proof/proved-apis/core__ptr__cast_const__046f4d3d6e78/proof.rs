#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub fn source_core_ptr_cast_const<T: core::marker::PointeeSized>(
    ptr: *mut T,
) -> (result: *const T)
    ensures
        result == ptr as *const T,
{
    ptr as _
}

} // verus!

fn main() {}