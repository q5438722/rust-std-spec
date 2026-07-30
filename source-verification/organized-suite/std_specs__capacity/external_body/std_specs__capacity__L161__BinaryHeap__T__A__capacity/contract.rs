pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::capacity ](
    heap: &BinaryHeap<T, A>,
) -> (result: usize)
    ensures
        result as nat == heap.spec_capacity(),
;
