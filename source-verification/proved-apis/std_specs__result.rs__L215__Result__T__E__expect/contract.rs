pub assume_specification<T, E: core::fmt::Debug>[ Result::<T, E>::expect ](
    result: Result<T, E>,
    msg: &str,
) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
;
