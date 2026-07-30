pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::reserve_exact ](
    v: &mut VecDeque<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
;
