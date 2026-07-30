#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_clear<T, A: Allocator>(vec: &mut Vec<T, A>)
    ensures
        final(vec).view() == Seq::<T>::empty(),
{
    vec.truncate(0);
}

} // verus!

fn main() {}