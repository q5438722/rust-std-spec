pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::get ](
    v: &VecDeque<T, A>,
    index: usize,
) -> (result: Option<&T>)
    ensures
        index < v@.len() ==> (result matches Some(value) && *value == v@[index as int]),
        index >= v@.len() ==> result is None,
;
