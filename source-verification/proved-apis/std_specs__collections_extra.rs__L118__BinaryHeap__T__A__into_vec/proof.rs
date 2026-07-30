#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

pub assume_specification<T, A: Allocator>[
    <Vec<T, A> as core::convert::From<BinaryHeap<T, A>>>::from
](heap: BinaryHeap<T, A>) -> (result: Vec<T, A>)
    ensures
        result@.to_multiset() == heap@,
;

fn source_binary_heap_into_vec<T, A: Allocator>(
    heap: BinaryHeap<T, A>,
) -> (result: Vec<T, A>)
    ensures
        result@.to_multiset() == heap@,
{
    heap.into()
}

} // verus!

fn main() {}