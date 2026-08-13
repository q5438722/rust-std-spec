    pub fn is_sorted_by<'a, F>(&'a self, mut compare: F) -> bool
    where
        F: FnMut(&'a T, &'a T) -> bool,
    {
        self.array_windows().all(|[a, b]| compare(a, b))
    }
