#![allow(dead_code)]

use core::hint;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub unsafe fn source_result_unwrap_err_unchecked<T, E>(
    result: Result<T, E>,
) -> (e: E)
    requires
        result is Err,
    ensures
        e == result->Err_0,
{
    match result {
        Ok(_) => unsafe { hint::unreachable_unchecked() },
        Err(e) => e,
    }
}

} // verus!

fn main() {}