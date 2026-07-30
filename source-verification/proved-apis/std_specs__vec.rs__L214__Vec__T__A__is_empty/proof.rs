#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn source_vec_is_empty<T, A: Allocator>(v: &Vec<T, A>) -> (res: bool)
    ensures
        res <==> v@.len() == 0,
{
    let res = v.len() == 0;
    proof {
        vstd::std_specs::vec::axiom_spec_len(v);
    }
    res
}

} // verus!

fn main() {}