#![feature(sized_hierarchy)]
#![allow(dead_code)]

use vstd::prelude::*;

verus! {

fn source_ptr_cast<T: core::marker::PointeeSized, U>(
    ptr: *const T,
) -> (result: *const U)
    ensures
        result == ptr as *const U,
    opens_invariants none
    no_unwind
{
    ptr as _
}

}

fn main() {}