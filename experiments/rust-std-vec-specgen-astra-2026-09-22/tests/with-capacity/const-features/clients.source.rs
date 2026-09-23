#![feature(allocator_api, const_heap, const_trait_impl)]

use vstd::prelude::*;

#[path = "../specs/vec/with_capacity.rs"]
mod source;

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
    source::with_capacity(capacity)
}

}
