#![feature(allocator_api)]
#![allow(dead_code)]

extern crate alloc;

use alloc::collections::VecDeque;
use core::alloc::Allocator;
use vstd::prelude::*;

verus! {

fn source_swap_remove_front<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    index: usize,
) -> (result: Option<T>)
    ensures
        match result {
            Some(value) => {
                &&& index < old(v)@.len()
                &&& value == old(v)@[index as int]
                &&& final(v)@ == old(v)@.update(index as int, old(v)@[0]).subrange(
                    1,
                    old(v)@.len() as int,
                )
            },
            None => {
                &&& old(v)@.len() <= index
                &&& final(v)@ == old(v)@
            },
        },
{
    let length = v.len();
    if index < length && index != 0 {
        v.swap(index, 0);
    } else if index >= length {
        return None;
    }
    v.pop_front()
}

fn source_swap_remove_back<T, A: Allocator>(
    v: &mut VecDeque<T, A>,
    index: usize,
) -> (result: Option<T>)
    ensures
        match result {
            Some(value) => {
                &&& index < old(v)@.len()
                &&& value == old(v)@[index as int]
                &&& final(v)@ == old(v)@.update(index as int, old(v)@.last()).drop_last()
            },
            None => {
                &&& old(v)@.len() <= index
                &&& final(v)@ == old(v)@
            },
        },
{
    let length = v.len();
    if length > 0 && index < length - 1 {
        v.swap(index, length - 1);
    } else if index >= length {
        return None;
    }
    v.pop_back()
}

} // verus!

fn main() {}
