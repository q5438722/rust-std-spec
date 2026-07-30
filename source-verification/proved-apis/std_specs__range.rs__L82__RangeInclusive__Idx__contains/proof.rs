#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    RangeBounds, RangeInclusive,
};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

pub fn raw_range_bounds_end_bound<'a, T: ?Sized, R: RangeBounds<T>>(
    r: &'a R,
) -> core::ops::Bound<&'a T>
{
    <R as RangeBounds<T>>::end_bound(r)
}

// Rust 1.96 selects the end-bound variant using RangeInclusive's private exhausted field.
pub axiom fn axiom_range_inclusive_end_bound_representation<'a, Idx>(
    r: &'a RangeInclusive<Idx>,
    result: core::ops::Bound<&'a Idx>,
)
    requires
        call_ensures(
            raw_range_bounds_end_bound::<Idx, RangeInclusive<Idx>>,
            (r,),
            result,
        ),
    ensures
        spec_bound(result) == if r@.exhausted {
            SpecBound::Excluded(&r@.end)
        } else {
            SpecBound::Included(&r@.end)
        },
;

fn source_range_inclusive_contains<Idx: PartialOrd<Idx>, U>(
    r: &RangeInclusive<Idx>,
    item: &U,
) -> (ret: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    ensures
        <RangeInclusive<Idx> as ContainsSpec<Idx, U>>::obeys_contains()
            ==> ret == r.contains_spec(item),
{
    let start_bound = <RangeInclusive<Idx> as RangeBounds<Idx>>::start_bound(r);
    let ret = (match start_bound {
        Included(start) => start <= item,
        Excluded(start) => start < item,
        Unbounded => true,
    }) && {
        let end_bound_fn = raw_range_bounds_end_bound::<Idx, RangeInclusive<Idx>>;
        let end_bound = end_bound_fn(r);
        proof {
            axiom_range_inclusive_end_bound_representation(r, end_bound);
        }
        match end_bound {
            Included(end) => item <= end,
            Excluded(end) => item < end,
            Unbounded => true,
        }
    };
    proof {
        assert(
            <RangeInclusive<Idx> as ContainsSpec<Idx, U>>::obeys_contains()
                ==> ret == r.contains_spec(item)
        );
    }
    ret
}

}

fn main() {}