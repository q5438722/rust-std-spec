pub assume_specification<Key>[ BTreeSet::<Key>::new ]() -> (m: BTreeSet<Key>)
    ensures
        m@ == Set::<Key>::empty(),
;
