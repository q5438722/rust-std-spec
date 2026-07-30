pub assume_specification<Key, S, A: Allocator>[ HashSet::<Key, S, A>::clear ](
    m: &mut HashSet<Key, S, A>,
)
    ensures
        final(m)@ == Set::<Key>::empty(),
;
