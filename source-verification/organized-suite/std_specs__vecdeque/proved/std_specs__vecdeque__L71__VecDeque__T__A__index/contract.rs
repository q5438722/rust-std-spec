pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::index ](
    v: &VecDeque<T, A>,
    i: usize,
) -> (result: &T)
    ensures
        result == v.spec_index(i as int),
;
