#![allow(dead_code)]
#![allow(unused_imports)]

use core::clone::Clone;
use core::ops::Bound;
use vstd::prelude::*;
use vstd::std_specs::range::spec_bound;

verus! {

pub fn source_bound_cloned<'a, T: Clone>(
    bound: Bound<&'a T>,
) -> (result: Bound<T>)
    ensures
        spec_bound(bound) is Unbounded ==> spec_bound(result) is Unbounded,
        spec_bound(bound) is Included ==> spec_bound(result) is Included
            && cloned::<T>(*(spec_bound(bound)->Included_0), spec_bound(result)->Included_0),
        spec_bound(bound) is Excluded ==> spec_bound(result) is Excluded
            && cloned::<T>(*(spec_bound(bound)->Excluded_0), spec_bound(result)->Excluded_0),
{
    match bound {
        Bound::Unbounded => Bound::Unbounded,
        Bound::Included(x) => {
            let cloned_x = x.clone();
            assert(cloned::<T>(*x, cloned_x));
            Bound::Included(cloned_x)
        }
        Bound::Excluded(x) => {
            let cloned_x = x.clone();
            assert(cloned::<T>(*x, cloned_x));
            Bound::Excluded(cloned_x)
        }
    }
}

} // verus!

fn main() {}