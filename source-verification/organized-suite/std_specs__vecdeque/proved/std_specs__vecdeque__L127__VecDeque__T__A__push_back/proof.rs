#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::push_back_mut ](
    v: &mut VecDeque<T, A>,
    value: T,
) -> (result: &mut T)
    ensures
        *result == value,
        final(v)@ == old(v)@.push(*final(result)),
;

fn vecdeque_push_back_proof<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    value: T,
)
    ensures
        final(v)@ == old(v)@.push(value),
{
    let _ = v.push_back_mut(value);
}

} // verus!

fn main() {}