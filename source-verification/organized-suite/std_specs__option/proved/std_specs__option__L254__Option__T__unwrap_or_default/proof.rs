#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_unwrap_or_default_proof<T: core::default::Default>(
    option: Option<T>,
) -> (res: T)
    ensures
        option.is_some() ==> res == option.unwrap(),
        option.is_none() ==> T::default.ensures((), res),
{
    match option {
        Some(x) => x,
        None => T::default(),
    }
}

} // verus!

fn main() {}