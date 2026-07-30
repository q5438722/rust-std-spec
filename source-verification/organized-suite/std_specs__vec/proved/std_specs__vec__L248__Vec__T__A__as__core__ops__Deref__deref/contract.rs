pub assume_specification<T, A: Allocator>[ <Vec<T, A> as core::ops::Deref>::deref ](
    vec: &Vec<T, A>,
) -> (slice: &[T])
    ensures
        slice@ == vec@,
;
