#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_unzip<T, U>(
    option: Option<(T, U)>,
) -> (res: (Option<T>, Option<U>))
    ensures
        res == match option {
            Some((a, b)) => (Some(a), Some(b)),
            None => (None, None),
        },
    no_unwind
{
    match option {
        Some((a, b)) => (Some(a), Some(b)),
        None => (None, None),
    }
}

} // verus!

fn main() {}