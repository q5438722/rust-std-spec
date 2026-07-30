#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub fn source_core_ptr_is_null<T: core::marker::PointeeSized>(
    ptr: *const T,
) -> (result: bool)
    ensures
        result <==> ptr@.addr == 0,
{
    // `const_eval_select!` executes this branch outside const evaluation.
    let ptr = ptr as *const u8;
    ptr.addr() == 0
}

} // verus!

fn main() {}