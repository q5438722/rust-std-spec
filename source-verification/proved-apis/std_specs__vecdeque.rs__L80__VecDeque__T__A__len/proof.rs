#![feature(allocator_api)]
#![allow(dead_code)]
#![allow(unused_imports)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;
use vstd::std_specs::vecdeque::*;

verus! {

fn slice_len<T>(slice: &[T]) -> (len: usize)
    ensures
        len == slice@.len(),
{
    let len = <[T]>::len(slice);
    proof {
        vstd::slice::axiom_spec_len(slice);
    }
    len
}

fn source_vec_dequeue_len<T, A: Allocator>(v: &VecDeque<T, A>) -> (len: usize)
    ensures
        len == spec_vec_dequeue_len(v),
{
    // `as_slices` exposes the private stored count as the total slice metadata.
    let (front, back) = v.as_slices();
    let front_len = slice_len(front);
    let back_len = slice_len(back);

    proof {
        axiom_spec_len(v);
        assert((front@ + back@).len() == front@.len() + back@.len());
    }

    front_len + back_len
}

} // verus!

fn main() {}