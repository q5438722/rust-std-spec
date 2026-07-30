pub assume_specification<T, U, F: FnOnce(T) -> U>[ Option::<T>::map ](a: Option<T>, f: F) -> (ret:
    Option<U>)
    requires
        a.is_some() ==> f.requires((a.unwrap(),)),
    ensures
        ret.is_some() == a.is_some(),
        ret.is_some() ==> f.ensures((a.unwrap(),), ret.unwrap()),
;
