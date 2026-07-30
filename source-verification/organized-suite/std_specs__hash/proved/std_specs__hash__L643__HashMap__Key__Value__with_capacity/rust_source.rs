pub fn with_capacity(capacity: usize) -> HashMap<K, V, RandomState> {
        HashMap::with_capacity_and_hasher(capacity, Default::default())
    }
