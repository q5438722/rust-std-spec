#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_and_then<T, U, F: FnOnce(T) -> Option<U>>(
    option: Option<T>,
    f: F,
) -> (res: Option<U>)
    requires
        option.is_some() ==> f.requires((option.unwrap(),)),
    ensures
        option.is_none() ==> res.is_none(),
        option.is_some() ==> f.ensures((option.unwrap(),), res),
{
    match option {
        Some(x) => f(x),
        None => None,
    }
}

} // verus!

fn main() {}