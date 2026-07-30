#![allow(dead_code)]
#![allow(unused_imports)]

use core::clone::Clone;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::result::*;

verus! {

pub fn source_thread_result_cloned<'a, T: Clone, E>(
    result: Result<&'a T, E>,
) -> (res: Result<T, E>)
    ensures
        result is Ok ==> res is Ok && cloned::<T>(*result->Ok_0, res->Ok_0),
        result is Err ==> res == Result::<T, E>::Err(result->Err_0),
{
    result.map(|t: &'a T| -> (u: T)
        ensures
            cloned::<T>(*t, u),
    {
        t.clone()
    })
}

} // verus!

fn main() {}