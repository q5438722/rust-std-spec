pub const fn split_at(&self, mid: usize) -> (&[T], &[T]) {
        match self.split_at_checked(mid) {
            Some(pair) => pair,
            None => panic!("mid > len"),
        }
    }
