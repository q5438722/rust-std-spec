#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_flatten<T>(
    option: Option<Option<T>>,
) -> (res: Option<T>)
    ensures
        res == match option {
            Option::Some(inner) => inner,
            Option::None => Option::None,
        },
    no_unwind
{
    match option {
        Option::Some(inner) => inner,
        Option::None => Option::None,
    }
}

} // verus!

fn main() {}