#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_unwrap_or_else<T, E, F>(
    result: Result<T, E>,
    op: F,
) -> (res: T)
    where
        F: FnOnce(E) -> T,
    requires
        result is Err ==> op.requires((result->Err_0,)),
    ensures
        result is Ok ==> res == result->Ok_0,
        result is Err ==> op.ensures((result->Err_0,), res),
{
    match result {
        Ok(t) => t,
        Err(e) => op(e),
    }
}

} // verus!

fn main() {}