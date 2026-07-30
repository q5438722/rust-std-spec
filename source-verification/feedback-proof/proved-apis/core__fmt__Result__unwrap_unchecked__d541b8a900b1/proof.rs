#![feature(const_precise_live_drops)]
#![allow(dead_code)]

use core::hint;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub assume_specification<T>[core::mem::forget](value: T);

pub const unsafe fn source_result_unwrap_unchecked<T, E>(
    result: Result<T, E>,
) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
{
    match result {
        Ok(t) => t,
        Err(e) => {
            core::mem::forget(e);
            unsafe { hint::unreachable_unchecked() }
        }
    }
}

} // verus!

fn main() {}