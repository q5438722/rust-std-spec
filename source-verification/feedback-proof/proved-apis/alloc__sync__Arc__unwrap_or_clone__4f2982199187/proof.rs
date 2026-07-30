#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::sync::Arc;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::smart_ptrs::*;

verus! {

pub assume_specification<T, A: Allocator>[ Arc::<T, A>::try_unwrap ](
    this: Arc<T, A>,
) -> (result: Result<T, Arc<T, A>>)
    ensures
        match result {
            Ok(value) => value == *this,
            Err(returned) => returned == this,
        },
;

fn source_arc_unwrap_or_clone<T: Clone, A: Allocator>(
    this: Arc<T, A>,
) -> (result: T)
    ensures
        cloned::<T>(*this, result),
{
    match Arc::try_unwrap(this) {
        Ok(value) => {
            assert(cloned::<T>(*this, value));
            value
        }
        Err(arc) => {
            let value = (*arc).clone();
            assert(cloned::<T>(*arc, value));
            assert(*arc == *this);
            assert(cloned::<T>(*this, value));
            value
        }
    }
}

} // verus!

fn main() {}