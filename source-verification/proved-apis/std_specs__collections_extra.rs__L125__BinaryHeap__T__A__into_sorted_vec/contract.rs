pub assume_specification<T: Ord, A: Allocator>[ BinaryHeap::<T, A>::into_sorted_vec ](
    heap: BinaryHeap<T, A>,
) -> (result: Vec<T, A>)
    ensures
        result@.to_multiset() == heap@,
;
