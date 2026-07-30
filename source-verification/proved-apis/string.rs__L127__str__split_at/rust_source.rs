pub const fn split_at(&self, mid: usize) -> (&str, &str) {
        match self.split_at_checked(mid) {
            None => slice_error_fail(self, 0, mid),
            Some(pair) => pair,
        }
    }
