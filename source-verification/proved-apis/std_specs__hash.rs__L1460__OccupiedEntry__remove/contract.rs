pub assume_specification<'a, K, V, A: Allocator>[ OccupiedEntry::remove ](
    entry: OccupiedEntry::<'a, K, V, A>,
) -> (value: V)
    ensures
        value == entry.value(),
        entry.final_value() == None,
;
