pub assume_specification<T, E: core::fmt::Debug>[ Result::<T, E>::unwrap ](
    result: Result<T, E>,
) -> (t: T)
    requires
        result is Ok,
    ensures
        t == result->Ok_0,
;
