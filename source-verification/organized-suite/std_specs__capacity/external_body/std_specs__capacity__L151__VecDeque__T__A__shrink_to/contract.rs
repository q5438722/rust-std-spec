pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::shrink_to ](
    v: &mut VecDeque<T, A>,
    min_capacity: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;
