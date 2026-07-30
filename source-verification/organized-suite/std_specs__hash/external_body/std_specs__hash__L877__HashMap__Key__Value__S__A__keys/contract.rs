pub assume_specification<'a, Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::keys ](
    m: &'a HashMap<Key, Value, S, A>,
) -> (keys: Keys<'a, Key, Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& keys == spec_keys_iter(m)
            &&& IteratorSpec::decrease(&keys) is Some
            &&& IteratorSpec::initial_value_relation(&keys, &keys)
        },
;
