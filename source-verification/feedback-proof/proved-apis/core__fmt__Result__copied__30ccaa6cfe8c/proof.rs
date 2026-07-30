#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_copied<T: Copy, E>(
    result: Result<&T, E>,
) -> (copied: Result<T, E>)
    ensures
        copied == match result {
            Result::Ok(value) => Result::Ok(*value),
            Result::Err(error) => Result::Err(error),
        },
{
    match result {
        Result::Ok(value) => {
            let v = *value;
            Result::Ok(v)
        },
        Result::Err(e) => Result::Err(e),
    }
}

} // verus!

fn main() {}