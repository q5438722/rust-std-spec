pub assume_specification<Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::clear ](
    m: &mut BTreeMap<Key, Value, A>,
)
    ensures
        final(m)@ == Map::<Key, Value>::empty(),
;
