pub assume_specification<T: core::default::Default>[ <Rc<
    T,
> as core::default::Default>::default ]() -> (res: Rc<T>)
    ensures
        T::default.ensures((), *res),
;
