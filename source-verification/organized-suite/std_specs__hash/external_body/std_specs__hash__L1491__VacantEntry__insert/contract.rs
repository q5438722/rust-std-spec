pub assume_specification<'a, K: 'a, V: 'a, A: Allocator>[ VacantEntry::insert ](
    entry: VacantEntry::<'a, K, V, A>,
    value: V,
) -> (value_ref: &mut V)
    ensures
        *value_ref == value,
        entry.final_value() == Some(*final(value_ref)),
;
