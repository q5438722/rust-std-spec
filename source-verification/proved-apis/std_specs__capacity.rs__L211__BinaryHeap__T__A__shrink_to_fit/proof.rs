#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;

verus! {

pub fn source_binary_heap_shrink_to_fit<T, A: Allocator>(
    heap: &mut BinaryHeap<T, A>,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len(),
        final(heap).spec_capacity() <= old(heap).spec_capacity(),
{
    let len = heap.len();
    // At the heap length, Vec::shrink_to has the same guard and RawVec call
    // as Vec::shrink_to_fit in Rust 1.96.
    heap.shrink_to(len);
}

} // verus!

fn main() {}