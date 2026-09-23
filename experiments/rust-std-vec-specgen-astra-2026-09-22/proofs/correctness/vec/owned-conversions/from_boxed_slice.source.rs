#![feature(allocator_api)]

use std::alloc::Allocator;
use vstd::prelude::*;

verus! {

pub fn from_boxed_slice<T, A: Allocator>(s: Box<[T], A>) -> (result: Vec<T, A>)
    ensures
        result@ == s@,
{
    s.into_vec()
}

}
