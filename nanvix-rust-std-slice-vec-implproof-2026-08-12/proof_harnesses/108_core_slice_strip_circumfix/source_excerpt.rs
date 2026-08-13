    pub fn strip_circumfix<S, P>(&self, prefix: &P, suffix: &S) -> Option<&[T]>
    where
        T: PartialEq,
        S: SlicePattern<Item = T> + ?Sized,
        P: SlicePattern<Item = T> + ?Sized,
    {
        self.strip_prefix(prefix)?.strip_suffix(suffix)
    }
