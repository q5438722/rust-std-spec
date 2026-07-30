#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::Bound;
use core::ops::Bound::{Excluded, Included, Unbounded};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

fn bound_pair_end_bound_proof<'s, T>(
    range: &'s (Bound<T>, Bound<T>),
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == spec_bound_ref(&range.1),
{
    match *range {
        (_, Included(ref end)) => Included(end),
        (_, Excluded(ref end)) => Excluded(end),
        (_, Unbounded) => Unbounded,
    }
}

}

fn main() {}