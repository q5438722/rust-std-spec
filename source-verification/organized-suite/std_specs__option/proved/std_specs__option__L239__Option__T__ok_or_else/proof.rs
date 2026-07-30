#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn option_ok_or_else_proof<T, E, F: FnOnce() -> E>(
    option: Option<T>,
    err: F,
) -> (res: Result<T, E>)
    requires
        option.is_none() ==> err.requires(()),
    ensures
        option.is_some() ==> res == Ok::<T, E>(option.unwrap()),
        option.is_none() ==> {
            &&& res.is_err()
            &&& err.ensures((), res->Err_0)
        },
{
    match option {
        Some(v) => Ok(v),
        None => Err(err()),
    }
}

} // verus!

fn main() {}