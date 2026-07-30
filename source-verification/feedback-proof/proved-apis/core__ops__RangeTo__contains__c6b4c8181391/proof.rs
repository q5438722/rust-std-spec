#![allow(dead_code)]
#![allow(unused_imports)]

use core::cmp::PartialOrd;
use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    RangeBounds as StdRangeBounds,
    RangeTo,
};
use vstd::prelude::*;
use vstd::std_specs::cmp::{PartialOrdIs, PartialOrdSpec};
use vstd::std_specs::range::*;

verus! {

pub trait RangeToContainsSpec<Idx, U>
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
{
    spec fn contains_spec(&self, item: &U) -> bool;
}

impl<Idx, U> RangeToContainsSpec<Idx, U> for RangeTo<Idx>
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
{
    open spec fn contains_spec(&self, item: &U) -> bool {
        item.is_lt(&self.end)
    }
}

// Proof-local copy boundary for core's unsupported RangeBounds::contains default.
pub trait RangeBounds<Idx> {
    fn contains<U>(&self, item: &U) -> (result: bool)
    where
        Idx: PartialOrd<U>,
        U: ?Sized + PartialOrd<Idx>,
        Self: RangeToContainsSpec<Idx, U>,
        ensures
            <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec()
                ==> result == self.contains_spec(item),
    ;
}

impl<Idx: PartialOrd<Idx>> RangeBounds<Idx> for RangeTo<Idx> {
    fn contains<U>(&self, item: &U) -> bool
    where
        Idx: PartialOrd<U>,
        U: ?Sized + PartialOrd<Idx>,
        Self: RangeToContainsSpec<Idx, U>,
    {
        (match <Self as StdRangeBounds<Idx>>::start_bound(self) {
            Included(start) => start <= item,
            Excluded(start) => start < item,
            Unbounded => true,
        }) && (match <Self as StdRangeBounds<Idx>>::end_bound(self) {
            Included(end) => item <= end,
            Excluded(end) => item < end,
            Unbounded => true,
        })
    }
}

fn source_range_to_contains<Idx: PartialOrd<Idx>, U>(
    range: &RangeTo<Idx>,
    item: &U,
) -> (result: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    requires
        <U as PartialOrdSpec<Idx>>::obeys_partial_cmp_spec(),
    ensures
        result == item.is_lt(&range.end),
{
    <RangeTo<Idx> as RangeBounds<Idx>>::contains(range, item)
}

}

fn main() {}