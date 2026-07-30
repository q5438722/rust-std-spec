pub assume_specification<T>[ BinaryHeap::<T>::new ]() -> (result: BinaryHeap<T>)
    ensures
        result@ == Multiset::<T>::empty(),
;
