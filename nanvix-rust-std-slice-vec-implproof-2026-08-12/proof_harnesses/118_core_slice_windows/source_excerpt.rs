    pub const fn windows(&self, size: usize) -> Windows<'_, T> {
        let size = NonZero::new(size).expect("window size must be non-zero");
        Windows::new(self, size)
    }
