#![allow(dead_code)]

use core::option::Option;
use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_option_transpose<T, E>(
    option: Option<Result<T, E>>,
) -> (res: Result<Option<T>, E>)
    ensures
        res == match option {
            Option::Some(Result::Ok(x)) => Result::Ok(Option::Some(x)),
            Option::Some(Result::Err(e)) => Result::Err(e),
            Option::None => Result::Ok(Option::None),
        },
    no_unwind
{
    match option {
        Some(Ok(x)) => Ok(Some(x)),
        Some(Err(e)) => Err(e),
        None => Ok(None),
    }
}

} // verus!

fn main() {}