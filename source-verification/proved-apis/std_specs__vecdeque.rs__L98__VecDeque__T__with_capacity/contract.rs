pub assume_specification<T>[ VecDeque::<T>::with_capacity ](capacity: usize) -> (v: VecDeque<T>)
    ensures
        v@ == Seq::<T>::empty(),
;
