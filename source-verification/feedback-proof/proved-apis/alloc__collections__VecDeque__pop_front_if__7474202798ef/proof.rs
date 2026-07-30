#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::vec_deque::VecDeque;
use core::alloc::Allocator;
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[VecDeque::<T, A>::front_mut](
    v: &mut VecDeque<T, A>,
) -> (result: Option<&mut T>)
    ensures
        old(v)@.len() == 0 ==> result is None && final(v)@ == old(v)@,
        old(v)@.len() > 0 ==> (result matches Some(value)
            && *value == old(v)@[0]
            && final(v)@ == old(v)@.update(0, *final(value))),
;

pub fn source_vec_deque_pop_front_if<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    predicate: impl FnOnce(&mut T) -> bool,
) -> (result: Option<T>)
    requires
        old(v)@.len() > 0 ==> forall|x: &mut T|
            *x == old(v)@[0] ==> predicate.requires((x,)),
    ensures
        old(v)@.len() == 0 ==> result is None && final(v)@ == old(v)@,
        old(v)@.len() > 0 ==> exists|x: &mut T, take: bool| {
            &&& *x == old(v)@[0]
            &&& predicate.ensures((x,), take)
            &&& (take ==> {
                &&& result == Some(*final(x))
                &&& final(v)@ == old(v)@.subrange(1, old(v)@.len() as int)
            })
            &&& (!take ==> {
                &&& result is None
                &&& final(v)@ == old(v)@.update(0, *final(x))
            })
        },
{
    let first = match v.front_mut() {
        Some(first) => first,
        None => return None,
    };
    if predicate(first) {
        v.pop_front()
    } else {
        None
    }
}

} // verus!

fn main() {}