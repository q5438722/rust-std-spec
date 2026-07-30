#![allow(dead_code)]

use core::ops::Bound::{self, Unbounded};
use core::ops::RangeFull;
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_full_start_bound_proof<'s, T: ?Sized>(
    range: &'s RangeFull,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
{
    Unbounded
}

}

fn main() {}