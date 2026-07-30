#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_ok_or_proof<T, E>(
    option: Option<T>,
    err: E,
) -> (res: Result<T, E>)
    ensures
        res == spec_ok_or(option, err),
{
    match option {
        Some(v) => Ok(v),
        None => Err(err),
    }
}

} // verus!

fn main() {}