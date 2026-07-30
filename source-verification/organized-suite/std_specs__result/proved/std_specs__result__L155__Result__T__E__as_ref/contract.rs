pub assume_specification<T, E>[ Result::<T, E>::as_ref ](result: &Result<T, E>) -> (r: Result<
    &T,
    &E,
>)
    ensures
        r is Ok <==> result is Ok,
        r is Ok ==> result->Ok_0 == r->Ok_0,
        r is Err <==> result is Err,
        r is Err ==> result->Err_0 == r->Err_0,
    no_unwind
;
