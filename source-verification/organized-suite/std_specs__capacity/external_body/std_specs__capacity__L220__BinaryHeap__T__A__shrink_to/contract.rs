pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::shrink_to ](
    heap: &mut BinaryHeap<T, A>,
    min_capacity: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len(),
        final(heap).spec_capacity() <= old(heap).spec_capacity(),
;
