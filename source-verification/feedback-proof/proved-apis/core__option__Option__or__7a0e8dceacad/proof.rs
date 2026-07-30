#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub fn source_option_or<T>(
    option: Option<T>,
    optb: Option<T>,
) -> (res: Option<T>)
    ensures
        option.is_some() ==> res == option,
        option.is_none() ==> res == optb,
    no_unwind
{
    match option {
        x @ Some(_) => x,
        None => optb,
    }
}

} // verus!

fn main() {}