pub assume_specification<Key: Borrow<Q> + Ord, A: Allocator + Clone, Q: Ord + ?Sized>[ BTreeSet::<
    Key,
    A,
>::contains ](m: &BTreeSet<Key, A>, k: &Q) -> (result: bool)
    ensures
        obeys_cmp::<Key>() ==> result == set_contains_borrowed_key(m@, k),
    no_unwind
;
