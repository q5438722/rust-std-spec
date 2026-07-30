#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;

verus! {

pub assume_specification[std::process::abort]() -> !;

fn source_binary_heap_reserve_exact<T, A: Allocator>(
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
{
    match heap.try_reserve_exact(additional) {
        Ok(()) => {
            assert(heap.spec_capacity() >= heap@.len() + additional as nat);
        }
        Err(_) => std::process::abort(),
    }
}

} // verus!

fn main() {}