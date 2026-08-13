    pub const fn as_ptr(&self) -> *const T {
        self as *const [T] as *const T
    }
