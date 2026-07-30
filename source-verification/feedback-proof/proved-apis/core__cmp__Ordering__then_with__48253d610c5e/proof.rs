#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;

verus! {

pub fn source_ordering_then_with<F: FnOnce() -> Ordering>(
    ordering: Ordering,
    f: F,
) -> (result: Ordering)
    requires
        ordering == Ordering::Equal ==> f.requires(()),
    ensures
        ordering == Ordering::Equal ==> f.ensures((), result),
        ordering != Ordering::Equal ==> result == ordering,
{
    match ordering {
        Ordering::Equal => f(),
        _ => ordering,
    }
}

} // verus!

fn main() {}