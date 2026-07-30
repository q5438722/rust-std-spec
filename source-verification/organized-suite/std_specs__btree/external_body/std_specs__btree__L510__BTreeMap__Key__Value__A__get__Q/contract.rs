pub assume_specification<
    'a,
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>[ BTreeMap::<Key, Value, A>::get::<Q> ](m: &'a BTreeMap<Key, Value, A>, k: &Q) -> (result: Option<
    &'a Value,
>)
    ensures
        obeys_cmp::<Key>() ==> match result {
            Some(v) => maps_borrowed_key_to_value(m@, k, *v),
            None => !contains_borrowed_key(m@, k),
        },
;
