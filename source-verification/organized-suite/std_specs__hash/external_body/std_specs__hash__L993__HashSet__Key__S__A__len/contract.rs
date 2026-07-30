pub assume_specification<Key, S, A: Allocator>[ HashSet::<Key, S, A>::len ](
    m: &HashSet<Key, S, A>,
) -> (len: usize)
    ensures
        len == spec_hash_set_len(m),
;
