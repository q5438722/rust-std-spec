#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_flatten<T, E>(
    result: Result<Result<T, E>, E>,
) -> (flattened: Result<T, E>)
    ensures
        result is Ok ==> flattened == result->Ok_0,
        result is Err ==> flattened is Err,
        result is Err ==> flattened->Err_0 == result->Err_0,
    no_unwind
{
    match result {
        Ok(inner) => inner,
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}