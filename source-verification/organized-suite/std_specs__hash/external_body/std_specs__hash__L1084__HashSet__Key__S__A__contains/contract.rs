pub assume_specification<
    Key: Borrow<Q> + Hash + Eq,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashSet::<Key, S, A>::contains ](m: &HashSet<Key, S, A>, k: &Q) -> (result: bool)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> result
            == set_contains_borrowed_key(m@, k),
;
