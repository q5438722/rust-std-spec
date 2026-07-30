pub assume_specification<K: Clone, V: Clone, A: Allocator + Clone>[ <BTreeMap::<
    K,
    V,
    A,
> as Clone>::clone ](this: &BTreeMap<K, V, A>) -> (other: BTreeMap<K, V, A>)
    ensures
        other@ == this@,
;
