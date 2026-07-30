pub assume_specification<'s, T>[ <RangeToInclusive<T> as RangeBounds<T>>::start_bound ](
    range: &'s RangeToInclusive<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
;
