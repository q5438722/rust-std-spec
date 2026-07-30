#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use core::clone::Clone;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

pub assume_specification<T, A: Allocator>[
    VecDeque::<T, A>::with_capacity_in
](
    capacity: usize,
    alloc: A,
) -> (result: VecDeque<T, A>)
    ensures
        result@ == Seq::<T>::empty(),
;

pub assume_specification<T, A: Allocator>[
    VecDeque::<T, A>::allocator
](
    deque: &VecDeque<T, A>,
) -> (result: &A);

fn source_vec_deque_clone<T: Clone, A: Allocator + Clone>(
    v: &VecDeque<T, A>,
) -> (res: VecDeque<T, A>)
    ensures
        res.len() == v.len(),
        forall|i| #![all_triggers] 0 <= i < v.len() ==> cloned::<T>(v[i], res[i]),
        vec_dequeue_clone_trigger(*v, res),
        v@ =~= res@ ==> v@ == res@,
{
    let mut deq = VecDeque::with_capacity_in(v.len(), v.allocator().clone());

    // This loop desugars `deq.extend(v.iter().cloned())` into its ordered
    // clone-and-append behavior without relying on the target clone contract.
    let mut i: usize = 0;
    while i < v.len()
        invariant
            i <= v@.len(),
            deq@.len() == i,
            forall|j: int| #![all_triggers]
                0 <= j < i ==> cloned::<T>(v@[j], deq@[j]),
        decreases v@.len() - i,
    {
        let element = v[i].clone();
        assert(cloned::<T>(v@[i as int], element));
        deq.push_back(element);
        i += 1;
    }

    assert(vec_dequeue_clone_trigger(*v, deq));
    assert(v@ =~= deq@ ==> v@ == deq@);
    deq
}

} // verus!

fn main() {}