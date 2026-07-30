#![allow(dead_code)]
#![allow(unused_imports)]

use core::fmt::Debug;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn source_result_unwrap_err<T: Debug, E>(result: Result<T, E>) -> (e: E)
    requires
        result is Err,
    ensures
        e == result->Err_0,
{
    match result {
        Ok(t) => {
            assert(false);
            vstd::vpanic!(
                "called `Result::unwrap_err()` on an `Ok` value: {:?}",
                &t
            )
        }
        Err(e) => e,
    }
}

} // verus!

fn main() {}