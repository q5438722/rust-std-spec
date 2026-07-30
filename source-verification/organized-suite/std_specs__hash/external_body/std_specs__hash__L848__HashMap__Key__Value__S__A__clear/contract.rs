pub assume_specification<Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::clear ](
    m: &mut HashMap<Key, Value, S, A>,
)
    ensures
        final(m)@ == Map::<Key, Value>::empty(),
;
