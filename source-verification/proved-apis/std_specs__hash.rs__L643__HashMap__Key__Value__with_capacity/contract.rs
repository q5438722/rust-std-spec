pub assume_specification<Key, Value>[ HashMap::<Key, Value>::with_capacity ](capacity: usize) -> (m:
    HashMap<Key, Value, RandomState>)
    ensures
        m@ == Map::<Key, Value>::empty(),
;
