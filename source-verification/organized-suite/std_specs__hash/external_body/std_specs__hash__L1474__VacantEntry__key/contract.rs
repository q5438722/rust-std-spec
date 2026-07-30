pub assume_specification<'a, 'b, K: 'a, V: 'a, A: Allocator>[ VacantEntry::key ](
        entry: &'b VacantEntry::<'a, K, V, A>,
    ) -> (key: &'b K)
        returns
            &entry.spec_key(),
    ;
