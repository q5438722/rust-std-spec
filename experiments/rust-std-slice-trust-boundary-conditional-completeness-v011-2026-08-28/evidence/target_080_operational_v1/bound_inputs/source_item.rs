    pub fn sort_unstable(&mut self)
    where
        T: Ord,
    {
        sort::unstable::sort(self, &mut T::lt);
    }
