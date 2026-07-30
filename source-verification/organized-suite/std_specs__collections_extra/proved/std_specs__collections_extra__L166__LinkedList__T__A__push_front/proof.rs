#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::LinkedList;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::push_front_mut ](
    list: &mut LinkedList<T, A>,
    item: T,
) -> (result: &mut T)
    ensures
        *result == item,
        final(list)@ == seq![*final(result)] + old(list)@,
;

fn linked_list_push_front_proof<T, A: Allocator>(
    list: &mut LinkedList<T, A>,
    item: T,
)
    ensures
        final(list)@ == seq![item] + old(list)@,
{
    let _ = list.push_front_mut(item);
}

} // verus!

fn main() {}