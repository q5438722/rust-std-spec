#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_zip<T, U>(
    option: Option<T>,
    other: Option<U>,
) -> (res: Option<(T, U)>)
    ensures
        res == match (option, other) {
            (Some(a), Some(b)) => Some((a, b)),
            _ => None,
        },
{
    match (option, other) {
        (Some(a), Some(b)) => Some((a, b)),
        _ => None,
    }
}

} // verus!

fn main() {}