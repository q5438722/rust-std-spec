#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn source_vecdeque_shrink_to_fit<T, A: Allocator>(v: &mut VecDeque<T, A>)
    ensures
        final(v)@ == old(v)@,
{
    v.shrink_to(0);
}

} // verus!

fn main() {}