#![allow(dead_code)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn result_err_proof<T, E>(result: Result<T, E>) -> (opt: Option<E>)
    ensures
        opt == err(result),
    no_unwind
{
    match result {
        Ok(_) => None,
        Err(x) => Some(x),
    }
}

} // verus!

fn main() {}