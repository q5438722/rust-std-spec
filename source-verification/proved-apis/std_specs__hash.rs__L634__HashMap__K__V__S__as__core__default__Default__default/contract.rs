pub assume_specification<K, V, S: core::default::Default>[ <HashMap<
    K,
    V,
    S,
> as core::default::Default>::default ]() -> (m: HashMap<K, V, S>)
    ensures
        m@ == Map::<K, V>::empty(),
;
