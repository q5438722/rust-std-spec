#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_or_else<T, E, F, O>(
    result: Result<T, E>,
    op: O,
) -> (res: Result<T, F>)
where
    O: FnOnce(E) -> Result<T, F>,
    requires
        result is Err ==> op.requires((result->Err_0,)),
        result is Err ==> forall|res1: Result<T, F>, res2: Result<T, F>|
            #![trigger op.ensures((result->Err_0,), res1),
                       op.ensures((result->Err_0,), res2)]
            op.ensures((result->Err_0,), res1)
                && op.ensures((result->Err_0,), res2)
                ==> res1 == res2,
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