pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::shrink_to_fit ](v: &mut VecDeque<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;
