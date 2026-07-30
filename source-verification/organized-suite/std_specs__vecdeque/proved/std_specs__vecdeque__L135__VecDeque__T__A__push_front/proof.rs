#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::push_front_mut ](
    v: &mut VecDeque<T, A>,
    value: T,
) -> (result: &mut T)
    ensures
        *result == value,
        final(v)@ == seq![*final(result)] + old(v)@,
;

fn vec_deque_push_front_proof<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    value: T,
)
    ensures
        final(v)@ == seq![value] + old(v)@,
{
    let _ = v.push_front_mut(value);
}

} // verus!

fn main() {}