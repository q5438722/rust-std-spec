pub assume_specification<
    'a,
    Key: Borrow<Q> + Hash + Eq,
    Value,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashMap::<Key, Value, S, A>::get::<Q> ](m: &'a HashMap<Key, Value, S, A>, k: &Q) -> (result:
    Option<&'a Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> match result {
            Some(v) => maps_borrowed_key_to_value(m@, k, *v),
            None => !contains_borrowed_key(m@, k),
        },
;
