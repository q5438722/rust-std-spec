#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::rc::Rc;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

fn source_rc_unwrap_or_clone<T: Clone, A: Allocator>(
    this: Rc<T, A>,
) -> (result: T)
    ensures
        cloned::<T>(*this, result),
{
    match Rc::try_unwrap(this) {
        Ok(value) => {
            assert(cloned::<T>(*this, value));
            value
        }
        Err(rc) => {
            let value = (*rc).clone();
            assert(cloned::<T>(*rc, value));
            assert(*rc == *this);
            assert(cloned::<T>(*this, value));
            value
        }
    }
}

} // verus!

fn main() {}