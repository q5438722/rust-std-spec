#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::insert_mut ](
    vec: &mut Vec<T, A>,
    index: usize,
    element: T,
) -> (result: &mut T)
    requires
        index <= old(vec).len(),
    ensures
        *result == element,
        final(vec)@ == old(vec)@.insert(index as int, *final(result)),
;

fn source_vec_insert<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    index: usize,
    element: T,
)
    requires
        index <= old(vec).len(),
    ensures
        final(vec)@ == old(vec)@.insert(index as int, element),
{
    let _ = vec.insert_mut(index, element);
}

} // verus!

fn main() {}