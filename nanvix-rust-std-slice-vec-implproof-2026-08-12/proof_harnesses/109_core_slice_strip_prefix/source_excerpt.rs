    pub fn strip_prefix<P: SlicePattern<Item = T> + ?Sized>(&self, prefix: &P) -> Option<&[T]>
    where
        T: PartialEq,
    {
        // This function will need rewriting if and when SlicePattern becomes more sophisticated.
        let prefix = prefix.as_slice();
        let n = prefix.len();
        if n <= self.len() {
            let (head, tail) = self.split_at(n);
            if head == prefix {
                return Some(tail);
            }
        }
        None
    }
