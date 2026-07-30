pub assume_specification<'a, Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::iter ](
    m: &'a HashMap<Key, Value, S, A>,
) -> (iter: hash_map::Iter<'a, Key, Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& iter == spec_hash_map_iter(m)
            &&& iter.remaining().no_duplicates()
            &&& IteratorSpec::decrease(&iter) is Some
            &&& IteratorSpec::initial_value_relation(&iter, &iter)
        },
;
