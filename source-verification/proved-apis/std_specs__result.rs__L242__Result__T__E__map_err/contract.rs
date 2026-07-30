pub assume_specification<T, E, F, O: FnOnce(E) -> F>[Result::<T, E>::map_err](result: Result<T, E>, op: O) -> (mapped_result: Result<T, F>)
    requires
        result.is_err() ==> op.requires((result->Err_0,)),
    ensures
        result.is_err() ==> mapped_result.is_err() && op.ensures(
            (result->Err_0,),
            mapped_result->Err_0,
        ),
        result.is_ok() ==> mapped_result == Result::<T, F>::Ok(result->Ok_0);
