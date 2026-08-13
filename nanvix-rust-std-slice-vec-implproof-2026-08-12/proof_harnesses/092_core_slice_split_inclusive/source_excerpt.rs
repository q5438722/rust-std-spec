    pub fn split_inclusive<F>(&self, pred: F) -> SplitInclusive<'_, T, F>
    where
        F: FnMut(&T) -> bool,
    {
        SplitInclusive::new(self, pred)
    }
