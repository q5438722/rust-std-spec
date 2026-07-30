pub assume_specification<T>[ Box::<T>::new ](t: T) -> (v: Box<T>)
    ensures
        *v == t,
;
