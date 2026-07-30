pub assume_specification<'a, 'b, K, V, A: Allocator>[ OccupiedEntry::get ](
    entry: &'b OccupiedEntry::<'a, K, V, A>,
) -> (value: &'b V)
    ensures
        *value == entry.value(),
;
