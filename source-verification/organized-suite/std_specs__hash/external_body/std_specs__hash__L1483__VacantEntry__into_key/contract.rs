pub assume_specification<'a, K: 'a, V: 'a, A: Allocator>[ VacantEntry::into_key ](
    entry: VacantEntry::<'a, K, V, A>,
) -> (key: K)
    ensures
        key == entry.key(),
        entry.final_value() == None,
;
