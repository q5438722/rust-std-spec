#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub fn source_split_last<T>(slice: &[T]) -> (ret: core::option::Option<(&T, &[T])>)
    ensures
        match ret {
            core::option::Option::None => slice@.len() == 0,
            core::option::Option::Some((last, init)) => {
                &&& slice@.len() > 0
                &&& *last == slice@[slice@.len() as int - 1]
                &&& init@ == slice@.subrange(0, slice@.len() as int - 1)
            },
        },
{
    let len = slice.len();
    if len >= 1 {
        let init = &slice[0..len - 1];
        let last = &slice[len - 1];
        Some((last, init))
    } else {
        None
    }
}

} // verus!

fn main() {}