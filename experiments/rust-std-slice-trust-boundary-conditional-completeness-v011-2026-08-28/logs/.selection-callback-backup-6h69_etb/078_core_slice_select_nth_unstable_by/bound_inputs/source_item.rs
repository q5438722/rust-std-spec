    pub fn select_nth_unstable_by<F>(
        &mut self,
        index: usize,
        mut compare: F,
    ) -> (&mut [T], &mut T, &mut [T])
    where
        F: FnMut(&T, &T) -> Ordering,
    {
        sort::select::partition_at_index(self, index, |a: &T, b: &T| compare(a, b) == Less)
    }
