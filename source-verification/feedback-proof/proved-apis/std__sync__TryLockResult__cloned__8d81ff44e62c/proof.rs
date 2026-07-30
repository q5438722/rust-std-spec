#![allow(dead_code)]
#![allow(unused_imports)]

use core::clone::Clone;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

pub fn source_try_lock_result_cloned<T: Clone, E>(
    result: Result<&T, E>,
) -> (cloned_result: Result<T, E>)
    ensures
        result is Ok ==> cloned_result is Ok
            && cloned::<T>(*result->Ok_0, cloned_result->Ok_0),
        result is Err ==> cloned_result == Result::Err(result->Err_0),
{
    result.map(|t: &T| -> (u: T)
        ensures
            cloned::<T>(*t, u),
    {
        t.clone()
    })
}

} // verus!

fn main() {}