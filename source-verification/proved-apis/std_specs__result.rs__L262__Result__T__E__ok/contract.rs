pub assume_specification<T, E>[ Result::<T, E>::ok ](result: Result<T, E>) -> (opt: Option<T>)
    ensures
        opt == ok(result),
    no_unwind
;
