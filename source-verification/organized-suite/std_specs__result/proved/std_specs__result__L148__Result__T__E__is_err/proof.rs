#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn result_is_err_proof<T, E>(r: &Result<T, E>) -> (b: bool)
    ensures
        b == is_err(r),
    no_unwind
{
    let b = !r.is_ok();
    proof {
        match *r {
            Result::Ok(_) => {},
            Result::Err(_) => {},
        }
    }
    b
}

} // verus!

fn main() {}