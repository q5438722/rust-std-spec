#![allow(dead_code)]
#![allow(unused_imports)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

fn source_option_get_or_insert_with<T, F: FnOnce() -> T>(
    option: &mut Option<T>,
    f: F,
) -> (res: &mut T)
    requires
        old(option).is_none() ==> f.requires(()),
    ensures
        old(option).is_some() ==> *res == old(option).unwrap(),
        old(option).is_none() ==> f.ensures((), *res),
        *final(option) == Some(*final(res)),
{
    if let None = option {
        // Rust 1.96 documents its forget(replace(...)) statement as effect-identical
        // to this assignment after the None check.
        *option = Some(f());
    }

    match option {
        Some(x) => x,
        None => {
            assert(false);
            vstd::vpanic!("get_or_insert_with left the option empty")
        },
    }
}

fn source_option_get_or_insert<T>(
    option: &mut Option<T>,
    value: T,
) -> (res: &mut T)
    ensures
        *res == (match *old(option) {
            Some(x) => x,
            None => value,
        }),
        *final(option) == Some(*final(res)),
{
    source_option_get_or_insert_with(
        option,
        || -> (res: T)
            ensures
                res == value,
        {
            value
        },
    )
}

} // verus!

fn main() {}