#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::LinkedList;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::collections_extra::*;

verus! {

pub assume_specification<T, A: Allocator>[ LinkedList::<T, A>::push_back_mut ](
    list: &mut LinkedList<T, A>,
    item: T,
) -> (result: &mut T)
    ensures
        *result == item,
        final(list)@ == old(list)@.push(*final(result)),
;

fn source_linked_list_push_back<T, A: Allocator>(
    list: &mut LinkedList<T, A>,
    item: T,
)
    ensures
        final(list)@ == old(list)@.push(item),
{
    let _ = list.push_back_mut(item);
}

} // verus!

fn main() {}