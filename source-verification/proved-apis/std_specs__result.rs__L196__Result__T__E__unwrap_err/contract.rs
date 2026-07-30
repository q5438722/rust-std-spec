pub assume_specification<T: core::fmt::Debug, E>[ Result::<T, E>::unwrap_err ](
    result: Result<T, E>,
) -> (e: E)
    requires
        result is Err,
    ensures
        e == result->Err_0,
;
