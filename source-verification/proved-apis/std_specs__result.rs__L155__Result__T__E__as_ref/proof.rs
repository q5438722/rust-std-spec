#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

fn source_result_as_ref<T, E>(result: &Result<T, E>) -> (r: Result<&T, &E>)
    ensures
        r is Ok <==> result is Ok,
        r is Ok ==> result->Ok_0 == r->Ok_0,
        r is Err <==> result is Err,
        r is Err ==> result->Err_0 == r->Err_0,
    no_unwind
{
    match *result {
        Ok(ref x) => Ok(x),
        Err(ref x) => Err(x),
    }
}

} // verus!

fn main() {}