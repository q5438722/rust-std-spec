pub assume_specification<Key, Value>[ BTreeMap::<Key, Value>::new ]() -> (m: BTreeMap<Key, Value>)
    ensures
        m@ == Map::<Key, Value>::empty(),
;
