#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_and<T, E, U>(
    result: Result<T, E>,
    res: Result<U, E>,
) -> (and_result: Result<U, E>)
    ensures
        result is Ok ==> and_result == res,
        result is Err ==> and_result == Result::<U, E>::Err(result->Err_0),
    no_unwind
{
    match result {
        Ok(_) => res,
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}