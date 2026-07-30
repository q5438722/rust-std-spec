#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_index<T, A: Allocator>(
    v: &VecDeque<T, A>,
    i: usize,
) -> (result: &T)
    requires
        i < v.len(),
    ensures
        result == v.spec_index(i as int),
{
    v.get(i).expect("Out of bounds access")
}

} // verus!

fn main() {}