#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::TryReserveError;
use alloc::vec::Vec;
use core::alloc::Allocator;
use core::mem::size_of;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::std_specs::vec::*;

verus! {

fn min_non_zero_cap(size: usize) -> usize {
    if size == 1 {
        8
    } else if size <= 1024 {
        4
    } else {
        1
    }
}

fn source_vec_try_reserve<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(vec)@ == old(vec)@,
{
    let len = vec.len();
    let capacity = vec.capacity();

    // Public-API desugaring of RawVec::try_reserve's needs-to-grow branch.
    if additional > capacity.wrapping_sub(len) {
        // The exact path constructs the same private CapacityOverflow error.
        if size_of::<T>() == 0 {
            return vec.try_reserve_exact(additional);
        }

        let required_capacity = match len.checked_add(additional) {
            Some(required_capacity) => required_capacity,
            None => return vec.try_reserve_exact(additional),
        };

        let doubled = capacity.wrapping_mul(2);
        let capacity =
            if doubled > required_capacity { doubled } else { required_capacity };
        let minimum = min_non_zero_cap(size_of::<T>());
        let capacity = if minimum > capacity { minimum } else { capacity };

        // RawVec::grow_exact now receives the same capacity as grow_amortized.
        vec.try_reserve_exact(capacity.wrapping_sub(len))
    } else {
        Ok(())
    }
}

} // verus!

fn main() {}