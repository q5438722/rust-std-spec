#![feature(sized_hierarchy)]
#![allow(dead_code)]
#![allow(internal_features)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::raw_ptr::*;

verus! {

#[allow(ambiguous_wide_pointer_comparisons)]
pub fn source_core_ptr_eq<T: core::marker::PointeeSized>(
    a: *const T,
    b: *const T,
) -> (result: bool)
    ensures
        result <==> (a@.addr == b@.addr && a@.metadata == b@.metadata),
{
    a == b
}

} // verus!

fn main() {}