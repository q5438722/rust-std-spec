#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_try_lock_result_and<T, E, U>(
    result: Result<T, E>,
    res: Result<U, E>,
) -> (ret: Result<U, E>)
    ensures
        result is Ok ==> ret == res,
        result is Err ==> ret == Result::<U, E>::Err(result->Err_0),
{
    match result {
        Ok(_) => res,
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}