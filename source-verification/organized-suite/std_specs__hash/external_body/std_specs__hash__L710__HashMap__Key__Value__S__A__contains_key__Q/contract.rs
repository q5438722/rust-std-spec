pub assume_specification<
    Key: Borrow<Q> + Hash + Eq,
    Value,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashMap::<Key, Value, S, A>::contains_key::<Q> ](
    m: &HashMap<Key, Value, S, A>,
    k: &Q,
) -> (result: bool)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> result == contains_borrowed_key(
            m@,
            k,
        ),
;
