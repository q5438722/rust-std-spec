#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::insert_mut ](
    v: &mut VecDeque<T, A>,
    index: usize,
    value: T,
) -> (result: &mut T)
    requires
        index <= old(v).len(),
    ensures
        *result == value,
        final(v)@ == old(v)@.insert(index as int, *final(result)),
;

fn source_vecdeque_insert<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    index: usize,
    value: T,
)
    requires
        index <= old(v).len(),
    ensures
        final(v)@ == old(v)@.insert(index as int, value),
{
    let _ = v.insert_mut(index, value);
}

} // verus!

fn main() {}