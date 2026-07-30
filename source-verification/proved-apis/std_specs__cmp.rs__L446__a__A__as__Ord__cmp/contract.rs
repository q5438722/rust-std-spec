pub assume_specification<'a, A: PointeeSized + Ord>[ <&'a A as Ord>::cmp ](
    a: &&'a A,
    b: &&'a A,
) -> core::cmp::Ordering
;
