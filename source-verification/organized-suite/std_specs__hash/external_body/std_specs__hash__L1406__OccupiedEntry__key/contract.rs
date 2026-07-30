pub assume_specification<'a, 'b, K, V, A: Allocator>[ OccupiedEntry::key ](
        entry: &'b OccupiedEntry::<'a, K, V, A>,
    ) -> (key: &'b K)
        returns
            &entry.spec_key(),
    ;
