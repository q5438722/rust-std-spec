pub assume_specification<T, U: From<T>>[ <T as Into<U>>::into ](a: T) -> (ret: U)
    ensures
        call_ensures(U::from, (a,), ret),
;
