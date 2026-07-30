#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_deref<T, A: Allocator>(
    vec: &Vec<T, A>,
) -> (slice: &[T])
    ensures
        slice@ == vec@,
{
    vec.as_slice()
}

} // verus!

fn main() {}