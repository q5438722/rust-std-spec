#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub fn source_option_and<T, U>(
    option: Option<T>,
    optb: Option<U>,
) -> (res: Option<U>)
    ensures
        option.is_none() ==> res.is_none(),
        option.is_some() ==> res == optb,
    no_unwind
{
    match option {
        Some(_) => optb,
        None => None,
    }
}

} // verus!

fn main() {}