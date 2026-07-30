#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_unwrap_or_default<T: core::default::Default, E>(
    result: Result<T, E>,
) -> (res: T)
    ensures
        result is Ok ==> res == result->Ok_0,
        result is Err ==> T::default.ensures((), res),
{
    match result {
        Ok(x) => x,
        Err(_) => Default::default(),
    }
}

} // verus!

fn main() {}