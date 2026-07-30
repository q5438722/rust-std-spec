#![allow(dead_code)]

use core::cmp::Ordering;
use vstd::prelude::*;

verus! {

pub fn source_ordering_reverse(ordering: Ordering) -> (result: Ordering)
    ensures
        result == (match ordering {
            Ordering::Less => Ordering::Greater,
            Ordering::Equal => Ordering::Equal,
            Ordering::Greater => Ordering::Less,
        }),
{
    match ordering {
        Ordering::Less => Ordering::Greater,
        Ordering::Equal => Ordering::Equal,
        Ordering::Greater => Ordering::Less,
    }
}

} // verus!

fn main() {}