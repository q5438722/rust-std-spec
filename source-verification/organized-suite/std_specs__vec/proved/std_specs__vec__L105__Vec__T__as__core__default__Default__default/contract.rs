pub assume_specification<T>[ <Vec<T> as core::default::Default>::default ]() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
;
