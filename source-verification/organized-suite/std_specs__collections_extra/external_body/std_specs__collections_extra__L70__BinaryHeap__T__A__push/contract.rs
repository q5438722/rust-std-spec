pub assume_specification<T: Ord, A: Allocator>[ BinaryHeap::<T, A>::push ](
    heap: &mut BinaryHeap<T, A>,
    item: T,
)
    ensures
        final(heap)@ == old(heap)@.insert(item),
;
