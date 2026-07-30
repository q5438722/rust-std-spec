#![allow(dead_code)]

use core::ops::{Bound, RangeInclusive};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

pub assume_specification<'s, T>[ RangeInclusive::<T>::start ](
    range: &'s RangeInclusive<T>,
) -> (result: &'s T)
    ensures
        result == range@.start,
;

fn source_range_inclusive_start_bound<'s, T>(
    range: &'s RangeInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range@.start),
{
    Bound::Included(range.start())
}

}

fn main() {}