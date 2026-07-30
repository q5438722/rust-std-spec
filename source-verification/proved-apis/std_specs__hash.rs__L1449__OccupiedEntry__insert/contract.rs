pub assume_specification<'a, K, V, A: Allocator>[ OccupiedEntry::insert ](
    entry: &mut OccupiedEntry::<'a, K, V, A>,
    value: V,
) -> (old_value: V)
    ensures
        old_value == old(entry).value(),
        final(entry).key() == old(entry).key(),
        final(entry).value() == value,
        final(entry).final_value() == old(entry).final_value(),
;
