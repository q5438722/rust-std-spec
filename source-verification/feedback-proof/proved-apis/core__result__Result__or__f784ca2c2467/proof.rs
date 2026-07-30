#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_or<T, E, F>(
    result: Result<T, E>,
    res: Result<T, F>,
) -> (output: Result<T, F>)
    ensures
        result is Ok ==> output == Result::<T, F>::Ok(result->Ok_0),
        result is Err ==> output == res,
    no_unwind
{
    match result {
        Ok(v) => Ok(v),
        Err(_) => res,
    }
}

} // verus!

fn main() {}