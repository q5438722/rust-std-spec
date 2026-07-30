pub assume_specification<T, A: Allocator>[ Vec::<T, A>::shrink_to_fit ](v: &mut Vec<T, A>)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len(),
        final(v).spec_capacity() <= old(v).spec_capacity(),
;
