pub assume_specification<
    Key: Borrow<Q> + Hash + Eq,
    S: BuildHasher,
    A: Allocator,
    Q: Hash + Eq + ?Sized,
>[ HashSet::<Key, S, A>::remove::<Q> ](m: &mut HashSet<Key, S, A>, k: &Q) -> (result: bool)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& sets_differ_by_borrowed_key(old(m)@, final(m)@, k)
            &&& result == set_contains_borrowed_key(old(m)@, k)
        },
;
