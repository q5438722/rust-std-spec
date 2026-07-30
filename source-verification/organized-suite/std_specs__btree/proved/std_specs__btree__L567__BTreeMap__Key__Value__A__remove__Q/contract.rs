pub assume_specification<
    Key: Borrow<Q> + Ord,
    Value,
    A: Allocator + Clone,
    Q: Ord + ?Sized,
>[ BTreeMap::<Key, Value, A>::remove::<Q> ](m: &mut BTreeMap<Key, Value, A>, k: &Q) -> (result:
    Option<Value>)
    ensures
        obeys_cmp::<Key>() ==> {
            &&& borrowed_key_removed(old(m)@, final(m)@, k)
            &&& match result {
                Some(v) => maps_borrowed_key_to_value(old(m)@, k, v),
                None => !contains_borrowed_key(old(m)@, k),
            }
        },
;
