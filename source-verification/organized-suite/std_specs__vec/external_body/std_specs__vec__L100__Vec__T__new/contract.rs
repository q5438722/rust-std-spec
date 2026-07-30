pub assume_specification<T>[ Vec::<T>::new ]() -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
;
