pub assume_specification<Key, A: Allocator + Clone>[ BTreeSet::<Key, A>::is_empty ](
    m: &BTreeSet<Key, A>,
) -> (res: bool)
    ensures
        res == m@.is_empty(),
;
