#![allow(dead_code)]

use core::ops::Bound;
use core::ops::Bound::{Excluded, Included, Unbounded};
use vstd::prelude::*;
use vstd::std_specs::range::{spec_bound, spec_bound_ref};

verus! {

pub fn source_bound_as_ref<T>(bound: &Bound<T>) -> (result: Bound<&T>)
    ensures
        spec_bound(result) == spec_bound_ref(bound),
{
    match *bound {
        Included(ref x) => Included(x),
        Excluded(ref x) => Excluded(x),
        Unbounded => Unbounded,
    }
}

} // verus!

fn main() {}