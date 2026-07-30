#![allow(dead_code)]

use core::option::Option;
use vstd::prelude::*;
use vstd::std_specs::option::*;

verus! {

pub assume_specification<T>[ core::mem::replace ](dest: &mut T, src: T) -> (res: T)
    ensures
        res == *old(dest),
        *final(dest) == src,
    opens_invariants none
    no_unwind
;

fn option_take_proof<T>(option: &mut Option<T>) -> (t: Option<T>)
    ensures
        t == *old(option),
        *final(option) is None,
    no_unwind
{
    core::mem::replace(option, None)
}

} // verus!

fn main() {}