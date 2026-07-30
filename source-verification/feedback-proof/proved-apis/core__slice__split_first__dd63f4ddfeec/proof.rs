#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_core_slice_split_first<T>(
    slice: &[T],
) -> (ret: core::option::Option<(&T, &[T])>)
    ensures
        match ret {
            None => slice@.len() == 0,
            Some((first, rest)) => {
                &&& slice@.len() > 0
                &&& *first == slice@[0]
                &&& rest@ == slice@.subrange(1, slice@.len() as int)
            },
        },
{
    if slice.len() >= 1 {
        let first = &slice[0];
        let tail = &slice[1..slice.len()];
        Some((first, tail))
    } else {
        None
    }
}

} // verus!

fn main() {}