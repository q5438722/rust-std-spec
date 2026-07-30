pub fn with_capacity(capacity: usize) -> HashSet<T, RandomState> {
        HashSet::with_capacity_and_hasher(capacity, Default::default())
    }
