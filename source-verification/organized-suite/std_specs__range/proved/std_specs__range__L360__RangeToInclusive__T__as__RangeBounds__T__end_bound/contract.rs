pub assume_specification<'s, T>[ <RangeToInclusive<T> as RangeBounds<T>>::end_bound ](
    range: &'s RangeToInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range.end),
;
