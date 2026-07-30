pub assume_specification<'_0, 'a, A: PointeeSized, B: PointeeSized>[ <&'a A as PartialOrd<&B>>::partial_cmp ](
    a: &&'a A,
    b: &&B,
) -> Option<core::cmp::Ordering>
where
    A: PartialOrd<B>,
;
