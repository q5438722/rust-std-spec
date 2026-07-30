pub assume_specification<T>[ LinkedList::<T>::new ]() -> (result: LinkedList<T>)
    ensures
        result@ == Seq::<T>::empty(),
;
