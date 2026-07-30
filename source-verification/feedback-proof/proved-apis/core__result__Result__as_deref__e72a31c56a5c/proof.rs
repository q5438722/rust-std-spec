#![allow(dead_code)]

use core::ops::Deref;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_as_deref<T: Deref, E>(
    result: &Result<T, E>,
) -> (res: Result<&T::Target, &E>)
    ensures
        match result {
            Ok(value) => res is Ok && call_ensures(
                <T as Deref>::deref,
                (value,),
                res->Ok_0,
            ),
            Err(error) => res is Err && res->Err_0 == error,
        },
{
    result.as_ref().map(Deref::deref)
}

} // verus!

fn main() {}