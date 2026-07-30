pub assume_specification<U: core::default::Default, T: core::default::Default>[ <(
    U,
    T,
) as core::default::Default>::default ]() -> (r: (U, T))
    ensures
        call_ensures(U::default, (), r.0),
        call_ensures(T::default, (), r.1),
;
