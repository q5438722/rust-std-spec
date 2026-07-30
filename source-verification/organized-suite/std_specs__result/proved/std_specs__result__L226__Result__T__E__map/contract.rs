pub assume_specification<T, E, U, F: FnOnce(T) -> U>[ Result::<T, E>::map ](
    result: Result<T, E>,
    op: F,
) -> (mapped_result: Result<U, E>)
    requires
        result.is_ok() ==> op.requires((result->Ok_0,)),
    ensures
        result.is_ok() ==> mapped_result.is_ok() && op.ensures(
            (result->Ok_0,),
            mapped_result->Ok_0,
        ),
        result.is_err() ==> mapped_result == Result::<U, E>::Err(result->Err_0),
;
