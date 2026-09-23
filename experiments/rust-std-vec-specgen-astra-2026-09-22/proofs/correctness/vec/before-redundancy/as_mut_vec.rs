#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn as_mut_vec<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>) -> (result: &'a mut Vec<T, A>)
    ensures
        *result == *old(vec),
        result@ == old(vec)@,
        *final(result) == *final(vec),
        final(result)@ == final(vec)@,
{
    vec
}

}
