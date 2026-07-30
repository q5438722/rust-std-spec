#![allow(dead_code)]

use vstd::prelude::*;
use core::result::Result;

verus! {

pub fn source_result_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> (value: T)
    ensures
        value == match result {
            Result::Ok(contained) => contained,
            Result::Err(_) => default,
        },
{
    match result {
        Result::Ok(t) => t,
        Result::Err(_) => default,
    }
}

} // verus!

fn main() {}