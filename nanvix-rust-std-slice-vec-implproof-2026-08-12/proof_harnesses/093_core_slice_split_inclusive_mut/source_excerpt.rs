    pub fn split_inclusive_mut<F>(&mut self, pred: F) -> SplitInclusiveMut<'_, T, F>
    where
        F: FnMut(&T) -> bool,
    {
        SplitInclusiveMut::new(self, pred)
    }
