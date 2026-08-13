    pub fn strip_suffix<P: SlicePattern<Item = T> + ?Sized>(&self, suffix: &P) -> Option<&[T]>
    where
        T: PartialEq,
    {
        // This function will need rewriting if and when SlicePattern becomes more sophisticated.
        let suffix = suffix.as_slice();
        let (len, n) = (self.len(), suffix.len());
        if n <= len {
            let (head, tail) = self.split_at(len - n);
            if tail == suffix {
                return Some(head);
            }
        }
        None
    }
