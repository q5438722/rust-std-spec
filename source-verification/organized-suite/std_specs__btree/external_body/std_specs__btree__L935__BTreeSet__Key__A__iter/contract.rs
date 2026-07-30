pub assume_specification<'a, Key, A: Allocator + Clone>[ BTreeSet::<Key, A>::iter ](
    m: &'a BTreeSet<Key, A>,
) -> (r: btree_set::Iter<'a, Key>)
    ensures
        key_obeys_cmp_spec::<Key>() ==> {
            &&& r == spec_btree_keys_iter(m)
            &&& IteratorSpec::decrease(&r) is Some
            &&& IteratorSpec::initial_value_relation(&r, &r)
        },
;
