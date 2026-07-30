#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_copied<'a, T: Copy, E>(
    result: Result<&'a T, E>,
) -> (res: Result<T, E>)
    ensures
        res == (match result {
            Result::Ok(value) => Result::Ok(*value),
            Result::Err(error) => Result::Err(error),
        }),
    no_unwind
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