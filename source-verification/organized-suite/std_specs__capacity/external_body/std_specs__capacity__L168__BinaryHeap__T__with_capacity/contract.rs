pub assume_specification<T>[ BinaryHeap::<T>::with_capacity ](capacity: usize) -> (result:
    BinaryHeap<T>)
    ensures
        result@ == Multiset::<T>::empty(),
        result.spec_capacity() >= capacity as nat,
;
