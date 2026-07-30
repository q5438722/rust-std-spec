pub assume_specification<'_0, 'a, A: PointeeSized, B: PointeeSized>[ <&'a A as PartialOrd<&B>>::lt ](
    a: &&'a A,
    b: &&B,
) -> bool
where
    A: PartialOrd<B>,
;
