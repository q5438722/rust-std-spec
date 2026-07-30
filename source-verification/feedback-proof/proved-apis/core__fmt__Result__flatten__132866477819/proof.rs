#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_flatten<T, E>(
    result: Result<Result<T, E>, E>,
) -> (flattened: Result<T, E>)
    ensures
        flattened == match result {
            Result::Ok(inner) => inner,
            Result::Err(error) => Result::Err(error),
        },
{
    match result {
        Result::Ok(inner) => inner,
        Result::Err(e) => Result::Err(e),
    }
}

} // verus!

fn main() {}