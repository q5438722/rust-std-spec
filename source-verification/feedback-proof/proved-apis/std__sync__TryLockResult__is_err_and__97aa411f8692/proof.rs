#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_try_lock_result_is_err_and<T, E, F: FnOnce(E) -> bool>(
    result: Result<T, E>,
    f: F,
) -> (ret: bool)
    requires
        result is Err ==> f.requires((result->Err_0,)),
    ensures
        result is Ok ==> !ret,
        result is Err ==> f.ensures((result->Err_0,), ret),
{
    match result {
        Ok(_) => false,
        Err(e) => f(e),
    }
}

} // verus!

fn main() {}