#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn source_result_is_ok<T, E>(r: &Result<T, E>) -> (b: bool)
    ensures
        b == is_ok(r),
    no_unwind
{
    match *r {
        Result::Ok(_) => true,
        _ => false,
    }
}

} // verus!

fn main() {}