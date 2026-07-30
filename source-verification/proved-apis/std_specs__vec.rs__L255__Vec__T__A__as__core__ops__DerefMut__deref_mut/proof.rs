#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_deref_mut<T, A: Allocator>(
    vec: &mut Vec<T, A>,
) -> (slice: &mut [T])
    ensures
        slice@ == old(vec)@,
        final(slice)@ == final(vec)@,
{
    vec.as_mut_slice()
}

}

fn main() {}