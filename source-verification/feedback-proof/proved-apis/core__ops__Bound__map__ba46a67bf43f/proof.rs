#![allow(dead_code)]

use core::ops::Bound;
use core::ops::Bound::{Excluded, Included, Unbounded};
use vstd::prelude::*;
use vstd::std_specs::range::spec_bound;

verus! {

pub fn source_bound_map<T, U, F>(
    bound: Bound<T>,
    f: F,
) -> (result: Bound<U>)
where
    F: FnOnce(T) -> U,
    requires
        spec_bound(bound) is Included ==> f.requires((spec_bound(bound)->Included_0,)),
        spec_bound(bound) is Excluded ==> f.requires((spec_bound(bound)->Excluded_0,)),
        spec_bound(bound) is Included ==> forall|u1: U, u2: U|
            #![trigger f.ensures((spec_bound(bound)->Included_0,), u1),
                       f.ensures((spec_bound(bound)->Included_0,), u2)]
            f.ensures((spec_bound(bound)->Included_0,), u1)
                && f.ensures((spec_bound(bound)->Included_0,), u2)
                ==> u1 == u2,
        spec_bound(bound) is Excluded ==> forall|u1: U, u2: U|
            #![trigger f.ensures((spec_bound(bound)->Excluded_0,), u1),
                       f.ensures((spec_bound(bound)->Excluded_0,), u2)]
            f.ensures((spec_bound(bound)->Excluded_0,), u1)
                && f.ensures((spec_bound(bound)->Excluded_0,), u2)
                ==> u1 == u2,
    ensures
        spec_bound(bound) is Unbounded ==> spec_bound(result) is Unbounded,
        spec_bound(bound) is Included ==> spec_bound(result) is Included && f.ensures(
            (spec_bound(bound)->Included_0,),
            spec_bound(result)->Included_0
        ),
        spec_bound(bound) is Excluded ==> spec_bound(result) is Excluded && f.ensures(
            (spec_bound(bound)->Excluded_0,),
            spec_bound(result)->Excluded_0
        ),
{
    match bound {
        Unbounded => Unbounded,
        Included(x) => Included(f(x)),
        Excluded(x) => Excluded(f(x)),
    }
}

} // verus!

fn main() {}