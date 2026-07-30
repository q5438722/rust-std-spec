pub assume_specification<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>[ BTreeMap::<Key, Value, A>::contains_key::<Q> ](m: &BTreeMap<Key, Value, A>, k: &Q) -> (result:
    bool)
    ensures
        obeys_cmp::<Key>() ==> result == contains_borrowed_key(m@, k),
;
