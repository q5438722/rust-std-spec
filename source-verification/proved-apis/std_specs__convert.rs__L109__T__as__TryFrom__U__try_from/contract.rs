pub assume_specification<T, U: Into<T>>[ <T as TryFrom<U>>::try_from ](a: U) -> (ret: Result<
    T,
    <T as TryFrom<U>>::Error,
>)
    ensures
        ret.is_ok(),
        call_ensures(U::into, (a,), ret.unwrap()),
;
