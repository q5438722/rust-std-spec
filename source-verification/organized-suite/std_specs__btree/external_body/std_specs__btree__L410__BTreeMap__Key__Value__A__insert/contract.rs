pub assume_specification<Key: Ord, Value, A: Allocator + Clone>[ BTreeMap::<
    Key,
    Value,
    A,
>::insert ](m: &mut BTreeMap<Key, Value, A>, k: Key, v: Value) -> (result: Option<Value>)
    ensures
        obeys_cmp::<Key>() ==> {
            &&& final(m)@ == old(m)@.insert(k, v)
            &&& match result {
                Some(v) => old(m)@.contains_key(k) && v == old(m)[k],
                None => !old(m)@.contains_key(k),
            }
        },
;
