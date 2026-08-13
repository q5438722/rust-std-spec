    pub fn sort_unstable_by_key<K, F>(&mut self, mut f: F)
    where
        F: FnMut(&T) -> K,
        K: Ord,
    {
        sort::unstable::sort(self, &mut |a, b| f(a).lt(&f(b)));
    }
