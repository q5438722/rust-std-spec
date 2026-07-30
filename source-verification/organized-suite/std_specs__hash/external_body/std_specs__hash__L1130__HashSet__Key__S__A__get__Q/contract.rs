pub assume_specification<
    'a,
    Key: Borrow<Q> + Hash + Eq,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashSet::<Key, S, A>::get::<Q> ](m: &'a HashSet<Key, S, A>, k: &Q) -> (result: Option<&'a Key>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> match result {
            Some(v) => sets_borrowed_key_to_key(m@, k, v),
            None => !set_contains_borrowed_key(m@, k),
        },
;
