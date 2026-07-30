#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_is_none_or<T, F: FnOnce(T) -> bool>(
    option: Option<T>,
    f: F,
) -> (res: bool)
    requires
        option.is_some() ==> f.requires((option.unwrap(),)),
        option.is_some() ==> forall|out1: bool, out2: bool|
            #![trigger f.ensures((option.unwrap(),), out1),
                       f.ensures((option.unwrap(),), out2)]
            f.ensures((option.unwrap(),), out1)
                && f.ensures((option.unwrap(),), out2)
                ==> out1 == out2,
    ensures
        option.is_none() ==> res,
        option.is_some() ==> f.ensures((option.unwrap(),), res),
{
    match option {
        None => true,
        Some(x) => f(x),
    }
}

} // verus!

fn main() {}