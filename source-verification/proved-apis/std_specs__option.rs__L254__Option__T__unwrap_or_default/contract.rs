pub assume_specification<T: core::default::Default>[ Option::<T>::unwrap_or_default ](
    option: Option<T>,
) -> (res: T)
    ensures
        option.is_some() ==> res == option.unwrap(),
        option.is_none() ==> T::default.ensures((), res),
;
