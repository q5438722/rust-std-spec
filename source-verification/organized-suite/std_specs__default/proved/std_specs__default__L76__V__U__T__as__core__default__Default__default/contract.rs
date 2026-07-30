pub assume_specification<
    V: core::default::Default,
    U: core::default::Default,
    T: core::default::Default,
>[ <(V, U, T) as core::default::Default>::default ]() -> (r: (V, U, T))
    ensures
        call_ensures(V::default, (), r.0),
        call_ensures(U::default, (), r.1),
        call_ensures(T::default, (), r.2),
;
