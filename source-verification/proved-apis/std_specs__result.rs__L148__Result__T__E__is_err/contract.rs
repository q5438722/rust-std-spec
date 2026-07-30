pub assume_specification<T, E>[ Result::<T, E>::is_err ](r: &Result<T, E>) -> (b: bool)
    ensures
        b == is_err(r),
    no_unwind
;
