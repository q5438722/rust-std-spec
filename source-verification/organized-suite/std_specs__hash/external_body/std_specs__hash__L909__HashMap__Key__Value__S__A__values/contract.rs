pub assume_specification<'a, Key, Value, S, A: Allocator>[ HashMap::<Key, Value, S, A>::values ](
    m: &'a HashMap<Key, Value, S, A>,
) -> (values: Values<'a, Key, Value>)
    ensures
        obeys_key_model::<Key>() && builds_valid_hashers::<S>() ==> {
            &&& values == spec_values_iter(m)
            &&& IteratorSpec::decrease(&values) is Some
            &&& IteratorSpec::initial_value_relation(&values, &values)
        },
;
