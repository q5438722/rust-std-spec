pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::peek ](
    heap: &BinaryHeap<T, A>,
) -> (result: Option<&T>)
    ensures
        result is None <==> heap@.len() == 0,
        result matches Some(value) ==> heap@.contains(*value),
;
