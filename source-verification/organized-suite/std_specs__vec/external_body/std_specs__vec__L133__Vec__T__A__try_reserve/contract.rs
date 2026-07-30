pub assume_specification<T, A: Allocator>[ Vec::<T, A>::try_reserve ](
    vec: &mut Vec<T, A>,
    additional: usize,
) -> (result: Result<(), TryReserveError>)
    ensures
        final(vec)@ == old(vec)@,
;
