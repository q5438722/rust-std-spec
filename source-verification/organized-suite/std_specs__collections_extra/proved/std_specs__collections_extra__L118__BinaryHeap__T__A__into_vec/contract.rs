pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::into_vec ](
    heap: BinaryHeap<T, A>,
) -> (result: Vec<T, A>)
    ensures
        result@.to_multiset() == heap@,
;
