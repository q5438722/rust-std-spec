#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_copied<'a, T: Copy>(
    opt: Option<&'a T>,
) -> (res: Option<T>)
    ensures
        res == (match opt {
            Some(v) => Some(*v),
            None => None,
        }),
    no_unwind
{
    match opt {
        Some(value) => {
            let v = *value;
            Some(v)
        },
        None => None,
    }
}

} // verus!

fn main() {}