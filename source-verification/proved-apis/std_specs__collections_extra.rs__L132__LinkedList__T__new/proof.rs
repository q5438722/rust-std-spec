#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::alloc::Global;
use alloc::collections::LinkedList;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

pub assume_specification[
    <Global as core::default::Default>::default
]() -> Global;

pub assume_specification<T, A: Allocator>[
    LinkedList::<T, A>::new_in
](alloc: A) -> (result: LinkedList<T, A>)
    ensures
        result@.len() == 0,
;

fn source_linked_list_new<T>() -> (result: LinkedList<T>)
    ensures
        result@ == Seq::<T>::empty(),
{
    let alloc = <Global as core::default::Default>::default();
    let result = LinkedList::<T, Global>::new_in(alloc);
    assert(result@ =~= Seq::<T>::empty());
    result
}

} // verus!

fn main() {}