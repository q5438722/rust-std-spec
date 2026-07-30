pub assume_specification<'s, T>[ <(Bound<T>, Bound<T>) as RangeBounds<T>>::end_bound ](
    range: &'s (Bound<T>, Bound<T>),
) -> (result: Bound<&'s T>)
    ensures
        spec_bound(result) == spec_bound_ref(&range.1),
;
