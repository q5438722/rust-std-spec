pub assume_specification<Idx: PartialOrd<Idx>, U>[ RangeInclusive::<Idx>::contains ](
    r: &RangeInclusive<Idx>,
    i: &U,
) -> (ret: bool) where Idx: PartialOrd<U>, U: ?Sized + PartialOrd<Idx>
    ensures
        <RangeInclusive::<Idx> as ContainsSpec<Idx, U>>::obeys_contains() ==> ret
            == r.contains_spec(i),
;
