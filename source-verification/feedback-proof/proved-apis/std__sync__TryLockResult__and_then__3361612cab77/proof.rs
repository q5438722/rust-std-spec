#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_try_lock_result_and_then<T, E, U, F>(
    result: Result<T, E>,
    op: F,
) -> (ret: Result<U, E>)
where
    F: FnOnce(T) -> Result<U, E>,
    requires
        result is Ok ==> op.requires((result->Ok_0,)),
    ensures
        result is Ok ==> op.ensures((result->Ok_0,), ret),
        result is Err ==> ret == Result::<U, E>::Err(result->Err_0),
{
    match result {
        Ok(t) => op(t),
        Err(e) => Err(e),
    }
}

} // verus!

fn main() {}