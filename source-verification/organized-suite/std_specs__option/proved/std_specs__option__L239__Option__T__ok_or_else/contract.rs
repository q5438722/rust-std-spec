pub assume_specification<T, E, F: FnOnce() -> E>[ Option::<T>::ok_or_else ](
    option: Option<T>,
    err: F,
) -> (res: Result<T, E>)
    requires
        option.is_none() ==> err.requires(()),
    ensures
        option.is_some() ==> res == Ok::<T, E>(option.unwrap()),
        option.is_none() ==> {
            &&& res.is_err()
            &&& err.ensures((), res->Err_0)
        },
;
