pub assume_specification<'a, K, V, A: Allocator>[ Entry::insert_entry ](
    entry: Entry::<'a, K, V, A>,
    value: V,
) -> (occ_entry: OccupiedEntry<'a, K, V, A>)
    ensures
        occ_entry.key() == entry.key(),
        occ_entry.value() == value,
        entry.final_value() == occ_entry.final_value(),
;
