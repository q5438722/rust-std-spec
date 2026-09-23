#![feature(allocator_api, const_heap, const_trait_impl)]

use vstd::prelude::*;

#[path = "../specs/with_capacity_candidate.rs"]
mod candidate;

verus! {

pub fn official<T>(capacity: usize) -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    Vec::<T>::with_capacity(capacity)
}

pub fn source<T>(capacity: usize) -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
{
    candidate::vec::with_capacity::with_capacity(capacity)
}

}
