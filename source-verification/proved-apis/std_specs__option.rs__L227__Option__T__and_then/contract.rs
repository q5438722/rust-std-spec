pub assume_specification<T, U, F: FnOnce(T) -> Option<U>>[ Option::<T>::and_then ](
    option: Option<T>,
    f: F,
) -> (res: Option<U>)
    requires
        option.is_some() ==> f.requires((option.unwrap(),)),
    ensures
        option.is_none() ==> res.is_none(),
        option.is_some() ==> f.ensures((option.unwrap(),), res),
;
