#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_with_capacity_in<T, A: Allocator>(
    capacity: usize,
    alloc: A,
) -> (v: Vec<T, A>)
    ensures
        v@ == Seq::<T>::empty(),
{
    // Representation-free desugaring of the private RawVec field construction.
    let mut v = Vec::<T, A>::new_in(alloc);
    v.reserve_exact(capacity);
    v
}

} // verus!

fn main() {}