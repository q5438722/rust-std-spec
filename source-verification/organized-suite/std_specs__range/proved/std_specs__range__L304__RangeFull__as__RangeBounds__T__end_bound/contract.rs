pub assume_specification<'s, T: ?Sized>[ <RangeFull as RangeBounds<T>>::end_bound ](
    range: &'s RangeFull,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
;
