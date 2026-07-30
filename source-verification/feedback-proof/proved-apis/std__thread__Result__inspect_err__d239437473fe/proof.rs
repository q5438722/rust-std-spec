#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_inspect_err<T, E, F: FnOnce(&E)>(
    result: Result<T, E>,
    f: F,
) -> (inspected: Result<T, E>)
    requires
        result is Err ==> f.requires((&result->Err_0,)),
    ensures
        inspected == result,
        result is Err ==> f.ensures((&result->Err_0,), ()),
{
    if let Err(ref e) = result {
        f(e);
    }

    result
}

} // verus!

fn main() {}