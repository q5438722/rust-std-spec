pub assume_specification<T>[ <BTreeSet<T> as core::default::Default>::default ]() -> (m: BTreeSet<
    T,
>)
    ensures
        m@ == Set::<T>::empty(),
;
