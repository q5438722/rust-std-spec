pub assume_specification<T: PartialEq<U>, U, A1: Allocator, A2: Allocator>[ <Vec<T, A1> as PartialEq<Vec<U, A2>>>::eq ](
    x: &Vec<T, A1>,
    y: &Vec<U, A2>,
) -> bool
;
