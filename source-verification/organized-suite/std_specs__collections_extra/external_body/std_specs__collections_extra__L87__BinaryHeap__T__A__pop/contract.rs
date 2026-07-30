pub assume_specification<T: Ord, A: Allocator>[ BinaryHeap::<T, A>::pop ](
    heap: &mut BinaryHeap<T, A>,
) -> (result: Option<T>)
    ensures
        match result {
            None => {
                &&& old(heap)@.len() == 0
                &&& final(heap)@ == old(heap)@
            },
            Some(value) => {
                &&& old(heap)@.contains(value)
                &&& final(heap)@ == old(heap)@.remove(value)
            },
        },
;
