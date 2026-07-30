#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_map_or<T, E, U, F>(
    result: Result<T, E>,
    default: U,
    f: F,
) -> (value: U)
where
    F: FnOnce(T) -> U,
    requires
        result is Ok ==> f.requires((result->Ok_0,)),
    ensures
        result is Ok ==> f.ensures((result->Ok_0,), value),
        result is Err ==> value == default,
{
    match result {
        Ok(t) => f(t),
        Err(_) => default,
    }
}

} // verus!

fn main() {}