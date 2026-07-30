#![allow(dead_code)]
#![allow(unused_imports)]

use core::fmt::Debug;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn source_result_expect<T, E: Debug>(
    result: Result<T, E>,
    msg: &str,
) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
{
    match result {
        Ok(t) => t,
        Err(e) => {
            assert(false);
            vstd::vpanic!("{}: {:?}", msg, &e)
        },
    }
}

} // verus!

fn main() {}