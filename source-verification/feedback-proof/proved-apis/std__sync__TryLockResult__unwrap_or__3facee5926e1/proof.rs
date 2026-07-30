#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> (res: T)
    ensures
        res == (match result {
            Result::Ok(value) => value,
            Result::Err(_) => default,
        }),
{
    match result {
        Result::Ok(t) => t,
        Result::Err(_) => default,
    }
}

} // verus!

fn main() {}