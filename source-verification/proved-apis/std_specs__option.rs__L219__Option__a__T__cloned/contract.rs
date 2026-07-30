pub assume_specification<'a, T: Clone>[ Option::<&'a T>::cloned ](opt: Option<&'a T>) -> (res:
    Option<T>)
    ensures
        opt.is_none() ==> res.is_none(),
        opt.is_some() ==> res.is_some() && cloned::<T>(*opt.unwrap(), res.unwrap()),
;
