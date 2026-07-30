pub assume_specification<Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::is_empty ](
    m: &HashMap<Key, Value, S, A>,
) -> (res: bool)
    ensures
        res == m@.is_empty(),
;
