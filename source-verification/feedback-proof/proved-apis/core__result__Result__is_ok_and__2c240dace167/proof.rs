#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_is_ok_and<T, E, F: FnOnce(T) -> bool>(
    result: Result<T, E>,
    f: F,
) -> (matches_ok: bool)
    requires
        result is Ok ==> f.requires((result->Ok_0,)),
    ensures
        result is Err ==> !matches_ok,
        result is Ok ==> f.ensures((result->Ok_0,), matches_ok),
{
    match result {
        Err(_) => false,
        Ok(x) => f(x),
    }
}

} // verus!

fn main() {}