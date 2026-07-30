pub assume_specification<'a, K, V, A: Allocator>[ OccupiedEntry::into_mut ](
    entry: OccupiedEntry::<'a, K, V, A>,
) -> (value: &mut V)
    ensures
        *value == entry.value(),
        entry.final_value() == Some(*final(value)),
;
