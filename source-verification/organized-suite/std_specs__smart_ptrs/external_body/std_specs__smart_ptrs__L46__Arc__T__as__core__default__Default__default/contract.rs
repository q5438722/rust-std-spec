pub assume_specification<T: core::default::Default>[ <Arc<
    T,
> as core::default::Default>::default ]() -> (res: Arc<T>)
    ensures
        T::default.ensures((), *res),
;
