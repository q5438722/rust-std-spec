#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;

verus! {

pub axiom fn axiom_vec_capacity_at_least_len<T, A: Allocator>(v: &Vec<T, A>)
    ensures
        v.spec_capacity() >= v@.len(),
;

pub fn source_vec_shrink_to_fit<T, A: Allocator>(v: &mut Vec<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
{
    let capacity = v.capacity();
    let len = v.len();
    proof {
        axiom_vec_capacity_at_least_len(v);
    }
    if capacity > len {
        v.shrink_to(len);
    }
}

} // verus!

fn main() {}