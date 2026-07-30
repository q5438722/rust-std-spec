pub assume_specification<
    'a,
    Key: Borrow<Q> + Ord,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>[ BTreeSet::<Key, A>::get::<Q> ](m: &'a BTreeSet<Key, A>, k: &Q) -> (result: Option<&'a Key>)
    ensures
        obeys_cmp::<Key>() ==> match result {
            Some(v) => sets_borrowed_key_to_key(m@, k, v),
            None => !set_contains_borrowed_key(m@, k),
        },
;
