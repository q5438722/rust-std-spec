pub fn with_capacity(capacity: usize) -> BinaryHeap<T> {
        BinaryHeap { data: Vec::with_capacity(capacity) }
    }
