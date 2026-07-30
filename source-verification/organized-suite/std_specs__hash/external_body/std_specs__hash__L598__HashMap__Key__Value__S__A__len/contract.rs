pub assume_specification<Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::len ](
    m: &HashMap<Key, Value, S, A>,
) -> (len: usize)
    ensures
        len == spec_hash_map_len(m),
;
