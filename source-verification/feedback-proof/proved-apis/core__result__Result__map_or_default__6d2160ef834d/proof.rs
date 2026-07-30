#![feature(result_option_map_or_default)]
#![allow(dead_code)]
#![allow(unused_imports)]

use core::result::Result;
use vstd::prelude::*;

verus! {

pub fn source_result_map_or_default<T, E, U, F>(
    result: Result<T, E>,
    f: F,
) -> (res: U)
where
    U: core::default::Default,
    F: FnOnce(T) -> U,
    requires
        result is Ok ==> f.requires((result->Ok_0,)),
        result is Ok ==> forall|u1: U, u2: U|
            #![trigger f.ensures((result->Ok_0,), u1),
                       f.ensures((result->Ok_0,), u2)]
            f.ensures((result->Ok_0,), u1)
                && f.ensures((result->Ok_0,), u2)
                ==> u1 == u2,
        result is Err ==> forall|u1: U, u2: U|
            #![trigger U::default.ensures((), u1),
                       U::default.ensures((), u2)]
            U::default.ensures((), u1)
                && U::default.ensures((), u2)
                ==> u1 == u2,
    ensures
        result is Ok ==> f.ensures((result->Ok_0,), res),
        result is Err ==> U::default.ensures((), res),
{
    match result {
        Ok(t) => f(t),
        Err(_) => U::default(),
    }
}

} // verus!

fn main() {}