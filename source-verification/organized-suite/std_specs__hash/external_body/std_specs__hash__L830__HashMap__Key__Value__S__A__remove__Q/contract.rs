pub assume_specification<
    Key: Borrow<Q> + Hash + Eq,
    Value,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashMap::<Key, Value, S, A>::remove::<Q> ](m: &mut HashMap<Key, Value, S, A>, k: &Q) -> (result:
    Option<Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& borrowed_key_removed(old(m)@, final(m)@, k)
            &&& match result {
                Some(v) => maps_borrowed_key_to_value(old(m)@, k, v),
                None => !contains_borrowed_key(old(m)@, k),
            }
        },
;
