#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

pub assume_specification[std::process::abort]() -> !;

fn source_vec_reserve<T, A: Allocator>(
    vec: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(vec)@ == old(vec)@,
{
    match vec.try_reserve(additional) {
        Ok(()) => {}
        Err(_) => std::process::abort(),
    }
}

} // verus!

fn main() {}