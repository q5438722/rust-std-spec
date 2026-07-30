#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_or_else<T, F>(
    option: Option<T>,
    f: F,
) -> (result: Option<T>)
where
    F: FnOnce() -> Option<T>,
    requires
        option is None ==> f.requires(()),
        option is None ==> forall|result1: Option<T>, result2: Option<T>|
            #![trigger f.ensures((), result1), f.ensures((), result2)]
            f.ensures((), result1)
                && f.ensures((), result2)
                ==> result1 == result2,
    ensures
        option is Some ==> result == option,
        option is None ==> f.ensures((), result),
{
    match option {
        x @ Some(_) => x,
        None => f(),
    }
}

} // verus!

fn main() {}