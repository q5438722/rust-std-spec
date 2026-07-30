#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification<T>[ core::mem::replace ](
    dest: &mut T,
    src: T,
) -> (res: T)
    ensures
        res == *old(dest),
        *final(dest) == src,
    opens_invariants none
    no_unwind
;

pub fn source_option_replace<T>(
    option: &mut core::option::Option<T>,
    value: T,
) -> (res: core::option::Option<T>)
    ensures
        res == *old(option),
        *final(option) == core::option::Option::Some(value),
{
    core::mem::replace(option, core::option::Option::Some(value))
}

} // verus!

fn main() {}