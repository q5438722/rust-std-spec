pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::clear ](heap: &mut BinaryHeap<T, A>)
    ensures
        final(heap)@ == Multiset::<T>::empty(),
;
