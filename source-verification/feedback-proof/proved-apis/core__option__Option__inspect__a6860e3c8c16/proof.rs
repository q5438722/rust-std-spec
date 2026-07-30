#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;

verus! {

pub fn source_option_inspect<T, F: FnOnce(&T)>(
    option: Option<T>,
    f: F,
) -> (res: Option<T>)
    requires
        option.is_some() ==> f.requires((&option.unwrap(),)),
    ensures
        res == option,
        option.is_some() ==> f.ensures((&option.unwrap(),), ()),
{
    if let Some(ref x) = option {
        f(x);
    }

    option
}

} // verus!

fn main() {}