#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::alloc::Allocator;
use alloc::vec::Vec;
use vstd::prelude::*;
use vstd::std_specs::capacity::*;

verus! {

pub assume_specification[std::process::abort]() -> !;

fn source_vec_reserve_exact<T, A: Allocator>(
    v: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len() + additional as nat,
{
    match v.try_reserve_exact(additional) {
        Ok(()) => {
            assert(v.spec_capacity() >= v@.len() + additional as nat);
        }
        Err(_) => std::process::abort(),
    }
}

} // verus!

fn main() {}