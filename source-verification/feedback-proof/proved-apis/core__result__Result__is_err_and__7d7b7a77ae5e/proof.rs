#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_is_err_and<T, E, F: FnOnce(E) -> bool>(
    result: Result<T, E>,
    f: F,
) -> (matches_err: bool)
    requires
        result is Err ==> f.requires((result->Err_0,)),
    ensures
        result is Ok ==> !matches_err,
        result is Err ==> f.ensures((result->Err_0,), matches_err),
{
    match result {
        Ok(_) => false,
        Err(e) => f(e),
    }
}

} // verus!

fn main() {}