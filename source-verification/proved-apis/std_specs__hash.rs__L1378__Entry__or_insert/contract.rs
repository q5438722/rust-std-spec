pub assume_specification<'a, K, V, A: Allocator>[ Entry::or_insert ](
    entry: Entry::<'a, K, V, A>,
    default: V,
) -> (value: &'a mut V)
    ensures
        *value == (match entry.value() {
            Some(v) => v,
            None => default,
        }),
        entry.final_value() == Some(*final(value)),
;
