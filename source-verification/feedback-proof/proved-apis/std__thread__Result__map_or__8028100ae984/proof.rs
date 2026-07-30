#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_thread_result_map_or<T, E, U, F>(
    result: Result<T, E>,
    default: U,
    f: F,
) -> (ret: U)
where
    F: FnOnce(T) -> U,
    requires
        result is Ok ==> f.requires((result->Ok_0,)),
        result is Ok ==> forall|u1: U, u2: U|
            #![trigger f.ensures((result->Ok_0,), u1),
                       f.ensures((result->Ok_0,), u2)]
            f.ensures((result->Ok_0,), u1)
                && f.ensures((result->Ok_0,), u2)
                ==> u1 == u2,
    ensures
        result is Ok ==> f.ensures((result->Ok_0,), ret),
        result is Err ==> ret == default,
{
    match result {
        Ok(t) => f(t),
        Err(_) => default,
    }
}

} // verus!

fn main() {}