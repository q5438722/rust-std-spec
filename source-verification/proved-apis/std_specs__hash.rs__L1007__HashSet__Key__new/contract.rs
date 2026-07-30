pub assume_specification<Key>[ HashSet::<Key>::new ]() -> (m: HashSet<Key, RandomState>)
    ensures
        m@ == Set::<Key>::empty(),
;
