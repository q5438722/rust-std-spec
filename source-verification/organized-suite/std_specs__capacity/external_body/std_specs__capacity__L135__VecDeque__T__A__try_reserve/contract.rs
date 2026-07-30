pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::try_reserve ](
    v: &mut VecDeque<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;
