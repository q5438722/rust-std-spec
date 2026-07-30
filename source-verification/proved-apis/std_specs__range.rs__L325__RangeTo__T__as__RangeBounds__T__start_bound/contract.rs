pub assume_specification<'s, T>[ <RangeTo<T> as RangeBounds<T>>::start_bound ](
    range: &'s RangeTo<T>,
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == SpecBound::Unbounded,
;
