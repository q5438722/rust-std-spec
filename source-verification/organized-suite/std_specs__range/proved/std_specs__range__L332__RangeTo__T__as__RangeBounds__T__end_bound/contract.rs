pub assume_specification<'s, T>[ <RangeTo<T> as RangeBounds<T>>::end_bound ](
    range: &'s RangeTo<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Excluded(&range.end),
;
