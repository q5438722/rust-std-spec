#![allow(dead_code)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn result_ok_proof<T, E>(result: Result<T, E>) -> (opt: Option<T>)
    ensures
        opt == ok(result),
    no_unwind
{
    match result {
        Ok(x) => Some(x),
        Err(_) => None,
    }
}

} // verus!

fn main() {}