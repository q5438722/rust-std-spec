pub assume_specification<T, F: FnOnce() -> T>[ Option::<T>::unwrap_or_else ](
    option: Option<T>,
    f: F,
) -> (res: T)
    requires
        option.is_none() ==> f.requires(()),
    ensures
        option.is_some() ==> res == option.unwrap(),
        option.is_none() ==> f.ensures((), res),
;
