#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn result_map_proof<T, E, U, F: FnOnce(T) -> U>(
    result: Result<T, E>,
    op: F,
) -> (mapped_result: Result<U, E>)
    requires
        result.is_ok() ==> op.requires((result->Ok_0,)),
    ensures
        result.is_ok() ==> mapped_result.is_ok() && op.ensures(
            (result->Ok_0,),
            mapped_result->Ok_0,
        ),
        result.is_err() ==> mapped_result == Result::<U, E>::Err(result->Err_0),
{
    match result {
        Ok(t) => Ok(op(t)),
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}