pub assume_specification<'b, T: core::marker::PointeeSized, 'a>[ <&'b T as Clone>::clone ](
    b: &'a &'b T,
) -> (res: &'b T)
    ensures
        res == b,
;
