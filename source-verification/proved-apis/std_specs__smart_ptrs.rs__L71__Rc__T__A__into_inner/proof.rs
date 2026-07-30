#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::rc::Rc;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

fn source_rc_into_inner<T, A: Allocator>(v: Rc<T, A>) -> (result: Option<T>)
    ensures
        result matches Some(t) ==> t == *v,
{
    Rc::try_unwrap(v).ok()
}

} // verus!

fn main() {}