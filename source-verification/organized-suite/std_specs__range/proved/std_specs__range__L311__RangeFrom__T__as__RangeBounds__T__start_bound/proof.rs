#![allow(dead_code)]

use core::ops::{Bound, RangeFrom};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_from_start_bound_proof<'s, T>(
    range: &'s RangeFrom<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range.start),
{
    Bound::Included(&range.start)
}

}

fn main() {}