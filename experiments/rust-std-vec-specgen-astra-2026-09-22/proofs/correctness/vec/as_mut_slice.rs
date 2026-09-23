#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn as_mut_slice<'a, T, A: Allocator>(vec: &'a mut Vec<T, A>) -> (result: &'a mut [T])
    ensures
        result@ == old(vec)@,
        final(result)@ == final(vec)@,
{
    vec
}

}
