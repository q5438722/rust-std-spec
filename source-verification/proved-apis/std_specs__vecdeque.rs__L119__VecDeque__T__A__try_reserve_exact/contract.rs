pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::try_reserve_exact ](
    v: &mut VecDeque<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
;
