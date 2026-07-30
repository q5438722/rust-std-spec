#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialOrd;
use core::ops::{Bound, RangeBounds, RangeToInclusive};
use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};

verus! {

pub fn source_range_to_inclusive_contains<Idx: PartialOrd<Idx>, U>(
    range: &RangeToInclusive<Idx>,
    item: &U,
) -> (result: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    ensures
        <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec()
            ==> result == item.is_le(&range.end),
{
    let result = (match <RangeToInclusive<Idx> as RangeBounds<Idx>>::start_bound(range) {
        Bound::Included(start) => start <= item,
        Bound::Excluded(start) => start < item,
        Bound::Unbounded => true,
    }) && (match <RangeToInclusive<Idx> as RangeBounds<Idx>>::end_bound(range) {
        Bound::Included(end) => item <= end,
        Bound::Excluded(end) => item < end,
        Bound::Unbounded => true,
    });
    proof {
        assert(
            <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec()
                ==> result == item.is_le(&range.end)
        );
    }
    result
}

} // verus!

fn main() {}