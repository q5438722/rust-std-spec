pub assume_specification<Key, Value>[ HashMap::<Key, Value>::new ]() -> (m: HashMap<
    Key,
    Value,
    RandomState,
>)
    ensures
        m@ == Map::<Key, Value>::empty(),
;
