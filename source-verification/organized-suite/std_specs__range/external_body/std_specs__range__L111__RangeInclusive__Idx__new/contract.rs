pub assume_specification<Idx>[ RangeInclusive::<Idx>::new ](start: Idx, end: Idx) -> (ret:
    core::ops::RangeInclusive<Idx>)
    ensures
        ret == spec_range_inclusive_new(start, end),
;
