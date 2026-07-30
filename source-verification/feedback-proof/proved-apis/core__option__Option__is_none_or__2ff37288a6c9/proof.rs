#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_is_none_or<T, F: FnOnce(T) -> bool>(
    option: Option<T>,
    f: F,
) -> (res: bool)
    requires
        option.is_some() ==> f.requires((option.unwrap(),)),
    ensures
        option.is_none() ==> res,
        option.is_some() ==> f.ensures((option.unwrap(),), res),
{
    match option {
        None => true,
        Some(x) => f(x),
    }
}

} // verus!

fn main() {}