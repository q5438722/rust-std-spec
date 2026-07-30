pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::reserve_exact ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
)
    ensures
        final(heap)@ == old(heap)@,
        final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;
