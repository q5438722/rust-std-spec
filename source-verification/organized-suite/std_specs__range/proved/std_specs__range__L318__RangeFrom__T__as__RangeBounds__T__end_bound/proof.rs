#![allow(dead_code)]
#![allow(unused_variables)]

use core::ops::Bound::{self, Unbounded};
use core::ops::RangeFrom;
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_from_end_bound_proof<'s, T>(
    range: &'s RangeFrom<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
{
    Unbounded
}

}

fn main() {}