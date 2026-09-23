#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn as_ref_vec<'a, T, A: Allocator>(vec: &'a Vec<T, A>) -> (result: &'a Vec<T, A>)
    ensures
        result == vec,
        result@ == vec@,
{
    vec
}

}
