    pub const fn split_at_mut_checked(&mut self, mid: usize) -> Option<(&mut [T], &mut [T])> {
        if mid <= self.len() {
            // SAFETY: `[ptr; mid]` and `[mid; len]` are inside `self`, which
            // fulfills the requirements of `split_at_unchecked`.
            Some(unsafe { self.split_at_mut_unchecked(mid) })
        } else {
            None
        }
    }
