#![allow(dead_code)]

use core::marker::Copy;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_lock_result_copied<'a, T: Copy, E>(
    result: Result<&'a T, E>,
) -> (res: Result<T, E>)
    ensures
        result is Ok ==> res == Result::<T, E>::Ok(*(result->Ok_0)),
        result is Err ==> res == Result::<T, E>::Err(result->Err_0),
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