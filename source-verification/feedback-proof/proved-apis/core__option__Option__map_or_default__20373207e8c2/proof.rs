#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_map_or_default<T, U, F>(
    option: Option<T>,
    f: F,
) -> (result: U)
where
    U: core::default::Default,
    F: FnOnce(T) -> U,
    requires
        option is Some ==> f.requires((option->0,)),
        option is Some ==> forall|u1: U, u2: U|
            #![trigger f.ensures((option->0,), u1),
                       f.ensures((option->0,), u2)]
            f.ensures((option->0,), u1)
                && f.ensures((option->0,), u2)
                ==> u1 == u2,
        option is None ==> forall|u1: U, u2: U|
            #![trigger U::default.ensures((), u1),
                       U::default.ensures((), u2)]
            U::default.ensures((), u1)
                && U::default.ensures((), u2)
                ==> u1 == u2,
    ensures
        option is Some ==> f.ensures((option->0,), result),
        option is None ==> U::default.ensures((), result),
{
    match option {
        Some(t) => f(t),
        None => U::default(),
    }
}

} // verus!

fn main() {}