pub assume_specification<Key, A: Allocator + Clone>[ BTreeSet::<Key, A>::len ](
    m: &BTreeSet<Key, A>,
) -> (len: usize)
    ensures
        len == spec_btree_set_len(m),
;
