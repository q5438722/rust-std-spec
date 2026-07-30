pub assume_specification<T: Clone>[ <Option<T> as Clone>::clone ](opt: &Option<T>) -> (res: Option<
    T,
>)
    ensures
        opt.is_none() ==> res.is_none(),
        opt.is_some() ==> res.is_some() && cloned::<T>(opt.unwrap(), res.unwrap()),
;
