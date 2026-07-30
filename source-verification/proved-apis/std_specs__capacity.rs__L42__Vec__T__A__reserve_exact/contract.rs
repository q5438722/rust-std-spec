pub assume_specification<T, A: Allocator>[ Vec::<T, A>::reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
        final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;
