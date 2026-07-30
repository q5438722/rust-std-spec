#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_or_else<T, E, F, O>(
    result: Result<T, E>,
    op: O,
) -> (ret: Result<T, F>)
where
    O: FnOnce(E) -> Result<T, F>,
    requires
        result is Err ==> op.requires((result->Err_0,)),
    ensures
        result is Ok ==> ret == Result::<T, F>::Ok(result->Ok_0),
        result is Err ==> op.ensures((result->Err_0,), ret),
{
    match result {
        Ok(t) => Ok(t),
        Err(e) => op(e),
    }
}

} // verus!

fn main() {}