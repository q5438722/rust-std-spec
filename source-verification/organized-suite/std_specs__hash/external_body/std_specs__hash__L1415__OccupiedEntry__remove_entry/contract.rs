pub assume_specification<'a, K, V, A: Allocator>[ OccupiedEntry::remove_entry ](
    entry: OccupiedEntry::<'a, K, V, A>,
) -> (kv: (K, V))
    ensures
        entry.final_value() == None,
    returns
        (*entry.key(), entry.value()),
;
