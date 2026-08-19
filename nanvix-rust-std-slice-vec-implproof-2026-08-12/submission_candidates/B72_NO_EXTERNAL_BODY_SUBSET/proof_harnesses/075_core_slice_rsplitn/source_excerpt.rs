    pub fn rsplitn<F>(&self, n: usize, pred: F) -> RSplitN<'_, T, F>
    where
        F: FnMut(&T) -> bool,
    {
        RSplitN::new(self.rsplit(pred), n)
    }
