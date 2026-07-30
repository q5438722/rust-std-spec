pub assume_specification<T>[ VecDeque::<T>::new ]() -> (v: VecDeque<T>)
    ensures
        v@ == Seq::<T>::empty(),
;
