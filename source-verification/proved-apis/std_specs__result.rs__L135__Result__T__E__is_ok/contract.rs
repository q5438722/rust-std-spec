pub assume_specification<T, E>[ Result::<T, E>::is_ok ](r: &Result<T, E>) -> (b: bool)
    ensures
        b == is_ok(r),
    no_unwind
;
