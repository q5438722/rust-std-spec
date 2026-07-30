pub assume_specification<T>[ <Option<T> as core::default::Default>::default ]() -> (r: Option<T>)
    ensures
        r == Option::<T>::None,
;
