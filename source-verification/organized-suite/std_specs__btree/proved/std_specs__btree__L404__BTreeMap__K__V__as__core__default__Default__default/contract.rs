pub assume_specification<K, V>[ <BTreeMap<K, V> as core::default::Default>::default ]() -> (m:
    BTreeMap<K, V>)
    ensures
        m@ == Map::<K, V>::empty(),
;
