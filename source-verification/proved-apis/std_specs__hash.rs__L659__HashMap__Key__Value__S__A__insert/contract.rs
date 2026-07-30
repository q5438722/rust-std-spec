pub assume_specification<Key: Eq + Hash, Value, S: BuildHasher, A: Allocator>[ HashMap::<
    Key,
    Value,
    S,
    A,
>::insert ](m: &mut HashMap<Key, Value, S, A>, k: Key, v: Value) -> (result: Option<Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& final(m)@ == old(m)@.insert(k, v)
            &&& match result {
                Some(v) => old(m)@.contains_key(k) && v == old(m)[k],
                None => !old(m)@.contains_key(k),
            }
        },
;
