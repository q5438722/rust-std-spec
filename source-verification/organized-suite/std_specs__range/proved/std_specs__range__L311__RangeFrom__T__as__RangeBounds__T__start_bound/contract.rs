pub assume_specification<'s, T>[ <RangeFrom<T> as RangeBounds<T>>::start_bound ](
    range: &'s RangeFrom<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range.start),
;
