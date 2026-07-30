pub assume_specification<T, U: TryFrom<T>>[ <T as TryInto<U>>::try_into ](a: T) -> (ret: Result<
    U,
    U::Error,
>)
    ensures
        call_ensures(U::try_from, (a,), ret),
;
