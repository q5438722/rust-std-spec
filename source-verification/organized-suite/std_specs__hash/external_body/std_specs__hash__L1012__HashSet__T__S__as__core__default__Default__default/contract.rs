pub assume_specification<T, S: core::default::Default>[ <HashSet<
    T,
    S,
> as core::default::Default>::default ]() -> (m: HashSet<T, S>)
    ensures
        m@ == Set::<T>::empty(),
;
