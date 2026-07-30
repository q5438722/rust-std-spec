pub assume_specification<Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::len ](
    m: &BTreeMap<Key, Value, A>,
) -> (len: usize)
    ensures
        len == spec_btree_map_len(m),
;
