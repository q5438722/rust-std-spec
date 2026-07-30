#![feature(allocator_api)]
#![feature(binary_heap_from_raw_vec)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::BinaryHeap;
use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::multiset::Multiset;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

pub assume_specification<T, A: Allocator>[
    BinaryHeap::<T, A>::from_raw_vec
](data: Vec<T, A>) -> (result: BinaryHeap<T, A>)
    ensures
        result@ == data@.to_multiset(),
;

fn source_binary_heap_new<T>() -> (result: BinaryHeap<T>)
    ensures
        result@ == Multiset::<T>::empty(),
{
    let data: Vec<T> = alloc::vec![];
    proof {
        vstd::seq_lib::to_multiset_len(data@);
        vstd::multiset::lemma_multiset_empty_len(data@.to_multiset());
    }
    unsafe {
        BinaryHeap::from_raw_vec(data)
    }
}

} // verus!

fn main() {}