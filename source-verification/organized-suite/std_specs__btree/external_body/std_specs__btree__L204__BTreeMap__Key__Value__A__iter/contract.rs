pub assume_specification<'a, Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::iter ](
    m: &'a BTreeMap<Key, Value, A>,
) -> (iter: btree_map::Iter<'a, Key, Value>)
    ensures
        key_obeys_cmp_spec::<Key>() ==> {
            &&& iter == spec_btree_map_iter(m)
            &&& iter.remaining().no_duplicates()
            &&& IteratorSpec::decrease(&iter) is Some
            &&& IteratorSpec::initial_value_relation(&iter, &iter)
            &&& increasing_seq(iter.remaining().map_values(|kv: (&Key, &Value)| *kv.0))
        },
;
