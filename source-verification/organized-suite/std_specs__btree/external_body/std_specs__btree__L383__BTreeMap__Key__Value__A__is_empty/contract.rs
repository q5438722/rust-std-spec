pub assume_specification<Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::is_empty ](
    m: &BTreeMap<Key, Value, A>,
) -> (res: bool)
    ensures
        res == m@.is_empty(),
;
