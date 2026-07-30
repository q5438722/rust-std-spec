#![allow(dead_code)]
#![allow(unused_imports)]

use core::ops::{
    Bound::{Excluded, Included, Unbounded},
    Range,
    RangeBounds as StdRangeBounds,
};
use vstd::prelude::*;
use vstd::std_specs::range::*;

verus! {

// Proof-local copy boundary for core's unsupported RangeBounds::contains default.
trait RangeBounds<T> {
    fn contains<U>(&self, item: &U) -> (ret: bool)
    where
        T: PartialOrd<U>,
        U: ?Sized + PartialOrd<T>,
        Self: ContainsSpec<T, U>,
        ensures
            <Self as ContainsSpec<T, U>>::obeys_contains()
                ==> ret == self.contains_spec(item),
    ;
}

impl<Idx: PartialOrd<Idx>> RangeBounds<Idx> for Range<Idx> {
    fn contains<U>(&self, item: &U) -> bool
    where
        Idx: PartialOrd<U>,
        U: ?Sized + PartialOrd<Idx>,
        Self: ContainsSpec<Idx, U>,
    {
        (match self.start_bound() {
            Included(start) => start <= item,
            Excluded(start) => start < item,
            Unbounded => true,
        }) && (match self.end_bound() {
            Included(end) => item <= end,
            Excluded(end) => item < end,
            Unbounded => true,
        })
    }
}

fn source_range_contains<Idx: PartialOrd<Idx>, U>(
    r: &Range<Idx>,
    item: &U,
) -> (ret: bool)
where
    Idx: PartialOrd<U>,
    U: ?Sized + PartialOrd<Idx>,
    ensures
        <Range<Idx> as ContainsSpec<Idx, U>>::obeys_contains()
            ==> ret == r.contains_spec(item),
{
    <Range<Idx> as RangeBounds<Idx>>::contains(r, item)
}

}

fn main() {}