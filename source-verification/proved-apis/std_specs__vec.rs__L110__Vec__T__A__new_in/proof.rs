#![allow(dead_code)]
#![allow(unused_imports)]
#![feature(allocator_api)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_new_in<T, A: Allocator>(alloc: A) -> (v: Vec<T, A>)
    ensures
        v@ == Seq::<T>::empty(),
{
    // At capacity zero, RawVec::with_capacity_in takes its zero-layout branch
    // and constructs RawVecInner::new_in, matching the private source fields.
    let v = Vec::<T, A>::with_capacity_in(0, alloc);
    assert(v@ == Seq::<T>::empty());
    v
}

} // verus!

fn main() {}