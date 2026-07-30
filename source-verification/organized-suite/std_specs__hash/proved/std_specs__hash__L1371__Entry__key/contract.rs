pub assume_specification<'a, 'b, K, V, A: Allocator>[ Entry::key ](
    entry: &'b Entry::<'a, K, V, A>,
) -> (key: &'b K)
    returns
        &entry.spec_key(),
;
