#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;

verus! {

fn source_result_or_else<T, E, F, O: FnOnce(E) -> Result<T, F>>(
    result: Result<T, E>,
    op: O,
) -> (res: Result<T, F>)
    requires
        result is Err ==> op.requires((result->Err_0,)),
    ensures
        result is Ok ==> res == Result::<T, F>::Ok(result->Ok_0),
        result is Err ==> op.ensures((result->Err_0,), res),
{
    match result {
        Ok(t) => Ok(t),
        Err(e) => op(e),
    }
}

} // verus!

fn main() {}