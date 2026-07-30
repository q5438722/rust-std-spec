#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> (res: T)
    ensures
        result is Ok ==> res == result->Ok_0,
        result is Err ==> res == default,
{
    match result {
        Ok(t) => t,
        Err(_) => default,
    }
}

} // verus!

fn main() {}