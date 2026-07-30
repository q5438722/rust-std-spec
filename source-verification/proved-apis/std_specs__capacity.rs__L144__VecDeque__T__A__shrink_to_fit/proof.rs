#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;

verus! {

pub fn source_vec_deque_shrink_to_fit<T, A: Allocator>(v: &mut VecDeque<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
{
    v.shrink_to(0);
}

} // verus!

fn main() {}