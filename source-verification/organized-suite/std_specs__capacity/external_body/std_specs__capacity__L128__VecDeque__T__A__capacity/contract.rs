pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::capacity ](
    v: &VecDeque<T, A>,
) -> (result: usize)
    ensures
        result as nat == v.spec_capacity(),
;
