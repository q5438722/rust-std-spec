#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_is_some_and<T, F: FnOnce(T) -> bool>(
    option: Option<T>,
    f: F,
) -> (res: bool)
    requires
        option.is_some() ==> f.requires((option.unwrap(),)),
    ensures
        option.is_none() ==> !res,
        option.is_some() ==> f.ensures((option.unwrap(),), res),
{
    match option {
        None => false,
        Some(x) => f(x),
    }
}

} // verus!

fn main() {}