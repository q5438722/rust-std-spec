pub assume_specification<T, E>[ Option::ok_or ](option: Option<T>, err: E) -> (res: Result<T, E>)
    ensures
        res == spec_ok_or(option, err),
;
