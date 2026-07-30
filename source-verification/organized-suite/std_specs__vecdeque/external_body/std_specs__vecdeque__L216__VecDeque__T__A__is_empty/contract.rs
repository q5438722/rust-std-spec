pub assume_specification<T, A: Allocator>[ VecDeque::<T, A>::is_empty ](
    v: &VecDeque<T, A>,
) -> (result: bool)
    ensures
        result <==> v@.len() == 0,
;
