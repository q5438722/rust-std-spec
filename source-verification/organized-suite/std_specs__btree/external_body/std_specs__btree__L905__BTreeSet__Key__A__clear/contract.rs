pub assume_specification<Key, A: Allocator + Clone>[ BTreeSet::<Key, A>::clear ](
    m: &mut BTreeSet<Key, A>,
) where A: Clone
    ensures
        final(m)@ == Set::<Key>::empty(),
;
