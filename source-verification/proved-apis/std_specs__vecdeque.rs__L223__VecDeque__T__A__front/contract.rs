pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::front ](v: &VecDeque<T, A>) -> (result:
    Option<&T>)
    ensures
        v@.len() == 0 ==> result is None,
        v@.len() > 0 ==> (result matches Some(value) && *value == v@[0]),
;
