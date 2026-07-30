pub assume_specification<'s, T>[ <RangeInclusive<T> as RangeBounds<T>>::start_bound ](
    range: &'s RangeInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Included(&range@.start),
;
