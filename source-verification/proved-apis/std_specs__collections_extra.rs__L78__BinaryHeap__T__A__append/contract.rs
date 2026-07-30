pub assume_specification<T: Ord, A: Allocator>[ BinaryHeap::<T, A>::append ](
    heap: &mut BinaryHeap<T, A>,
    other: &mut BinaryHeap<T, A>,
)
    ensures
        final(heap)@ == old(heap)@.add(old(other)@),
        final(other)@ == Multiset::<T>::empty(),
;
