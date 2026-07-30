pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::is_empty ](
    heap: &BinaryHeap<T, A>,
) -> (result: bool)
    ensures
        result <==> heap@.len() == 0,
;
