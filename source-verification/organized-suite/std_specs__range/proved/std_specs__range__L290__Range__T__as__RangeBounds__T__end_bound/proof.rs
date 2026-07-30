#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{Bound, Range};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn range_end_bound_proof<'s, T>(range: &'s Range<T>) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Excluded(&range.end),
{
    Bound::Excluded(&range.end)
}

}

fn main() {}