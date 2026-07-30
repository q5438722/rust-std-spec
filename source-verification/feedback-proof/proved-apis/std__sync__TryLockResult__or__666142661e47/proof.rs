#![allow(dead_code)]

use vstd::prelude::*;
use core::result::Result;

verus! {

pub fn source_try_lock_result_or<T, E, F>(
    result: Result<T, E>,
    res: Result<T, F>,
) -> (combined: Result<T, F>)
    ensures
        result is Ok ==> combined == Result::<T, F>::Ok(result->Ok_0),
        result is Err ==> combined == res,
{
    match result {
        Ok(v) => Ok(v),
        Err(_) => res,
    }
}

} // verus!

fn main() {}