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

pub fn source_core_mem_take<T: core::default::Default>(
    dest: &mut T,
) -> (res: T)
    ensures
        res == *old(dest),
        T::default.ensures((), *final(dest)),
{
    core::mem::replace(dest, T::default())
}

} // verus!

fn main() {}