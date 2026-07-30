pub assume_specification<K: Clone, A: Allocator + Clone>[ <BTreeSet::<K, A> as Clone>::clone ](
    this: &BTreeSet<K, A>,
) -> (other: BTreeSet<K, A>)
    ensures
        other@ == this@,
;
