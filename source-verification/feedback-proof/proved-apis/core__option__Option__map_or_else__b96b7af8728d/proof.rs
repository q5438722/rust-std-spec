#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_map_or_else<T, U, D, F>(
    option: Option<T>,
    default: D,
    f: F,
) -> (result: U)
where
    D: FnOnce() -> U,
    F: FnOnce(T) -> U,
    requires
        option is Some ==> f.requires((option->0,)),
        option is None ==> default.requires(()),
        option is Some ==> forall|u1: U, u2: U|
            #![trigger f.ensures((option->0,), u1),
                       f.ensures((option->0,), u2)]
            f.ensures((option->0,), u1)
                && f.ensures((option->0,), u2)
                ==> u1 == u2,
        option is None ==> forall|u1: U, u2: U|
            #![trigger default.ensures((), u1),
                       default.ensures((), u2)]
            default.ensures((), u1)
                && default.ensures((), u2)
                ==> u1 == u2,
    ensures
        option is Some ==> f.ensures((option->0,), result),
        option is None ==> default.ensures((), result),
{
    match option {
        Some(t) => f(t),
        None => default(),
    }
}

} // verus!

fn main() {}