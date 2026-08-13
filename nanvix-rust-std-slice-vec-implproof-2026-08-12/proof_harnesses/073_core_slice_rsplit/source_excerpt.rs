    pub fn rsplit<F>(&self, pred: F) -> RSplit<'_, T, F>
    where
        F: FnMut(&T) -> bool,
    {
        RSplit::new(self, pred)
    }
