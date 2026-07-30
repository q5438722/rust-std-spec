pub assume_specification<T, A: Allocator>[ Vec::<T, A>::try_reserve_exact ](
    v: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(v)@ == old(v)@,
        result is Ok ==> final(v).spec_capacity() >= old(v)@.len() + additional as nat,
;
