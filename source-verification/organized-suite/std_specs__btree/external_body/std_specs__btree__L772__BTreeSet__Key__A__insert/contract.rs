pub assume_specification<Key: Ord, A: Allocator + Clone>[ BTreeSet::<Key, A>::insert ](
    m: &mut BTreeSet<Key, A>,
    k: Key,
) -> (result: bool)
    ensures
        obeys_cmp::<Key>() ==> {
            &&& final(m)@ == old(m)@.insert(k)
            &&& result == !old(m)@.contains(k)
        },
;
