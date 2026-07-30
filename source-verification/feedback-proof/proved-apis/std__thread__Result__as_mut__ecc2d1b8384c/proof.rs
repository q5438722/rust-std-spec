#![allow(dead_code)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_as_mut<T, E>(
    result: &mut Result<T, E>,
) -> (res: Result<&mut T, &mut E>)
    ensures
        (match *old(result) {
            Result::Ok(v) => {
                &&& res is Ok
                &&& *res->Ok_0 == v
                &&& *final(result) == Result::<T, E>::Ok(*final(res->Ok_0))
            },
            Result::Err(e) => {
                &&& res is Err
                &&& *res->Err_0 == e
                &&& *final(result) == Result::<T, E>::Err(*final(res->Err_0))
            },
        }),
{
    match *result {
        Ok(ref mut x) => Ok(x),
        Err(ref mut x) => Err(x),
    }
}

} // verus!

fn main() {}