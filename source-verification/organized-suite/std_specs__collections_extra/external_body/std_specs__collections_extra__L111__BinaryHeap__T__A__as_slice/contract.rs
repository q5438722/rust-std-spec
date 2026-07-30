pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::as_slice ](
    heap: &BinaryHeap<T, A>,
) -> (result: &[T])
    ensures
        result@.to_multiset() == heap@,
;
