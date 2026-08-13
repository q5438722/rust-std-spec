    pub const fn split_at_checked(&self, mid: usize) -> Option<(&[T], &[T])> {
        if mid <= self.len() {
            // SAFETY: `[ptr; mid]` and `[mid; len]` are inside `self`, which
            // fulfills the requirements of `split_at_unchecked`.
            Some(unsafe { self.split_at_unchecked(mid) })
        } else {
            None
        }
    }
