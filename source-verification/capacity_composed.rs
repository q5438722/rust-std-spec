#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::{BinaryHeap, VecDeque};
use alloc::string::String;
use alloc::vec::Vec;
use vstd::multiset::Multiset;
use vstd::prelude::*;
use vstd::std_specs::capacity::CapacitySpec;

verus! {

fn source_vec_with_capacity<T>(capacity: usize) -> (result: Vec<T>)
    ensures
        result@ == Seq::<T>::empty(),
{
    let mut result = Vec::new();
    result.reserve(capacity);
    result
}

fn source_vecdeque_with_capacity<T>(capacity: usize) -> (result: VecDeque<T>)
    ensures
        result@ == Seq::<T>::empty(),
{
    let mut result = VecDeque::new();
    result.reserve(capacity);
    result
}

fn source_string_with_capacity(capacity: usize) -> (result: String)
    ensures
        result@ == Seq::<char>::empty(),
        result.spec_capacity() >= capacity as nat,
{
    let mut result = String::new();
    result.reserve_exact(capacity);
    result
}

fn source_binary_heap_with_capacity<T>(capacity: usize) -> (result: BinaryHeap<T>)
    ensures
        result@ == Multiset::<T>::empty(),
        result.spec_capacity() >= capacity as nat,
{
    let mut result = BinaryHeap::new();
    result.reserve_exact(capacity);
    result
}

} // verus!

fn main() {}
