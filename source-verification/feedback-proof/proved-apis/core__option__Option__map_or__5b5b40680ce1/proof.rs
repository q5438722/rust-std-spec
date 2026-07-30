#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_map_or<T, U, F>(
    option: Option<T>,
    default: U,
    f: F,
) -> (result: U)
where
    F: FnOnce(T) -> U,
    requires
        option is Some ==> f.requires((option->0,)),
        option is Some ==> forall|result1: U, result2: U|
            #![trigger f.ensures((option->0,), result1),
                       f.ensures((option->0,), result2)]
            f.ensures((option->0,), result1)
                && f.ensures((option->0,), result2)
                ==> result1 == result2,
    ensures
        option is Some ==> f.ensures((option->0,), result),
        option is None ==> result == default,
{
    match option {
        Some(t) => f(t),
        None => default,
    }
}

} // verus!

fn main() {}