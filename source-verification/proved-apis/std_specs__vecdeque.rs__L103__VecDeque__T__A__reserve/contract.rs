pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::reserve ](
    v: &mut VecDeque<T, A>,
    additional: usize,
)
    ensures
        final(v)@ == old(v)@,
;
