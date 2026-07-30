#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{Bound, RangeToInclusive};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_to_inclusive_end_bound_proof<'s, T>(
    range: &'s RangeToInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range.end),
{
    Bound::Included(&range.end)
}

}

fn main() {}