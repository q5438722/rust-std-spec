pub assume_specification<'a, Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::keys ](
    m: &'a BTreeMap<Key, Value, A>,
) -> (keys: Keys<'a, Key, Value>)
    ensures
        key_obeys_cmp_spec::<Key>() ==> {
            &&& keys == spec_keys_iter(m)
            &&& IteratorSpec::decrease(&keys) is Some
            &&& IteratorSpec::initial_value_relation(&keys, &keys)
        },
;
