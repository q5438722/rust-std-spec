pub assume_specification<K: Clone, V: Clone, S: Clone, A: Allocator + Clone>[ <HashMap::<
    K,
    V,
    S,
    A,
> as Clone>::clone ](this: &HashMap<K, V, S, A>) -> (other: HashMap<K, V, S, A>)
    ensures
        other@.dom() == this@.dom(),
        forall|key|
            #![trigger other@.dom().contains(key)]
            other@.dom().contains(key) ==> cloned(this@[key], #[trigger] other@[key]),
;
