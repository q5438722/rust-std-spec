#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

fn slice_length<T>(data: &[T]) -> (result: usize)
    ensures
        result as nat == data@.len(),
{
    <[T]>::len(data)
}

fn source_binary_heap_len<T, A: Allocator>(
    heap: &BinaryHeap<T, A>,
) -> (result: usize)
    ensures
        result as nat == heap@.len(),
{
    let data = heap.as_slice();
    let result = slice_length(data);
    proof {
        vstd::seq_lib::to_multiset_len(data@);
    }
    result
}

} // verus!

fn main() {}