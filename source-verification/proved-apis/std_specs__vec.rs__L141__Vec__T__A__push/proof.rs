#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification<T, A: Allocator>[ Vec::<T, A>::push_mut ](
    vec: &mut Vec<T, A>,
    value: T,
) -> (result: &mut T)
    ensures
        *result == value,
        final(vec)@ == old(vec)@.push(*final(result)),
;

fn source_vec_push<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    value: T,
)
    ensures
        final(vec)@ == old(vec)@.push(value),
{
    let _ = vec.push_mut(value);
}

} // verus!

fn main() {}