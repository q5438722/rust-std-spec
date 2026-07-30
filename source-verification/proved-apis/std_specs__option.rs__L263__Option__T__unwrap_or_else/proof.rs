#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_unwrap_or_else<T, F: FnOnce() -> T>(
    option: Option<T>,
    f: F,
) -> (res: T)
    requires
        option.is_none() ==> f.requires(()),
    ensures
        option.is_some() ==> res == option.unwrap(),
        option.is_none() ==> f.ensures((), res),
{
    match option {
        Some(x) => x,
        None => f(),
    }
}

} // verus!

fn main() {}