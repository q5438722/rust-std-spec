#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

fn source_binary_heap_peek<T, A: Allocator>(
    heap: &BinaryHeap<T, A>,
) -> (result: Option<&T>)
    ensures
        result is None <==> heap@.len() == 0,
        result matches Some(value) ==> heap@.contains(*value),
{
    let data = heap.as_slice();
    let result = data.get(0);
    proof {
        vstd::slice::axiom_spec_len(data);
        vstd::slice::axiom_slice_get_usize(data, 0);
        vstd::seq_lib::to_multiset_len(data@);
        if data@.len() > 0 {
            assert(data@.contains(data@[0]));
            vstd::seq_lib::to_multiset_contains(data@, data@[0]);
        }
    }
    result
}

} // verus!

fn main() {}