#![allow(dead_code)]

use core::hint;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub unsafe fn source_thread_result_unwrap_err_unchecked<T, E>(
    result: Result<T, E>,
) -> (error: E)
    requires
        result is Err,
    ensures
        error == result->Err_0,
{
    match result {
        Ok(_) => unsafe { hint::unreachable_unchecked() },
        Err(e) => e,
    }
}

} // verus!

fn main() {}