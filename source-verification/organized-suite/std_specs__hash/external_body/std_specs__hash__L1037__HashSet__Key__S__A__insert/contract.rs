pub assume_specification<Key: Eq + Hash, S: BuildHasher, A: Allocator>[ HashSet::<
    Key,
    S,
    A,
>::insert ](m: &mut HashSet<Key, S, A>, k: Key) -> (result: bool)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& final(m)@ == old(m)@.insert(k)
            &&& result == !old(m)@.contains(k)
        },
;
