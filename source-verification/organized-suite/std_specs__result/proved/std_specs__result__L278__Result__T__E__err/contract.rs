pub assume_specification<T, E>[ Result::<T, E>::err ](result: Result<T, E>) -> (opt: Option<E>)
    ensures
        opt == err(result),
    no_unwind
;
