pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::shrink_to_fit ](
    heap: &mut BinaryHeap<T, A>,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len(),
        final(heap).spec_capacity() <= old(heap).spec_capacity(),
;
