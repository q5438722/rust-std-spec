#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_inspect<T, E, F: FnOnce(&T)>(
    result: Result<T, E>,
    f: F,
) -> (inspected: Result<T, E>)
    requires
        result is Ok ==> f.requires((&(result->Ok_0),)),
    ensures
        inspected == result,
        result is Ok ==> f.ensures((&(result->Ok_0),), ()),
{
    if let Ok(ref t) = result {
        f(t);
    }

    result
}

} // verus!

fn main() {}