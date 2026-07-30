#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub fn source_core_ptr_addr_eq<
    T: core::marker::PointeeSized,
    U: core::marker::PointeeSized,
>(
    p: *const T,
    q: *const U,
) -> (result: bool)
    ensures
        result <==> p@.addr == q@.addr,
{
    (p as *const ()) == (q as *const ())
}

} // verus!

fn main() {}