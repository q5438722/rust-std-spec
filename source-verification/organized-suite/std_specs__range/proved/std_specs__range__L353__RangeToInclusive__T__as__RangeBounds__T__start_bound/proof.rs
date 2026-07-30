#![allow(dead_code)]
#![allow(unused_variables)]

use core::ops::Bound::{self, Unbounded};
use core::ops::RangeToInclusive;
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_to_inclusive_start_bound_proof<'s, T>(
    range: &'s RangeToInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
{
    Unbounded
}

}

fn main() {}