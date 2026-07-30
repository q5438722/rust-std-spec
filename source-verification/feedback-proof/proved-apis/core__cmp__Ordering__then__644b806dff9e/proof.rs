#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;

verus! {

pub fn source_ordering_then(
    ordering: core::cmp::Ordering,
    other: core::cmp::Ordering,
) -> (result: core::cmp::Ordering)
    ensures
        result == (match ordering {
            core::cmp::Ordering::Equal => other,
            _ => ordering,
        }),
{
    match ordering {
        Ordering::Equal => other,
        _ => ordering,
    }
}

} // verus!

fn main() {}