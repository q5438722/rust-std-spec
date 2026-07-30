pub assume_specification<'a, Key, S, A: Allocator>[ HashSet::<Key, S, A>::iter ](
    m: &'a HashSet<Key, S, A>,
) -> (hash_keys: hash_set::Iter<'a, Key>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& hash_keys == spec_hash_keys_iter(m)
            &&& IteratorSpec::decrease(&hash_keys) is Some
            &&& IteratorSpec::initial_value_relation(&hash_keys, &hash_keys)
        },
;
