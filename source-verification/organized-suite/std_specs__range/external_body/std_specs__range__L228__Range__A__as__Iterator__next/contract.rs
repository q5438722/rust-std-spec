pub assume_specification<A: core::iter::Step>[ <Range<A> as Iterator>::next ](
    range: &mut Range<A>,
) -> (r: Option<A>)
    ensures
        (*final(range), r) == spec_range_next(*old(range)),
;
