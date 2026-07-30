pub assume_specification<'a, 'b, K, V, A: Allocator>[ OccupiedEntry::get_mut ](
    entry: &'b mut OccupiedEntry::<'a, K, V, A>,
) -> (value: &'b mut V)
    ensures
        *value == old(entry).value(),
        final(entry).key() == old(entry).key(),
        final(entry).value() == *final(value),
        final(entry).final_value() == old(entry).final_value(),
;
