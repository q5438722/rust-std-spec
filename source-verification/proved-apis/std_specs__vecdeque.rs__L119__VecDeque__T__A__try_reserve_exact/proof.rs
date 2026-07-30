#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::{TryReserveError, VecDeque};
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn source_vecdeque_try_reserve_exact<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
{
    let len = v.len();
    let new_cap = match len.checked_add(additional) {
        Some(new_cap) => new_cap,
        // Reproduce the private CapacityOverflow path through the sibling API.
        None => return v.try_reserve(additional),
    };
    let old_cap = v.capacity();

    if new_cap > old_cap {
        // Abstract private RawVec growth and relocation at the view level.
        match v.try_reserve(additional) {
            Ok(()) => {}
            Err(error) => return Err(error),
        }
    }
    Ok(())
}

} // verus!

fn main() {}