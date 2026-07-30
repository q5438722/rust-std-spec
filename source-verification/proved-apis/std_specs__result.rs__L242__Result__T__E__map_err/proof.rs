#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn source_result_map_err<T, E, F, O: FnOnce(E) -> F>(
    result: Result<T, E>,
    op: O,
) -> (mapped_result: Result<T, F>)
    requires
        result.is_err() ==> op.requires((result->Err_0,)),
    ensures
        result.is_err() ==> mapped_result.is_err() && op.ensures(
            (result->Err_0,),
            mapped_result->Err_0,
        ),
        result.is_ok() ==> mapped_result == Result::<T, F>::Ok(result->Ok_0),
{
    match result {
        Ok(t) => Ok(t),
        Err(e) => Err(op(e)),
    }
}

} // verus!

fn main() {}