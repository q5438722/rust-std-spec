#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{Bound, RangeTo};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn source_range_to_end_bound<'s, T>(
    range: &'s RangeTo<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Excluded(&range.end),
{
    Bound::Excluded(&range.end)
}

}

fn main() {}