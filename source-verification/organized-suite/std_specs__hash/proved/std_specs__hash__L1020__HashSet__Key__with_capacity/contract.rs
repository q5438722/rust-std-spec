pub assume_specification<Key>[ HashSet::<Key>::with_capacity ](capacity: usize) -> (m: HashSet<
    Key,
    RandomState,
>)
    ensures
        m@ == Set::<Key>::empty(),
;
