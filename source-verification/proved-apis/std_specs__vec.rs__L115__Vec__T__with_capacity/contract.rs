pub assume_specification<T>[ Vec::<T>::with_capacity ](capacity: usize) -> (v: Vec<T>)
    ensures
        v@ == Seq::<T>::empty(),
;
