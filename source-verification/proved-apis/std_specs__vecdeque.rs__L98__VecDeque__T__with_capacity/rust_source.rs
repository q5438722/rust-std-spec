pub fn with_capacity(capacity: usize) -> VecDeque<T> {
        Self::with_capacity_in(capacity, Global)
    }
