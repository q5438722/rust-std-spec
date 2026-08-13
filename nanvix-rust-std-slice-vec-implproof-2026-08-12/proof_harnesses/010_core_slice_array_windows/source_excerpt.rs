    pub const fn array_windows<const N: usize>(&self) -> ArrayWindows<'_, T, N> {
        assert!(N != 0, "window size must be non-zero");
        ArrayWindows::new(self)
    }
