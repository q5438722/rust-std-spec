#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::vec::Vec;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vec::*;

verus! {

fn slice_length<T>(slice: &[T]) -> (len: usize)
    ensures
        len == slice@.len(),
{
    let len = <[T]>::len(slice);
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    len
}

fn source_vec_len<T, A: Allocator>(vec: &Vec<T, A>) -> (len: usize)
    ensures
        len == spec_vec_len(vec),
{
    // `as_slice` exposes the source's private `self.len` field as slice metadata.
    let slice = vec.as_slice();
    let len = slice_length(slice);

    proof {
        vstd::std_specs::vec::axiom_spec_len(vec);
    }

    len
}

} // verus!

fn main() {}