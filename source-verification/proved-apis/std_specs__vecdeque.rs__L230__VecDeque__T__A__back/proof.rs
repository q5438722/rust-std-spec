#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::{BinaryHeap, LinkedList, VecDeque};
use core::alloc::Allocator;
use vstd::prelude::*;

verus! {

fn source_binary_heap_is_empty<T, A: Allocator>(
    heap: &BinaryHeap<T, A>,
) -> (result: bool)
    ensures
        result <==> heap@.len() == 0,
{
    heap.len() == 0
}

fn source_linked_list_is_empty<T, A: Allocator>(
    list: &LinkedList<T, A>,
) -> (result: bool)
    ensures
        result <==> list@.len() == 0,
{
    list.len() == 0
}

fn source_vecdeque_default<T>() -> (result: VecDeque<T>)
    ensures
        result@ == Seq::<T>::empty(),
{
    VecDeque::new()
}

fn source_vecdeque_is_empty<T, A: Allocator>(
    deque: &VecDeque<T, A>,
) -> (result: bool)
    ensures
        result <==> deque@.len() == 0,
{
    deque.len() == 0
}

fn source_vecdeque_front<T, A: Allocator>(
    deque: &VecDeque<T, A>,
) -> (result: Option<&T>)
    ensures
        deque@.len() == 0 ==> result is None,
        deque@.len() > 0 ==> (result matches Some(value) && *value == deque@[0]),
{
    deque.get(0)
}

fn source_vecdeque_back<T, A: Allocator>(
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
