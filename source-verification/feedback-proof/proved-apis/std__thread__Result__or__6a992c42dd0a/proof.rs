#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_or<T, E, F>(
    result: Result<T, E>,
    res: Result<T, F>,
) -> (ret: Result<T, F>)
    ensures
        result is Ok ==> ret == Result::<T, F>::Ok(result->Ok_0),
        result is Err ==> ret == res,
{
    match result {
        Ok(v) => Ok(v),
        Err(_) => res,
    }
}

} // verus!

fn main() {}