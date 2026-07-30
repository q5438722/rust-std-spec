pub assume_specification<Key: Borrow<Q> + Ord, A: Allocator + Clone, Q: Ord + ?Sized>[ BTreeSet::<
    Key,
    A,
>::remove::<Q> ](m: &mut BTreeSet<Key, A>, k: &Q) -> (result: bool)
    ensures
        obeys_cmp::<Key>() ==> {
            &&& sets_differ_by_borrowed_key(old(m)@, final(m)@, k)
            &&& result == set_contains_borrowed_key(old(m)@, k)
        },
;
