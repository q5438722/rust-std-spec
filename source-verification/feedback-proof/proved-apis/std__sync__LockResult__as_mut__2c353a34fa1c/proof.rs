#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_as_mut<T, E>(
    result: &mut Result<T, E>,
) -> (res: Result<&mut T, &mut E>)
    ensures
        (match *old(result) {
            Result::Ok(value) => {
                &&& *final(result) is Ok
                &&& res is Ok
                &&& *(res->Ok_0) == value
                &&& *final(res->Ok_0) == (*final(result))->Ok_0
            },
            Result::Err(error) => {
                &&& *final(result) is Err
                &&& res is Err
                &&& *(res->Err_0) == error
                &&& *final(res->Err_0) == (*final(result))->Err_0
            },
        }),
    no_unwind
{
    match *result {
        Ok(ref mut x) => Ok(x),
        Err(ref mut x) => Err(x),
    }
}

} // verus!

fn main() {}