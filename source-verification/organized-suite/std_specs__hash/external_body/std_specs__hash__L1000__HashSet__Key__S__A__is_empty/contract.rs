pub assume_specification<Key, S, A: Allocator>[ HashSet::<Key, S, A>::is_empty ](
    m: &HashSet<Key, S, A>,
) -> (res: bool)
    ensures
        res == m@.is_empty(),
;
