#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> (value: T)
    ensures
        result is Ok ==> value == result->Ok_0,
        result is Err ==> value == default,
{
    match result {
        Ok(t) => t,
        Err(_) => default,
    }
}

} // verus!

fn main() {}