#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::{BinaryHeap, LinkedList, VecDeque};
use core::alloc::Allocator;
use vstd::prelude::*;

verus! {

fn binary_heap_is_empty_proof<T, A: Allocator>(
    heap: &BinaryHeap<T, A>,
) -> (result: bool)
    ensures
        result <==> heap@.len() == 0,
{
    heap.len() == 0
}

fn linked_list_is_empty_proof<T, A: Allocator>(
    list: &LinkedList<T, A>,
) -> (result: bool)
    ensures
        result <==> list@.len() == 0,
{
    list.len() == 0
}

fn vecdeque_default_proof<T>() -> (result: VecDeque<T>)
    ensures
        result@ == Seq::<T>::empty(),
{
    VecDeque::new()
}

fn vecdeque_is_empty_proof<T, A: Allocator>(
    deque: &VecDeque<T, A>,
) -> (result: bool)
    ensures
        result <==> deque@.len() == 0,
{
    deque.len() == 0
}

fn vecdeque_front_proof<T, A: Allocator>(
    deque: &VecDeque<T, A>,
) -> (result: Option<&T>)
    ensures
        deque@.len() == 0 ==> result is None,
        deque@.len() > 0 ==> (result matches Some(value) && *value == deque@[0]),
{
    deque.get(0)
}

fn vecdeque_back_proof<T, A: Allocator>(
    deque: &VecDeque<T, A>,
) -> (result: Option<&T>)
    ensures
        deque@.len() == 0 ==> result is None,
        deque@.len() > 0 ==> (result matches Some(value) && *value == deque@.last()),
{
    deque.get(deque.len().wrapping_sub(1))
}

} // verus!

fn main() {}
