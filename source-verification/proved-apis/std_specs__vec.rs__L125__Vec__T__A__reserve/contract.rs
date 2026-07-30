pub assume_specification<T, A: Allocator>[ Vec::<T, A>::reserve ](
    vec: &mut Vec<T, A>,
    additional: usize,
)
    ensures
        final(vec)@ == old(vec)@,
;
