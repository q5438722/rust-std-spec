pub assume_specification<'a, Key: Hash + Eq, Value, S: BuildHasher, A: Allocator>[ HashMap::<
    Key,
    Value,
    S,
    A,
>::entry ](m: &'a mut HashMap<Key, Value, S, A>, key: Key) -> (entry: Entry<'a, Key, Value, A>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> (entry.key() == key
            && entry.value() == old(m)@.get(key) && final(m)@ == (match entry.final_value() {
            Some(value) => old(m)@.insert(key, value),
            None => old(m)@.remove(key),
        })),
;
