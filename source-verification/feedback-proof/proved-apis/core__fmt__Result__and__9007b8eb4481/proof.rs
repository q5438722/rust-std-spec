#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_and<T, E, U>(
    result: Result<T, E>,
    res: Result<U, E>,
) -> (out: Result<U, E>)
    ensures
        result is Ok ==> out == res,
        result is Err ==> out == Result::<U, E>::Err(result->Err_0),
{
    match result {
        Ok(_) => res,
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}