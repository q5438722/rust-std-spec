pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::len ](
    heap: &BinaryHeap<T, A>,
) -> (result: usize)
    ensures
        result as nat == heap@.len(),
;
