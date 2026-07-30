pub assume_specification<T, A: Allocator> [ <Vec<T, A>>::is_empty ](
    v: &Vec<T, A>,
) -> (res: bool)
    ensures res <==> v@.len() == 0,
;
