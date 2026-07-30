pub assume_specification<Idx: PartialOrd<Idx>, U>[ Range::<Idx>::contains ](
    r: &Range<Idx>,
    i: &U,
) -> (ret: bool) where Idx: PartialOrd<U>, U: ?Sized + PartialOrd<Idx>
    ensures
        <Range::<Idx> as ContainsSpec<Idx, U>>::obeys_contains() ==> ret == r.contains_spec(i),
;
