#![allow(dead_code)]

use core::ops::Bound;
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn bound_pair_start_bound_proof<'s, T>(
    range: &'s (Bound<T>, Bound<T>),
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == spec_bound_ref(&range.0),
{
    match *range {
        (Bound::Included(ref start), _) => Bound::Included(start),
        (Bound::Excluded(ref start), _) => Bound::Excluded(start),
        (Bound::Unbounded, _) => Bound::Unbounded,
    }
}

}

fn main() {}