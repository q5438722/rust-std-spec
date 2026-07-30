#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_map_or_else<T, E, U, D, F>(
    result: Result<T, E>,
    default: D,
    f: F,
) -> (res: U)
where
    D: FnOnce(E) -> U,
    F: FnOnce(T) -> U,
    requires
        result is Err ==> default.requires((result->Err_0,)),
        result is Ok ==> f.requires((result->Ok_0,)),
        result is Err ==> forall|u1: U, u2: U|
            #![trigger default.ensures((result->Err_0,), u1),
                       default.ensures((result->Err_0,), u2)]
            default.ensures((result->Err_0,), u1)
                && default.ensures((result->Err_0,), u2)
                ==> u1 == u2,
        result is Ok ==> forall|u1: U, u2: U|
            #![trigger f.ensures((result->Ok_0,), u1),
                       f.ensures((result->Ok_0,), u2)]
            f.ensures((result->Ok_0,), u1)
                && f.ensures((result->Ok_0,), u2)
                ==> u1 == u2,
    ensures
        result is Err ==> default.ensures((result->Err_0,), res),
        result is Ok ==> f.ensures((result->Ok_0,), res),
{
    match result {
        Ok(t) => f(t),
        Err(e) => default(e),
    }
}

} // verus!

fn main() {}