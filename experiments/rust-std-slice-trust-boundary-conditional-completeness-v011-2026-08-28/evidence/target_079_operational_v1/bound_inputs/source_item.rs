    pub fn select_nth_unstable_by_key<K, F>(
        &mut self,
        index: usize,
        mut f: F,
    ) -> (&mut [T], &mut T, &mut [T])
    where
        F: FnMut(&T) -> K,
        K: Ord,
    {
        sort::select::partition_at_index(self, index, |a: &T, b: &T| f(a).lt(&f(b)))
    }
