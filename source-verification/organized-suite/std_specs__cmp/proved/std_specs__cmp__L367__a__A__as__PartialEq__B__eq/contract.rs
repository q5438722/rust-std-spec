pub assume_specification<'_0, 'a, A: PointeeSized, B: PointeeSized>[ <&'a A as PartialEq<&B>>::eq ](
    a: &&'a A,
    b: &&B,
) -> bool
where
    A: PartialEq<B>,
;
