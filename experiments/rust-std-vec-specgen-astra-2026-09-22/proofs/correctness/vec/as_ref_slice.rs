#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn as_ref_slice<'a, T, A: Allocator>(vec: &'a Vec<T, A>) -> (result: &'a [T])
    ensures
        result@ == vec@,
{
    vec
}

}
