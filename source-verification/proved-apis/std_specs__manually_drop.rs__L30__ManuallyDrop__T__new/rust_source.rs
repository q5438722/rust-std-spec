pub const fn new(value: T) -> ManuallyDrop<T> {
        ManuallyDrop { value: MaybeDangling::new(value) }
    }
