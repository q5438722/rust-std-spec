#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

#[verifier::inline]
pub open spec fn spec_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> T {
    match result {
        Result::Ok(t) => t,
        Result::Err(_) => default,
    }
}

pub fn source_result_unwrap_or<T, E>(
    result: Result<T, E>,
    default: T,
) -> (t: T)
    ensures
        match result {
            Result::Ok(value) => t == value,
            Result::Err(_) => t == default,
        },
{
    match result {
        Result::Ok(t) => t,
        Result::Err(_) => default,
    }
}

} // verus!

fn main() {}