#![allow(dead_code)]

use core::ops::{Bound, Range};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn source_range_start_bound<'s, T>(
    range: &'s Range<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range.start),
{
    Bound::Included(&range.start)
}

}

fn main() {}