    pub fn sort_unstable_by<F>(&mut self, mut compare: F)
    where
        F: FnMut(&T, &T) -> Ordering,
    {
        sort::unstable::sort(self, &mut |a, b| compare(a, b) == Ordering::Less);
    }
