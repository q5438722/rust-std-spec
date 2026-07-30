#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::vec_deque::VecDeque;
use core::alloc::Allocator;
use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[VecDeque::<T, A>::back_mut](
    v: &mut VecDeque<T, A>,
) -> (result: Option<&mut T>)
    ensures
        old(v)@.len() == 0 ==> result is None && final(v)@ == old(v)@,
        old(v)@.len() > 0 ==> (result matches Some(value)
            && *value == old(v)@[old(v)@.len() as int - 1]
            && final(v)@ == old(v)@.update(
                old(v)@.len() as int - 1,
                *final(value),
            )),
;

pub fn source_vec_deque_pop_back_if<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    predicate: impl FnOnce(&mut T) -> bool,
) -> (result: Option<T>)
    requires
        old(v)@.len() > 0 ==> forall|x: &mut T| #![auto]
            *x == old(v)@[old(v)@.len() as int - 1] ==> predicate.requires((x,)),
    ensures
        old(v)@.len() == 0 ==> result is None && final(v)@ == old(v)@,
        old(v)@.len() > 0 ==> exists|x: &mut T, take: bool| #![auto] {
            &&& *x == old(v)@[old(v)@.len() as int - 1]
            &&& predicate.ensures((x,), take)
            &&& (take ==> {
                &&& result == Some(*final(x))
                &&& final(v)@ == old(v)@.subrange(0, old(v)@.len() as int - 1)
            })
            &&& (!take ==> {
                &&& result is None
                &&& final(v)@ == old(v)@.update(
                    old(v)@.len() as int - 1,
                    *final(x),
                )
            })
        },
{
    let last = match v.back_mut() {
        Some(last) => last,
        None => return None,
    };
    if predicate(last) {
        v.pop_back()
    } else {
        None
    }
}

} // verus!

fn main() {}