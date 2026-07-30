pub assume_specification<T, A: Allocator>[ BinaryHeap::<T, A>::try_reserve_exact ](
    heap: &mut BinaryHeap<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(heap)@ == old(heap)@,
        result is Ok ==> final(heap).spec_capacity() >= old(heap)@.len() + additional as nat,
;
