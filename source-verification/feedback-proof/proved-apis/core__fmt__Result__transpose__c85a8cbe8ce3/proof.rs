#![allow(dead_code)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_transpose<T, E>(
    result: Result<Option<T>, E>,
) -> (out: Option<Result<T, E>>)
    ensures
        out == match result {
            Result::Ok(Option::Some(value)) => Option::Some(Result::Ok(value)),
            Result::Ok(Option::None) => Option::None,
            Result::Err(error) => Option::Some(Result::Err(error)),
        },
{
    match result {
        Ok(Some(x)) => Some(Ok(x)),
        Ok(None) => None,
        Err(e) => Some(Err(e)),
    }
}

} // verus!

fn main() {}