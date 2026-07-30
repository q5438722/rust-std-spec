pub assume_specification<'a, Key, Value, A: Allocator + Clone>[ BTreeMap::<Key, Value, A>::values ](
    m: &'a BTreeMap<Key, Value, A>,
) -> (values: Values<'a, Key, Value>)
    ensures
        key_obeys_cmp_spec::<Key>() ==> {
            &&& values == spec_values_iter(m)
            &&& IteratorSpec::decrease(&values) is Some
            &&& IteratorSpec::initial_value_relation(&values, &values)
            &&& exists|key_seq: Seq<Key>|
                {
                    &&& increasing_seq(key_seq)
                    &&& key_seq.to_set() == m@.dom()
                    &&& key_seq.no_duplicates()
                    &&& IteratorSpec::remaining(&values) == key_seq.map(|i: int, k| &m@[k])
                }
        },
;
